# Uscita dell'Italia dal Pay-As-You-Go

---

## 1. Il contesto

Nel sistema a ripartizione (PAYG) i contributi di chi lavora finanziano le pensioni correnti: non esiste capitale accantonato. Il passaggio alla capitalizzazione reale impone alla generazione di mezzo un doppio pagamento — finanziare i propri conti e continuare a pagare i pensionati attuali, privi di fondo.

Il costo della transizione non si elimina, si sposta soltanto: nel chi paga e nel quando. Ogni schema "a costo zero" nasconde un errore contabile.

Perché affrontarlo, allora. Il guadagno del piano rispetto al baseline è generazionale: una o due generazioni di giovani smettono di essere prigioniere del rendimento nozionale PAYG e risparmiano sul mercato a rendimenti composti decenti. Parte del differenziale è premio al rischio, non un regalo; ma per un giovane italiano l'alternativa non è tra rischio e sicurezza: è tra rischio di mercato diversificato e rischio demografico concentrato su un solo paese. Il secondo non è più sicuro — è solo non diversificabile.

### Il rendimento nozionale del PAYG italiano è reale zero

Non è un'ipotesi: è un dato. Il rendimento nozionale del sistema contributivo **è per legge** il tasso di capitalizzazione del montante, pubblicato ogni anno nella nota ISTAT del Ministero del Lavoro. Confrontandolo con l'inflazione (HICP Eurostat) si ottiene il rendimento **reale** effettivamente riconosciuto:

| Periodo | Nozionale nominale | Inflazione | **Nozionale reale** |
|---|---|---|---|
| 1996-2025 (dall'avvio del contributivo) | 2,82% | 2,08% | **+0,73%** |
| 2006-2025 (ultimi 20 anni) | 1,78% | 2,00% | **−0,21%** |
| 2011-2025 (ultimi 15 anni) | 1,35% | 1,98% | **−0,62%** |
| 2016-2025 (ultimi 10 anni) | 1,70% | 2,20% | **−0,49%** |

*Fonti: tassi ufficiali di capitalizzazione 1976-2025 (nota ISTAT/Ministero del Lavoro, estratti in `analisi/output/scarto_tassi_per_anno.csv`); HICP Italia (Eurostat `prc_hicp_aind`). Medie geometriche.*

Il sistema ha riconosciuto un rendimento reale **negativo** in ognuno degli ultimi tre orizzonti significativi. Questo documento adotta perciò **0% reale** come ipotesi centrale per il PAYG — già generosa rispetto ai −0,2/−0,6% osservati, e coerente con il bordo basso delle proiezioni RGS/Ageing Report (0,5-0,8%, a loro volta ottimistiche rispetto al realizzato).

È il punto centrale della tesi: **il PAYG non offre un rendimento modesto, non ne offre affatto.** Un giovane che versa il 33% per 40 anni riceve indietro, in termini reali, poco più di quanto ha versato. Il confronto con un fondo al 2,5% reale netto non è quindi "rischio contro sicurezza", ma "rendimento contro nessun rendimento".

> ⚠️ **Da ricalcolare.** La tabella qui sotto è ancora costruita sull'ipotesi precedente (PAYG all'1% reale). Con il PAYG a 0% reale la pensione PAYG scende e il vantaggio della proposta **cresce**: i numeri vanno rifatti, e si muoveranno a favore della proposta, non contro.

