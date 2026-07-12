# Fase 2 — Estensioni note, documentate e non eseguite

> **Perché questo file esiste.** Il gettito dello Scenario B (**€10,6 mld netti**, range
> 9,2-11,5) è un **bordo basso consapevole**, non una svista. Tre estensioni note alzano
> tutte il numero, e una quarta questione concettuale resta aperta. Qui sono censite con la
> loro direzione, cosa servirebbe per quantificarle, e dove stanno le fonti già individuate.
> Quando servirà il numero pieno, si parte da qui.

---

## 1. Fondi speciali con regole privilegiate

**Cosa**: Telefonici, Volo, Elettrici, Trasporti, IPOST, ENPALS avevano **aliquote di
rendimento superiori al 2%** annuo. Sono state allineate all'AGO solo dal **1/1/1995**
(art. 17 L. 724/1994).

**Direzione**: ⬆️ **ALZA il gettito.** Con aliquote di rendimento più generose, la
retribuzione implicita dietro una data pensione è **più bassa** → contributi versati minori
→ **eccesso più alto** di quanto il modello (che applica regole AGO) stimi.

**Peso**: nel 2017 i soli ex Fondi Speciali autonomi (Trasporti, Elettrici, Telefonici,
Dirigenti) hanno pesato per il **39,9% del disavanzo previdenziale** (≈8,4 mld su 21 mld).
Importi medi: telefonici ~€8.200/mese, volo ~€7.900, ferrovieri >€7.000, elettrici ~€5.500.

**Cosa servirebbe**: le aliquote di rendimento specifiche di ciascun fondo ante-1995
(normativa istitutiva dei fondi) + numerosità e importi medi per fondo.

**Fonti già individuate**: art. 17 L. 724/1994; Osservatorio INPS "Pensioni vigenti" con
dettaglio per gestione (cubo accessibile via API — ricetta in `analisi/fase_finale_cubo389.py`,
campo `"zip": true`); 6° Rapporto Itinerari Previdenziali (dati 2017).

---

## 2. Ex-INPDAI — massimale contributivo proprio

**Cosa**: il fondo dirigenti industria (soppresso dal 1/1/2003, art. 42 L. 289/2002) aveva un
**massimale contributivo proprio**: art. 3 c. 7 D.Lgs. 181/1997 (radice L. 967/1953 art. 6).
Valori INPS (Circ. 38/2012, All. 1, Tab. T): **€170.657 (2011)**, **€175.265 (2012)**; alla
soppressione, **€143.106**. **Sopra quella cifra i dirigenti NON versavano contributi.** Il
massimale è stato abolito dal 1/1/2003.
Inoltre: aliquote di rendimento più favorevoli del FPLD **fino al 31/12/1994**; retribuzione
pensionabile sugli ultimi 5 anni (quota A) e 10 anni (quota B), con criteri INPDAI.

**Direzione**: ⬆️ **ALZA il gettito, e proprio nella coda alta** — cioè dove lo Scenario B
preleva. Il modello assume contributi sull'**intera** retribuzione (corretto per il FPLD: cfr.
INPS Circ. 177/1996); per un dirigente ex-INPDAI con €250.000 di retribuzione, i contributi
reali si fermavano a ~€150-175k. **La loro componente non finanziata è sottostimata.**

**Peso**: il Fondo dirigenti pesava per il **48% del disavanzo dei fondi speciali**, pur essendo
il **2,3% delle pensioni** e lo **0,82% dei contribuenti attivi**.

**Cosa servirebbe**: numerosità e distribuzione degli importi dei pensionati ex-INPDAI
(**non trovata da fonte primaria**), e la serie storica del loro massimale contributivo.

**Fonti già individuate**: INPS Circ. 83/2003 e Circ. 107/2003 (regole della soppressione);
INPS Circ. 38/2012 All. 1 Tab. T (massimale); dossier Camera A.C. 5307; Osservatorio INPS per
gestione.

⚠️ **Da NON usare**: gli indicatori "aliquota di equilibrio 797%" o "pensione/contributo 481%"
del fondo dirigenti sono **artefatti contabili** — è un fondo **chiuso** (nessun iscritto dal
2003), quindi il rapporto pensionati/attivi esplode per costruzione. Non provano nulla
sull'equità attuariale individuale.

---

## 3. Quota A calcolata sull'ultima retribuzione

**Cosa**: per l'anzianità **ante-1993** (quota A), la retribuzione pensionabile è la media degli
**ultimi 5 anni**. Uno scatto di carriera finale gonfiava la pensione **senza contributi
corrispondenti** sugli anni precedenti.

**Direzione**: ⬆️ **ALZA il gettito.** Il modello usa un profilo salariale liscio (AMECO +
premio costante): non cattura lo **scatto finale**.

**Cosa servirebbe**: uno scenario "ultimo quinquennio +15% / +30%" per misurare quanto sposta.
È l'estensione **più economica** delle tre: non richiede dati nuovi, solo un parametro in più
nel profilo salariale.

---

## 4. Pubblico impiego — questione concettuale aperta, non solo un dato mancante

**Cosa**: la Gestione Dipendenti Pubblici è **esclusa** dal cubo 389 (che copre solo le 5
gestioni private) e dalla nostra intera stima. Vale il **26,6% degli importi** in pagamento.
Regole proprie e più generose: DPR 1092/1973 art. 44 → **2,33%/anno** per i primi 15 anni; e
**fino al 1992 nessun tetto pensionabile** che abbattesse i rendimenti.

**Ma c'è di più di un dato mancante.** Nel pubblico impiego una parte rilevante della
contribuzione è **figurativa**: lo Stato è insieme datore di lavoro e assicuratore, e i
"contributi" del datore pubblico sono una partita di giro dentro il bilancio dello Stato.
Chiedersi «quanto ha versato questo pensionato» ha un significato diverso rispetto al privato.
**Il concetto di "componente non finanziata" va ridefinito prima di poterlo misurare** — non è
un'estensione meccanica del metodo.

**Direzione**: ⬆️ probabile rialzo (regole più generose), **ma non è la stessa grandezza**.

**Cosa servirebbe**: prima una definizione, poi i dati. La richiesta di dati già formulata
(cfr. `analisi/output/richiesta_dati_verificata.md`) chiede esplicitamente l'estensione della
scomposizione per regime **al pubblico impiego**.

---

## Sintesi

| Estensione | Direzione | Costo di quantificazione |
|---|---|---|
| 1. Fondi speciali (aliquote >2% ante-1995) | ⬆️ | medio — servono le norme dei singoli fondi |
| 2. Ex-INPDAI (massimale contributivo) | ⬆️ **sulla coda alta** | medio — manca la numerosità |
| 3. Quota A (ultima retribuzione) | ⬆️ | **basso** — solo un parametro |
| 4. Pubblico impiego | ⬆️ *ma da ridefinire* | alto — questione concettuale, poi dati |

**Tutte spingono al rialzo. Il €10,6 mld regge da solo, ed è il bordo basso.**
