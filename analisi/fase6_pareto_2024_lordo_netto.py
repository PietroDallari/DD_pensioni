"""
PUNTI 6 + 5 — Pareto spezzata ancorata al 2024, gettito LORDO e NETTO.

METODO (e perche' non riscalo i conteggi)
-----------------------------------------
Le istruzioni propongono di riscalare le numerosita' 2014-2018 al 2024 con il
rapporto delle numerosita' nella classe comune 3.000+. Moltiplicare TUTTI i
conteggi per quel fattore pero' confonde due effetti diversi:
  - la deriva NOMINALE (le stesse persone superano una soglia fissa perche' la
    pensione e' indicizzata);
  - la crescita REALE della platea.
Uso invece la proprieta' che serve davvero: l'esponente di Pareto e' INVARIANTE
DI SCALA. Quindi:
  1. alpha si stima sulle ancore COEVE 2017 (rapporti di numerosita' -> immune
     alla deriva nominale);
  2. il LIVELLO si ancora direttamente alla distribuzione 2024 gia' costruita.
Cosi' forma e livello vengono ciascuno dalla fonte piu' adatta.

ANCORE
------
  forma:    N(>=3.500)=711.000 e N(>=5.000)=266.180   INPS 2017 (persone)
            -> alpha1 = 2,75  (tratto 3.500-10.000)
            coda 2014: ~230k>=5.000, ~13k>=10.000     -> alpha2 = 4,15 (oltre 10.000)
  livello:  N(>=3.000 EUR/mese, euro 2024) dalla distribuzione INPS 2016
            rivalutata con HICP.

PUNTO 5 — GETTITO NETTO
-----------------------
Se il tetto taglia X lordi, lo Stato perde l'IRPEF su X. Il risparmio vero e'
  X_netto = X_lordo - IRPEF persa = X * (1 - aliquota MARGINALE effettiva)
L'aliquota marginale non si assume: si calcola numericamente derivando la
funzione fiscale del calcolatore (IRPEF + addizionali) nel punto di ciascuno.
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
ANNO = 2024
SOGLIA_NETTA = 2500.0

ALPHA1 = math.log(711_000 / 266_180) / math.log(5000 / 3500)   # 3.500 -> 10.000
ALPHA2 = math.log(230_000 / 13_000) / math.log(10_000 / 5_000)  # oltre 10.000
X_BREAK = 10_000.0 * 1.199   # punto di rottura, portato a euro 2024


def netto_annuo(lordo_annuo: float) -> float:
    return ppc.pension_net_annual_estimate(lordo_annuo, ANNO)


def aliquota_marginale(lordo_annuo: float, h: float = 100.0) -> float:
    """Derivata numerica della funzione fiscale: quanta IRPEF si perde per ogni
    euro di pensione tagliato."""
    return 1.0 - (netto_annuo(lordo_annuo) - netto_annuo(lordo_annuo - h)) / h


def livello_2024() -> tuple[float, float]:
    """N(>= 3.000 EUR/mese) in euro 2024, dalla distribuzione INPS 2016 rivalutata."""
    d = pd.read_csv(OUT / "distribuzione_pensionati.csv")
    # la colonna lordo_mensile e' gia' in euro 2024; sommo chi sta sopra 3.000
    # interpolando dentro la classe che contiene la soglia
    d = d.sort_values("lordo_mensile")
    tot = 0.0
    for _, r in d.iterrows():
        if r.lordo_mensile >= 3000:
            tot += r.numero_beneficiari
    # la classe 2.500-2.999 (2016) rivalutata copre ~3.062-3.673: sta gia' sopra 3.000
    return tot, 3000.0


def main() -> None:
    n3000, x0 = livello_2024()
    print("=" * 100)
    print("PUNTO 6 — PARETO SPEZZATA, FORMA DAL 2017, LIVELLO DAL 2024")
    print("=" * 100)
    print(f"  alpha1 (3.500-10.000) = {ALPHA1:.2f}   [ancore coeve INPS 2017]")
    print(f"  alpha2 (oltre 10.000) = {ALPHA2:.2f}   [ancora 2014]")
    print(f"  livello: N(>= {x0:,.0f} EUR/mese, euro 2024) = {n3000:,.0f}")

    # media della classe aperta 3.000+ sotto la coda spezzata
    rng = np.random.default_rng(0)
    u = rng.uniform(size=3_000_000)
    x = x0 * (1 - u) ** (-1 / ALPHA1)
    oltre = x > X_BREAK
    u2 = rng.uniform(size=int(oltre.sum()))
    x[oltre] = X_BREAK * (1 - u2) ** (-1 / ALPHA2)
    print(f"  MEDIA della classe aperta 3.000+ : {x.mean():,.0f} EUR/mese lordi")
    print(f"     (atteso dalle istruzioni: 4.300-4.800)  "
          f"{'OK' if 4300 <= x.mean() <= 4800 else 'FUORI INTERVALLO'}")

    # --- Scenario A: tetto 2.500 netti ---
    lordo_soglia = ppc.pension_gross_annual_from_net(SOGLIA_NETTA * MENSILITA, ANNO) / MENSILITA
    print()
    print("=" * 100)
    print("PUNTO 5 — SCENARIO A: TETTO 2.500 NETTI, LORDO E NETTO D'IMPOSTA")
    print("=" * 100)
    print(f"  soglia: {SOGLIA_NETTA:,.0f} netti/mese = {lordo_soglia:,.0f} LORDI/mese")

    griglia = np.unique(np.round(x, -1))
    net_map = {g: netto_annuo(g * MENSILITA) / MENSILITA for g in griglia}
    marg_map = {g: aliquota_marginale(g * MENSILITA) for g in griglia}
    xr = np.round(x, -1)
    netti = np.array([net_map[g] for g in xr])
    marg = np.array([marg_map[g] for g in xr])

    colpito = netti > SOGLIA_NETTA
    taglio_netto_mese = np.where(colpito, netti - SOGLIA_NETTA, 0.0)
    # il taglio si applica al LORDO: quanto lordo serve tagliare per far scendere
    # il netto alla soglia? = (netto - soglia) / (1 - aliquota marginale)
    taglio_lordo_mese = np.where(colpito, taglio_netto_mese / (1 - marg), 0.0)

    quota = float(colpito.mean())
    platea = n3000 * quota
    lordo = n3000 * taglio_lordo_mese.mean() * MENSILITA / 1e9
    netto = n3000 * taglio_netto_mese.mean() * MENSILITA / 1e9

    print(f"  quota della classe 3.000+ colpita : {quota*100:>6,.1f} %")
    print(f"  platea                            : {platea/1e6:>6,.2f} mln")
    print(f"  aliquota marginale media          : {marg[colpito].mean()*100:>6,.1f} %")
    print()
    print(f"  GETTITO LORDO (pensione tagliata) : {lordo:>6,.1f} mld/anno")
    print(f"  GETTITO NETTO (al netto dell'IRPEF persa) : {netto:>6,.1f} mld/anno")
    print(f"  rapporto netto/lordo              : {netto/lordo*100:>6,.0f} %   "
          f"(atteso ~60%)")

    # --- Scenario B: netto d'imposta sullo stesso principio ---
    print()
    print("=" * 100)
    print("SCENARIO B — ECCESSO MISURATO, LORDO E NETTO")
    print("=" * 100)
    t = marg[colpito].mean()
    for lo, hi in [(1.8, 7.7)]:
        print(f"  gettito LORDO : {lo:,.1f} - {hi:,.1f} mld/anno  (da microsimulazione)")
        print(f"  gettito NETTO : {lo*(1-t):,.1f} - {hi*(1-t):,.1f} mld/anno  "
              f"(aliquota marginale {t*100:.0f}%)")

    pd.DataFrame([
        {"scenario": "A_tetto_2500_netti", "gettito_lordo_mld": lordo,
         "gettito_netto_mld": netto, "platea_mln": platea / 1e6,
         "aliquota_marginale_media_pct": marg[colpito].mean() * 100,
         "alpha1": ALPHA1, "alpha2": ALPHA2,
         "media_classe_aperta": x.mean(),
         "fonte": "forma: INPS 2017 (711k>=3.500; 266k>=5.000) + coda 2014; "
                  "livello: INPS 1824 (2016) rivalutato HICP 2024",
         "flag_qualita": "ancorato"},
        {"scenario": "B_eccesso_misurato_min", "gettito_lordo_mld": 1.8,
         "gettito_netto_mld": 1.8 * (1 - t), "platea_mln": None,
         "aliquota_marginale_media_pct": t * 100, "alpha1": None, "alpha2": None,
         "media_classe_aperta": None,
         "fonte": "microsimulazione su controfattuale contributivo",
         "flag_qualita": "intervallo"},
        {"scenario": "B_eccesso_misurato_max", "gettito_lordo_mld": 7.7,
         "gettito_netto_mld": 7.7 * (1 - t), "platea_mln": None,
         "aliquota_marginale_media_pct": t * 100, "alpha1": None, "alpha2": None,
         "media_classe_aperta": None,
         "fonte": "microsimulazione su controfattuale contributivo",
         "flag_qualita": "intervallo"},
    ]).to_csv(OUT / "scenari_lordo_netto.csv", index=False)
    print(f"\n  Scritto {OUT / 'scenari_lordo_netto.csv'}")


if __name__ == "__main__":
    main()
