# Cross-check Scenario B (cubo 389) — VERDETTO: la stima precedente è ROTTA

## 1. I dati puliti (cubo 389, RETRIBUTIVO, solo `Categoria = Vecchiaia`, vigenti 1.1.2026)

Il filtro Vecchiaia è decisivo: il retributivo passa da 7,79 a **4,85 mln** di pensioni (le
~2,9 mln escluse erano superstiti/invalidità) e l'importo medio sale da 1.213 a **1.447 €**.

| Gruppo | N | Importo medio | Età alla decorrenza* |
|---|---|---|---|
| **LEGACY** (decorrenza ≤ 2010) | 4.220.653 | **1.480,91 €** | **58,1 anni** |
| RECENTI (decorrenza 2016-17) | 47.821 | 947,54 € | 65,6 anni |
| **Fattore di scala sull'importo** | | **1,56 ×** (range 1,28-1,66) | **−7,5 anni** |

\* derivata: età_2026 − (2026 − anno_decorrenza), ponderata. La coorte "fino al 1995" è
open-ended e resta esclusa dal calcolo dell'età.

Lo stock legacy ha importi **1,56× più alti** *e* carriere **~7,5 anni più corte**.
Entrambi gli effetti alzano la componente non finanziata. Il "bordo basso" calcolato su
coorti 2016-17 sottostima su **due** dimensioni, non una.

(Misto Dini va in direzione opposta: coorti vecchie a 0,61× delle recenti. Va scalato in giù.)

## 2. IL PROBLEMA VERO: il nostro modello era rotto

Nel calcolare il controfattuale contributivo per queste coorti il calcolatore usava una
crescita salariale del **2% nominale fisso**. Ma queste carriere corrono dal **1970 al 2002**,
quando l'inflazione era ~10%/anno e i tassi di capitalizzazione (= crescita del PIL nominale)
erano del **15-22%**.

Salari fermi al 2% + montante capitalizzato al 15-22% = **montante gonfiato** ⇒ il
controfattuale contributivo esce **più alto della pensione effettiva** ⇒ eccesso **ZERO**.
È assurdo, ed è l'errore su cui poggiava la stima di 5,5-7,3 mld/anno.

## 3. Sensibilità — è l'ipotesi salariale a comandare, non la coorte

Stock legacy retributivo privato (4,22 mln, dec. ≤2010, età 58, 33 anni di contributi):

| Ipotesi sulla crescita dei salari | Quota non finanziata | Eccesso/anno |
|---|---|---|
| PIL nominale − 2pp | 16,7% | 13,6 mld |
| PIL nominale − 1pp | 29,7% | 24,1 mld |
| **= PIL nominale** (quota salari costante) | **40,1%** | **32,5 mld** |
| PIL nominale + 1pp | 48,4% | 39,3 mld |
| ~~2% nominale fisso (vecchio metodo)~~ | ~~0,0%~~ | ~~0,0 mld~~ |

**L'intervallo plausibile è 14-39 mld/anno sul solo retributivo privato di vecchiaia**,
contro i 5,5-7,3 mld che avevamo stimato per l'intero sistema.

## 4. Verdetto

- La stima dello Scenario B (5,5-7,3 mld) **non è un bordo basso: è sbagliata.** Non va
  scalata, va **rifatta**.
- La direzione dell'errore è **verso l'alto**, e di molto: la componente non finanziata è
  un ordine di grandezza maggiore.
- L'ipotesi dominante non è la coorte né l'anzianità: è il **sentiero salariale nominale**
  lungo la carriera, che non osserviamo. È lì che si concentra tutta l'incertezza.
- **Nessun numero di Scenario B va nel report** finché il profilo salariale non è ancorato a
  una serie storica vera delle retribuzioni italiane (ISTAT/OCSE), invece che a un parametro
  del calcolatore pensato per carriere recenti.

## 5. Cosa serve per chiuderlo

Una serie storica delle **retribuzioni nominali italiane 1970-2025** (ISTAT: retribuzioni
lorde per ULA, o indice delle retribuzioni contrattuali; in alternativa OCSE average wages).
Con quella, il profilo salariale smette di essere un'assunzione e diventa un dato, e
l'intervallo 14-39 si stringe.
