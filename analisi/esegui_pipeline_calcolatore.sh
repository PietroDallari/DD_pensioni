#!/usr/bin/env bash
# Ricostruisce da zero il calcolatore "pensione pagata" con i dati ufficiali.
# Non modifica il repo pensioni_italia/: venv e script stanno qui in analisi/.
#
#   bash analisi/esegui_pipeline_calcolatore.sh
set -euo pipefail

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

# --- 2. Tassi di capitalizzazione dal PIL nominale ISTAT (SDMX) ---------------
# -> output/data/clean/tassi_capitalizzazione_montante.csv
#    output/data/clean/pil_nominale_capitalizzazione.csv
"$PY" calcolatore/src/download_capitalization_data.py

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
