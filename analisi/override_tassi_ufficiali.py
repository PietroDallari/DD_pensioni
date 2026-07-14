"""
Override: rivaluta il montante con i COEFFICIENTI UFFICIALI PUBBLICATI,
non con il ricalcolo dai livelli di PIL nominale correnti.

MOTIVAZIONE
-----------
Il calcolatore di Nazareno ricalcola il tasso di capitalizzazione come
    (PIL_t-1 / PIL_t-6)^(1/5) - 1
usando le edizioni ISTAT del PIL nominale *disponibili oggi*, e tiene il tasso
ufficiale pubblicato solo come colonna di controllo (`tasso_ufficiale_pubblicato`).
Cfr. calcolatore/README.md:20 e pension_paid_calculator.py:868.

Per il nostro scopo questo introduce un errore SISTEMATICO. Noi misuriamo
l'eccesso della pensione effettiva sul controfattuale contributivo "come lo
liquiderebbe l'INPS": INPS rivaluta il montante con i coefficienti pubblicati
per legge, calcolati sulle edizioni PIL disponibili *allora*. Le revisioni dei
conti nazionali cambiano retroattivamente i livelli di PIL, quindi il ricalcolo
produce un montante che nessun assicurato ha mai avuto. Su 30-40 anni di
capitalizzazione composta lo scarto si accumula e finisce dritto nella
"componente non finanziata" che vogliamo quantificare: distorsione della base
imponibile, non dettaglio cosmetico.

LOGICA
------
  tasso = tasso_ufficiale_pubblicato   se presente
        = ricalcolo da PIL             altrimenti (fallback: anni recentissimi
                                       o futuri senza ancora la nota ministeriale)
Il ricalcolo NON viene buttato: resta come colonna di controllo nei CSV emessi.

IMPLEMENTAZIONE
---------------
Monkey-patch di `pension_paid_calculator.capitalization_for_year`, che e' il
collo di bottiglia unico usato da build_simplified_career, build_accurate_career
e parameter_tables. Il repo di Nazareno NON viene modificato. Gli output della
variante ufficiale sono scritti in analisi/output/, non in quelli del repo.

USO
---
    analisi/.venv/Scripts/python.exe analisi/override_tassi_ufficiali.py
"""
from __future__ import annotations

import dataclasses
import math
from pathlib import Path
import sys

ANALISI_DIR = Path(__file__).resolve().parent
REPO_DIR = ANALISI_DIR.parent / "pensioni_italia"
OUT_DIR = ANALISI_DIR / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

for path in [REPO_DIR / "scripts", REPO_DIR / "scripts" / "src", REPO_DIR / "calcolatore" / "src"]:
    if str(path) not in sys.path:
        sys.path.append(str(path))

import pandas as pd  # noqa: E402
import pension_paid_calculator as ppc  # noqa: E402


# --- SECONDO OVERRIDE: il sentiero salariale resta AMECO ----------------------
# Dal commit upstream 52abdf7 il calcolatore usa gli INDICI ISTAT DELLE RETRIBUZIONI
# CONTRATTUALI (dataflow 155_318) per dare forma al sentiero salariale fra i punti noti,
# al posto dell'interpolazione geometrica: salary_profile() chiama prima
# contractual_salary_profile() e, se questa risponde, usa la sua forma.
#
# NOI COSTRUIAMO IL SENTIERO CON AMECO (retribuzioni nominali per occupato, 1960-2025) e lo
# passiamo al calcolatore come ral_iniziale + ral_finale. Lasciare attivo il profilo
# contrattuale significherebbe "estremi AMECO + interno CCNL": un metodo diverso da quello
# che il report dichiara.
#
# PERCHE' AMECO E NON I CONTRATTUALI: gli indici ISTAT misurano le retribuzioni CONTRATTUALI
# (i minimi negoziali), AMECO le retribuzioni EFFETTIVAMENTE percepite per occupato. Il
# controfattuale contributivo si costruisce sui contributi VERSATI, che seguono la
# retribuzione effettiva (imponibile), non il minimo tabellare. La differenza non e' neutra:
# lo slittamento salariale (superminimi, scatti, premi) sta nella prima e non nella seconda.
#
# EFFETTO MISURATO della scelta: con gli indici contrattuali l'eccesso non finanziato
# salirebbe di 2-3 punti per fascia (bordo alto 43,3% -> 44,3%) e il gettito dello Scenario B
# di +0,1 mld. La nostra scelta e' quindi la PIU' CONSERVATIVA delle due.
#
# Il bypass e' idempotente e non tocca il repo di Nazareno.
if hasattr(ppc, "contractual_salary_profile"):
    ppc.contractual_salary_profile = lambda years, scenario, known_points: None


# --- L'override ---------------------------------------------------------------
_original_capitalization_for_year = ppc.capitalization_for_year

