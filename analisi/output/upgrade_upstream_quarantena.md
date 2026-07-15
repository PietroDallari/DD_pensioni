# Upgrade del pin upstream — **VERIFICATO E ADOTTATO** ✅

> **Esito finale**: pin aggiornato a `0d7a5b7` **con bypass AMECO dichiarato**. La regressione
> da clone pulito è verde — le nostre grandezze escono a **delta zero** — e i test del
> calcolatore passano 22/22. Il bypass conserva il sentiero salariale AMECO neutralizzando
> `contractual_salary_profile`, stesso pattern dell'override sui tassi ufficiali; il repo di
> Nazareno non è modificato.
>
> Il percorso che ha portato qui è documentato sotto. La prima valutazione era «non adottato»
> perché un intervallo dichiarato si rompeva *se* si adottavano gli indici contrattuali; la
> soluzione (opzione b: adottare i bug fix ma bypassare il sentiero contrattuale) conserva il
> metodo AMECO e riporta il delta a zero — cfr. §8.

## 1. Cosa correggono davvero i commit di Nazareno

| Commit | Correzione, nel merito |
|---|---|
| `bcfda17` | **Bug reale**: con `mesi_lavorati_annui < 12`, 37 e 41 anni di contributi producevano lo **stesso montante** (`min(8, 10.8)` = `min(8, 12)` = 8). Ora moltiplica invece di prendere il minimo. |
| `a36819a` | I contributi si allocano **all'indietro dal pensionamento**: i buchi finiscono a inizio carriera. Motivazione dell'autore: *«ricostruzione prudente per chi ha buchi a inizio carriera»*. Aggiunge anche la scomposizione contributi lavoratore/datore. |
| `52abdf7` | Nuovo `download_contract_wages.py` (**indici ISTAT delle retribuzioni contrattuali**, dataflow 155_318) + ipotesi di longevità. |
| `0d7a5b7` | Perequazione della pensione in `calculate_paid_pension_metrics`. |
| `19485d7` | Categorie di assistenza territoriale — non ci riguarda. |

I primi due **non ci toccano**: si attivano solo se `anni_contribuiti < anni_disponibili` o
`mesi < 12`, e noi usiamo sempre `anni = disponibili` e `mesi = 12`. *(Predizione fatta prima
del test, e confermata: il caso legacy 33a/58 esce a delta 0,000%.)*

## 2. Ma un terzo cambiamento ci tocca — e non l'avevo previsto

`52abdf7` modifica **`salary_profile`**, che ora chiama prima `contractual_salary_profile()`:
**usa gli indici ISTAT delle retribuzioni contrattuali per dare forma al sentiero salariale
fra i punti noti**, invece dell'interpolazione geometrica.

È un **miglioramento reale** del calcolatore. Ma per noi è un **conflitto di metodo**: il
nostro Scenario B costruisce il sentiero salariale con **AMECO** (retribuzioni nominali per
occupato, 1960-2025), e lo passa al calcolatore come `ral_iniziale` + `ral_finale`. Col pin
nuovo, il calcolatore **sovrascrive la forma interna del sentiero** con gli indici CCNL.

Il risultato non sarebbe più «sentiero AMECO», ma «**estremi AMECO + interno CCNL**» — una
cosa diversa da quella che il report dichiara.

## 3. La tabella dei delta

| Grandezza | Pin vecchio | Pin nuovo | Δ |
|---|---|---|---|
| quota non finanziata, legacy 33a/58 | 37,66% | 37,66% | **0,000%** |
| quota non finanziata, carriera 38a/63 | 37,95% | 38,87% | +2,40% |
| quota non finanziata, carriera piena 40a/65 | 32,46% | 33,44% | +3,01% |
| pensione contributiva, 38a/63 | 14.518,6 | 14.305,3 | −1,47% |
| montante scenario demo `carriera_lunga` | 615.129 | 645.161 | **+4,88%** |

E sullo Scenario B completo (configurazione 3, premio correlato):

| Fascia | Quota vecchia | Quota nuova |
|---|---|---|
| 2.000 | 40,9% | 41,8% |
| 3.000 | 43,3% | **44,3%** |
| 5.000 | 37,1% | 38,5% |
| 8.000 | 30,5% | 32,4% |
| 10.000 | 28,1% | 30,1% |
| **Gettito netto** | **10,6 mld** | **10,7 mld** |

## 4. Il criterio, applicato

Fissato **prima** di guardare i risultati:

| Test | Esito |
|---|---|
| Eccesso resta in **28-43%** | ❌ **ROTTO** — diventa **30,1-44,3%** |
| Gettito resta in **9-12 mld** | ✅ 10,7 |
| Vintage IVS resta sopra **212** | ✅ non dipende dal calcolatore |
| Picco BTP resta in **61-103** | ✅ non dipende dal calcolatore |

