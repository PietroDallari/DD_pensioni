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
| `analisi/output/passivita_riconoscimento.csv` | Passività a **doppia via**: €2.599 (top-down, ADL Eurostat) vs €2.297 (bottom-up, coorti × montante). Divergenza 11,6%. Centrale adottato: **€2.450** = media aritmetica arrotondata. Da qui scalano linearmente l'interesse nozionale (41,7 mld/anno) e il carry dello spread (63,7) |
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

**L'upgrade è stato verificato e NON adottato.** Non è un rinvio: è una decisione documentata
in `analisi/output/upgrade_upstream_quarantena.md`.

I due bug fix upstream (`bcfda17`, `a36819a`) **non ci toccano** — si attivano solo con
`anni_contribuiti < anni_disponibili` o `mesi < 12`, e noi usiamo sempre gli estremi.
Ma `52abdf7` cambia `salary_profile`: usa ora gli **indici ISTAT delle retribuzioni
contrattuali** al posto dell'interpolazione geometrica. Il nostro Scenario B costruisce il
sentiero con **AMECO**: adottare il pin renderebbe il metodo dichiarato nel report diverso da
quello eseguito dal codice. È una **scelta di metodo**, non un aggiornamento di numeri.

Effetto misurato: eccesso +1-2 punti per fascia (bordo alto 43,3% → 44,3%, fuori
dall'intervallo dichiarato 28-43); gettito +0,1 mld (10,6 → 10,7). Nessuna conclusione
si inverte.

## Regressione — verificata

Da clone pulito, con il pin attivo, la pipeline riproduce:

| Numero | Valore |
|---|---|
| Spesa pensioni COFOG 2024 | €359,6 mld |
| Clawback IRPEF (MEF) | €65,1 mld |
| Spesa a carico dei contributi | €254,7 mld |
| Passività di riconoscimento — **Via A** (top-down, ADL Eurostat) | €2.599 mld |
| Passività di riconoscimento — **Via B** (bottom-up, coorti) | €2.297 mld |
| Passività — **centrale adottato** (media delle due, arrotondata) | **€2.450 mld** |
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
