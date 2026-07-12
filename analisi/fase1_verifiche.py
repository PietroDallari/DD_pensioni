"""
FASE 1 — Verifiche dati bloccanti prima di ricalcolare il modello.

Produce:
  output/perimetro_spesa.csv        (1.1) riconciliazione della spesa pensionistica
  output/distribuzione_pensionati.csv (1.3) fasce lorde/nette, numerosita', importi
  output/parametri_verificati.csv   (1.2 + sintesi) ogni parametro con fonte, anno, flag

Ogni riga porta: valore, fonte, anno, flag_qualita.
flag_qualita:  verificato | stima_esplicita | non_calcolabile | da_verificare
"""
from __future__ import annotations

import io
from pathlib import Path
import sys

import pandas as pd
import requests

ANALISI = Path(__file__).resolve().parent
REPO = ANALISI.parent / "pensioni_italia"
OUT = ANALISI / "output"
OUT.mkdir(parents=True, exist_ok=True)
for p in [REPO / "scripts", REPO / "scripts" / "src", REPO / "calcolatore" / "src"]:
    if str(p) not in sys.path:
        sys.path.append(str(p))

import pension_paid_calculator as ppc  # noqa: E402

MENSILITA = 13.0
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
URL_BENEFICIARI = "http://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5302.csv"  # dataset 1824

CENTRI = {
    "Fino a 249,99": 125, "250,00-499,99": 375, "500,00-749,99": 625,
    "750,00-999,99": 875, "1000,00-1249,99": 1125, "1250,00-1499,99": 1375,
    "1500,00-1749,99": 1625, "1750,00-1999,99": 1875, "2000,00-2249,99": 2125,
    "2250,00-2499,99": 2375, "2500,00-2999,99": 2750,
}


def eurostat(dataset: str, **filtri) -> dict[int, float]:
    q = "&".join(f"{k}={v}" for k, v in filtri.items())
    r = requests.get(f"{EUROSTAT}/{dataset}?format=JSON&geo=IT&{q}", timeout=90)
    r.raise_for_status()
    j = r.json()
    idx = j["dimension"]["time"]["category"]["index"]
    val = j["value"]
    return {int(k): val[str(v)] for k, v in idx.items() if str(v) in val}


# ---------------------------------------------------------------- 1.1 perimetro
def perimetro_spesa() -> tuple[pd.DataFrame, int]:
    voci = {
        "GF1002": "Vecchiaia (old age)",
        "GF1003": "Superstiti",
        "GF1001": "Malattia e invalidita",
        "GF1004": "Famiglia e figli",
        "GF1005": "Disoccupazione",
        "GF1007": "Esclusione sociale",
        "GF10": "Protezione sociale (totale)",
    }
    serie = {lab: eurostat("gov_10a_exp", unit="MIO_EUR", sector="S13", na_item="TE", cofog99=c)
             for c, lab in voci.items()}
    anno = max(set.intersection(*[set(s) for s in serie.values()]))
    righe = [{
        "voce": lab, "importo_mld": s[anno] / 1000, "anno": anno,
        "fonte": "Eurostat gov_10a_exp (COFOG, S13)",
        "flag_qualita": "verificato",
    } for lab, s in serie.items()]
    pens = serie["Vecchiaia (old age)"][anno] + serie["Superstiti"][anno]
    righe.append({
        "voce": ">> PENSIONI (vecchiaia + superstiti)", "importo_mld": pens / 1000, "anno": anno,
        "fonte": "Eurostat gov_10a_exp (somma GF1002+GF1003)", "flag_qualita": "verificato",
    })
    righe.append({
        "voce": ">> di cui quota previdenziale vs GIAS", "importo_mld": None, "anno": anno,
        "fonte": "Rendiconto generale INPS (PDF, non ancora estratto)",
        "flag_qualita": "da_verificare",
    })
    return pd.DataFrame(righe), anno


# ------------------------------------------------- 1.3 distribuzione + 1.2 IRPEF
def distribuzione(anno_target: int) -> tuple[pd.DataFrame, int]:
    r = requests.get(URL_BENEFICIARI, timeout=120)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.content.decode("latin-1")), sep=",", quotechar='"')
    d.columns = [c.strip() for c in d.columns]
    anno_dati = int(d["Anno"].max())
    N = d[d["Anno"].eq(anno_dati)].groupby("Classe importo")["Numero beneficiari"].sum()

    # Rivalutazione degli importi dall'anno dei dati all'anno target (HICP Eurostat):
    # le classi INPS sono in euro correnti dell'anno dei dati.
    hicp = eurostat("prc_hicp_aind", unit="INX_A_AVG", coicop="CP00")
    reflator = hicp[anno_target] / hicp[anno_dati]

    righe = []
    for classe, n in N.items():
        aperta = "3000" in str(classe)
        centro_nom = 3214.0 if aperta else CENTRI.get(str(classe))
        if centro_nom is None:
            continue
        lordo_mese = centro_nom * reflator
        lordo_anno = lordo_mese * MENSILITA
        netto_anno = ppc.pension_net_annual_estimate(lordo_anno, anno_target)
        irpef_anno = lordo_anno - netto_anno
        righe.append({
            "classe_lorda_originale": classe,
            "anno_dati": anno_dati,
            "anno_valori": anno_target,
            "numero_beneficiari": float(n),
            "lordo_mensile": lordo_mese,
            "netto_mensile_stimato": netto_anno / MENSILITA,
            "lordo_annuo": lordo_anno,
            "netto_annuo_stimato": netto_anno,
            "irpef_e_addizionali_annue": irpef_anno,
            "aliquota_media_effettiva_pct": irpef_anno / lordo_anno * 100,
            "classe_aperta": aperta,
            "sopra_2000_lordi": lordo_mese >= 2000,
            "sopra_2500_netti": netto_anno / MENSILITA >= 2500,
            "fonte": "INPS open data dataset 1824 (ID-5302); rivalutato con HICP Eurostat",
            "flag_qualita": "stima_esplicita" if aperta else "verificato",
        })
    return pd.DataFrame(righe), anno_dati


