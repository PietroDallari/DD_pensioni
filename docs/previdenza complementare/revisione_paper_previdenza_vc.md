# Revisione — "Prima i Fondi Pensione, poi il Venture Capital" (Policy Paper ORA! | Innovazione, maggio 2026)

Data revisione: 16 luglio 2026 — **v2, con esiti delle verifiche su fonte primaria**

**Legenda stati:** ✅ risolto · 🔧 fix pronto, da applicare · 📌 riassegnato · 🔴 aperto

**Nota di metodo.** La revisione è avvenuta in tre passaggi, documentati item per item così che ogni correzione sia ripercorribile: (1) verifica di coerenza interna (aritmetica delle tabelle, incroci tra sezioni); (2) verifica su fonti secondarie (stampa specializzata, comunicati ufficiali); (3) verifica su fonte primaria dove la secondaria non bastava — in particolare il PDF del report Growth Capital / Italian Tech Alliance FY-25 (scaricato e parsato, conservato come evidenza) e i testi originali di Gompers-Lerner. Ogni numero corretto riporta la fonte e la pagina.

---

## 1. Posizionamento e punti validi

Il paper regge. La tesi è una tesi di **sequenza**, non di merito: l'obiettivo (capitale previdenziale nel VC italiano) è condiviso, ma le misure recenti invertono l'ordine logico chiedendo a un secondo pilastro sottodimensionato di comportarsi da LP istituzionale maturo.

Punti di forza da preservare in revisione:

- **La lettura corretta di ERISA.** La chiarificazione del 1979 rimosse un vincolo a un sistema già grande e competente; non lo creò. È l'argomento più forte del paper e disinnesca il riferimento storico più abusato dai sostenitori delle misure attuali. (E la verifica E3, sotto, ha confermato che il testo è fedele alla fonte.)
- **L'incoerenza dimensionale.** Fino a ~2 mld di flussi indotti verso un mercato che investe ~1,7 mld/anno e i cui gestori raccolgono in media ~590 mln/anno (serie 2020–2025 ora verificata su fonte primaria).
- **L'incoerenza fiduciaria.** Dati Kauffman sulla dispersione dei rendimenti VC (20/100 sopra PME+3%; 4/30 tra i fondi >400 mln) e sul "bucket filling" da mandati obbligatori — verificati, corrispondono al report.
- **La gestione dell'obiezione "perdiamo anni"** in conclusione: parallelismo con strumenti distinti per ciascun fronte, non scorciatoia unica.
- **La distinzione cassa vs attuariale sul costo dell'EET** (§2.3): corretta, ed è esattamente il punto dove tipicamente si annida l'errore lordo/netto.

Corroborazione aggiuntiva emersa in verifica: la sezione 4.3 del report GC FY-25 riproduce indipendentemente le tabelle Ambrosetti su cui il paper si appoggia (AUM/PIL, allocazione 26,4/40,1, esposizioni 0,14%/0,29%, scenari 503/908/1.963, LP per area 33/32/24/9/2) — tutte coincidenti.

---

## 2. Errori accertati

### E1 — Numero di round VC (tabella §2.6) ✅ RISOLTO
**Sintomo.** La colonna "numero di round" riportava 3.113 / 3.717 / 3.405 / 2.701 / 2.446 / 2.091 per gli anni 2020–2025: valori ~5 volte superiori a quelli noti per l'Italia e, anomalia narrativa, in *calo* costante mentre il testo parla di mercato in crescita.

**Processo di verifica.** Primo controllo su fonti secondarie: la stampa di gennaio 2026 (comunicato GC/ITA) dà per il 2025 "1,735 miliardi in 436 round" — incompatibile con 2.091. Secondo passo, fonte primaria: scaricato e parsato il PDF del report *Venture Capital Report — Italy Q4-25 & FY-25* (74 pagine). **Causa radice trovata:** la colonna incriminata è la serie dei round del **Regno Unito**, copiata verbatim da pagina 17 del report (§2.2.1, "Snapshot on Venture Capital in the UK") e incollata sotto la tabella Italia. Non un problema di perimetro o metodologia: un errore di copia-incolla tra due tabelle dello stesso report.

