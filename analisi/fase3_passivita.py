"""
PUNTO 3 — PASSIVITA' DI RICONOSCIMENTO, stima a due vie.

VIA A (top-down, dai conti nazionali)
-------------------------------------
Eurostat nasa_10_pens1, schema S13PS ("Social security pension schemes"),
voce F63 (pension entitlements): ADL Italia 2021 = 7.681 mld (349% del PIL).
L'ADL comprende SIA i diritti dei pensionati attuali SIA quelli maturati dai
lavoratori attivi:
    ADL = PV(pensioni gia' in pagamento) + PV(diritti maturati dagli attivi)
La passivita' di riconoscimento e' il SECONDO addendo (quello che lo Stato deve a
chi switcha), al netto della quota retributiva dei misti.
    -> passivita' = ADL - PV(pensioni in pagamento) - quota retributiva dei misti

VIA B (bottom-up, dalle coorti)
-------------------------------
Occupati in regime contributivo per classe d'eta' x montante medio per eta'.
Il montante medio si costruisce con il calcolatore di Nazareno usato "al
contrario": storia retributiva mediana capitalizzata coi tassi UFFICIALI gia'
estratti. Nessun codice nuovo: solo un loop sulle coorti.

AVVERTENZA METODOLOGICA (da leggere prima di confrontare A e B)
--------------------------------------------------------------
A e B misurano cose vicine ma NON identiche:
  - l'ADL e' un valore attuale ATTUARIALE: sconta il flusso futuro di prestazioni
    gia' maturate a un tasso di sconto (Eurostat/ESA: ~5% nominale) e incorpora
    l'indicizzazione futura;
  - il montante contributivo e' un SALDO NOZIONALE: contributi versati
    capitalizzati al tasso nozionale (~1,7% nominale).
Poiche' il tasso di sconto (5%) supera il tasso nozionale (1,7%), le due grandezze
NON devono coincidere. Un divario tra A e B e' atteso e non e' un errore: e' la
differenza tra "quanto vale la promessa" e "quanto e' stato accreditato".
"""
from __future__ import annotations

from pathlib import Path
import sys

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

ADL_2021 = 7_681.0          # mld, Eurostat nasa_10_pens1 S13PS F63_LS 2021
SPESA_PENSIONI = 359.6      # mld, COFOG 2024 (vecchiaia + superstiti)
TASSO_SCONTO = 0.05         # coerente con l'ADL Eurostat/ESA
ANNI_ESTINZIONE = 30
ANNO = 2024
RAL_MEDIANA = 27_000.0


def pv_pensioni_in_pagamento(spesa: float, r: float, n: int) -> float:
    """PV del flusso legacy, decrescente linearmente a zero su n anni."""
    return sum(spesa * max(0.0, 1 - t / n) / (1 + r) ** t for t in range(n + 1))


def montante_medio(anni_contributi: int, eta: int) -> float:
    """Montante nozionale accumulato da un lavoratore mediano con `anni` di
    contributi, capitalizzato coi tassi UFFICIALI (calcolatore di Nazareno)."""
    scen = dict(ppc.DEFAULT_SCENARIO)
    scen.update({
        "scenario_id": "coorte_attiva",
        "anno_inizio": ANNO - anni_contributi, "anno_fine": ANNO - 1,
        "anno_pensione": ANNO, "data_pensionamento": f"{ANNO}-01-01",
        "anno_nascita": ANNO - eta, "data_nascita": f"{ANNO - eta}-01-01",
        "eta_pensione": eta, "anni_contribuiti": anni_contributi,
        "ral_finale": RAL_MEDIANA, "ral_iniziale": None,
        "progressione": "media", "percentuale_lavoro": 100.0, "mesi_lavorati_annui": 12.0,
    })
    car = ppc.build_simplified_career(scen)
    return float(car["montante_fine_anno"].iloc[-1])


def occupati_per_eta() -> dict[str, float]:
    """Occupati italiani per classe d'eta' (Eurostat lfsa_egan)."""
    u = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_egan"
         "?format=JSON&geo=IT&sex=T&unit=THS_PER&citizen=TOTAL")
    j = requests.get(u, timeout=90).json()
    age = j["dimension"]["age"]["category"]["index"]
    time = j["dimension"]["time"]["category"]["index"]
    val = j["value"]
    ymax = max(int(t) for t in time)
    ti = time[str(ymax)]
    n_age = len(age)
    out = {}
    for a, ai in age.items():
        k = str(ai * len(time) + ti)
        if k in val:
            out[a] = val[k]
    return out, ymax


