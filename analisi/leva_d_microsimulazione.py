"""
LEVA D/F — Ricalcolo della "componente non finanziata" e del gettito del prelievo.

COSA SOSTITUISCE
----------------
Il doc (§4-D) stima:  650.000 x 60.000 EUR x 50% = ~20 mld/anno.
Quattro difetti: (a) mescola soglia NETTA e media LORDA; (b) il 50% piatto e'
arbitrario (e la Leva F ammette che andrebbe presa "la sola componente non
finanziata" -> D ed F sono la stessa leva, con rischio di doppio conteggio);
(c) una media piatta appiattisce la coda, mentre la componente non finanziata e'
convessa nell'importo; (d) assume senza verificarlo che i pensionati ricchi
siano tutti retributivi.

METODO
------
Microsimulazione per celle sulla distribuzione INPS reale, invece di un
moltiplicatore unico. Per ogni classe di importo:

  1. N e importo medio           <- INPS open data (dataset 1824 e 1650)
  2. P = pensione annua lorda    <- importo medio mensile x 13
  3. W = P / (0.02 * n)          <- INVERSIONE della formula retributiva:
                                    il retributivo paga ~2% dell'ultima
                                    retribuzione per ogni anno di anzianita'.
                                    Da P e n si risale alla RAL finale W.
  4. P_contrib = calcolatore(W, n, eta)   <- controfattuale contributivo, con i
                                             TASSI UFFICIALI di capitalizzazione
                                             (cfr. override_tassi_ufficiali.py)
  5. non_finanziata = max(0, P - P_contrib)
  6. gettito = N x non_finanziata x aliquota_prelievo x quota_retributiva

Il passo 3 e' l'assunzione critica: dalla distribuzione osserviamo SOLO
l'importo, non la carriera. Per questo il risultato e' pubblicato come
INTERVALLO su n (anzianita'), non come numero puntuale.

LIMITI DA NON NASCONDERE
------------------------
- La classe superiore INPS e' APERTA ("3000 e piu'"): la forma della coda non e'
  osservabile. Il gettito della coda e' quindi il pezzo piu' fragile.
- La serie dei beneficiari per classe si ferma al 2016 (dataset 1824).
- La distribuzione congiunta IMPORTO x REGIME non esiste negli open data INPS:
  il dataset 1648 da' il regime ma senza classi di importo. La quota retributiva
  per classe e' quindi IMPUTATA, non osservata.
- Per questa ragione Nazareno ha rimosso dal calcolatore le colonne aggregate e
  ha bloccato la rimozione con un test (README: "Il risultato individuale non
  viene applicato alla spesa pensionistica nazionale"). Qui l'aggregazione viene
  fatta, ma con l'imputazione esplicita e la sensibilita' dichiarata.

USO
---
    analisi/.venv/Scripts/python.exe analisi/leva_d_microsimulazione.py
"""
from __future__ import annotations

import io
from pathlib import Path
import sys

import pandas as pd
import requests

ANALISI_DIR = Path(__file__).resolve().parent
REPO_DIR = ANALISI_DIR.parent / "pensioni_italia"
OUT_DIR = ANALISI_DIR / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

for p in [REPO_DIR / "scripts", REPO_DIR / "scripts" / "src", REPO_DIR / "calcolatore" / "src"]:
    if str(p) not in sys.path:
        sys.path.append(str(p))

import pension_paid_calculator as ppc  # noqa: E402
from override_tassi_ufficiali import capitalization_for_year_ufficiale  # noqa: E402

# Rivaluta il montante con i coefficienti UFFICIALI (non il ricalcolo da PIL).
ppc.capitalization_for_year = capitalization_for_year_ufficiale

URL_BENEFICIARI = "http://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5302.csv"   # 1824
URL_IMPORTI = "http://www.inps.it/docallegati/Mig/OpenData/CSV/dataset_5074.csv"  # 1650
URL_REGIME = "http://www.inps.it/docallegati/Mig/OpenData/CSV/dataset_5072.csv"   # 1648

MENSILITA = 13.0
ANNO_PENSIONE = 2025
ETA_PENSIONE = 65