In concreto, per due profili di lavoratore dipendente (valori reali; carriera di 40 anni, crescita salariale reale 1%, pensione a 67, coefficiente ~5,2%; PAYG rivalutato all'1% reale — *ipotesi superata, cfr. sopra* —, fondo al 2,5% reale netto):

| | Mediano (RAL €27k) | Top 10% (RAL €40k) |
|---|---|---|
| Pensione PAYG (versando il 33%) | €27.600/anno | €40.900/anno |
| Pensione proposta (versando il 25%) | €28.700/anno | €42.500/anno |
| Risparmio annuo in busta (8 punti) | ~€2.600 | ~€3.900 |
| Capitale accumulato a 67 anni | ~€550k | ~€820k |

Stessa pensione (o poco più), 8 punti di contributi in meno per 40 anni, e a fine carriera un capitale proprio — ereditabile e visibile — al posto di un saldo nozionale. Le ipotesi sono prudenti verso la proposta: l'1% reale per il PAYG è il bordo alto delle proiezioni demografiche (RGS/Ageing Report: 0,5-0,8%), mentre il 2,5% netto reale è conservativo per un profilo lifecycle giovane.

---

## 2. Le quattro popolazioni da gestire

| Gruppo | Chi sono | Stato | Trattamento nel piano |
|---|---|---|---|
| **1. Legacy in pensione** | Retributivi/misti già pensionati (~16 mln) | ~€290 mld/anno, si estingue in ~30 anni | Si pagano (diritti acquisiti). Unico intervento: prelievo obbligatorio sui retributivi ricchi |
| **2. Contributivi che switchano** | Entrati dal 1996, ~12-13 mln, under ~50 | Conti nozionali "paper": i contributi versati sono stati spesi | Passato riconosciuto come IOU; futuro auto-finanziato |
| **3. Misti ancora attivi** | <18 anni di contributi nel 1995, ~8-9 mln, ~48-67enni | Dal 2012 maturano già contributivo (riforma Fornero) | Resta dovuta solo la quota retributiva pre-1996; margine modesto e protetto |
| **4. Lavoratori futuri** | Nuovi ingressi | — | Interamente a capitalizzazione dal primo giorno |

---

## 3. Ipotesi

| Parametro | Valore | Fonte/nota |
|---|---|---|
| Spesa pensionistica (legacy) | ~€290 mld/anno | INPS 2025 (~15,3% PIL); cala a ~0 in ~30 anni |
| Contributi IVS totali | ~€240 mld/anno | Di cui ~€100 mld dai contributivi puri |
| Disavanzo strutturale attuale | €290 − €240 = €50 mld/anno | Coperto dalla fiscalità generale |
| Rendimento nozionale PAYG | **0% reale** | **Dato, non ipotesi**: tassi ufficiali di capitalizzazione vs HICP → −0,21% (20 anni), −0,62% (15 anni). Cfr. §1 |
| Beneficiari totali | **16,06 mln** | INPS open data 2016 (dataset 1824) — conferma la stima |
| Pensionati > €3.000 **lordi**/mese | **1,10 mln** (6,9%) | INPS open data 2016 (dataset 1824). ⚠️ La platea in **netto** non è osservabile: la classe INPS superiore è aperta ("3.000 e più") |
| Regime di liquidazione (quota di spesa) | **85,9% retributivo, 13,0% misto, 1,1% contributivo puro** | INPS open data (dataset 1648). Conferma: i pensionati ricchi sono retributivi/misti |
| Componente non finanziata (retributivo vs controfattuale contributivo) | **~17% a 25 anni di anzianità, ~8% a 38, ~4% a 40** | Microsimulazione su distribuzione INPS + calcolatore. **Non il 50%** — cfr. §4-D |
| TFR — flusso annuo | ~€30 mld/anno | Mobilizzabile (denaro nuovo) |
| TFR — stock in azienda | ~€242 mld | Non mobilizzabile in blocco (debito embedded nei bilanci) |
| Rendimento fondi | 5% nominale | |
| Rendimento BTP 50 anni | 4,3% | Decennale ~3,7% |
| PIL | ~€2.200 mld | |
| Debito pubblico | ~€3.000 mld (~136% PIL) | |

Le cifre sono ordini di grandezza, non un modello calibrato.

### Il perimetro dei €290 mld è ambiguo — e va verificato

Era stato ipotizzato che i €290 mld di spesa (e quindi il disavanzo di €50 mld) fossero **gonfiati dall'assistenza** (GIAS: invalidità civile, assegni sociali, sgravi), che non è previdenza ed è per definizione finanziata dalla fiscalità generale. Se fosse così, il disavanzo previdenziale vero sarebbe minore e l'intero piano più leggero.

**La verifica non conferma l'ipotesi.** Eurostat COFOG (`gov_10a_exp`, Italia 2023):

| Voce | €mld |
|---|---|
| Vecchiaia (*old age*) | 290,9 |
| Superstiti | 50,4 |
| **Pensioni vere (vecchiaia + superstiti)** | **341,3** |
| Malattia/invalidità, famiglia, disoccupazione, esclusione sociale | 108,1 |
| Protezione sociale (totale) | 449,3 |

I €290 mld del documento coincidono con la sola voce **"vecchiaia" della PA nel suo complesso** — non con l'INPS, e **al netto dei €50 mld di superstiti**. Il perimetro è quindi ambiguo, e se si usa l'aggregato pensionistico corretto (€341 mld) la spesa è **più alta**, non più bassa: il disavanzo peggiorerebbe.

Verdetto: **ipotesi non confermata, questione aperta.** Risolverla richiede il Rendiconto generale INPS, che separa gestioni previdenziali e GIAS — disponibile solo come PDF e non ancora estratto. Finché non è fatto, i €290 mld e i €50 mld di disavanzo vanno trattati come **numeri di perimetro incerto**, non come dati.

---

## 4. Le leve

### A — Carve-out con aliquota ridotta

I contributivi dirottano i propri contributi sui fondi privati. Non serve però il 33%: con rendimento reale al 5% (contro un rendimento nozionale PAYG ~2,7%) basta circa il 25% per una pensione equivalente. Gli 8 punti residui restano in PAYG a finanziare il legacy. In pratica dirottano 25/33 × €100 mld = €76 mld, e €24 mld restano in PAYG.

Nota di policy: ogni punto non trattenuto in PAYG è uno sgravio sul costo del lavoro ma un punto di disavanzo in più.

### B — Flusso TFR ai fondi (~€30 mld/anno)

Il TFR maturando confluisce per default nei fondi pensione, costruendo il pilastro a capitalizzazione senza toccare l'IVS. Consente di dirottare ~€30 mld di IVS in meno, al netto dei ~€6 mld del Fondo Tesoreria che lo Stato perde come finanziamento: miglioramento netto ~€24 mld/anno.

Limite: solo il flusso è mobilizzabile. Lo stock (€242 mld) è debito embedded nei bilanci aziendali — quei fondi sono già stati impiegati come finanziamento interno e non costituiscono cassa pronta. Si possono spostare solo gradualmente, su 20-30 anni, con un costo di liquidità reale per le imprese.

### C — Riconoscimento del "paper" dei contributivi

Il saldo nozionale accumulato viene riconosciuto come IOU dello Stato, accreditato sul conto del lavoratore e pagato come rendita solo al pensionamento. Nessuna cassa immediata; la passività (~€1.300-1.500 mld, pari ai saldi nozionali della coorte attuale) scorre via su ~40-70 anni.

### D — Prelievo sui retributivi ricchi → fondo di ammortamento del "paper"

Perché solo il retributivo: il retributivo è calcolato sull'ultimo stipendio e contiene strutturalmente una componente non finanziata (eroga più di quanto versato); il prelievo recupera quella componente. Il contributivo eroga circa quanto versato: tagliarlo equivarrebbe a confiscare i contributi versati, in contraddizione con lo switch stesso.

Il presupposto **regge**: i dati INPS (dataset 1648) confermano che il 98,9% della spesa pensionistica va a regimi retributivo (85,9%) o misto (13,0%), e appena l'1,1% a contributivo puro. La platea esiste.

> ⚠️ **Questa leva è in corso di riprogettazione: la formulazione precedente non regge alla verifica sui dati.**
>
> La versione originale prelevava il **50% della pensione** dei retributivi sopra €3.000 netti/mese, stimando ~€20 mld/anno (650.000 × €60.000 × 50%). La microsimulazione sulla distribuzione INPS reale mostra tre problemi:
>
> 1. **Il 50% piatto non è la componente non finanziata.** Confrontando ogni classe di importo col proprio controfattuale interamente contributivo, l'eccesso effettivo è **~8%** della pensione a 38 anni di anzianità — non 50%. Un prelievo al 50% **confischerebbe contributi versati**, distruggendo proprio la difesa costituzionale della leva (§10).
> 2. **Il gettito difendibile è 1,8-7,7 mld/anno**, non 20. Prelevando il 100% della *sola* componente non finanziata sopra €3.000 lordi: €7,7 mld (25 anni di anzianità) → €1,8 mld (40 anni). **Da 3 a 13 volte meno** della stima originale.
> 3. **L'asse di targeting è sbagliato.** La generosità non finanziata non cresce con l'importo: cresce al **calare dell'anzianità** (~17% a 25 anni, ~8% a 38, ~4% a 40). Un dirigente con 40 anni di contributi ha una pensione quasi pari al suo controfattuale contributivo; una baby-pensione con 20 anni no. **La leva va agganciata al rapporto pensione/anni versati, non alla soglia di importo.**
>
> **Limite di stima, dichiarato.** Una stima aggregata *solida* non è ottenibile dai soli open data: la distribuzione congiunta **importo × anzianità × regime non esiste** (il dataset con il regime non ha le classi di importo, e nessun dataset incrocia anzianità e importo). La quota retributiva per classe è quindi imputata, non osservata. Il calcolo è invece **pienamente eseguibile da chi ha i microdati** (INPS/RGS dispongono degli estratti contributivi individuali): è un limite di *accesso ai dati*, non di metodo.
>
> Conseguenza sul piano: il Comparto 2 (§6) non è più coperto per ~⅔ dal fondo della Leva D. **Il §6 e il §7 vanno ricalcolati.**

Durata e profilo: non si crea più alcun retributivo puro (le maturazioni sono cessate nel 1995/2011), quindi la platea con quota retributiva coincide con i pensionati attuali più i misti che andranno in pensione fino al ~2045-2050. La base è perciò finita e calante. È asset-liability matching con la passività di riconoscimento (Leva C), con una coda: la fonte si esaurisce intorno al 2070 mentre le rendite di riconoscimento corrono fino al ~2095.

Durata e profilo: non si crea più alcun retributivo puro (le maturazioni sono cessate nel 1995/2011), quindi la platea con quota retributiva coincide con i pensionati attuali più i misti che andranno in pensione fino al ~2045-2050. La base è perciò finita e calante: ~€20 mld/anno stabili per ~25 anni, poi in discesa verso zero entro il ~2070. È asset-liability matching con la passività di riconoscimento (Leva C), con una coda: la fonte si esaurisce intorno al 2070 mentre le rendite di riconoscimento corrono fino al ~2095, e il divario è coperto dal decumulo del fondo già accumulato.

### E — BTP a 50 anni sul disavanzo residuo

Il disavanzo legacy che resta dopo le leve A e B si finanzia con debito ultra-lungo, distribuendo il picco sulle generazioni che ne beneficiano (i lavoratori futuri, liberi dal PAYG). È bridge financing dentro il Comparto 1: il debito emesso nei primi anni viene ammortizzato dall'avanzo PAYG che emerge quando il legacy si estingue (i contributi trattenuti superano la spesa residua). La Leva E non è quindi una cedola permanente, ma un onere calante che si autoestingue; il picco è ~€1.300 mld.

### F — Chiusura del residuo di riconoscimento (~€500 mld)

Il fondo della Leva D copre ~⅔ della passività di riconoscimento. Il residuo (~€500 mld nominali) si chiude in larga parte senza nuovo debito:

1. Spread di tasso. La passività è indicizzata al nozionale (~2,7%), il fondo rende 5%: lo spread di ~2,3 punti riduce il gap in termini matched a ~€300-400 mld. L'IOU resta inoltre finanziamento sotto-mercato (2,7% contro 4,3% del BTP 50y): conviene portarlo come claim nozionale anziché convertirlo in BTP, con un risparmio di ~€8 mld/anno su €500 mld.

2. ~~Prelievo affinato. Prelevare la sola componente non finanziata della pensione retributiva (non il 50% piatto) e abbassare la soglia a €2.500 netti: ~€100-200 mld aggiuntivi.~~
   > ⚠️ **Ritirato: era un doppio conteggio.** "Prelevare la sola componente non finanziata" **è** la Leva D fatta correttamente, non una leva aggiuntiva. Le due non si sommano: sono la stessa base imponibile, contata due volte. Nella riformulazione (§4-D) la componente non finanziata è già prelevata al 100%, e il gettito totale è €1,8-7,7 mld/anno — non €20 mld + €100-200 mld.
   >
   > La soglia in netto (€2.500 o €3.000) resta inoltre **non calcolabile** sugli open data: €3.000 netti/mese ≈ €4.372 lordi, che cade *dentro* la classe INPS superiore aperta ("3.000 e più"), la cui coda non è osservabile.

(L'avanzo PAYG da estinzione del legacy non è una fonte del Comparto 2: appartiene al Comparto 1 e ammortizza la Leva E — §4-E.)

Opzione di riserva: per l'eventuale residuo finale, collocamento come BTP Previdenza retail con wrapper fiscale a rendimento sotto-mercato — sempre debito, ma più economico del BTP istituzionale.

---

## 5. Il disavanzo corrente, passo per passo

| Voce | €/anno |
|---|---|
| Uscita pensioni (legacy) | −290 |
| Contributi residui se i contributivi dirottano tutto (240 − 100) | +140 |
| **= Disavanzo grezzo** | **−150** |
| Leva A — €24 mld restano in PAYG (aliquota 25% non 33%) | +24 |
| Leva B — il flusso TFR libera €30 mld di IVS (netto €6 mld Tesoreria) | +24 |
| **= Disavanzo residuo da finanziare** | **≈ −100** |

Il disavanzo residuo (~€100 mld) cala verso zero in ~25 anni man mano che il legacy si estingue.

---

## 6. I due comparti

Il piano separa due passività, ciascuna con la propria fonte.

### Comparto 1 — Legacy (pensionati attuali)
- Passività: ~€290 mld/anno calanti, valore attuale ~€2.700-3.000 mld
- Fonti: contributi trattenuti in PAYG (Leve A+B), BTP a 50 anni sul residuo, fiscalità
- BTP: picco ~€1.300 mld (+~60 punti di PIL nella fase calda), cedola di picco ~€56 mld/anno; ammortizzato dall'avanzo PAYG quando il legacy si estingue — onere calante, non permanente

### Comparto 2 — Riconoscimento (paper dei contributivi)
- Passività: ~€1.300-1.500 mld di saldi nozionali, dovuti su ~40-70 anni
- Fonte: prelievo sui retributivi ricchi (Leva D), ~€20 mld/anno calanti, investiti; durata finita agganciata alla quota retributiva (§4-D)
- Il fondo accumula (~€430 mld già al 15° anno), tocca un picco intorno a ~€1.000 mld, poi si decumula pagando gli IOU. Copre ~⅔ della passività; il residuo ~€500 mld si chiude con la Leva F, in larga parte senza nuovo debito

Neutralità di cassa del prelievo: il risparmio sulla spesa legacy (€20 mld) è esattamente compensato dall'investimento dei medesimi €20 mld nel Comparto 2. Il prelievo non riduce quindi il fabbisogno corrente, ma genera risparmio nazionale nuovo dedicato al riconoscimento. Nessun doppio conteggio.

---

## 7. Il conto finale a ~30 anni

| Voce | Importo |
|---|---|
| Debito esplicito (BTP 50y, solo legacy) | picco +€1.300 mld (~+60 punti di PIL), poi ammortizzato dall'avanzo PAYG |
| Onere del debito legacy | cedola di picco ~€56 mld/anno, calante (non permanente) |
| Comparto riconoscimento (~€1.300-1.500 mld) | fondo ~€1.000 mld + Leva F (spread + prelievo affinato) → coperto in larga parte senza nuovo debito |
| Stato dopo ~50-70 anni | fuori dalla previdenza |

---

## 8. Profilo nel tempo (illustrativo)

Stock di fine periodo in €mld; la spesa legacy è un flusso annuo. Anno 0 = avvio (qui 2018). Ordini di grandezza.

| €mld | 2018 | 2033 | 2048 | 2063 | 2078 | 2093 |
|---|---|---|---|---|---|---|
| Spesa legacy PAYG (flusso/anno) | 290 | 145 | ~0 | 0 | 0 | 0 |
| BTP legacy in essere (Leva E) | 0 | 1.100 | 900 | 250 | 0 | 0 |
| Fondo riconoscimento (Leva D) | 0 | 430 | 1.000 | 700 | 250 | 0 |
| Passività riconoscimento residua | 1.400 | 1.400 | 1.100 | 700 | 300 | 0 |
| Pilastro privato (% PIL, indic.) | 11% | 40% | 80% | 115% | 140% | 160% |

Ipotesi pilastro: crescita PIL nominale 2,5% (reale <1%), rendimento 4% netto nominale; contributi al pilastro in salita dal ~5% al ~11% del PIL man mano che l'intero sistema passa a capitalizzazione. Poiché il rendimento (4%) supera la crescita (2,5%), il rapporto fondo/PIL sale fino a maturità, atterrando nell'intervallo dei sistemi maturi (Australia ~145%, Paesi Bassi ~190%). Con un rendimento del 5% netto il pilastro supererebbe il 200%.

Lettura: la spesa legacy si spegne entro il ~2048; il BTP tocca il picco (~€1.300 mld) intorno al 2040 e viene poi ammortizzato dall'avanzo PAYG; il fondo riconoscimento sale fino a ~€1.000 mld e si decumula pagando gli IOU; la passività di riconoscimento si estingue entro il ~2093. A fine corsa tutti gli strumenti di transizione sono a zero, lo Stato è fuori dalla previdenza e il pilastro privato ha sostituito il PAYG.

---

## 9. Presidio europeo sulla gobba di debito

Il rischio principale del piano non è di solvibilità ma di credibilità nel transitorio: il debito ponte (picco ~€1.300 mld, ~60 punti di PIL, ~2040) è autofinanziante per costruzione, ma per ~30 anni il mercato deve crederci. Uno shock di fiducia a metà percorso — spread in salita, rollover più caro — comprometterebbe un piano altrimenti solido.

Una garanzia europea sul solo debito di transizione rompe il circolo: se il rollover è assicurato, la crisi di fiducia non parte e la garanzia verosimilmente non viene mai escussa (logica OMT 2012: l'annuncio spense lo spread senza acquisti). Forme possibili, in ordine di leggerezza: linea precauzionale ESM (PCCL/ECCL), già esistente; garanzia UE su una tranche dedicata e segregata di BTP-transizione, sul modello SURE/NGEU; backstop BCE via TPI, che copre proprio dinamiche di spread non giustificate dai fondamentali.

Il prezzo è la condizionalità: la garanzia richiederebbe che carve-out, prelievo e riconoscimento siano blindati per la durata del piano. Paradossalmente è un pregio — il commitment esterno risolve anche il vincolo domestico della continuità politica su più legislature.

Argomento negoziale: la conversione del debito pensionistico implicito di un grande paese in un pilastro capitalizzato da ~150% del PIL è un obiettivo dichiarato della Capital Markets Union — trilioni di risparmio previdenziale investibile nei mercati europei. Non un salvataggio da chiedere, ma un progetto da co-firmare.

---

## 10. Vincoli principali

1. Diritti acquisiti. Il prelievo obbligatorio (Leva D) è costituzionalmente contestabile (cfr. Corte Cost. 70/2015). Il targeting sui soli retributivi ricchi è la difesa più solida: si recupera una generosità dimostrabilmente non finanziata, non si confiscano contributi versati. Resta il rischio di contenzioso, e la base è finita (§4-D).
2. Fase calda. Per ~30 anni il debito viaggia ~60 punti di PIL sopra la baseline: il rientro è di progetto, non garantito. Mitigante: presidio europeo (§9).
3. Non si parte da zero. Contributivo e previdenza complementare coprono già parte di questo percorso. Realisticamente si accelera una transizione in corso, non si disegna da foglio bianco.

---

## 11. Verdetto

Il piano è contabilmente coerente: ogni leva è stata verificata contro l'illusione di un finanziamento gratuito. Il suo guadagno di fondo è generazionale — liberare una o due generazioni dal rendimento nozionale di un PIL in declino demografico e dar loro accesso al rendimento composto di mercato (§1). Tre famiglie di leve fanno il lavoro:
- il carve-out graduale (Leva A) contiene il disavanzo annuo;
- i contributi di imprese e lavoratori (flusso TFR e adesione automatica, Leva B) costruiscono il pilastro a capitalizzazione senza cassa pubblica;
- mercato e prelievo sui retributivi (Leve D-E) distribuiscono il residuo su chi beneficia della riforma e su chi ha ricevuto la generosità non finanziata.

Sotto resta il consumo reale del legacy: spostabile nel chi e nel quando, mai cancellabile. Il debito della Leva E (picco ~€1.300 mld) non è un costo permanente: l'avanzo PAYG che emerge con l'estinzione del legacy lo ammortizza, riducendo la cedola di picco (~€56 mld/anno) a un onere calante. Il residuo del riconoscimento (~€500 mld) si chiude con la Leva F — spread di tasso e prelievo affinato — in larga parte senza aggiungere debito, con il collocamento retail sotto-mercato come sola riserva. Il rischio residuo — la credibilità del rientro durante la gobba — è presidiabile con la garanzia europea (§9), che al tempo stesso blinda la continuità politica del piano. A fine corsa lo Stato esce dalla previdenza.