def main() -> None:
    print("=" * 100)
    print("VIA A — TOP-DOWN DAI CONTI NAZIONALI")
    print("=" * 100)
    pv_leg = pv_pensioni_in_pagamento(SPESA_PENSIONI, TASSO_SCONTO, ANNI_ESTINZIONE)
    print(f"  ADL totale (Eurostat S13PS, 2021)        : {ADL_2021:>8,.0f} mld")
    print(f"  PV pensioni in pagamento                 : {pv_leg:>8,.0f} mld")
    print(f"     (spesa {SPESA_PENSIONI:,.1f} mld, lineare a zero su {ANNI_ESTINZIONE} anni, "
          f"sconto {TASSO_SCONTO*100:.0f}%)")
    attivi = ADL_2021 - pv_leg
    print(f"  = DIRITTI MATURATI DAGLI ATTIVI          : {attivi:>8,.0f} mld")
    print()
    print("  di cui la passivita' di riconoscimento e' la parte dei CONTRIBUTIVI.")
    for quota_misti in (0.25, 0.35, 0.45):
        print(f"     se la quota retributiva dei misti e' il {quota_misti*100:.0f}%: "
              f"passivita' = {attivi*(1-quota_misti):>7,.0f} mld")

    print()
    print("=" * 100)
    print("VIA B — BOTTOM-UP DALLE COORTI")
    print("=" * 100)
    occ, anno_occ = occupati_per_eta()
    # classi Eurostat utili
    classi = {"Y25-29": 27, "Y30-34": 32, "Y35-39": 37, "Y40-44": 42,
              "Y45-49": 47, "Y50-54": 52}
    tot = 0.0
    print(f"  occupati per classe d'eta' (Eurostat lfsa_egan, {anno_occ}):")
    print(f"  {'classe':>8}{'occupati':>12}{'anni contr.':>13}{'montante medio':>17}{'totale':>12}")
    for cl, eta in classi.items():
        if cl not in occ:
            continue
        n = occ[cl] * 1000
        # regime contributivo puro: chi ha iniziato dopo il 1996
        anno_ingresso = ANNO - (eta - 25)
        if anno_ingresso < 1996:
            quota_contributiva = 0.0
        else:
            quota_contributiva = 1.0
        anni = max(1, eta - 25)
        m = montante_medio(anni, eta)
        contrib = n * quota_contributiva * m / 1e9
        tot += contrib
        print(f"  {cl:>8}{n/1e6:>10,.2f}M{anni:>13}{m:>16,.0f}{contrib:>10,.0f} mld")
    print(f"\n  TOTALE montanti nozionali dei contributivi puri: {tot:,.0f} mld")

    print()
    print("=" * 100)
    print("CONFRONTO E SCELTA")
    print("=" * 100)
    a_centro = attivi * (1 - 0.35)
    print(f"  VIA A (ADL - PV legacy, misti al 35%) : {a_centro:>8,.0f} mld")
    print(f"  VIA B (montanti nozionali bottom-up)  : {tot:>8,.0f} mld")
    div = abs(a_centro - tot) / max(a_centro, tot) * 100
    print(f"  divergenza                            : {div:>8,.0f} %")
    print()
    print(f"  PLACEHOLDER PRECEDENTE                :    1,400 mld  <-- MUORE in ogni caso")
    print()
    print("  Le due vie misurano cose diverse (PV attuariale scontato al 5% vs saldo")
    print("  nozionale capitalizzato all'1,7%): un divario e' ATTESO, non e' un errore.")
    print("  Per il riconoscimento come IOU al valore nozionale, la grandezza corretta")
    print("  e' la VIA B: e' quanto e' stato materialmente accreditato sui conti.")

    pd.DataFrame([
        {"parametro": "adl_totale_s13ps", "valore": ADL_2021, "unita": "mld EUR",
         "anno": 2021, "fonte": "Eurostat nasa_10_pens1, penscheme=S13PS, na_item=F63_LS",
         "flag_qualita": "verificato"},
        {"parametro": "pv_pensioni_in_pagamento", "valore": pv_leg, "unita": "mld EUR",
         "anno": ANNO, "fonte": f"COFOG 359,6 lineare a zero su 30 anni, sconto 5%",
         "flag_qualita": "stima_esplicita"},
        {"parametro": "diritti_maturati_attivi", "valore": attivi, "unita": "mld EUR",
         "anno": 2021, "fonte": "Via A: ADL - PV legacy", "flag_qualita": "stima_esplicita"},
        {"parametro": "passivita_riconoscimento_via_A", "valore": a_centro, "unita": "mld EUR",
         "anno": 2021, "fonte": "Via A, misti al 35%", "flag_qualita": "stima_esplicita"},
        {"parametro": "passivita_riconoscimento_via_B", "valore": tot, "unita": "mld EUR",
         "anno": ANNO, "fonte": "Via B: occupati Eurostat lfsa_egan x montante da calcolatore",
         "flag_qualita": "stima_esplicita"},
    ]).to_csv(OUT / "passivita_riconoscimento.csv", index=False)
    print(f"\n  Scritto {OUT / 'passivita_riconoscimento.csv'}")


if __name__ == "__main__":
    main()