# Punti centrali della classe. La classe superiore e' APERTA: il valore e'
# ricavato dall'importo medio osservato nel dataset 1650, non inventato.
CENTRI = {
    "Fino a 249,99": 125, "250,00-499,99": 375, "500,00-749,99": 625,
    "750,00-999,99": 875, "1000,00-1249,99": 1125, "1250,00-1499,99": 1375,
    "1500,00-1749,99": 1625, "1750,00-1999,99": 1875, "2000,00-2249,99": 2125,
    "2250,00-2499,99": 2375, "2500,00-2999,99": 2750,
}
CLASSE_APERTA = "3000,00 e più"


def scarica(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.content.decode("latin-1")), sep=",", quotechar='"')
    d.columns = [c.strip() for c in d.columns]
    return d


def media_classe_aperta() -> float:
    """Importo medio mensile della classe aperta '3000 e piu'', dal dataset 1650."""
    d = scarica(URL_IMPORTI)
    top = d[d["Classe di importo"].astype(str).str.contains("3000", na=False)]
    top = top[top["Anno"].eq(top["Anno"].max())]
    # media ponderata sull'importo complessivo annuo (proxy del peso della cella)
    w = pd.to_numeric(top["Importo complessivo annuo"], errors="coerce").fillna(0)
    m = pd.to_numeric(top["Importo medio mensile"], errors="coerce")
    return float((m * w).sum() / w.sum()) if w.sum() else float(m.mean())


def quote_regime() -> pd.DataFrame:
    """Quota di spesa per regime di liquidazione (dataset 1648, ultimo anno)."""
    d = scarica(URL_REGIME)
    d = d[d["Anno"].eq(d["Anno"].max())]
    d["imp"] = pd.to_numeric(d["Importo complessivo annuo"], errors="coerce")
    q = d.groupby("Regime di liquidazione")["imp"].sum()
    return (q / q.sum()).sort_values(ascending=False)


def pensione_contributiva(ral_finale: float, anni: int) -> float:
    """Controfattuale contributivo per una RAL finale e un'anzianita' dati."""
    scen = dict(ppc.DEFAULT_SCENARIO)
    scen.update({
        "scenario_id": "cella",
        "anno_inizio": ANNO_PENSIONE - anni,
        "anno_fine": ANNO_PENSIONE - 1,
        "anno_pensione": ANNO_PENSIONE,
        "data_pensionamento": f"{ANNO_PENSIONE}-01-01",
        "anno_nascita": ANNO_PENSIONE - ETA_PENSIONE,
        "data_nascita": f"{ANNO_PENSIONE - ETA_PENSIONE}-01-01",
        "eta_pensione": ETA_PENSIONE,
        "anni_contribuiti": anni,
        "ral_finale": float(ral_finale),
        "ral_iniziale": None,
        "progressione": "media",
        "percentuale_lavoro": 100.0,
        "mesi_lavorati_annui": 12.0,
    })
    car = ppc.build_simplified_career(scen)
    montante = float(car["montante_fine_anno"].iloc[-1])
    coef = ppc.transformation_coefficient(ANNO_PENSIONE, ETA_PENSIONE, 0)
    return montante * coef.coefficiente


