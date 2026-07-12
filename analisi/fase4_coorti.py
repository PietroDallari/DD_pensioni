"""
PUNTO 4 — Modello per COORTI DI DECORRENZA.

OBIETTIVO: stringere l'intervallo dell'eccesso non finanziato (oggi 1,8-7,7 mld,
rapporto max/min = 4,3) sotto un rapporto di 2.

PERCHE' LE COORTI RISOLVONO IL PROBLEMA
---------------------------------------
L'eccesso retributivo dipende dall'ANZIANITA' (verificato: ~17% a 25 anni, ~8% a
38, ~4% a 40). Nella distribuzione per classe di importo l'anzianita' non c'e', e
va assunta -> intervallo largo. Nei dati per ANNO DI DECORRENZA c'e' invece
l'ETA' MEDIA al pensionamento, che identifica l'anzianita' molto meglio:
    anzianita' ~ eta' alla decorrenza - eta' di ingresso nel lavoro
e l'anno di decorrenza identifica il REGIME (quota di carriera ante-1996).

COPERTURA: i dataset per anno di decorrenza sono in larga parte della Gestione
dipendenti pubblici. La copertura e' quindi PARZIALE e sbilanciata sul pubblico
impiego (carriere piu' lunghe e continue della media). Dichiarato, non discusso.

FONTE: INPS open data, dataset 1580 (ID-5045) e 1577 (ID-5042).
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
from override_tassi_ufficiali import capitalization_for_year_ufficiale  # noqa: E402

ppc.capitalization_for_year = capitalization_for_year_ufficiale

MENSILITA = 13.0
URL_1580 = "http://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5046.csv"
URL_1577 = "http://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5042.csv"
# eta' di ingresso nel mercato del lavoro: unica assunzione residua, su cui si fa
# la sensibilita'. Il pubblico impiego entra tardi (laurea) -> 24-27.
ETA_INGRESSO = (24, 25, 27)


def scarica(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.content.decode("latin-1")), sep=",", quotechar='"')
    d.columns = [c.strip() for c in d.columns]
    return d


def eta_da_classe(s: str) -> float | None:
    nums = [int(x) for x in "".join(c if c.isdigit() else " " for c in str(s)).split()]
    nums = [n for n in nums if 40 <= n <= 90]
    return float(np.mean(nums)) if nums else None


def contributivo(ral_finale: float, anni: int, eta: int, anno_dec: int) -> float:
    scen = dict(ppc.DEFAULT_SCENARIO)
    scen.update({
        "scenario_id": "coorte",
        "anno_inizio": anno_dec - anni, "anno_fine": anno_dec - 1,
        "anno_pensione": anno_dec, "data_pensionamento": f"{anno_dec}-01-01",
        "anno_nascita": anno_dec - eta, "data_nascita": f"{anno_dec - eta}-01-01",
        "eta_pensione": eta, "anni_contribuiti": anni,
        "ral_finale": float(ral_finale), "ral_iniziale": None,
        "progressione": "media", "percentuale_lavoro": 100.0, "mesi_lavorati_annui": 12.0,
    })
    car = ppc.build_simplified_career(scen)
    montante = float(car["montante_fine_anno"].iloc[-1])
    coef = ppc.transformation_coefficient(anno_dec, eta, 0)
    return montante * coef.coefficiente


def main() -> None:
    d = scarica(URL_1580)
    d["eta"] = d["Classe di eta"].map(eta_da_classe)
    d = d.dropna(subset=["eta"])
    d["anno_dec"] = pd.to_numeric(d["Anno di decorrenza"], errors="coerce")
    d["n"] = pd.to_numeric(d["Numero pensioni"], errors="coerce")
    d["imp"] = pd.to_numeric(d["Importo medio mensile"], errors="coerce")
    d = d.dropna(subset=["anno_dec", "n", "imp"])
    d = d[(d.anno_dec >= 1990) & (d.anno_dec <= 2020) & (d.imp > 0)]

    print("=" * 100)
    print("PUNTO 4 — COORTI DI DECORRENZA (INPS 1580, Gestione dipendenti pubblici)")
    print("=" * 100)
    print(f"  celle utilizzabili: {len(d)}   pensioni: {d.n.sum():,.0f}")
    print(f"  decorrenze: {int(d.anno_dec.min())}-{int(d.anno_dec.max())}   "
          f"eta' media ponderata: {(d.eta*d.n).sum()/d.n.sum():.1f}")
    print("  COPERTURA PARZIALE: gestione dipendenti pubblici. Carriere piu' lunghe e")
    print("  continue della media nazionale -> l'eccesso qui stimato e' un BORDO BASSO.")
    print()

    risultati = []
    for eta_ing in ETA_INGRESSO:
        tot_ecc = 0.0
        tot_pens = 0.0
        for _, r in d.iterrows():
            eta = int(round(r.eta))
            anni = int(round(eta - eta_ing))
            if anni < 10 or anni > 45:
                continue
            anno_dec = int(r.anno_dec)
            P = float(r.imp) * MENSILITA                 # pensione annua lorda
            # inversione retributiva: 2% dell'ultima retribuzione per anno
            W = P / (0.02 * anni)
            try:
                P_c = contributivo(W, anni, eta, anno_dec)
            except Exception:
                continue
            ecc = max(0.0, P - P_c)
            tot_ecc += ecc * float(r.n)
            tot_pens += P * float(r.n)
        quota = tot_ecc / tot_pens * 100 if tot_pens else 0
        risultati.append({"eta_ingresso": eta_ing, "quota_eccesso_pct": quota,
                          "massa_pensioni_mld": tot_pens / 1e9,
                          "eccesso_mld": tot_ecc / 1e9})
        print(f"  eta' ingresso {eta_ing}:  quota non finanziata = {quota:5.1f}%  "
              f"(anzianita' media {(d.eta*d.n).sum()/d.n.sum()-eta_ing:.1f} anni)")

    q = pd.DataFrame(risultati)
    qmin, qmax = q.quota_eccesso_pct.min(), q.quota_eccesso_pct.max()

    # applico la quota alla massa pensionistica RETRIBUTIVA nazionale
    par = pd.read_csv(OUT / "parametri_verificati.csv")
    massa = float(par.loc[par.parametro.eq("massa_lorda_pensionistica_da_distribuzione"),
                          "valore"].iloc[0])
    quota_retr = 0.989   # dataset 1648
    print()
    print("=" * 100)
    print("ECCESSO NON FINANZIATO NAZIONALE")
    print("=" * 100)
    print(f"  massa pensionistica lorda        : {massa:,.1f} mld")
    print(f"  quota retributivo+misto          : {quota_retr*100:,.1f} %")
    print(f"  quota non finanziata (da coorti) : {qmin:.1f} - {qmax:.1f} %")
    lo = massa * quota_retr * qmin / 100
    hi = massa * quota_retr * qmax / 100
    print()
    print(f"  ECCESSO TOTALE : {lo:,.1f} - {hi:,.1f} mld/anno   "
          f"(rapporto max/min = {hi/lo:.2f})")
    print(f"  precedente     :   1,8 -   7,7 mld/anno   (rapporto 4,28)")
    print(f"  obiettivo      : rapporto < 2   -> {'RAGGIUNTO' if hi/lo < 2 else 'NON raggiunto'}")

    q["eccesso_nazionale_mld"] = massa * quota_retr * q.quota_eccesso_pct / 100
    q.to_csv(OUT / "eccesso_per_coorte.csv", index=False)
    print(f"\n  Scritto {OUT / 'eccesso_per_coorte.csv'}")


if __name__ == "__main__":
    main()
