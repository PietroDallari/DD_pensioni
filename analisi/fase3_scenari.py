"""
FASE 3 — I due scenari di prelievo, con risoluzione della coda.

IL PROBLEMA DELLA CLASSE APERTA
-------------------------------
La classe INPS superiore e' aperta ("3.000 e piu'"). Usare la sua MEDIA per
calcolare un tetto e' sbagliato: il tetto morde l'ECCESSO, che e' convesso.
Con la sola media (3.935 EUR lordi/mese al 2024, 2.726 netti) il tetto a 2.500
netti raccoglierebbe appena ~226 EUR/mese a testa. Ma dentro la classe ci sono
pensioni molto piu' alte, il cui eccesso e' grande: usare la media le cancella.

SOLUZIONE: fit di una coda di Pareto sulla classe aperta.
Per una Pareto di soglia x_m e indice alpha:  media = x_m * alpha/(alpha-1).
Conoscendo x_m (inizio classe) e la media osservata, alpha e' identificato:
    alpha = media / (media - x_m)
Il gettito del tetto si integra poi numericamente sulla coda.

Cio' che il fit NON puo' fare: inventare informazione. Se la media osservata e'
vicina a x_m, la Pareto implicata e' sottile e il gettito basso. Il risultato e'
quindi CONDIZIONATO alla media della classe aperta, che e' l'unico dato di coda
che INPS pubblica. Va dichiarato.
"""
from __future__ import annotations

import io
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import requests

ANALISI = Path(__file__).resolve().parent
REPO = ANALISI.parent / "pensioni_italia"
OUT = ANALISI / "output"
for p in [REPO / "scripts", REPO / "scripts" / "src", REPO / "calcolatore" / "src"]:
    if str(p) not in sys.path:
        sys.path.append(str(p))

import pension_paid_calculator as ppc  # noqa: E402

MENSILITA = 13.0
ANNO_VALORI = 2024
ANNO_DATI = 2016
SOGLIA_NETTA = 2500.0


def reflator() -> float:
    u = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_aind"
         "?format=JSON&geo=IT&unit=INX_A_AVG&coicop=CP00")
    j = requests.get(u, timeout=90).json()
    idx = j["dimension"]["time"]["category"]["index"]
    val = j["value"]
    h = {int(k): val[str(v)] for k, v in idx.items() if str(v) in val}
    return h[ANNO_VALORI] / h[ANNO_DATI]


def netto_mensile(lordo_mensile: float) -> float:
    return ppc.pension_net_annual_estimate(lordo_mensile * MENSILITA, ANNO_VALORI) / MENSILITA


def main() -> None:
    k = reflator()
    dis = pd.read_csv(OUT / "distribuzione_pensionati.csv")
    aperta = dis[dis.classe_aperta].iloc[0]

    N_coda = float(aperta.numero_beneficiari)
    x_m = 3000.0 * k                      # inizio classe, rivalutato
    media = float(aperta.lordo_mensile)   # media osservata, rivalutata

    alpha = media / (media - x_m)
    print("=" * 92)
    print("FIT DELLA CODA (classe aperta '3.000 e piu'')")
    print("=" * 92)
    print(f"  soglia classe x_m (2024)      : {x_m:>10,.0f} EUR/mese lordi")
    print(f"  media osservata della classe  : {media:>10,.0f} EUR/mese lordi")
    print(f"  numerosita'                   : {N_coda/1e6:>10,.2f} mln")
    print(f"  alpha di Pareto implicito     : {alpha:>10,.2f}")
    print(f"  -> coda {'SOTTILE' if alpha > 4 else 'GRASSA'}: la media e' "
          f"{'vicina' if alpha > 4 else 'lontana'} alla soglia di classe.")
    print(f"  99o pct della coda            : {x_m*(100)**(1/alpha):>10,.0f} EUR/mese lordi")

    # --- Scenario A: tetto a 2.500 netti, integrato sulla coda -----------------
    # campiono la Pareto e applico il tetto sul NETTO
    u = np.random.default_rng(0).uniform(size=2_000_000)
    lordi = x_m * (1 - u) ** (-1 / alpha)
    netti = np.array([netto_mensile(x) for x in np.unique(np.round(lordi, 0))])
    mappa = dict(zip(np.unique(np.round(lordi, 0)), netti))
    netti_full = np.array([mappa[x] for x in np.round(lordi, 0)])
    eccesso_mensile = np.maximum(0.0, netti_full - SOGLIA_NETTA)
    quota_sopra = float((netti_full > SOGLIA_NETTA).mean())
    gettito_A = N_coda * eccesso_mensile.mean() * MENSILITA / 1e9

    # confronto: stima ingenua con la sola media di classe
    gettito_A_naive = N_coda * max(0.0, netto_mensile(media) - SOGLIA_NETTA) * MENSILITA / 1e9

    print()
    print("=" * 92)
    print("SCENARIO A — TETTO A 2.500 EUR NETTI/MESE")
    print("=" * 92)
    print(f"  quota della coda effettivamente sopra soglia : {quota_sopra*100:>6,.1f} %")
    print(f"  platea colpita                               : {N_coda*quota_sopra/1e6:>6,.2f} mln")
    print(f"  eccesso medio prelevato                      : {eccesso_mensile.mean():>6,.0f} EUR/mese")
    print()
    print(f"  GETTITO (coda Pareto)      : {gettito_A:>6,.1f} mld/anno   <-- stima")
    print(f"  gettito (sola media classe): {gettito_A_naive:>6,.1f} mld/anno   (ingenuo, sottostima)")
    print(f"  placeholder nel modello    :   12.0 mld/anno")

    # --- Scenario B -----------------------------------------------------------
    print()
    print("=" * 92)
    print("SCENARIO B — ECCESSO MISURATO SUL CONTROFATTUALE CONTRIBUTIVO")
    print("=" * 92)
    print("  Intervallo da leva_d_microsimulazione.py: 1,8 - 7,7 mld/anno")
    print("  (non stretto: richiede il modello per coorti di decorrenza, Fase 1.4)")
    print("  Con franchigia a 2.500 netti garantiti, il gettito e' <= questo intervallo.")

    pd.DataFrame([{
        "scenario": "A_tetto_2500_netti", "gettito_mld_anno": gettito_A,
        "platea_mln": N_coda * quota_sopra / 1e6,
        "metodo": f"coda Pareto alpha={alpha:.2f} fittata su media classe aperta",
        "flag_qualita": "stima_esplicita",
        "limite": "condizionata alla media della classe aperta; unico dato di coda pubblicato",
    }, {
        "scenario": "B_eccesso_misurato", "gettito_mld_anno": None,
        "platea_mln": None, "metodo": "controfattuale contributivo individuale",
        "flag_qualita": "intervallo", "limite": "1,8-7,7 mld; serve modello per coorti",
    }]).to_csv(OUT / "scenari_prelievo.csv", index=False)
    print(f"\nScritto {OUT / 'scenari_prelievo.csv'}")


if __name__ == "__main__":
    main()
