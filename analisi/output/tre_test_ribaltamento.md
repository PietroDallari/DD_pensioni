# I tre test sul "ribaltamento" — ESITO: **il ribaltamento è RESPINTO**

> **Ipotesi sotto esame**: le aliquote di rendimento decrescenti (D.Lgs. 503/1992 art.12)
> obbligavano i futuri pensionati ricchi a retribuzioni altissime su cui hanno versato →
> componente non finanziata ≈ 0 → **la Leva D manca il bersaglio**.
>
> **VERDETTO: RESPINTO.** Era un artefatto di un'assunzione irrealistica.

## TEST 1 — Premio di carriera correlato al censo ❌ **UCCIDE IL RIBALTAMENTO**

Il modello incrociava pensione × premio come **indipendenti**. Non lo sono: le pensioni alte
nascono da carriere **ripide**. Il «ricco a premio 0» — uno che guadagna €225.000 **piatti
dai 25 anni** per 38 anni — non è un caso tipico: è **assurdo**. E l'intera conclusione
viveva solo in quella colonna.

**Quota media sopra €5.000: da 4,2% → 26,3%.** Criterio del test (>15-20%): **superato.**

## TEST 2 — Verifiche normative ✅ **il modello aveva ragione, ed è conservativo**

- **Contributi sopra il tetto: si versavano PIENI.** Prova regina: l'art. 3-ter D.L. 384/1992
  impone **+1 punto** sopra la prima fascia — *non si aggiunge un punto sopra una soglia dove
  non si versa nulla*. E il massimale (art. 2 c.18 L. 335/1995) vale solo per i **nuovi
  iscritti dal 1996**: per i vecchi iscritti, INPS Circ. 177/1996 — «l'**intera retribuzione**,
  senza applicare il massimale».
- **Ante-1988**: sopra il tetto il rendimento era **zero** (non 1,60/1,35…). Il modello,
  applicando le fasce anche a quegli anni, **sovrastima il rendimento dei ricchi** → è
  conservativo.
- **Serie storica del tetto** recuperata (INPS Circ. 114/2009): 1993 = €27.617 → 2010 =
  €42.364 → 2024 = €55.008. *Correzione: i €43.042 che usavo erano il 2011, non il 2010.*

## TEST 3 — Quota A / ex-INPDAI ⚠️ **spinge ancora nella stessa direzione**

**Ex-INPDAI** (dirigenti industria, fondo soppresso nel 2003, L. 289/2002 art. 42): avevano un
**massimale contributivo proprio** (€143k-175k) fino al 2002 e rendimenti più generosi fino al
1994. **Versavano MENO di quanto il modello assume → il loro eccesso è più ALTO.** Pesavano per
il **48% del disavanzo dei fondi speciali** pur essendo il 2,3% delle pensioni.
Numerosità da fonte primaria: **NON TROVATA** (da estrarre dall'Osservatorio INPS per gestione).

## ⚠️ Il falso allarme più serio — e il modello lo aveva già gestito

Segnalato: l'aliquota IVS storica era **19-27%**, non 33%; applicare il 33% retroattivamente
avrebbe gonfiato i contributi versati, rendendo la conclusione un artefatto.
**Verificato: il modello usa già le aliquote storiche.**

| Anno | Aliquota di computo usata dal montante |
|---|---|
| 1972 | **19,21%** |
| 1976 | 23,51% |
| 1993 | 27,17% |
| 1996+ | 33,00% |

Media pre-1996: **24,35%**. Il codice di Nazareno lo gestiva
(`computation = 0.33 if year >= 1996 else financing`), e i valori **coincidono esattamente**
con la serie INPS Circ. 114/2009.

## Nota sulla letteratura — non esiste il muro contro cui temevamo di sbattere

Nessun lavoro calcola l'IRR del retributivo **per fascia di reddito**. La letteratura
(Castellino, Fornero, CeRP, Gronchi) disaggrega per coorte, categoria professionale, *pendenza
della carriera* — **non per livello di reddito**. C'è un **vuoto**, non un muro.

Il benchmark macro però esiste e **ci convalida**:
- **Castellino & Fornero**: contribuzione effettiva **27%** nel 1992 contro un'aliquota di
  equilibrio del **45-55%** ⇒ **circa metà della pensione media non era finanziata**. Il nostro
  38-43% sulle pensioni ordinarie è in linea.
- **Ferraresi & Fornero** (CeRP WP 2/00): NPVR del lavoratore rappresentativo **110-152%**,
  IRR reale 2,2-3,5% — **sempre positivo**, come nel nostro modello col premio correlato.
- **Gronchi (1995)**: il retributivo premia le **carriere ripide** — che è *esattamente* il
  meccanismo del Test 1.

---

# TABELLA FINALE — quota non finanziata per fascia

| Pensione/mese | (1) indip. pr0 | (2) + premio **correlato** | (3) + tetti storici + art.3-ter | (4) + ex-INPDAI |
|---|---|---|---|---|
| 2.000 | 38,0% | 40,9% | **40,9%** | n.q. |
| 3.000 | 34,8% | 43,4% | **43,3%** | n.q. |
| 4.000 | 25,3% | 40,7% | **40,5%** | n.q. |
| 5.000 | 14,3% | 37,5% | **37,1%** | ↑ |
| 8.000 | **0,0%** | 31,2% | **30,5%** | ↑ |
| 10.000 | **0,0%** | 28,9% | **28,1%** | ↑ |
| **media > 5.000** | **4,2%** | 26,3% | **25,8%** | ↑ |

La configurazione (4) non è quantificabile (manca la numerosità ex-INPDAI) ma la **direzione è
certa: alza** la quota della coda alta.

## Gettito dello Scenario B

| Configurazione | Lordo | **Netto** |
|---|---|---|
| (1) indipendente, premio 0 | 7,6 | 4,2 mld |
| **(2)-(3) premio correlato + norma verificata** | **19,2** | **~10,6 mld** |
| — sensibilità sulla pendenza (0,7-1,3) | 16,7-20,9 | **9,2-11,5** |
| (4) + ex-INPDAI | ↑ | ↑ |
| **Scenario A (tetto)** | 31,1 | **17,1 mld** |

# CONCLUSIONE

**L'eccesso è positivo ovunque, grande (26-43%), decrescente nell'importo ma mai nullo.**
La Leva D **è difendibile**: colpisce una platea che ha effettivamente ricevuto una generosità
non finanziata di ~26% anche nella fascia alta.

Lo Scenario B rende **~€10,6 mld netti** (range 9,2-11,5) — il **62% del tetto** — restando
quello costituzionalmente blindato. La configurazione (4), se quantificata, lo alzerebbe.

## Limiti dichiarati

1. **Premio di carriera**: ipotesi dominante, calibrata (0 → +2,25), non osservata.
   Sensibilità sulla pendenza (±30%) → gettito 9,2-11,5 mld.
2. **Ex-INPDAI e fondi speciali**: non quantificati. Direzione nota (alzano).
3. **Quota A sull'ultima retribuzione** (scatto finale di carriera): non modellata. Alza.
4. **Tassi di capitalizzazione pre-1996**: controfattuale costruito, non dato osservato.