NOTA_UFFICIALE = (
    "Tasso ufficiale pubblicato (nota ISTAT/Ministero del Lavoro), quello applicato per "
    "legge da INPS alla rivalutazione del montante. Override rispetto al ricalcolo dai "
    "livelli di PIL nominale correnti, che risente delle revisioni dei conti nazionali."
)
NOTA_FALLBACK = (
    "Tasso ufficiale non ancora pubblicato per questo anno: usato il ricalcolo "
    "(PIL t-1 / PIL t-6)^(1/5)-1 come fallback."
)


def capitalization_for_year_ufficiale(year: int) -> ppc.CapitalizationInfo:
    """Come l'originale, ma il tasso applicato e' quello ufficiale se disponibile."""
    cap = _original_capitalization_for_year(year)
    ufficiale = cap.tasso_ufficiale_pubblicato
    if ufficiale is None or (isinstance(ufficiale, float) and math.isnan(ufficiale)):
        return dataclasses.replace(
            cap,
            natura_dato=f"{cap.natura_dato}__fallback_ricalcolo_pil",
            note=f"{NOTA_FALLBACK} {cap.note}",
        )
    return dataclasses.replace(
        cap,
        tasso=float(ufficiale),
        natura_dato="ufficiale_pubblicato_istat_ministero",
        note=f"{NOTA_UFFICIALE} Ricalcolo di controllo: {cap.tasso:.6f}.",
    )


def _run(label: str, patched: bool) -> pd.DataFrame:
    ppc.capitalization_for_year = (
        capitalization_for_year_ufficiale if patched else _original_capitalization_for_year
    )
    if patched:
        # Scrive in analisi/output/, cosi' gli artefatti del repo restano quelli
        # della pipeline originale di Nazareno.
        ppc.ANALYTIC_OUTPUT_PATHS = {
            key: OUT_DIR / f"{Path(value).stem}__tassi_ufficiali.csv"
            for key, value in ppc.ANALYTIC_OUTPUT_PATHS.items()
        }
    result = ppc.run_pension_paid_calculator()
    result.insert(1, "variante_tasso", label)
    return result


def main() -> None:
    originali = dict(ppc.ANALYTIC_OUTPUT_PATHS)

    base = _run("ricalcolo_pil", patched=False)
    ppc.ANALYTIC_OUTPUT_PATHS = originali
    uff = _run("ufficiale_pubblicato", patched=True)

    # --- Tabella A: scarto anno per anno sui tassi ----------------------------
    tassi = pd.read_csv(REPO_DIR / "output" / "data" / "clean" / "tassi_capitalizzazione_montante.csv")
    tassi_out = tassi[[
        "anno", "tasso_ufficiale_pubblicato", "tasso_capitalizzazione", "scarto_da_tasso_ufficiale",
    ]].rename(columns={"tasso_capitalizzazione": "tasso_ricalcolato_da_pil"})
    tassi_out.to_csv(OUT_DIR / "scarto_tassi_per_anno.csv", index=False)

    # --- Tabella B: impatto sui tre scenari -----------------------------------
    chiavi = [
        "montante_contributivo",
        "pensione_contributiva_annua_equivalente",
        "pensione_contributiva_mensile_equivalente",
        "differenza_annua_lorda",
        "differenza_mensile_lorda",
        "differenza_percentuale_su_contributiva",
        "rapporto_prestazioni_attese_montante",
    ]
    a = base.set_index("scenario_id")
    b = uff.set_index("scenario_id")
    righe = []
    for scenario_id in a.index:
        for k in chiavi:
            va, vb = float(a.loc[scenario_id, k]), float(b.loc[scenario_id, k])
            righe.append({
                "scenario_id": scenario_id,
                "metrica": k,
                "ricalcolo_pil": va,
                "ufficiale_pubblicato": vb,
                "delta_assoluto": vb - va,
                "delta_pct": (vb - va) / va * 100 if va else None,
            })
    confronto = pd.DataFrame(righe)
    confronto.to_csv(OUT_DIR / "confronto_scenari_tassi_ufficiali.csv", index=False)

    pd.concat([base, uff], ignore_index=True).to_csv(
        OUT_DIR / "calcolatore_base__entrambe_le_varianti.csv", index=False
    )

    # --- Stampa ---------------------------------------------------------------
    pd.set_option("display.width", 200)
    print("\n=== SCARTO SUI TASSI (anni con scarto maggiore) ===")
    top = tassi_out.reindex(
        tassi_out.scarto_da_tasso_ufficiale.abs().sort_values(ascending=False).index
    ).head(8)
    print(top.to_string(index=False, float_format=lambda x: f"{x: .6f}"))

    print("\n=== IMPATTO SUL CONTROFATTUALE CONTRIBUTIVO ===")
    for scenario_id in a.index:
        sub = confronto[confronto.scenario_id.eq(scenario_id)]
        print(f"\n--- {scenario_id} ---")
        print(sub[["metrica", "ricalcolo_pil", "ufficiale_pubblicato", "delta_assoluto", "delta_pct"]]
              .to_string(index=False, float_format=lambda x: f"{x: ,.2f}"))

    print(f"\nOutput scritti in {OUT_DIR}")


if __name__ == "__main__":
    main()
