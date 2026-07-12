"""
FASE 3b — Coda di Pareto ANCORATA su due punti osservati.

IL PROBLEMA PRECEDENTE
----------------------
In fase3_scenari.py la Pareto era calibrata sulla MEDIA della classe aperta, un
valore che avevo DERIVATO dal dataset INPS 1650 con una ponderazione discutibile.
Ne usciva alpha=15 (coda sottilissima) e un gettito di 3,2 mld. Era SBAGLIATO:
la media implicita di quella Pareto (3.214 EUR/mese) e' incompatibile con i dati
di coda pubblicati.

LA CORREZIONE
-------------
Due punti osservati, STESSO PERIMETRO (pensionati = persone, non singole pensioni):
  N(>= 3.000 EUR/mese lordi) = 1.104.624   INPS open data 1824 (2016)
  N(>= 5.000 EUR/mese lordi) =   266.180   INPS, Rapporto "Prestazioni
                                            pensionistiche e beneficiari" (2017),
                                            1,7% dei pensionati, 80,8% uomini
Per una Pareto:  N(>x) = N(>xm) * (xm/x)^alpha
  => alpha = ln(N1/N0) / ln(x0/x1)

CROSS-CHECK INDIPENDENTE
------------------------
Il contributo di solidarieta' (L. 145/2018, c. 261) colpiva i trattamenti diretti
sopra 100.000 EUR lordi/anno. Platea stimata nelle relazioni: ~16.000 (soglia
100k, testo definitivo) - ~40.000 (soglia 90k, versione iniziale). Se la Pareso
calibrata su 3k/5k predice bene anche li', la coda e' affidabile. Se sovrastima,
la coda vera decade PIU' IN FRETTA dell'estrema e il gettito va corretto in basso.
(Perimetro non identico: il contributo escludeva superstiti, invalidita' e
contributivo puro -> ci si aspetta che la Pareto sovrastimi un po'.)
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

X0, N0 = 3000.0, 1_104_624      # INPS open data 1824 (2016)
ANCORE = {                       # x1 -> N1, con fonte
    "INPS 2017 (Prestazioni pensionistiche e beneficiari)": (5000.0, 266_180),
    "Itinerari Previdenziali 2018": (5000.0, 199_000),
    "stampa/INPS 2023 (~400k, 2,6%)": (5000.0, 400_000),
}
# reflazione 2016 -> 2024 (HICP): le soglie osservate sono in euro dell'anno del dato
REFLATOR = 1.2244


def alpha_da_due_punti(x0: float, n0: float, x1: float, n1: float) -> float:
    return math.log(n1 / n0) / math.log(x0 / x1)


def netto_mensile(lordo_mensile: float) -> float:
    return ppc.pension_net_annual_estimate(lordo_mensile * MENSILITA, ANNO) / MENSILITA


def gettito_tetto(alpha: float, xm_nom: float, n_tot: float, rng) -> tuple[float, float, float]:
    """Gettito annuo del tetto a SOGLIA_NETTA, integrando sulla coda di Pareto."""
    u = rng.uniform(size=600_000)
    lordi_nom = xm_nom * (1 - u) ** (-1 / alpha)     # in euro dell'anno del dato
    lordi = lordi_nom * REFLATOR                      # rivalutati al 2024
    griglia = np.unique(np.round(lordi, -1))
    mappa = {g: netto_mensile(g) for g in griglia}
    netti = np.array([mappa[g] for g in np.round(lordi, -1)])
    ecc = np.maximum(0.0, netti - SOGLIA_NETTA)
    gettito = n_tot * ecc.mean() * MENSILITA / 1e9
    quota = float((netti > SOGLIA_NETTA).mean())
    return gettito, quota, float(lordi.mean())


def platea_sopra(alpha: float, xm_nom: float, n_tot: float, soglia_nom: float) -> float:
    return n_tot * (xm_nom / soglia_nom) ** alpha


def main() -> None:
    rng = np.random.default_rng(0)
    print("=" * 100)
    print("CALIBRAZIONE DELLA CODA SU DUE PUNTI OSSERVATI")
    print("=" * 100)
    print(f"  punto 0 (nostro dato) : N(>= {X0:,.0f} EUR/mese) = {N0:,}")
    print()

    righe = []
    for fonte, (x1, n1) in ANCORE.items():
        a = alpha_da_due_punti(X0, N0, x1, n1)
        media_nom = X0 * a / (a - 1) if a > 1 else float("inf")
        # cross-check: platea sopra 100.000 EUR lordi/anno (= 7.692/mese su 13 mensilita')
        p100k = platea_sopra(a, X0, N0, 100_000 / MENSILITA)
        g, quota, media_sim = gettito_tetto(a, X0, N0, rng)
        righe.append({
            "ancora": fonte, "N_sopra_5000": n1, "alpha": a,
            "media_classe_aperta_implicita": media_nom,
            "platea_sopra_100k_annui_predetta": p100k,
            "gettito_tetto2500_mld": g,
        })
        print(f"  {fonte}")
        print(f"     N(>= {x1:,.0f}) = {n1:>9,}  ->  alpha = {a:5.2f}   "
              f"media classe aperta implicita = {media_nom:,.0f} EUR/mese")
        print(f"     platea predetta > 100.000 EUR/anno : {p100k:>9,.0f}")
        print(f"     GETTITO tetto 2.500 netti          : {g:>9,.1f} mld/anno")
        print()

    print("=" * 100)
    print("CROSS-CHECK INDIPENDENTE — contributo di solidarieta' 2019 (L.145/2018 c.261)")
    print("=" * 100)
    print("  Platea OSSERVATA sopra 100.000 EUR lordi/anno: ~16.000 (soglia 100k, testo")
    print("  definitivo) - ~40.000 (soglia 90k, stima lavoce.info).")
    print("  Perimetro piu' stretto del nostro (esclude superstiti, invalidita', contributivo")
    print("  puro): ci aspettiamo che la Pareto sovrastimi, ma non di un ordine di grandezza.")
    print()
    d = pd.DataFrame(righe)
    for _, r in d.iterrows():
        rap = r.platea_sopra_100k_annui_predetta / 40_000
        ok = "COERENTE" if rap < 3 else "SOVRASTIMA FORTE -> coda estrema troppo grassa"
        print(f"  alpha={r.alpha:4.2f}: predice {r.platea_sopra_100k_annui_predetta:>8,.0f} "
              f"vs ~16-40k osservati  ({rap:4.1f}x il bordo alto)  -> {ok}")

    d.to_csv(OUT / "coda_ancorata.csv", index=False)
    print()
    print("=" * 100)
    print("ESITO")
    print("=" * 100)
    lo, hi = d.gettito_tetto2500_mld.min(), d.gettito_tetto2500_mld.max()
    print(f"  Gettito Scenario A (tetto 2.500 netti): {lo:,.1f} - {hi:,.1f} mld/anno")
    print(f"  (era 3-28 mld non ancorato; era 3,2 con la media di classe SBAGLIATA)")
    print(f"\n  Scritto {OUT / 'coda_ancorata.csv'}")


if __name__ == "__main__":
    main()
