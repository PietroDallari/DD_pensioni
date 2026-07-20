# DD_pensioni

Analisi sulla transizione del sistema pensionistico italiano dalla ripartizione (PAYG)
alla capitalizzazione, e sulla misura della **componente non finanziata** delle pensioni
in essere — cioè la quota di prestazione che eccede il controfattuale interamente
contributivo.

Questo repo contiene **solo il nostro lavoro**. Il calcolatore su cui si appoggia è di
Nazareno Lecis e resta il suo:
👉 https://github.com/NazarenoLecis/pensioni_italia

## Struttura

| Percorso | Contenuto |
|---|---|
| [`docs/Pensioni.md`](docs/Pensioni.md) | Position paper "Per un Welfare sostenibile". |
| [`docs/report_transizione_v3.md`](docs/report_transizione_v3.md) | Rapporto tecnico "Uscita dell'Italia dal Pay-As-You-Go" (ogni cifra replicabile dalla pipeline). |
| [`docs/nota_riconciliazione_position_paper.md`](docs/nota_riconciliazione_position_paper.md) | Riconciliazione punto per punto tra i due documenti. |
| [`docs/previdenza complementare/`](docs/previdenza%20complementare/) | Paper collaterale: previdenza complementare e venture capital. |
| `docs/old stuff/` | Versioni superate, tenute per storico. |
| [`analisi/`](analisi/) | La pipeline riproducibile: verifiche dati e scenari, in fasi (`fase1_…` → `fase6_…`), più le leve di micro-simulazione e riconciliazione dei perimetri. |
| [`transition_model.py`](transition_model.py) | Il modello di transizione (due comparti, profilo temporale, profili lavoratore, scenari di prelievo A/B). |
| [`analisi/esegui_pipeline_calcolatore.sh`](analisi/esegui_pipeline_calcolatore.sh) | Ricostruisce da zero il calcolatore di Nazareno con i dati ufficiali (ISTAT SDMX, INPS, tavole di mortalità) e popola le cache. |
| [`analisi/override_tassi_ufficiali.py`](analisi/override_tassi_ufficiali.py) | Il nostro override metodologico (sotto). |
| [`analisi/cache_istat/`](analisi/cache_istat/) | Snapshot delle fonti ISTAT/INPS, fallback quando ISTAT è giù (vedi il suo README). |
| [`analisi/output/`](analisi/output/) | Tutti i risultati: CSV dei parametri e degli scenari + le note `.md` (eccesso per profilo, cross-check, test di robustezza). |

> **Per rigenerare ogni numero del report** — comandi, ordine e cosa produce
> ciascuno — vedi **[`README_replica.md`](README_replica.md)**. Questo README dà
> il quadro; `README_replica.md` è la guida operativa alla replica.

## Setup

```bash
git clone https://github.com/NazarenoLecis/pensioni_italia.git   # accanto a analisi/ e docs/
bash analisi/esegui_pipeline_calcolatore.sh                      # crea il venv e ricostruisce i dati
analisi/.venv/Scripts/python.exe analisi/override_tassi_ufficiali.py
```

Due dipendenze non sono in `requirements.txt` del repo upstream ma servono davvero:
`xlrd` (l'allegato aliquote INPS è un `.xls`) e — solo dietro proxy TLS aziendale —
`pip-system-certs`, altrimenti ISTAT/INPS falliscono con `CERTIFICATE_VERIFY_FAILED`.

## L'override: perché

Il calcolatore upstream rivaluta il montante con un tasso **ricalcolato** dai livelli di
PIL nominale ISTAT *correnti*, `(PIL t-1 / PIL t-6)^(1/5) - 1`, e tiene il tasso ufficiale
pubblicato solo come colonna di controllo.

È una scelta difendibile per la domanda che si pone l'autore, ma introduce un errore
**sistematico** per la nostra: noi misuriamo l'eccesso della pensione effettiva sul
controfattuale *come lo liquiderebbe l'INPS*. INPS rivaluta con i coefficienti pubblicati
per legge, calcolati sulle edizioni PIL disponibili *allora*. Le revisioni dei conti
nazionali cambiano retroattivamente i livelli di PIL, quindi il ricalcolo produce un
montante che nessun assicurato ha mai avuto.

L'override applica il **tasso ufficiale pubblicato** se disponibile, con fallback sul
ricalcolo per gli anni senza ancora la nota ministeriale. È implementato come monkey-patch
in `analisi/`: **il repo di Nazareno non viene modificato**.

## Risultato

Il ricalcolo **sovrastima sistematicamente il montante**, tanto più quanto è lunga la
carriera — e quindi **sottostima la componente non finanziata**:

| Scenario | Montante (ricalcolo) | Montante (ufficiale) | Δ montante | Δ eccesso annuo |
|---|---|---|---|---|
| generico FPLD (29 anni) | 364.392 | 358.220 | **−1,69%** | **+5,1%** |
| carriera lunga mista (40 anni) | 630.060 | 615.129 | **−2,37%** | **−78,5%** |
| part-time (24 anni) | 164.440 | 161.804 | **−1,60%** | **+1,2%** |

L'errore sul montante è modesto (1,6–2,4%) ma si amplifica sulla *differenza*, ottenuta per
sottrazione tra grandezze vicine. Il caso `carriera_lunga_mista` è il più istruttivo: col
ricalcolo appare come un pensionato che ha ricevuto *meno* di quanto versato (fuori dalla
platea); coi coefficienti ufficiali il saldo negativo quasi si azzera. **L'errore non sposta
solo gli importi — sposta il confine di chi entra o esce dalla platea.**

## Limiti noti

- Il ramo di fallback dell'override non è attivo sui dati attuali (tutti gli anni 1976–2025
  hanno il tasso ufficiale): è testato solo forzando il caso, non in produzione.
- L'impatto **aggregato** non è stimato: dipende dalla distribuzione della platea attorno
  alla soglia, e i tre scenari qui sono demo, non un campione.
- Il calcolatore upstream non ricostruisce la pensione retributiva/mista INPS: il regime
  è classificato in modo indicativo.

## Licenza e attribuzione

Il calcolatore è di [Nazareno Lecis](https://github.com/NazarenoLecis/pensioni_italia),
con la sua licenza. Qui non ne viene ridistribuito il codice.
