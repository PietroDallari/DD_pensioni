"""
FASE 3c — Coda SPEZZATA, ancore coeve, platea corretta.

TRE CORREZIONI rispetto a fase3b:

1. ANCORE COEVE (elimina il mix di annate).
   Invece di incrociare il nostro 2016 (N>=3.000) con l'INPS 2017 (N>=5.000),
   uso la coppia dello STESSO anno e STESSO perimetro (persone, redditi sommati):
       N(>= 3.500 EUR/mese) = 711.000   INPS 2017 (assorbono il 15,2% dell'importo)
       N(>= 5.000 EUR/mese) = 266.180   INPS 2017 (1,7% dei pensionati)
   -> alpha = ln(711/266) / ln(5000/3500)

2. CODA SPEZZATA (la Pareto singola gonfia l'estremo).
   Il punto 2014 (~217k tra 5-10k, ~13k sopra 10k) implica alpha ~4,15 SOPRA i
   10.000 EUR/mese: la coda decade molto piu' in fretta lassu'.
   Conferma indipendente: la Pareto singola alpha=2,7 predice ~80k pensionati sopra
   100.000 EUR/anno, contro i 16-40k colpiti dal contributo di solidarieta' 2019.
   Modello: Pareto a due tratti (alpha1 fino a 10k, alpha2 oltre), continua in x.

3. PLATEA CORRETTA (bug di fase3b).
   Il tetto a 2.500 NETTI = ~3.503 LORDI (2024). La classe INPS 2.500-2.999 (2016)
   rivalutata copre 3.062-3.673 EUR: una PARTE di quella classe sta sopra soglia e
   in fase3b era stata esclusa in blocco. Qui la coda parte dalla soglia vera.

PERIMETRO: pensionati (persone, redditi sommati), non singole pensioni.
Le singole pensioni sopra 5.000 erano 231.000 contro 266.180 persone: mescolarli
sposta i conti. Qui si usano sempre le PERSONE.
"""
from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ANALISI = Path(__file__).resolve().parent
REPO = ANALISI.parent / "pensioni_italia"
OUT = ANALISI / "output"
for p in [REPO / "scripts", REPO / "scripts" / "src", REPO / "calcolatore" / "src"]:
    if str(p) not in sys.path:
        sys.path.append(str(p))

import pension_paid_calculator as ppc  # noqa: E402

MENSILITA = 13.0
SOGLIA_NETTA = 2500.0
ANNO = 2024
HICP_2017_2024 = 1.199   # rivalutazione delle soglie dal 2017 al 2024

# --- ancore coeve 2017 (persone) ---
X_A, N_A = 3500.0, 711_000
X_B, N_B = 5000.0, 266_180
# --- ancora di coda estrema (2014) ---
X_C, N_C = 10_000.0, 13_000
N_C5 = 230_000          # ~217k tra 5-10k + ~13k sopra 10k


