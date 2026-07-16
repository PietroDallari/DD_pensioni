# Revisione — "Prima i Fondi Pensione, poi il Venture Capital" (Policy Paper ORA! | Innovazione, maggio 2026)

Data revisione: 16 luglio 2026

---

## 1. Posizionamento e punti validi

Il paper regge. La tesi è una tesi di **sequenza**, non di merito: l'obiettivo (capitale previdenziale nel VC italiano) è condiviso, ma le misure recenti invertono l'ordine logico chiedendo a un secondo pilastro sottodimensionato di comportarsi da LP istituzionale maturo.

Punti di forza da preservare in revisione:

- **La lettura corretta di ERISA.** La chiarificazione del 1979 rimosse un vincolo a un sistema già grande e competente; non lo creò. È l'argomento più forte del paper e disinnesca il riferimento storico più abusato dai sostenitori delle misure attuali.
- **L'incoerenza dimensionale.** Fino a ~2 mld di flussi indotti verso un mercato che investe ~1,7 mld/anno e i cui gestori raccolgono 545 mln/anno.
- **L'incoerenza fiduciaria.** Dati Kauffman sulla dispersione dei rendimenti VC (20/100 sopra PME+3%; 4/30 tra i fondi >400 mln) e sul "bucket filling" da mandati obbligatori — verificati, corrispondono al report.
- **La gestione dell'obiezione "perdiamo anni"** in conclusione: parallelismo con strumenti distinti per ciascun fronte, non scorciatoia unica.
- **La distinzione cassa vs attuariale sul costo dell'EET** (§2.3): corretta, ed è esattamente il punto dove tipicamente si annida l'errore lordo/netto.

I problemi stanno nei dati di contorno e in alcune incoerenze interne, elencati sotto.

---

## 2. Errori accertati (da correggere prima di qualsiasi circolazione)

### E1 — Numero di round VC (tabella §2.6): sbagliato di ~10x ✅ RISOLTO (16 lug 2026, fonte primaria)
La tabella riportava 2.091 round nel 2025 (2.446 nel 2024, 3.717 nel 2021, ecc.). **Diagnosi precisa dalla fonte primaria** (report FY-25 scaricato e parsato): quei conteggi **non sono europei** (Europa 2025 = 10.206 round) ma sono la **serie UK** presa da pag. 17 del report — §2.2.1 "Snapshot on Venture Capital in the UK" (UK: 3.113 / 3.717 / 3.405 / 2.701 / 2.446 / 2.091 round; 16,4–21,6 mld €). Qualcuno ha incollato la colonna round della slide UK sotto una tabella Italia. Gli **ammontari** Italia invece tornavano esatti.

Serie Italia corretta, dal report FY-25 §3.1.1 (database Growth Capital, dato annuale rivisto, include round confidenziali):

| Anno | Investito (mln €) | Round |
|---|---|---|
| 2020 | 537 | 189 |
| 2021 | 1.283 | 290 |
| 2022 | 1.867 | 327 |
| 2023 | 1.156 | 316 |
| 2024 | 1.463 | 405 |
| 2025 | 1.735 | 436 |

Verifica incrociata: i round trimestrali di pag. 23 sommano esattamente agli annuali di pag. 22 per ogni anno (2025: 102+107+105+122 = 436). Il "389 vs 436" temuto (somma trimestri disclosed-only) è superato: nel report FY-25 i trimestri sono già rivisti per includere i round confidenziali. Ammontari: zero scostamenti vs paper (nota: pag. 22 etichetta 2020 come 536M e 2024 come 1.465M, ma pag. 9/24 e i "key numbers" usano 537M e 1.463M — micro-incoerenza di arrotondamento interna al report; il paper usa già la versione 537/1.463). Il 2024 è rivisto a **405** round (era 417 nel report FY-24). **Tabella §2.6 corretta nel paper + nota metodologica aggiunta.** PDF fonte conservato in cartella: `GrowthCapital_ITA_VC-Report-Italy_Q4-25_FY-25.pdf`.

**Bonus Z6 (fundraising annuale 2020-2025)** ricostruito da §4.1.1 (pag. 53) e inserito nel paper in sostituzione della tabella trimestrale (i cui conteggi nuovi-fondi +3/+4/+2/+2 = 11 non tornavano col totale annuo di 9): 2020 441M/7 · 2021 603M/9 · 2022 375M/6 · 2023 136M/4 · 2024 1.447M/15 · 2025 545M/9. Rafforza l'argomento "2 mld ≈ 4x la raccolta annuale dei gestori italiani". **Bonus corroborazione**: il report FY-25 §4.3 riproduce direttamente le tavole Ambrosetti usate nel paper (AUM/PIL, asset allocation 26,4/40,1 ecc., 0,14%/0,29%, scenari 503/908/1.963, LP per area 33/32/24/9/2) — tutte verificate coincidenti.

