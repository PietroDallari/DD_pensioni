# Replica — come rigenerare tutti i numeri del report

Ogni numero del report nasce da uno di questi comandi. Nessun dato è inserito a mano.

## Prerequisiti

```bash
git clone https://github.com/PietroDallari/DD_pensioni.git
cd DD_pensioni
git clone https://github.com/NazarenoLecis/pensioni_italia.git   # il calcolatore upstream
bash analisi/esegui_pipeline_calcolatore.sh                      # crea il venv e scarica i dati ufficiali
```

Lo script crea `analisi/.venv` e installa le dipendenze. Due non sono in `requirements.txt`
upstream ma servono: **`xlrd`** (l'allegato aliquote INPS è un `.xls`) e — solo dietro proxy
TLS aziendale — **`pip-system-certs`**, altrimenti ISTAT/INPS falliscono con
`CERTIFICATE_VERIFY_FAILED`.

> Su Linux/macOS sostituire `analisi/.venv/Scripts/python.exe` con `analisi/.venv/bin/python`.

## I comandi

```bash
PY=analisi/.venv/Scripts/python.exe

# 1. Fase 1 — verifiche dati (perimetro spesa, distribuzione, clawback)
$PY analisi/fase1_verifiche.py

# 2. Riconciliazione dei perimetri COFOG / INPS / MEF
$PY analisi/riconciliazione_perimetri.py

# 3. Passività di riconoscimento (due vie: ADL Eurostat vs bottom-up)
$PY analisi/fase3_passivita.py

# 4. Coda di Pareto ancorata e scenari lordo/netto
$PY analisi/fase6_pareto_2024_lordo_netto.py

# 5. Scenario B — ricalibrato su serie salariali storiche (AMECO)
$PY analisi/scenarioB_serie_salariali.py

# 6. Il modello di transizione (due comparti, profilo temporale, profili lavoratore)
$PY transition_model.py --csv analisi/output
```

## Cosa produce ciascuno

| File | Contenuto |
|---|---|
| `analisi/output/parametri_verificati.csv` | **37 parametri**, ciascuno con valore, unità, anno, fonte, flag di qualità. Zero placeholder. È il file di riferimento. |
| `analisi/output/perimetro_spesa.csv` | Riconciliazione COFOG: vecchiaia + superstiti = €359,6 mld (2024) |
| `analisi/output/distribuzione_pensionati.csv` | Distribuzione per fascia lorda/netta, con IRPEF per fascia |
| `analisi/output/passivita_riconoscimento.csv` | Passività a due vie: €2.599 (top-down) vs €2.297 (bottom-up) → adottato €2.450 mld |
| `analisi/output/scenari_lordo_netto.csv` | Scenari A e B, lordo e netto del clawback IRPEF perso |
| `analisi/output/scenarioB_ricalibrato.csv` | Scenario B con sentiero salariale AMECO |
| `analisi/output/coda_spezzata.csv` | Pareto ancorata su due punti INPS + coda spezzata sopra €10.000 |
| `analisi/output/comparto_legacy.csv` | Comparto 1: disavanzo, stock BTP, estinzione |
| `analisi/output/comparto2_scenario{A,B}.csv` | Comparto 2: fondo, payout, scoperto |
| `analisi/output/eccesso_per_profilo.md` | **Quota non finanziata per fascia di pensione** (configurazione 3) |
| `analisi/output/tre_test_ribaltamento.md` | I tre test che hanno respinto il "ribaltamento" |
| `analisi/output/crosscheck_389.md` | Cross-check sulle coorti di decorrenza |
| `analisi/output/richiesta_dati_verificata.md` | Cosa INPS pubblica e cosa no — a prova di contraddittorio |
| `analisi/FASE2_estensioni.md` | Le tre estensioni note che alzano il gettito (backlog) |

## Fonti scaricate a runtime (nessun file manuale)

| Fonte | Cosa |
|---|---|
| **ISTAT SDMX** | PIL nominale → tassi di capitalizzazione del montante |
| **Nota ISTAT / Min. Lavoro** | Tassi di capitalizzazione **ufficiali** (PDF) |
| **INPS open data** | Aliquote IVS storiche; distribuzione beneficiari (dataset 1824); regime di liquidazione (1648) |
| **INPS Osservatori (API)** | Cubo 389, pensioni per regime di liquidazione. ⚠️ L'API richiede `"zip": true` nel payload — senza, risponde con un errore Base-64 fuorviante. Ricetta in `analisi/fase_finale_cubo389.py` |
| **Eurostat** | COFOG (`gov_10a_exp`), HICP (`prc_hicp_aind`), pension entitlements (`nasa_10_pens1`), occupati (`lfsa_egan`) |
| **AMECO** (Commissione UE) | `ITA.1.0.0.0.HWCDW` — retribuzioni nominali per occupato, dal 1960 |

## ⚠️ Il commit upstream è PINNATO

`esegui_pipeline_calcolatore.sh` fa `git checkout 1007648` sul repo di Nazareno. **Non è
pignoleria**: la regressione da clone pulito ha mostrato che l'upstream si muove — al
12/07/2026 aveva 5 commit successivi, fra cui *«Refine pension calculator contribution
modelling»* e *«Fix simplified contribution-year scaling»*, che **cambiano i numeri** (es.
montante dello scenario `carriera_lunga_mista`: 630.060 → 660.875).

Senza pin, chiunque cloni ottiene risultati diversi da quelli del report.

**Per aggiornare il pin**: cambiare l'hash e **riverificare** i numeri, non solo rigirarli.
L'upstream ha correzioni al modello contributivo che **non abbiamo incorporato** — è una voce
del backlog in `analisi/FASE2_estensioni.md`.

## Regressione — verificata

Da clone pulito, con il pin attivo, la pipeline riproduce:

| Numero | Valore |
|---|---|
| Spesa pensioni COFOG 2024 | €359,6 mld |
| Clawback IRPEF (MEF) | €65,1 mld |
| Spesa a carico dei contributi | €254,7 mld |
| Passività di riconoscimento (Via A) | €2.599 mld |
| Picco BTP del ponte | €94 mld (4% del PIL), 2027 |
| Profilo mediano: PAYG vs proposta | €22.650 → €27.239 (**+20%**) |
| Test del calcolatore | **17/17 passati** |

## Due note metodologiche che il lettore deve conoscere

1. **I tassi di capitalizzazione sono quelli UFFICIALI**, non ricalcolati. Il calcolatore
   upstream ricalcola i tassi dai livelli di PIL correnti; noi applichiamo i coefficienti
   pubblicati (quelli che INPS ha applicato per legge). L'override è in
   `analisi/override_tassi_ufficiali.py` — **il repo di Nazareno non è modificato.**
2. **Le due ipotesi dichiarate** dello Scenario B: il **premio di carriera** (correlato al
   censo, calibrato ma non osservato) e i **tassi di capitalizzazione pre-1996** (un
   controfattuale costruito — il contributivo nasce nel 1996). Entrambe marcate
   `ipotesi_dichiarata` in `parametri_verificati.csv`.