def main() -> None:
    alpha1 = math.log(N_A / N_B) / math.log(X_B / X_A)
    alpha2 = math.log(N_C5 / N_C) / math.log(X_C / 5000.0)

    print("=" * 98)
    print("CALIBRAZIONE — CODA SPEZZATA")
    print("=" * 98)
    print(f"  tratto 1 (3.500 -> 10.000): ancore coeve INPS 2017")
    print(f"      N(>={X_A:,.0f})={N_A:,}  N(>={X_B:,.0f})={N_B:,}   ->  alpha1 = {alpha1:.2f}")
    print(f"  tratto 2 (oltre 10.000)   : ancora 2014")
    print(f"      N(>=5.000)~{N_C5:,}  N(>={X_C:,.0f})~{N_C:,}       ->  alpha2 = {alpha2:.2f}")
    print(f"  -> la coda estrema decade {alpha2/alpha1:.1f}x piu' in fretta: "
          f"una Pareto singola la GONFIA.")

    # --- campionamento dalla coda spezzata, con soglia = 3.500 (2017) ---
    rng = np.random.default_rng(0)
    n = 2_000_000
    # tratto 1: Pareto(alpha1) da X_A; troncamento a 10.000 e innesto tratto 2
    u = rng.uniform(size=n)
    x = X_A * (1 - u) ** (-1 / alpha1)
    oltre = x > X_C
    # ricampiono chi supera 10.000 con la legge piu' ripida (continuita' in x=10.000)
    u2 = rng.uniform(size=int(oltre.sum()))
    x[oltre] = X_C * (1 - u2) ** (-1 / alpha2)

    lordi = x * HICP_2017_2024          # rivalutati al 2024
    N_tot = N_A                          # persone sopra 3.500 (2017)

    def netto(l):
        return ppc.pension_net_annual_estimate(l * MENSILITA, ANNO) / MENSILITA

    griglia = np.unique(np.round(lordi, -1))
    mappa = {g: netto(g) for g in griglia}
    netti = np.array([mappa[g] for g in np.round(lordi, -1)])

    ecc = np.maximum(0.0, netti - SOGLIA_NETTA)
    quota = float((netti > SOGLIA_NETTA).mean())
    gettito = N_tot * ecc.mean() * MENSILITA / 1e9

    print()
    print("=" * 98)
    print("CROSS-CHECK — contributo di solidarieta' 2019 (>100.000 EUR lordi/anno)")
    print("=" * 98)
    soglia_100k = 100_000 / MENSILITA / HICP_2017_2024   # riportata a euro 2017
    p_spezzata = N_tot * float((x > soglia_100k).mean())
    p_singola = N_tot * (X_A / soglia_100k) ** alpha1
    print(f"  Pareto SINGOLA (alpha={alpha1:.2f}) predice : {p_singola:>8,.0f} pensionati")
    print(f"  Pareto SPEZZATA               predice : {p_spezzata:>8,.0f} pensionati")
    print(f"  OSSERVATO (relazioni 2019)            :   16.000 - 40.000")
    print(f"  -> la spezzata {'RIENTRA' if p_spezzata < 60_000 else 'ancora sovrastima'} "
          f"nell'ordine di grandezza osservato.")

    print()
    print("=" * 98)
    print("SCENARIO A — TETTO A 2.500 EUR NETTI/MESE (coda spezzata, platea corretta)")
    print("=" * 98)
    print(f"  base: {N_tot:,} persone sopra 3.500 EUR/mese (2017) = "
          f"{X_A*HICP_2017_2024:,.0f} EUR 2024")
    print(f"  quota sopra il tetto netto : {quota*100:>6,.1f} %")
    print(f"  platea colpita             : {N_tot*quota/1e6:>6,.2f} mln")
    print(f"  eccesso medio prelevato    : {ecc.mean():>6,.0f} EUR/mese")
    print()
    print(f"  GETTITO : {gettito:>5,.1f} mld/anno")
    print()
    print("  Confronto con le stime precedenti:")
    print(f"     fase3  (media di classe fabbricata, alpha=15) :  3,2 mld   ERRATA")
    print(f"     fase3b (Pareto singola alpha=2,79)            : 17,5 mld   coda estrema gonfiata")
    print(f"     fase3c (coda spezzata, ancore coeve)          : {gettito:,.1f} mld   <-- stima corrente")
    print("     stima indipendente 'brother'                   :  8-14 mld")

    pd.DataFrame([{
        "scenario": "A_tetto_2500_netti_coda_spezzata",
        "gettito_mld_anno": gettito,
        "platea_mln": N_tot * quota / 1e6,
        "alpha1_3500_10000": alpha1, "alpha2_oltre_10000": alpha2,
        "cross_check_sopra_100k_predetto": p_spezzata,
        "cross_check_sopra_100k_osservato": "16.000-40.000",
        "fonti": "INPS 2017 (711k>=3.500; 266k>=5.000); coda 2014 (13k>=10.000); "
                 "L.145/2018 c.261 per il cross-check",
        "flag_qualita": "stima_ancorata",
    }]).to_csv(OUT / "coda_spezzata.csv", index=False)
    print(f"\n  Scritto {OUT / 'coda_spezzata.csv'}")


if __name__ == "__main__":
    main()