### E2 — GBER: Regolamento (UE) 651/**2014**, non 651/2015 ✅ CORRETTO nel paper
§3.2. Errore piccolo ma collocato nel passaggio in cui il paper accusa il legislatore di sciatteria definitoria: lì i refusi normativi non sono ammessi.

### E3 — Contraddizione interna sulla tabella Gompers-Lerner ⛔
Il testo (§1 e §4) afferma che "otto anni dopo" i fondi pensione erano "oltre la metà di tutti i commitment"; la tabella mostrata dà per il 1987: 27% privati + 12% pubblici = **39%**. La frase di G&L si riferisce al 1986 (colonna assente) e a una definizione aggregata. Un lettore ostile fa la somma e contesta. Azione: nota esplicativa oppure riformulare in "erano già la prima fonte di capitale".

### E4 — Date ERISA incoerenti tra testo e bibliografia ✅ CORRETTO nel paper
Testo: 1979 (corretto — final regulation DOL sulla prudent man rule, giugno 1979, 44 FR 37221). Bibliografia aggiornata: la voce ex-"Advisory Opinion, 1980" è ora "Regulation relating to the 'prudent man' standard of care (29 CFR 2550.404a-1), giugno 1979", coerente col testo.

### E5 — Tabella PitchBook: duplicato e refuso ⛔
"Fondenergia" e "Fondenergia Fondo Pensione Complementare" compaiono come due righe distinte (1 commitment ciascuna): quasi certamente la stessa entità → dedup (o 2 commitment su una riga). Refuso: "Fondo Pensione **dei** Intesa Sanpaolo". Inoltre: la tabella è su fondi **PE** usata come proxy della capacità VC — legittimo, ma va dichiarato esplicitamente nel testo.

---

## 3. Zone rosse metodologiche e di perimetro

