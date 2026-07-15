# Snapshot delle fonti ufficiali — fallback per la replica

**Perché esiste.** Il calcolatore fa chiamate di rete **al livello del modulo**: importare
`pension_paid_calculator` scarica, se manca la cache, i tassi di capitalizzazione ISTAT e le
retribuzioni contrattuali ISTAT. **ISTAT è instabile**: durante l'istruttoria è andato giù
più volte, e senza cache l'import fallisce — anche per gli script che quei dati non li usano.

Un retry non risolve: **dipende comunque dall'uptime ISTAT**. Questo snapshot lo rimuove.

**Cosa contiene.** I quattro file che il calcolatore scarica, esattamente come prodotti dai
suoi script di download, al momento della chiusura dell'istruttoria:

| File | Fonte | Prodotto da |
|---|---|---|
| `tassi_capitalizzazione_montante.csv` | ISTAT SDMX (PIL nominale) + nota ISTAT/Min. Lavoro | `calcolatore/src/download_capitalization_data.py` |
| `pil_nominale_capitalizzazione.csv` | ISTAT SDMX, dataflow 92_506 e 284_159 | idem |
| `retribuzioni_contrattuali_ccnl.csv` | ISTAT SDMX, dataflow 155_318 | `calcolatore/src/download_contract_wages.py` |
| `aliquote_ivs_fpld_periodi.csv` | INPS, allegato storico aliquote (.xls) | `scripts/src/build_contribution_rate_history.py` |

**Come viene usato.** `esegui_pipeline_calcolatore.sh` prova a scaricare dalle fonti vive (con
retry). Se ISTAT non risponde, **ricade su questo snapshot** e lo dichiara a video.

**Non è un dato inserito a mano**: è l'output degli script di download upstream, versionato per
rendere la replica deterministica. Per rigenerarlo da zero basta cancellare la cache e rilanciare
la pipeline con ISTAT raggiungibile.
