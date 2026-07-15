#!/usr/bin/env bash
# Ricostruisce da zero il calcolatore "pensione pagata" con i dati ufficiali.
# Non modifica il repo pensioni_italia/: venv e script stanno qui in analisi/.
#
#   bash analisi/esegui_pipeline_calcolatore.sh
set -euo pipefail

# COMMIT UPSTREAM PINNATO. Tutti i numeri del report sono calcolati contro questo commit
# del calcolatore di Nazareno. Il pin serve perche' l'upstream si muove e i suoi cambiamenti
# possono spostare i risultati: aggiornarlo richiede di RIVERIFICARE, non solo rigirare.
#
# 0d7a5b7 (adottato dopo verifica): incorpora i bug fix upstream, che per il nostro uso sono a
# DELTA ZERO (misurato: si attivano solo con anni_contribuiti < anni_disponibili o mesi < 12,
# e noi usiamo sempre gli estremi). Il cambiamento al sentiero salariale (indici contrattuali
# ISTAT) e' invece BYPASSATO in analisi/override_tassi_ufficiali.py, perche' noi costruiamo il
# sentiero con AMECO — scelta dichiarata, cfr. quel modulo e parametri_verificati.csv.
PIN_UPSTREAM="0d7a5b7"

ANALISI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$ANALISI_DIR/../pensioni_italia" && pwd)"
VENV="$ANALISI_DIR/.venv"
PY="$VENV/Scripts/python.exe"   # su Linux/macOS: $VENV/bin/python

# --- 1. Ambiente -------------------------------------------------------------
# Due dipendenze non sono in requirements.txt del repo ma servono davvero:
#   xlrd            -> build_contribution_rate_history.py legge un .xls con engine="xlrd"
#   pip-system-certs-> dietro proxy TLS aziendale (Zscaler/Netskope) requests deve
#                      fidarsi del cert store di Windows, altrimenti ISTAT/INPS
#                      falliscono con CERTIFICATE_VERIFY_FAILED (self-signed in chain).
# Nota: il repo dichiara pandas>=2.2 e target py310, ma la pipeline e' stata
# eseguita con successo su pandas 3.0.3 / Python 3.13 (17/17 test verdi).
if [ ! -x "$PY" ]; then
  python -m venv "$VENV"
  "$PY" -m pip install --upgrade pip
fi
"$PY" -m pip install --quiet \
  pandas requests openpyxl pyarrow matplotlib PyMuPDF \
  xlrd pip-system-certs pytest

cd "$REPO_DIR"

# --- 1-bis. Pin del commit upstream --------------------------------------------
if git rev-parse --verify "$PIN_UPSTREAM" >/dev/null 2>&1; then
  attuale="$(git rev-parse --short HEAD)"
  if [ "$attuale" != "$PIN_UPSTREAM" ]; then
    echo ">> pinning upstream: $attuale -> $PIN_UPSTREAM"
    git checkout -q "$PIN_UPSTREAM"
  fi
else
  echo "ATTENZIONE: commit $PIN_UPSTREAM non trovato. I numeri potrebbero divergere."
fi

# --- 1-ter. PREREQUISITO: popolare le cache di rete ---------------------------
# Il calcolatore fa chiamate di rete AL LIVELLO DEL MODULO: importare
# pension_paid_calculator scarica (se manca la cache) i tassi di capitalizzazione ISTAT e
# le retribuzioni contrattuali ISTAT. Senza cache, l'import FALLISCE se ISTAT e' giu' —
# anche per gli script che quei dati non li usano.
# Popolarle qui rende la replica indipendente dall'uptime ISTAT al momento dell'import.
# ISTAT e' notoriamente instabile: durante l'istruttoria e' andato giu' piu' volte. Il
# calcolatore fa chiamate di rete AL LIVELLO DEL MODULO (importare pension_paid_calculator
# scarica, se manca la cache, tassi di capitalizzazione e retribuzioni contrattuali): senza
# cache l'import FALLISCE, anche per gli script che quei dati non li usano.
#
# Un retry non basta: dipenderebbe comunque dall'uptime ISTAT. Qui si prova la fonte viva e,
# se non risponde, si RICADE SU UNO SNAPSHOT VERSIONATO (analisi/cache_istat/), che e' l'output
# degli stessi script di download. Cosi' la replica e' DETERMINISTICA e non dipende da ISTAT.
CACHE_SNAPSHOT="$ANALISI_DIR/cache_istat"
CLEAN_DIR="$REPO_DIR/output/data/clean"
mkdir -p "$CLEAN_DIR"

assicura_cache() {
  local script="$1" file="$2" nome="$3"
  [ -f "$CLEAN_DIR/$file" ] && return 0
  for tentativo in 1 2 3; do
    echo ">> $nome — download, tentativo $tentativo/3"
    if "$PY" "$script" >/dev/null 2>&1 && [ -f "$CLEAN_DIR/$file" ]; then
      echo ">> $nome — scaricato dalla fonte viva"
      return 0
    fi
    sleep $((tentativo * 15))
  done
  if [ -f "$CACHE_SNAPSHOT/$file" ]; then
    echo ">> $nome — ISTAT non risponde: USO LO SNAPSHOT VERSIONATO (analisi/cache_istat/)"
    cp "$CACHE_SNAPSHOT/$file" "$CLEAN_DIR/$file"
    return 0
  fi
  echo "ERRORE: $nome non disponibile ne' da ISTAT ne' da snapshot."
  return 1
}

assicura_cache calcolatore/src/download_contract_wages.py   retribuzioni_contrattuali_ccnl.csv "retribuzioni contrattuali ISTAT (155_318)"
assicura_cache calcolatore/src/download_capitalization_data.py   tassi_capitalizzazione_montante.csv "tassi di capitalizzazione ISTAT"
[ -f "$CLEAN_DIR/pil_nominale_capitalizzazione.csv" ] ||   cp "$CACHE_SNAPSHOT/pil_nominale_capitalizzazione.csv" "$CLEAN_DIR/" 2>/dev/null || true

# --- 2. Tassi di capitalizzazione: gia' assicurati sopra (fonte viva o snapshot) ---

# --- 3. Aliquote contributive IVS FPLD (allegato storico INPS) ----------------
# -> output/data/clean/aliquote_ivs_fpld_periodi.csv
#    output/data/final/tabella_parametri_sistema.csv
"$PY" scripts/src/build_contribution_rate_history.py

# --- 4. Test -----------------------------------------------------------------
"$PY" -m pytest calcolatore/tests/ -q

# --- 5. Calcolatore sui 3 scenari demo ---------------------------------------
# -> output/data/final/calcolatore_pensione_pagata_*.csv
"$PY" code/calcolatore_pensione_pagata.py

echo
echo "OK: pipeline completata."
