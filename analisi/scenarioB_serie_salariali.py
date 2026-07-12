"""
SCENARIO B — RICALIBRATO su serie salariali storiche vere.

L'ERRORE CHE CORREGGE
---------------------
Il calcolatore assumeva una crescita salariale del 2% NOMINALE fisso. Ma le carriere
dei pensionati retributivi corrono dal 1970 al 2002-2010, quando l'inflazione era
~10%/anno. Salari fermi al 2% + montante capitalizzato ai tassi veri (15-22% negli
anni '70-'80) = montante GONFIATO -> controfattuale piu' alto della pensione effettiva
-> eccesso ZERO. La stima di 5,5-7,3 mld/anno poggiava su questo.

LA CORREZIONE
-------------
Sentiero salariale = serie storica vera delle retribuzioni nominali italiane.
Fonte primaria: AMECO (Commissione UE), ITA.1.0.0.0.HWCDW "Nominal compensation per
employee, total economy", annuale dal 1960. Banca dati ufficiale UE: incontestabile.
Riscontri: ISTAT (retribuzioni per ULA) e OCSE (average annual wages, dal 1990).

DUE IPOTESI-CHIAVE, ENTRAMBE DICHIARATE
---------------------------------------
1. PREMIO DI CARRIERA. La serie aggregata da' la crescita del salario MEDIO
   dell'economia. La carriera individuale ci aggiunge la progressione (anzianita',
   avanzamenti): tipicamente +1-2 punti l'anno sopra l'aggregato. Ignorarlo
   sottostima il montante e GONFIA l'eccesso — l'errore opposto a quello appena
   trovato. Parametrizzato: premio 0 / +1 / +2 punti.
2. TASSI DI CAPITALIZZAZIONE PRE-1996. Il sistema contributivo nasce nel 1996: i
   "tassi di capitalizzazione" per gli anni precedenti sono un CONTROFATTUALE
   COSTRUITO (dai livelli di PIL nominale), non un dato osservato. La scelta di
   costruirli cosi' e' un'ipotesi, non una misura, e va dichiarata accanto alla prima.

ANCORA DI VALIDAZIONE
---------------------
Prima di fidarsi: il controfattuale deve riprodurre un tasso di sostituzione
contributivo-equivalente plausibile (~60-75% dell'ultima retribuzione). Se esce
molto sopra o sotto, c'e' un parametro storto e il risultato non si usa.
"""
from __future__ import annotations

import io
from pathlib import Path
import sys
import zipfile

import pandas as pd
import requests

ANALISI = Path(__file__).resolve().parent
REPO = ANALISI.parent / "pensioni_italia"
OUT = ANALISI / "output"
for p in [ANALISI, REPO / "scripts", REPO / "scripts" / "src", REPO / "calcolatore" / "src"]:
    if str(p) not in sys.path:
        sys.path.append(str(p))

import pension_paid_calculator as ppc  # noqa: E402
from override_tassi_ufficiali import capitalization_for_year_ufficiale  # noqa: E402

ppc.capitalization_for_year = capitalization_for_year_ufficiale

MENSILITA = 13.0
AMECO_URL = "https://ec.europa.eu/economy_finance/db_indicators/ameco/documents/ameco7.zip"
SERIE = "ITA.1.0.0.0.HWCDW"   # Nominal compensation per employee, total economy


def salari_ameco() -> dict[int, float]:
    """Indice dei salari nominali italiani, 1960-oggi (AMECO)."""
    z = zipfile.ZipFile(io.BytesIO(requests.get(AMECO_URL, timeout=180).content))
    txt = z.read(z.namelist()[0]).decode("latin-1")
    righe = txt.splitlines()
    anni = [int(a) for a in righe[0].split(";")[5:] if a.strip().isdigit()]
    for r in righe:
        if r.startswith(SERIE + ";"):
            campi = r.split(";")[5:]
            out = {}
            for a, v in zip(anni, campi):
                v = v.strip().replace(",", ".")
                if v and v not in ("NA", "-"):
                    try:
                        out[a] = float(v)
                    except ValueError:
                        pass
            return out
    raise SystemExit(f"serie {SERIE} non trovata in AMECO")


def eccesso(imp_mese: float, eta_dec: int, anno_dec: int, W: dict[int, float],
            premio: float, eta_ing: int = 25) -> dict:
    """Componente non finanziata di una pensione retributiva, col sentiero salariale vero."""
    anni = int(round(eta_dec - eta_ing))
    P = imp_mese * MENSILITA                 # pensione annua effettiva
    ral_finale = P / (0.02 * anni)           # inversione della formula retributiva
    yrs = list(range(anno_dec - anni, anno_dec))
    # profilo: salario aggregato AMECO + premio di carriera composto
    base = {y: W[y] for y in yrs if y in W}
    if len(base) < anni * 0.8:
        raise ValueError(f"serie salariale incompleta per {yrs[0]}-{yrs[-1]}")
    ultimo = max(base)
    prof = {}
    for y in yrs:
        wy = base.get(y, base[min(base, key=lambda k: abs(k - y))])
        prof[y] = (wy / base[ultimo]) * ((1 + premio) ** (y - ultimo))
    ral_iniziale = ral_finale * prof[yrs[0]]

    s = dict(ppc.DEFAULT_SCENARIO)
    s.update({
        "scenario_id": "B", "anno_inizio": yrs[0], "anno_fine": yrs[-1],
        "anno_pensione": anno_dec, "data_pensionamento": f"{anno_dec}-01-01",
        "anno_nascita": anno_dec - eta_dec, "data_nascita": f"{anno_dec - eta_dec}-01-01",
        "eta_pensione": eta_dec, "anni_contribuiti": anni,
        "ral_iniziale": ral_iniziale, "ral_finale": ral_finale,
        "percentuale_lavoro": 100.0, "mesi_lavorati_annui": 12.0,
    })
    car = ppc.build_simplified_career(s)
    montante = float(car["montante_fine_anno"].iloc[-1])
    coef = ppc.transformation_coefficient(anno_dec, eta_dec, 0)
    P_contrib = montante * coef.coefficiente
    return {
        "pensione_effettiva": P, "pensione_contributiva": P_contrib,
        "eccesso": max(0.0, P - P_contrib), "quota_pct": max(0.0, P - P_contrib) / P * 100,
        "ral_finale": ral_finale, "anni": anni,
        "tasso_sostituzione_retributivo": P / ral_finale * 100,
        "tasso_sostituzione_contributivo": P_contrib / ral_finale * 100,
    }