def main() -> None:
    print("=" * 96)
    print("FASE 1.1 — PERIMETRO DELLA SPESA")
    print("=" * 96)
    per, anno = perimetro_spesa()
    per.to_csv(OUT / "perimetro_spesa.csv", index=False)
    print(per.to_string(index=False, float_format=lambda x: f"{x:,.1f}"))

    print()
    print("=" * 96)
    print(f"FASE 1.3 — DISTRIBUZIONE PENSIONATI (valori rivalutati al {anno})")
    print("=" * 96)
    dis, anno_dati = distribuzione(anno)
    dis.to_csv(OUT / "distribuzione_pensionati.csv", index=False)
    cols = ["classe_lorda_originale", "numero_beneficiari", "lordo_mensile",
            "netto_mensile_stimato", "aliquota_media_effettiva_pct", "sopra_2500_netti"]
    print(dis[cols].to_string(index=False, float_format=lambda x: f"{x:,.0f}"))
    print(f"\nATTENZIONE: i dati di numerosita' sono {anno_dati}, gli importi sono rivalutati "
          f"al {anno} con HICP.\nLa numerosita' NON e' aggiornata: e' il limite piu' serio di questa tabella.")

    # ---- 1.2 clawback IRPEF, bottom-up dalla distribuzione
    irpef_tot = (dis.numero_beneficiari * dis.irpef_e_addizionali_annue).sum()
    lordo_tot = (dis.numero_beneficiari * dis.lordo_annuo).sum()
    print()
    print("=" * 96)
    print("FASE 1.2 — CLAWBACK IRPEF (stima bottom-up dalla distribuzione)")
    print("=" * 96)
    print(f"  Massa lorda pensionistica implicita : {lordo_tot/1e9:>8,.1f} mld")
    print(f"  IRPEF + addizionali sui trattamenti : {irpef_tot/1e9:>8,.1f} mld")
    print(f"  Aliquota media effettiva            : {irpef_tot/lordo_tot*100:>8,.1f} %")
    print(f"  Atteso dalle istruzioni             :    55-60 mld")

    # platea sopra soglie
    s2500n = dis[dis.sopra_2500_netti]
    print()
    print(f"  Platea sopra 2.500 EUR NETTI/mese: {s2500n.numero_beneficiari.sum()/1e6:,.2f} mln"
          if len(s2500n) else "  Platea sopra 2.500 EUR NETTI/mese: NON CALCOLABILE (classe aperta)")

    # ---- parametri verificati
    par = pd.DataFrame([
        {"parametro": "spesa_pensioni_vecchiaia_superstiti", "valore": per.loc[per.voce.str.startswith(">> PENSIONI"), "importo_mld"].iloc[0],
         "unita": "mld EUR", "anno": anno, "fonte": "Eurostat gov_10a_exp GF1002+GF1003", "flag_qualita": "verificato"},
        {"parametro": "massa_lorda_pensionistica_da_distribuzione", "valore": lordo_tot/1e9,
         "unita": "mld EUR", "anno": anno, "fonte": "INPS 1824 rivalutato HICP", "flag_qualita": "stima_esplicita"},
        {"parametro": "clawback_irpef_su_pensioni", "valore": irpef_tot/1e9,
         "unita": "mld EUR", "anno": anno, "fonte": "bottom-up da distribuzione INPS + IRPEF del calcolatore",
         "flag_qualita": "stima_esplicita"},
        {"parametro": "beneficiari_totali", "valore": dis.numero_beneficiari.sum()/1e6,
         "unita": "mln", "anno": anno_dati, "fonte": "INPS open data 1824", "flag_qualita": "verificato"},
        {"parametro": "nozionale_payg_reale", "valore": 0.0, "unita": "%", "anno": "1996-2025",
         "fonte": "tassi ufficiali capitalizzazione vs HICP Eurostat", "flag_qualita": "verificato"},
        {"parametro": "quota_spesa_regime_retributivo_e_misto", "valore": 98.9, "unita": "%", "anno": 2017,
         "fonte": "INPS open data dataset 1648", "flag_qualita": "verificato"},
        {"parametro": "quota_previdenziale_vs_gias", "valore": None, "unita": "mld EUR", "anno": None,
         "fonte": "Rendiconto generale INPS (PDF)", "flag_qualita": "da_verificare"},
        {"parametro": "passivita_riconoscimento", "valore": None, "unita": "mld EUR", "anno": None,
         "fonte": "RGS/NADEF o stima bottom-up", "flag_qualita": "da_verificare"},
        {"parametro": "platea_sopra_2500_netti", "valore": None, "unita": "mln",
         "anno": anno_dati, "fonte": "INPS 1824 — classe superiore APERTA",
         "flag_qualita": "non_calcolabile"},
    ])
    par.to_csv(OUT / "parametri_verificati.csv", index=False)
    print()
    print("=" * 96)
    print("PARAMETRI VERIFICATI")
    print("=" * 96)
    print(par[["parametro", "valore", "unita", "anno", "flag_qualita"]]
          .to_string(index=False, float_format=lambda x: f"{x:,.1f}"))
    print(f"\nScritti in {OUT}")


if __name__ == "__main__":
    main()