def main() -> None:
    ben = scarica(URL_BENEFICIARI)
    anno = int(ben["Anno"].max())
    N = ben[ben["Anno"].eq(anno)].groupby("Classe importo")["Numero beneficiari"].sum()

    centri = dict(CENTRI)
    centri[CLASSE_APERTA] = media_classe_aperta()
    print(f"Importo medio osservato nella classe aperta '3000 e piu'': "
          f"{centri[CLASSE_APERTA]:,.0f} EUR/mese\n")

    regimi = quote_regime()
    print("Quota di SPESA per regime di liquidazione (dataset 1648, ultimo anno):")
    for k, v in regimi.items():
        print(f"   {k:<20} {v*100:5.1f}%")
    print()

    # soglia netta -> lordo, con la funzione fiscale del calcolatore
    lordo_da_3000_netti = ppc.pension_gross_annual_from_net(3000 * MENSILITA) / MENSILITA
    lordo_da_2500_netti = ppc.pension_gross_annual_from_net(2500 * MENSILITA) / MENSILITA
    print(f"Soglia 3.000 EUR NETTI/mese  ->  {lordo_da_3000_netti:,.0f} EUR LORDI/mese")
    print(f"Soglia 2.500 EUR NETTI/mese  ->  {lordo_da_2500_netti:,.0f} EUR LORDI/mese\n")

    def centro(classe: str) -> float | None:
        """Match robusto: la classe aperta contiene '3000' ma l'encoding di 'piu'' varia."""
        if "3000" in str(classe):
            return centri[CLASSE_APERTA]
        return CENTRI.get(str(classe))

    righe = []
    for anzianita in (25, 30, 35, 38, 40):
        for classe, n_ben in N.items():
            mensile = centro(classe)
            if mensile is None:
                print(f"ATTENZIONE: classe non mappata, esclusa: {classe!r}")
                continue
            P = mensile * MENSILITA                      # pensione annua lorda
            W = P / (0.02 * anzianita)                   # RAL finale implicita (retributivo)
            P_contrib = pensione_contributiva(W, anzianita)
            non_fin = max(0.0, P - P_contrib)
            righe.append({
                "anzianita_ipotesi": anzianita,
                "classe_importo": classe,
                "beneficiari": float(n_ben),
                "pensione_mensile_lorda": mensile,
                "pensione_annua_lorda": P,
                "ral_finale_implicita": W,
                "pensione_contributiva_equivalente": P_contrib,
                "componente_non_finanziata_annua": non_fin,
                "quota_non_finanziata_pct": non_fin / P * 100 if P else 0.0,
                "sopra_3000_lordi": mensile >= 3000,
                "sopra_soglia_3000_netti": mensile >= lordo_da_3000_netti,
                "sopra_soglia_2500_netti": mensile >= lordo_da_2500_netti,
            })
    d = pd.DataFrame(righe)
    d.to_csv(OUT_DIR / "leva_d_celle.csv", index=False)

    print("=" * 108)
    print("COMPONENTE NON FINANZIATA PER CLASSE (ipotesi centrale: 38 anni di anzianita')")
    print("=" * 108)
    c = d[d.anzianita_ipotesi.eq(38)].sort_values("pensione_mensile_lorda")
    print(c[["classe_importo", "beneficiari", "pensione_mensile_lorda", "ral_finale_implicita",
             "pensione_contributiva_equivalente", "componente_non_finanziata_annua",
             "quota_non_finanziata_pct"]]
          .to_string(index=False, float_format=lambda x: f"{x:,.0f}"))

    print()
    print("=" * 108)
    print("GETTITO ANNUO DEL PRELIEVO — confronto con la stima del doc (~20 mld)")
    print("=" * 108)
    q_retributivo = float(regimi.get("Retributivo", 0)) + float(regimi.get("Misto", 0))
    print(f"quota retributivo+misto sulla spesa (dato INPS): {q_retributivo*100:.1f}%")
    print()
    print("NB: la quota non finanziata NON dipende dalla classe di importo (il modello e'"
          "\n    lineare per costruzione): dipende dall'ANZIANITA'. E' li' che sta la leva.\n")
    print(f"{'anzianita':>10} {'scenario':<38} {'platea':>12} {'gettito':>14}")
    print("-" * 80)
    for anz in (25, 30, 35, 38, 40):
        s = d[d.anzianita_ipotesi.eq(anz)]
        for lab, col, aliq in [
            ("doc: 50% della pensione, >3000 lordi", "sopra_3000_lordi", None),
            ("100% comp. non fin., >3000 lordi", "sopra_3000_lordi", 1.00),
            ("100% comp. non fin., >soglia 3000 netti", "sopra_soglia_3000_netti", 1.00),
            ("100% comp. non fin., >soglia 2500 netti", "sopra_soglia_2500_netti", 1.00),
        ]:
            sub = s[s[col]]
            platea = sub.beneficiari.sum()
            if platea == 0:
                # La soglia cade DENTRO la classe aperta "3000 e piu'", la cui coda
                # non e' osservabile: il gettito non e' zero, e' NON CALCOLABILE.
                print(f"{anz:>10} {lab:<38} {'n.c.':>9}     {'n.c. (classe aperta)':>10}")
                continue
            if aliq is None:
                gettito = (sub.beneficiari * sub.pensione_annua_lorda * 0.50).sum()
            else:
                gettito = (sub.beneficiari * sub.componente_non_finanziata_annua * aliq
                           * q_retributivo).sum()
            print(f"{anz:>10} {lab:<38} {platea/1e6:>9.2f} mln {gettito/1e9:>10.1f} mld")
        print()

    print(f"Dettaglio per cella salvato in {OUT_DIR / 'leva_d_celle.csv'}")


if __name__ == "__main__":
    main()