**Correzione applicata** (dal grafico Italia, §3.1.1, p. 22 del report):

| Anno | Investito (mln €) | Round (errato) | Round (corretto) |
|---|---|---|---|
| 2020 | 537 | ~~3.113~~ | **189** |
| 2021 | 1.283 | ~~3.717~~ | **290** |
| 2022 | 1.867 | ~~3.405~~ | **327** |
| 2023 | 1.156 | ~~2.701~~ | **316** |
| 2024 | 1.463 | ~~2.446~~ | **405** |
| 2025 | 1.735 | ~~2.091~~ | **436** |

**Controlli incrociati superati:** (a) i trimestrali del report (p. 23) sommano esattamente agli annuali per ogni anno (2025: 102+107+105+122 = 436); (b) Q3=105 e Q4=122 coincidono con il comunicato stampa di gennaio 2026; (c) gli scostamenti rispetto ai dati stampa dei primi trimestri (all'epoca Q1=88, Q3=75) sono spiegati dall'integrazione retroattiva dei round confidenziali, ora documentata in una nota metodologica di 3 righe nel paper; (d) la colonna ammontari coincide al centesimo con quella già presente nel paper — nessuna correzione necessaria; (e) il 2024 è rivisto retroattivamente a 405 (era 417 nel report FY-24), coerente con la metodologia GC.

**Effetto collaterale positivo:** la serie corretta mostra round in *crescita* (189→436), coerente con la narrativa "mercato pur in crescita" — la serie sbagliata la contraddiceva.

**Evidenza:** PDF conservato in `docs/previdenza complementare/GrowthCapital_ITA_VC-Report-Italy_Q4-25_FY-25.pdf`.

### E2 — GBER ✅ RISOLTO
Corretto in §3.2: Regolamento (UE) **651/2014** (era 651/2015). Verificato: il GBER è il Reg. (UE) n. 651/2014 della Commissione, 17 giugno 2014.

### E3 — "Oltre la metà" vs tabella Gompers-Lerner ✅ RISOLTO (fix da applicare 🔧)
**Sintomo.** Il testo (§1 e §4) afferma che "otto anni dopo" i fondi pensione erano "oltre la metà di tutti i commitment"; la tabella mostrata dà per il 1987: 27% privati + 12% pubblici = 39%. Apparente contraddizione interna.

**Processo di verifica.** Recuperata la formulazione originale degli autori (il PDF JEP sull'AEA è dietro bot-protection; il contenuto è confermato da fonti primarie degli stessi autori, in particolare Gompers 2004, capitolo per l'*Handbook of Corporate Finance* a cura di Eckbo, che riporta le stesse cifre). Il testo originale dice: nel **1978**, quando 424 milioni di dollari furono investiti in nuovi fondi VC, gli individui erano la quota maggiore (32%) e i fondi pensione solo il 15%; nel **1986**, con oltre 4 miliardi investiti, i fondi pensione superavano il 50% di tutti i commitment.

**Esito: il paper è fedele alla fonte.** "Otto anni dopo" va contato da base 1978 → **1986**, non 1987. Il problema è di impaginazione: il 1986 non compare tra le colonne della tabella (che riporta anni campione: 1979, 1983, 1987...), e il lettore ancora mentalmente sul 1979, calcola 1987, somma 27+12 = 39% e conclude che il testo sbaglia. Peraltro la serie tabellare e il dato aggregato citato nel testo provengono da aggregazioni parzialmente diverse.

**Fix (due mosse):**
1. In §1 e §4, sostituire "Otto anni dopo" con "**Nel 1986**" esplicito.
2. Nota a piè della tabella: *"Il dato del 1986 (>50%) citato nel testo non compare tra le colonne della tabella, che riporta anni campione; per il 1987 la serie tabellare dà 27% privati + 12% pubblici, su una definizione e aggregazione parzialmente diverse."*
3. (Opzionale) Aggiungere in bibliografia Gompers, P., "Venture Capital", in Eckbo (a cura di), *Handbook of Corporate Finance*, 2004, come fonte di conferma.

### E4 — Date ERISA ✅ RISOLTO
Bibliografia allineata al 1979 (final regulation DOL sulla prudent man rule; il riferimento precedente a un "Advisory Opinion, 1980" era incoerente col testo, che correttamente indica il 1979).

### E5 — Tabella PitchBook: duplicato e refuso 📌 RIASSEGNATO A ORA
**Problema.** "Fondenergia" e "Fondenergia Fondo Pensione Complementare" compaiono come due righe distinte (1 commitment ciascuna): quasi certamente la stessa entità, ma stabilire se si tratti di 1 o 2 commitment richiede l'estratto raw PitchBook, a cui questa revisione non ha accesso. **Va verificato da chi in ORA ha effettuato l'estrazione originale.**

**Fix conservativo applicabile subito (non richiede dati):**
1. Correggere il refuso: "Fondo Pensione **di** Intesa Sanpaolo" (era "dei").
2. Unire le due righe Fondenergia con asterisco: *"possibile duplicazione di entità nell'estratto PitchBook, in verifica"*.
3. Dichiarare esplicitamente nel testo che la tabella riguarda commitment a fondi **PE** ed è usata come proxy della capacità di investimento in asset illiquidi, VC incluso.

Nessuna di queste modifiche cambia il messaggio della sezione: "la grande maggioranza si ferma a 1 commitment" regge in entrambi gli esiti della verifica.

---

## 3. Zone rosse metodologiche e di perimetro

### Z1 — "Obbligo" vs "condizione per la detassazione" 🔴 APERTO
§3.1 apre con "obbligo di destinare almeno il 5%... del portafoglio"; §3.2–3.3 e la meccanica descritta (10% del 10% qualificato ≈ 1% dell'AUM) dicono altro: **quota condizionale per accedere a un beneficio fiscale**, non obbligo di portafoglio. È il fianco più esposto del paper: un difensore delle misure lo smonta su questo. Azione: uniformare il linguaggio in tutto il documento (exec summary incluso) e verificare sul testo di legge il perimetro esatto (portafoglio totale vs investimenti qualificati).

### Z2 — "Meno del 40%" è fragile 🔴 APERTO
10,4 mln iscritti / 26 mln forze di lavoro = 40,0% tondo; con il perimetro COVIP (iscritti effettivi su forze di lavoro) il 2025 probabilmente supera il 40%. Azione: "circa il 40%", con numeratore e denominatore espliciti.

### Z3 — Mismatch temporale nell'executive summary 🔴 APERTO
261,2 mld è lo stock a fine 2025; l'11,3% AUM/PIL è il dato 2023 (Ambrosetti/OECD). 261 su PIL 2025 ≈ 12%. Azione: scegliere una coppia coerente di anni.

### Z4 — Perimetro dei contributi: 17,4 mld sotto-dichiara 🔴 APERTO
La tabella somma solo negoziali + PIP nuovi + aperti (7,9+5,6+3,9). Il bollettino COVIP "principali dati" **esclude** preesistenti e PIP vecchi; il totale di sistema è più alto (~20 mld nel 2024, Relazione annuale). Azione: qualificare il perimetro o usare il totale di sistema.

### Z5 — Base dello 0,14% non dichiarata 🔴 APERTO (attenuato)
191 mln / 0,14% ≈ 136 mld ≠ 261 mld: Ambrosetti usa un perimetro di AUM ristretto o datato. La verifica primaria ha nel frattempo confermato che le tabelle Ambrosetti sono riprodotte identiche anche nel report GC FY-25 (§4.3), quindi il dato è consolidato nella letteratura di settore — ma la base su cui è calcolata la percentuale va comunque dichiarata.

### Z6 — Commitment vs deployment ✅ RAFFORZATO CON DATI PRIMARI (riformulazione da applicare 🔧)
**Problema originario:** confrontare 2 mld di commitment (dispiegati su 3–5 anni) con 1,735 mld di investito annuo mischia stock e flusso; il confronto corretto è col fundraising dei gestori.

**Verifica primaria (report GC FY-25, §4.1.1, p. 53) — serie annuale del fundraising:**

| Anno | Raccolta (mln €) | Nuovi fondi |
|---|---|---|
| 2020 | 441 | 7 |
| 2021 | 603 | 9 |
| 2022 | 375 | 6 |
| 2023 | 136 | 4 |
| 2024 | 1.447 | 15 |
| 2025 | 545 | 9 |

Nel processo è emerso e corretto anche un **errore aritmetico nella vecchia tabella trimestrale** del paper: i nuovi fondi per trimestre (+3/+4/+2/+2) sommavano a 11, non ai 9 dichiarati nell'annuale. La tabella trimestrale è stata sostituita dalla serie annuale sopra.

**Avvertenza anti-cherry-picking sulla formulazione.** Il claim "2 mld ≈ 4x la raccolta annuale" regge contro il 2025 (545 mln) ma non contro il 2024 (1.447 mln → ~1,4x). La formulazione robusta usa la **media 2020–2025: ~590 mln/anno → i 2 mld sono ~3,4 volte la raccolta media annuale dei gestori italiani**. Da riformulare così nel paper per non esporre il fianco all'accusa di scelta opportunistica dell'anno.

### Z7 — Due numeri senza fonte 🔴 APERTO
(a) ABP a "30 mld di contributi/anno": sembra alto (ordine più plausibile 15–17 mld/anno) → verificare sul rapporto annuale ABP.
(b) "Mezzo miliardo" di risparmio dal Fondo di garanzia TFR: non derivato. Lo 0,20% su un monte retributivo privato di ~600 mld dà ~1,2 mld a regime pieno; la riduzione sarebbe proporzionale alla quota di TFR conferita, con code sul pregresso. Azione: esplicitare la base di calcolo o marcare come stima da relazione tecnica.

### Z8 — Duplicazione editoriale in §2.3 🔴 APERTO
I due paragrafi consecutivi su TFR/Fondo di Tesoreria ripetono due volte le soglie 60/50/40 e la frase "resta TFR". Refuso di drafting: fondere.

---

## 4. Punti verificati che reggono ✅

- Limite di deducibilità **5.300 €** dal periodo d'imposta 2026 (L. 199/2025, art. 1 c. 201, che modifica l'art. 8 D.Lgs. 252/2005; extra-deduzione giovani a 2.650 €/anno, plafond 7.950 €).
- Range **230–430 mln per miliardo dedotto**: coerente con i nuovi scaglioni IRPEF 23/33/43.
- Aritmetica interna COVIP e MEF: 261,2 = somma componenti; 17,4 = somma tabella; 2.605 mld / 4,9 mln beneficiari = 529 €.
- **Due mega round da 356 mln** = Bending Spoons 234M + AAvantgarde 122M; 356/1.735 = 20,5%.
- **Colonna ammontari VC 2020–2025**: verificata al centesimo contro il report primario GC FY-25 — zero scostamenti.
- **Impasse attuativa** corroborata: Italian Tech Alliance stessa ha lamentato pubblicamente i dubbi interpretativi che impediscono l'applicazione dell'incentivo.
- **Testo su Gompers-Lerner fedele alla fonte** (v. E3): la contraddizione era apparente, di impaginazione.
- **Tabelle Ambrosetti** riprodotte identiche nel report GC FY-25 (§4.3): AUM/PIL, allocazioni, esposizioni, scenari, LP per area.
- Parametri TFR: aliquota 6,91%, rivalutazione 1,5% + 75% inflazione, Fondo di garanzia 0,20% / 0,40% dirigenti industriali.

---

## 5. Raccordo con il lavoro sulla transizione out-of-PAYG

### Attrito da risolvere: il TFR è rivendicato due volte ⚠️
Il piano di transizione usa la redirezione del TFR come componente del carve-out verso i conti capitalizzati del **primo** pilastro; questo paper (e la tesi Lavoro che assume come prerequisito) propone il conferimento obbligatorio del TFR ai fondi pensione del **secondo** pilastro. Stesso flusso, due destinazioni. Serve una decisione di architettura prima che i due documenti circolino insieme: TFR al primo pilastro capitalizzato, al secondo, o regola di riparto esplicita.

### Complementarità da esplicitare (rimandi incrociati)
1. **Scala.** La transizione risolve il problema di scala che il paper diagnostica: un carve-out del 25–33% del monte contributivo genera flussi annui che in pochi anni sovrastano i 261 mld del secondo pilastro e cambiano il baseline dell'11,3% AUM/PIL. Il paper dovrebbe menzionare che nel quadro ORA la massa critica non arriva solo dal secondo pilastro.
2. **Principio anti-mandato trasversale.** La lezione ERISA vale a fortiori per la transizione: la tentazione di indirizzare per legge i flussi del carve-out verso "economia reale" italiana è identica a quella qui criticata. Un principio comune (neutralità allocativa, solo standard fiduciari) rafforza entrambi i documenti e vaccina il piano di transizione da un'obiezione prevedibile.
3. **Assorbimento e cornice CMU/europea.** L'argomento "2 mld distorcono un mercato da 1,7" è la versione in miniatura del problema di assorbimento dei flussi da carve-out, a cui il lavoro sulla transizione risponde con la cornice europea: il paper potrebbe rimandarvi invece di lasciare il tema implicito.
4. **Quadro fiscale cumulato.** EET + deducibilità 10k (0,7–2,2 mld lordi) devono stare nello stesso quadro di finanza pubblica del bridge BTP (picco 3–5 punti PIL), con la solita disciplina lordo/netto e cassa/competenza.
5. **Disciplina dei perimetri.** I problemi Z3–Z5 sono la stessa famiglia degli errori morfologici già documentati altrove (perimetri conflati, stock/flussi, anni disallineati) — e anche l'errore E1 appartiene alla famiglia: una serie geografica sbagliata sotto un'etichetta giusta. Vale la stessa regola: ogni numero con base, anno, geografia e fonte espliciti.

---

## Riepilogo operativo

| Item | Stato | Prossima azione | Chi |
|---|---|---|---|
| E1 round VC | ✅ risolto | — (tabella corretta nel paper) | fatto |
| E2 GBER | ✅ risolto | — | fatto |
| E3 Gompers-Lerner | ✅ verificato | applicare fix "Nel 1986" + nota tabella | redazione |
| E4 date ERISA | ✅ risolto | — | fatto |
| E5 PitchBook | 📌 riassegnato | verificare estratto raw; intanto fix conservativo | ORA (chi ha fatto l'estrazione) |
| Z1 obbligo/incentivo | 🔴 aperto | uniformare linguaggio + verifica testo di legge | redazione |
| Z2 "meno del 40%" | 🔴 aperto | riformulare "circa il 40%" con perimetro | redazione |
| Z3 mismatch anni | 🔴 aperto | allineare stock e ratio | redazione |
| Z4 perimetro contributi | 🔴 aperto | qualificare o usare totale di sistema | redazione |
| Z5 base 0,14% | 🔴 attenuato | dichiarare la base AUM | redazione |
| Z6 commitment/fundraising | 🔧 fix pronto | riformulare con media 2020–25 (~3,4x) | redazione |
| Z7 ABP + Fondo garanzia | 🔴 aperto | sourcing (rapporto ABP; base di calcolo) | redazione/analisi |
| Z8 duplicazione §2.3 | 🔴 aperto | fondere i paragrafi | redazione |
