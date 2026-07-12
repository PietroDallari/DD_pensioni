# Richiesta di dati — versione a prova di contraddittorio

> **Controllo eseguito prima della stampa.** L'affermazione originaria («i dati anzianità ×
> importo × regime non sono pubblicati, servono i microdati INPS») è **vera nella sostanza
> ma indifendibile nella forma**: lascia intendere che il regime di liquidazione non sia
> pubblicato. **Lo è.** Chiunque può aprire l'Osservatorio in trenta secondi e smentirci.

## Cosa INPS pubblica DAVVERO (verificato su tutti i 194 cubi statistici e i 2.323 dataset open data)

| Incrocio | Pubblicato? |
|---|---|
| regime × importo **medio** (× gestione, categoria, sesso, territorio, anno decorrenza) | **SÌ** |
| importo (classi) × età × categoria × gestione | **SÌ** |
| anzianità contributiva **media** × tipo pensione × sesso × gestione | **SÌ** (solo media) |
| regime × **classi** di importo (distribuzione) | **NO** |
| anzianità × importo | **NO** |
| anzianità × regime | **NO** |
| **anzianità × importo × regime** | **NO** |

**Il regime di liquidazione È pubblicato**: Osservatorio INPS «Pensioni per regime di
liquidazione», valori *Retributivo / Misto riforma Dini / Misto riforma Fornero /
Contributivo puro*.
- Cubo 372 (pensioni **liquidate**, 2016-2025): https://servizi2.inps.it/servizi/osservatoristatistici/6/27/o/372
- Cubo 389 (pensioni **vigenti**, 2017-2026, **con anno di decorrenza**): https://servizi2.inps.it/servizi/osservatoristatistici/6/37/o/389

**VisitINPS Scholars esiste ed è attivo**: bandi aperti, banche dati che includono
«Percettori di pensione 1995-2025» e il «Campione del 13% degli estratti conto per i nati
dopo il 1950» — cioè proprio l'archivio da cui si ricostruisce l'anzianità individuale.
https://www.inps.it/it/it/dati-e-bilanci/attivit--di-ricerca/programma-visitinps-scholars.html

→ Dire «pubblicate i microdati» invita la risposta: *«c'è VisitINPS, candidatevi.»*

## I TRE limiti reali — è qui che sta la richiesta legittima

1. **Solo l'importo MEDIO, mai la distribuzione.** Non si può ricostruire quanta massa
   pensionistica retributiva stia sopra una soglia. Per la componente non finanziata serve
   la *distribuzione*, non la media.
2. **L'anzianità contributiva è pubblicata solo come MEDIA**, mai incrociata con l'importo
   né con il regime. Assente come dimensione in tutti e 194 i cubi pensionistici.
3. **La Gestione Dipendenti Pubblici è esclusa dalla scomposizione per regime**: copre solo
   FPLD, CD/CM, Artigiani, Commercianti, Gestione separata. Il pubblico impiego —
   **14,9% delle pensioni ma 26,6% degli importi**, il blocco retributivo più pesante — non
   ha alcuna scomposizione per regime.

## Formulazione da usare nel programma

> INPS pubblica le pensioni per regime di liquidazione (retributivo, misto Dini, misto
> Fornero, contributivo puro), ma **solo con l'importo medio** e **solo per le gestioni
> private**: la Gestione Dipendenti Pubblici — il 26,6% degli importi in pagamento — non ha
> alcuna scomposizione per regime. E l'**anzianità contributiva** è pubblicata solo come
> **media**, mai incrociata con l'importo né con il regime. Manca cioè esattamente la tavola
> che serve per quantificare la componente non finanziata delle pensioni retributive:
> **anzianità contributiva × classi di importo × regime di liquidazione, estesa al pubblico
> impiego**. INPS possiede il dato nei propri archivi gestionali e può produrlo in forma
> aggregata senza alcun ostacolo tecnico o di privacy (bastano le soglie di riservatezza già
> in uso). Chiediamo che lo pubblichi, e che l'accesso ai microdati — oggi possibile solo
> vincendo un bando VisitINPS — sia esteso e semplificato.

## Trappola lessicale da evitare in contraddittorio

Centinaia di dataset INPS contengono «pensione di **anzianità**»: è la **categoria** di
pensione (vs vecchiaia), **non** l'anzianità contributiva. Non farsi confondere.

## Altre fonti verificate come NEGATIVE

- **RGS**, «Le tendenze di medio-lungo periodo», Rapporto n.26 (2025): zero occorrenze di
  «classi di importo». L'anzianità compare solo come parametro del lavoratore-tipo.
- **ISTAT**, «Trattamenti pensionistici e beneficiari»: classi di importo sì, anzianità e
  regime no.
- **Eurostat** (ESSPROS): nessuna dimensione «anni di contribuzione».
- **Appendici statistiche** dei Rapporti annuali INPS XXIV e XXV (XLSX aperti e letti):
  zero tavole su regime, zero su anzianità.
- **NUVASP**: cessato nel 2012. Osservatorio Min. Lavoro (DM 41/2023): non ha mai
  pubblicato nulla.

## DATO NUOVO DA SFRUTTARE (non ancora incorporato nella nostra analisi)

Il **cubo 389** (pensioni vigenti per regime, **2017-2026**, con **anno di decorrenza** e
**importo complessivo annuo**) è più recente e più ricco del dataset open data 1648
(2012-2017) che abbiamo usato per la quota retributivo+misto (98,9%). Da aggiornare.