def main() -> None:
    W = salari_ameco()
    print("SERIE SALARIALE — AMECO, Italia, compensation per employee (nominale)")
    print(f"  copertura: {min(W)}-{max(W)}  ({len(W)} osservazioni)")
    g = lambda a, b: (W[b] / W[a]) ** (1 / (b - a)) - 1
    print(f"  crescita nominale media 1970-1990: {g(1970,1990)*100:5.1f}% /anno")
    print(f"  crescita nominale media 1990-2010: {g(1990,2010)*100:5.1f}% /anno")
    print(f"  crescita nominale media 2010-2024: {g(2010,2024)*100:5.1f}% /anno")
    print("  (il vecchio modello assumeva 2,0% su TUTTO il periodo)")

    # stock legacy retributivo privato di vecchiaia (cubo 389)
    N_LEGACY = 4_220_653
    IMP_LEGACY = 1_480.91
    ETA_LEGACY = 58
    ANNO_LEGACY = 2003

    print()
    print("=" * 96)
    print("ANCORA DI VALIDAZIONE — il tasso di sostituzione e' plausibile?")
    print("=" * 96)
    print(f"  {'premio carriera':<18}{'RAL finale':>12}{'t.sost. RETR.':>15}{'t.sost. CONTR.':>16}{'plausibile?':>14}")
    print("  " + "-" * 74)
    righe = []
    for premio in (0.0, 0.01, 0.02):
        r = eccesso(IMP_LEGACY, ETA_LEGACY, ANNO_LEGACY, W, premio)
        ok = "SI" if 55 <= r["tasso_sostituzione_contributivo"] <= 80 else "NO — fuori range"
        print(f"  {premio*100:>3.0f} punti/anno   {r['ral_finale']:>12,.0f}"
              f"{r['tasso_sostituzione_retributivo']:>14.1f}%{r['tasso_sostituzione_contributivo']:>15.1f}%{ok:>14}")
        righe.append({"premio": premio, **r})

    print()
    print("  Atteso per il contributivo-equivalente: 60-75% dell'ultima retribuzione.")

    print()
    print("=" * 96)
    print("SCENARIO B — ECCESSO NON FINANZIATO, stock legacy retributivo privato (vecchiaia)")
    print("=" * 96)
    print(f"  base: {N_LEGACY:,} pensioni, {IMP_LEGACY:,.0f} EUR/mese, eta' decorrenza {ETA_LEGACY}")
    print()
    print(f"  {'premio carriera':<18}{'quota non fin.':>16}{'eccesso/pensione':>19}{'ECCESSO/ANNO':>16}")
    print("  " + "-" * 69)
    for r in righe:
        print(f"  {r['premio']*100:>3.0f} punti/anno   {r['quota_pct']:>15.1f}%"
              f"{r['eccesso']:>18,.0f}{N_LEGACY*r['eccesso']/1e9:>14,.1f} mld")

    print()
    print("  CONFRONTO:")
    print("     vecchia stima (salari +2% fisso, coorti recenti GDP) :  5,5 - 7,3 mld/anno")
    print(f"     nuova stima (AMECO, premio 0-2 punti)                : "
          f"{min(N_LEGACY*r['eccesso']/1e9 for r in righe):,.1f} - "
          f"{max(N_LEGACY*r['eccesso']/1e9 for r in righe):,.1f} mld/anno")
    print()
    print("  PERIMETRO: solo retributivo di VECCHIAIA delle 5 gestioni PRIVATE.")
    print("  Esclusi: Gestione Dipendenti Pubblici (piu' retributiva), invalidita',")
    print("  superstiti, misto Dini/Fornero. Il totale di sistema e' PIU' ALTO.")

    pd.DataFrame(righe).assign(
        eccesso_annuo_mld=lambda d: N_LEGACY * d.eccesso / 1e9,
        n_pensioni=N_LEGACY,
        fonte="AMECO ITA.1.0.0.0.HWCDW + cubo INPS 389 (retributivo, vecchiaia)",
    ).to_csv(OUT / "scenarioB_ricalibrato.csv", index=False)
    print(f"\n  Scritto {OUT / 'scenarioB_ricalibrato.csv'}")


if __name__ == "__main__":
    main()