### Z1 — "Obbligo" vs "condizione per la detassazione" 🔴
§3.1 apre con "obbligo di destinare almeno il 5%... del portafoglio"; §3.2–3.3 e la meccanica descritta (10% del 10% qualificato ≈ 1% dell'AUM) dicono altro: **quota condizionale per accedere a un beneficio fiscale**, non obbligo di portafoglio. È il fianco più esposto del paper: un difensore delle misure lo smonta su questo. Azione: uniformare il linguaggio in tutto il documento (exec summary incluso) e verificare sul testo di legge il perimetro esatto (portafoglio totale vs investimenti qualificati).

### Z2 — "Meno del 40%" è fragile 🔴
10,4 mln iscritti / 26 mln forze di lavoro = 40,0% tondo; con il perimetro COVIP (iscritti effettivi su forze di lavoro) il 2025 probabilmente supera il 40%. Azione: "circa il 40%", con numeratore e denominatore espliciti.

### Z3 — Mismatch temporale nell'executive summary 🔴
261,2 mld è lo stock a fine 2025; l'11,3% AUM/PIL è il dato 2023 (Ambrosetti/OECD). 261 su PIL 2025 ≈ 12%. Accostati nella stessa frase creano un'incoerenza verificabile in dieci secondi. Azione: scegliere una coppia coerente di anni (o 2023/2023 o 2025/2025 con ratio ricalcolato).

### Z4 — Perimetro dei contributi: 17,4 mld sotto-dichiara 🔴
La tabella somma solo negoziali + PIP nuovi + aperti (7,9+5,6+3,9). Il bollettino COVIP "principali dati" **esclude** preesistenti e PIP vecchi; la Relazione annuale li include e il totale di sistema è più alto (~20 mld nel 2024). Dire "i contributi raccolti nel 2025 ammontano a 17,4 mld" senza qualificare il perimetro è una conflazione di perimetri. Azione: qualificare ("nelle forme rilevate dal bollettino COVIP") o usare il totale di sistema.

### Z5 — Base dello 0,14% non dichiarata 🔴
191 mln / 0,14% ≈ 136 mld ≠ 261 mld: Ambrosetti usa evidentemente un perimetro di AUM ristretto o datato. Azione: dichiarare la base su cui è calcolata la percentuale.

### Z6 — Commitment vs deployment (stock vs flusso) 🔴
Confrontare 2 mld di commitment (dispiegati su 3–5 anni) con 1,735 mld di investito annuo mischia categorie. Il confronto corretto — e più forte — è col **fundraising**: 545 mln raccolti da 9 nuovi fondi nel 2025 → i 2 mld sarebbero ~4x la raccolta annuale dei gestori italiani. Correzione che rafforza la tesi.

### Z7 — Due numeri senza fonte 🔴
(a) ABP a "30 mld di contributi/anno": sembra alto (i premi ABP viaggiano più sull'ordine dei 15–17 mld/anno) → verificare sul rapporto annuale ABP.
(b) "Mezzo miliardo" di risparmio dal Fondo di garanzia TFR: non derivato. Lo 0,20% su un monte retributivo privato di ~600 mld dà ~1,2 mld a regime pieno; la riduzione sarebbe proporzionale alla quota di TFR conferita, con code sul pregresso. Azione: esplicitare la base di calcolo o marcare come stima da relazione tecnica.

### Z8 — Duplicazione editoriale in §2.3 🔴
I due paragrafi consecutivi su TFR/Fondo di Tesoreria ripetono due volte le soglie 60/50/40 e la frase "resta TFR". Refuso di drafting: fondere.

---

## 4. Punti verificati che reggono ✅

- Limite di deducibilità **5.300 €** dal periodo d'imposta 2026 (L. 199/2025, art. 1 c. 201, che modifica l'art. 8 D.Lgs. 252/2005; extra-deduzione giovani a 2.650 €/anno, plafond 7.950 €).
- Range **230–430 mln per miliardo dedotto**: coerente con i nuovi scaglioni IRPEF 23/33/43.
- Aritmetica interna COVIP e MEF: 261,2 = somma componenti; 17,4 = somma tabella; 2.605 mld / 4,9 mln beneficiari = 529 €.
- **Due mega round da 356 mln** = Bending Spoons 234M + AAvantgarde 122M; 356/1.735 = 20,5%.
- **Impasse attuativa** corroborata: Italian Tech Alliance stessa ha lamentato pubblicamente i dubbi interpretativi che impediscono l'applicazione dell'incentivo.
- Parametri TFR: aliquota 6,91%, rivalutazione 1,5% + 75% inflazione, Fondo di garanzia 0,20% / 0,40% dirigenti industriali.
- Fundraising 2025: 145+280+35+85 = 545 mln, 9 fondi — confermato.

---

## 5. Raccordo con il lavoro sulla transizione out-of-PAYG

### Attrito da risolvere: il TFR è rivendicato due volte ⚠️
Il piano di transizione usa la redirezione del TFR come componente del carve-out verso i conti capitalizzati del **primo** pilastro; questo paper (e la tesi Lavoro che assume come prerequisito) propone il conferimento obbligatorio del TFR ai fondi pensione del **secondo** pilastro. Stesso flusso, due destinazioni. Serve una decisione di architettura prima che i due documenti circolino insieme: TFR al primo pilastro capitalizzato, al secondo, o regola di riparto esplicita.

### Complementarità da esplicitare (rimandi incrociati)
1. **Scala.** La transizione risolve il problema di scala che il paper diagnostica: un carve-out del 25–33% del monte contributivo genera flussi annui che in pochi anni sovrastano i 261 mld del secondo pilastro e cambiano il baseline dell'11,3% AUM/PIL. Il paper dovrebbe menzionare che nel quadro ORA la massa critica non arriva solo dal secondo pilastro.
2. **Principio anti-mandato trasversale.** La lezione ERISA vale a fortiori per la transizione: la tentazione di indirizzare per legge i flussi del carve-out verso "economia reale" italiana è identica a quella qui criticata. Un principio comune (neutralità allocativa, solo standard fiduciari) rafforza entrambi i documenti e vaccina il piano di transizione da un'obiezione prevedibile.
3. **Assorbimento e cornice CMU/europea.** L'argomento "2 mld distorcono un mercato da 1,7" è la versione in miniatura del problema di assorbimento dei flussi da carve-out, a cui il lavoro sulla transizione risponde con la cornice europea: il paper potrebbe rimandarvi invece di lasciare il tema implicito.
4. **Quadro fiscale cumulato.** EET + deducibilità 10k (0,7–2,2 mld lordi) devono stare nello stesso quadro di finanza pubblica del bridge BTP (picco 3–5 punti PIL), con la solita disciplina lordo/netto e cassa/competenza.
5. **Disciplina dei perimetri.** I problemi Z3–Z5 sono la stessa famiglia dei tre errori morfologici documentati nel lavoro sulla transizione (perimetri conflati, stock/flussi, anni disallineati). Vale la stessa regola: ogni numero con base, anno e fonte espliciti.