**Un intervallo si rompe** (il bordo alto dell'eccesso: 43,3 → 44,3). Il criterio dice:
*«se anche un solo intervallo si rompe, il pin nuovo va in quarantena — si decide insieme, non
in autonomia»*.

## 5. Perché la quarantena è la scelta giusta, non un formalismo

Presa da sola, la rottura è **cosmetica**: nessuna conclusione si inverte, l'eccesso resta
positivo ovunque e decrescente nell'importo, il gettito si muove di **+0,1 mld**. Basterebbe
aggiornare l'intervallo dichiarato da «28-43» a «30-44».

**Ma il punto 2 non è cosmetico.** Adottare il pin significherebbe che il report dichiara un
metodo («sentiero salariale AMECO») che il codice non esegue più. Le opzioni sono due, e sono
una **scelta di metodo**, non un aggiornamento di numeri:

- **(a)** Adottare il pin e **abbandonare AMECO**, lasciando che il calcolatore usi gli indici
  CCNL ISTAT. Più aderente alle dinamiche contrattuali reali, ma perde la copertura 1960-2025
  di AMECO e cambia la fonte dichiarata nel report.
- **(b)** Adottare il pin e **bypassare `contractual_salary_profile`**, per conservare il
  sentiero AMECO. Tecnicamente possibile (un secondo monkey-patch), ma significa rifiutare
  proprio il miglioramento che il commit introduce.

Non la decido io.

## 6. Effetto collaterale da valutare comunque

Il nuovo upstream fa una **chiamata di rete all'import del modulo**: `load_contract_wages()` è
al livello del modulo, e senza cache scarica dal dataflow ISTAT `155_318`. Finché non è
popolata, **`import pension_paid_calculator` fallisce senza rete** — anche per i nostri script
che le retribuzioni contrattuali non le usano.

È una fragilità nuova (il pin vecchio ha lo stesso pattern solo per i tassi di
capitalizzazione, che però abbiamo già in cache). Vale la pena segnalarla a Nazareno: è il
tipo di cosa che un autore vuole sapere, e apre la collaborazione.

## 7. Stato

- Pin: **`1007648`**, invariato.
- Il report resta riproducibile: regressione verde, nessun numero cambia.
- Backlog aggiornato in `analisi/FASE2_estensioni.md`.

---

## 8. Esito: adottato con bypass (aggiornamento finale)

La quarantena si è chiusa scegliendo l'**opzione (b)**: adottare il pin `0d7a5b7` — così
incassiamo i due bug fix upstream, che per noi sono a delta zero — e **bypassare
`contractual_salary_profile`** per conservare il sentiero salariale AMECO.

**Perché (b) e non (a).** Gli indici ISTAT delle retribuzioni contrattuali misurano i **minimi
negoziali**; AMECO le retribuzioni **effettivamente percepite** per occupato. Il controfattuale
contributivo si costruisce sui contributi **versati**, che seguono l'imponibile reale, non il
minimo tabellare: lo slittamento salariale (superminimi, scatti, premi) sta nella prima serie e
non nella seconda. La scelta AMECO è anche la **più conservativa** — gli indici contrattuali
alzerebbero l'eccesso di 2-3 punti per fascia e il gettito di +0,1 mld.

**Verifica.** Regressione da **clone pulito** con pin nuovo + bypass:

| Grandezza | Report | Clone pulito | Delta |
|---|---|---|---|
| quota legacy 33a/58 | 37,662% | 37,662% | < 0,0004 |
| quota carriera 38a/63 | 37,955% | 37,955% | < 0,0004 |
| quota piena 40a/65 | 32,463% | 32,463% | < 0,0004 |
| passività Via A / Via B | 2.599 / 2.297 | 2.599 / 2.297 | 0 |
| picco BTP | 94 mld | 94 mld | 0 |
| profilo mediano | 22.650 → 27.239 | idem | 0 |
| test calcolatore | — | **22/22** | — |

**Delta zero confermato.** Nessun numero del report cambia; la voce di backlog è chiusa.

**Robustezza di rete** (requisito collaterale, risolto). Il calcolatore fa chiamate di rete
all'import del modulo, e ISTAT è instabile. La pipeline ora: (1) prova la fonte viva con retry;
(2) se ISTAT non risponde, ricade su uno **snapshot versionato** (`analisi/cache_istat/`, 68K,
output degli script di download upstream). La replica è così **deterministica** e non dipende
dall'uptime ISTAT. La fragilità upstream (rete all'import) resta da segnalare a Nazareno.
