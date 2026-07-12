"""
Modello di transizione PAYG -> capitalizzazione (Italia).
Replica e parametrizza la contabilita usata nel report: due comparti
(legacy e riconoscimento), profilo temporale, tabella profili lavoratore,
due scenari di prelievo (A: tetto 2500 netti; B: eccesso misurato).

Uso:  python transition_model.py            -> stampa tutte le tabelle
      python transition_model.py --csv DIR  -> salva anche i CSV in DIR

Convenzione: tutti gli importi in EUR mld correnti salvo indicazione.
I parametri marcati DA VERIFICARE vanno sostituiti con i valori della
Fase 1 delle istruzioni prima di citare qualunque output.
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass, field
from pathlib import Path

# ----------------------------------------------------------------------
# ASSUNZIONI (blocco unico: ogni numero del report nasce da qui)
# ----------------------------------------------------------------------

@dataclass
class Assumptions:
    anno_avvio: int = 2018            # anno 0 della transizione
    orizzonte: int = 2093             # fine simulazione

    # --- macro (nominali, coerenti tra loro) ---
    pil_iniziale: float = 2200.0      # EUR mld
    crescita_pil_nom: float = 0.025   # 2,5% nominale
    inflazione: float = 0.017
    tasso_nozionale_nom: float = 0.017  # = inflazione: 0% reale (verificato serie ufficiale vs HICP)
    rendimento_fondo_nom: float = 0.04  # netto tasse e costi
    rendimento_btp50: float = 0.043

    # --- perimetro di spesa (Fase 1.1/1.2) ---
    # VERIFICATO: Eurostat gov_10a_exp (COFOG S13) 2024, GF1002 306,4 + GF1003 53,2.
    # Cross-check indipendente: la massa lorda ricostruita dalla distribuzione INPS
    # (perimetro persone, rivalutata a prezzi 2024) da' 355,4 -> scarto 1,2%.
    # PERIMETRO PREVIDENZIALE PURO. Il legacy da finanziare coi contributi NON e' la
    # spesa pensionistica totale: e' quella al netto delle quote gia' a carico della
    # fiscalita' via GIAS (INPS Rendiconto 2024: 320,6 - 65,9 = 254,7).
    # La GIAS resta, ma come LINEA FISCALE SEPARATA che non si estingue col legacy:
    # non e' un disavanzo previdenziale, e' assistenza dentro il perimetro pensioni.
    spesa_ivs_lorda: float = 254.7      # a carico dei contributi
    spesa_gias_pensionistica: float = 65.9   # fiscalita', linea separata
    spesa_assistenza_fuori_pensioni: float = 29.3  # inv. civile + assegni sociali
    # VERIFICATO E RICONCILIATO (analisi/riconciliazione_perimetri.py).
    # MEF, Dichiarazioni 2024 (a.i. 2023), contribuenti con reddito PREVALENTE da
    # pensione: imposta netta 57,365 + addizionale regionale 5,438 + comunale 2,288.
    # I tre numeri che sembravano in conflitto erano TRE COSE DIVERSE:
    #   78,4 = imposta LORDA (e il mio bottom-up misurava questa: 78,8)
    #   71,1 = ritenuta alla fonte INPS sui trattamenti (Rendiconto 2024 Tab.38 p.101)
    #   57,4 = imposta NETTA, dopo 22,8 mld di detrazioni  <- il gettito vero
    # Lo scarto del 30% stava tutto nelle DETRAZIONI: la funzione fiscale del
    # calcolatore ne implicava ~7 mld contro i 22,8 registrati dal MEF.
    # NB: la ricalibrazione tocca l'aliquota MEDIA, non la MARGINALE (le detrazioni si
    # azzerano sopra i 50.000): il rapporto netto/lordo degli scenari (55%) non cambia.
    # 65,1 mld e' il clawback sull'INTERA spesa pensionistica (320,6). Sul perimetro
    # previdenziale puro (254,7) la quota proporzionale e' 65,1 x 254,7/320,6 = 51,7.
    clawback_irpef: float = 51.7
    anni_estinzione_legacy: int = 30  # spesa legacy lineare a zero

    # --- contributi ---
    contributi_ivs: float = 240.0     # totale IVS
    contributi_contributivi: float = 100.0  # quota dei contributivi puri (dirottabile)
    aliquota_piena: float = 0.33
    aliquota_carveout: float = 0.25   # quanto dirottano; 8 punti restano in PAYG
    tfr_flusso_netto: float = 24.0    # 30 lordi - 6 Fondo Tesoreria perso

    # --- riconoscimento (Comparto 2) ---
    # VERIFICATO a due vie (analisi/fase3_passivita.py), convergenti al 12%:
    #   Via A (top-down): ADL Eurostat nasa_10_pens1 S13PS 2021 = 7.681 mld
    #                     meno PV pensioni in pagamento (3.682) = 3.999 diritti degli
    #                     attivi; al netto della quota retributiva dei misti (35%) -> 2.599
    #   Via B (bottom-up): occupati contributivi per eta' (Eurostat lfsa_egan) x montante
    #                     medio dal calcolatore coi tassi ufficiali          -> 2.297
    # Il placeholder di 1.400 era sottostimato di ~1,8x.
    passivita_riconoscimento: float = 2450.0  # centro 2.300-2.600
    coda_riconoscimento: int = 70     # anni su cui scorre la passivita
    exit_levy: float = 0.05           # quota di nozionale NON riconosciuta (0.05 = 95% riconosciuto)

    # --- Scenario A: tetto 2500 netti ---
    # ANCORATO su due punti osservati (analisi/fase3b_coda_ancorata.py):
    #   N(>= 3.000 EUR/mese) = 1.104.624   INPS open data 1824 (2016)
    #   N(>= 5.000 EUR/mese) =   266.180   INPS, "Prestazioni pensionistiche e
    #                                      beneficiari" 2017 (1,7% dei pensionati)
    # Stesso perimetro (persone, non singole pensioni) -> Pareto alpha = 2,79.
    # CROSS-CHECK indipendente: la coda cosi' calibrata predice ~80k pensionati sopra
    # 100.000 EUR lordi/anno, contro i 16-40k effettivamente colpiti dal contributo di
    # solidarieta' 2019 (L.145/2018 c.261) — coerente, dato che quel perimetro escludeva
    # superstiti, invalidita' e contributivo puro. Il cross-check RIGETTA l'ancora
    # alternativa (400k sopra 5.000, stampa 2023): implicherebbe 170k sopra 100k/anno,
    # 4,2x l'osservato.
    # Intervallo difendibile: 13,5 (alpha 3,36) - 17,5 (alpha 2,79) mld/anno.
    # Gettito NETTO del clawback IRPEF perso (analisi/fase6_pareto_2024_lordo_netto.py):
    # lordo tagliato 31,1 mld -> netto per lo Stato 17,1 (aliquota marginale media 44,1%).
    gettito_tetto2500: float = 17.1   # NETTO. Lordo = 31,1
    tetto_temporaneo_anni: int = 0    # 0 = strutturale; >0 = versione temporanea

    # --- Scenario B: eccesso misurato ---
    # Da coorti di decorrenza (analisi/fase4_coorti.py): eccesso lordo 5,5-7,3 mld.
    # NETTO del clawback (aliquota marginale 44%): 3,1-4,1.
    gettito_eccesso_min: float = 3.1  # NETTO. Lordo = 5,5
    gettito_eccesso_max: float = 4.1  # NETTO. Lordo = 7,3
    anni_picco_eccesso: int = 25      # base piatta, poi declino lineare a zero
    anni_fine_eccesso: int = 50

    # --- profili lavoratore ---
    ral_mediana: float = 27000.0
    ral_top10: float = 40000.0
    carriera_anni: int = 40
    crescita_salario_reale: float = 0.01
    coeff_trasformazione: float = 0.052


# ----------------------------------------------------------------------
# COMPARTO 1 — LEGACY: disavanzo corrente, BTP ponte, ammortamento
# ----------------------------------------------------------------------

def comparto_legacy(a: Assumptions) -> list[dict]:
    """Profilo annuale: spesa legacy, entrate trattenute, disavanzo/avanzo,
    stock BTP con emissione a copertura del disavanzo e ammortamento
    dall'avanzo. Flussi netti di cassa (clawback IRPEF incluso)."""
    rows = []
    btp = 0.0
    n = a.orizzonte - a.anno_avvio + 1
    for i in range(n):
        anno = a.anno_avvio + i
        quota_residua = max(0.0, 1 - i / a.anni_estinzione_legacy)
        spesa_lorda = a.spesa_ivs_lorda * quota_residua
        clawback = a.clawback_irpef * quota_residua
        # entrate che restano in PAYG:
        # - contributi dei non-contributivi (misti/retributivi al lavoro), che si
        #   estinguono con la loro uscita (~stessa scala del legacy, semplificazione)
        # - gli 8 punti dei contributivi (aliquota piena - carveout)
        # - effetto TFR (meno IVS da dirottare)
        contrib_altri = (a.contributi_ivs - a.contributi_contributivi) * quota_residua
        otto_punti = a.contributi_contributivi * (1 - a.aliquota_carveout / a.aliquota_piena)
        # dopo l'estinzione del legacy il carve-out sale verso il 100%:
        # 8 punti e effetto-TFR si spengono linearmente negli anni 30-40
        rampa_uscita = max(0.0, min(1.0, 1 - (i - a.anni_estinzione_legacy) / 10))
        entrate = contrib_altri + (otto_punti + a.tfr_flusso_netto) * rampa_uscita
        saldo = entrate + clawback - spesa_lorda
        interessi = btp * a.rendimento_btp50
        if saldo < 0:
            btp += -saldo + interessi          # emetto per coprire disavanzo+cedole
        else:
            btp = max(0.0, btp + interessi - saldo)  # avanzo ammortizza
        rows.append(dict(anno=anno, spesa_legacy=spesa_lorda, entrate_payg=entrate,
                         clawback_irpef=clawback, saldo_corrente=saldo, stock_btp=btp))
    return rows


# ----------------------------------------------------------------------
# COMPARTO 2 — RICONOSCIMENTO: fondo da prelievo, exit levy, spread
# ----------------------------------------------------------------------

def gettito_prelievo(a: Assumptions, scenario: str, i: int, mid: bool = True) -> float:
    if scenario == "A":
        if a.tetto_temporaneo_anni and i >= a.tetto_temporaneo_anni:
            return 0.0
        # base calante con l'estinzione dei retributivi sopra soglia (~25 anni)
        return a.gettito_tetto2500 * max(0.0, 1 - i / 25)
    g = (a.gettito_eccesso_min + a.gettito_eccesso_max) / 2 if mid else a.gettito_eccesso_min
    if i < a.anni_picco_eccesso:
        return g
    if i < a.anni_fine_eccesso:
        return g * (1 - (i - a.anni_picco_eccesso) / (a.anni_fine_eccesso - a.anni_picco_eccesso))
    return 0.0


def comparto_riconoscimento(a: Assumptions, scenario: str) -> list[dict]:
    """Passivita che scorre sulla coda, fondo che accumula il prelievo al
    rendimento netto e si decumula pagando le rendite. La passivita e
    ridotta all'origine dall'exit levy e cresce al tasso nozionale."""
    rows = []
    passivita = a.passivita_riconoscimento * (1 - a.exit_levy)
    fondo = 0.0
    n = a.orizzonte - a.anno_avvio + 1
    # payout: rendite ~zero per i primi 15 anni, poi lineari sulla coda
    grace = 15
    for i in range(n):
        anno = a.anno_avvio + i
        prelievo = gettito_prelievo(a, scenario, i)
        fondo = fondo * (1 + a.rendimento_fondo_nom) + prelievo
        payout = 0.0
        if i >= grace and passivita > 0:
            anni_restanti = max(1, a.coda_riconoscimento - i)
            payout = passivita / anni_restanti
        passivita = max(0.0, passivita * (1 + a.tasso_nozionale_nom) - payout)
        pagato_dal_fondo = min(fondo, payout)
        fondo -= pagato_dal_fondo
        scoperto = payout - pagato_dal_fondo   # va su BTP/fiscalita
        rows.append(dict(anno=anno, gettito_prelievo=prelievo, fondo=fondo,
                         payout_riconoscimento=payout, scoperto=scoperto,
                         passivita_residua=passivita))
    return rows


# ----------------------------------------------------------------------
# COMPARTO 2 — RISTRUTTURATO: NIENTE PRE-FINANZIAMENTO
# ----------------------------------------------------------------------
# Il fondo dedicato e' morto: la passivita' (2.450) matura ~42 mld/anno di solo
# interesse nozionale, contro 17 (A) o 3-4 (B) di gettito. Copre il 7%. Nessuna
# calibrazione del prelievo chiude un buco cosi'.
# La ristrutturazione onesta: il riconoscimento NON si pre-finanzia. Si porta come
# DEBITO NOZIONALE e si paga per cassa quando scade — che e' esattamente cio' che
# il sistema NDC gia' fa oggi. Il valore del piano si sposta tutto sulla LEVA DELLO
# SPREAD: portare la passivita' al tasso nozionale invece che convertirla in BTP.
# Il prelievo smette di essere "la copertura" e diventa un contributo parziale al
# servizio del debito. Va presentato cosi'.

def comparto2_carry(a: Assumptions, scenario: str) -> dict:
    """Costo di carry del riconoscimento, e quanto ne copre il prelievo."""
    carry_nozionale = a.passivita_riconoscimento * a.tasso_nozionale_nom
    carry_btp = a.passivita_riconoscimento * a.rendimento_btp50
    risparmio_spread = carry_btp - carry_nozionale
    g0 = gettito_prelievo(a, scenario, 0)
    return dict(
        passivita=a.passivita_riconoscimento,
        carry_nozionale=carry_nozionale,
        carry_se_convertito_in_btp=carry_btp,
        risparmio_spread_annuo=risparmio_spread,
        gettito_prelievo_iniziale=g0,
        quota_carry_coperta_dal_prelievo=g0 / carry_nozionale * 100,
        onere_netto_a_carico_fiscalita=carry_nozionale - g0,
    )


# ----------------------------------------------------------------------
# PROFILI LAVORATORE (nozionale 0% reale)
# ----------------------------------------------------------------------

def profilo_lavoratore(a: Assumptions, ral: float) -> dict:
    g, anni = a.crescita_salario_reale, a.carriera_anni
    r_fondo_reale = (1 + a.rendimento_fondo_nom) / (1 + a.inflazione) - 1
    r_noz_reale = (1 + a.tasso_nozionale_nom) / (1 + a.inflazione) - 1
    finale = ral * (1 + g) ** anni
    m_payg = sum(a.aliquota_piena * ral * (1 + g) ** t * (1 + r_noz_reale) ** (anni - t)
                 for t in range(anni))
    m_fondo = sum(a.aliquota_carveout * ral * (1 + g) ** t * (1 + r_fondo_reale) ** (anni - t)
                  for t in range(anni))
    otto_punti = (a.aliquota_piena - a.aliquota_carveout)
    risparmio = otto_punti * ral * ((1 + g) ** anni - 1) / g / anni  # media annua
    return dict(ral=ral, stipendio_finale=finale,
                pensione_payg=m_payg * a.coeff_trasformazione,
                pensione_proposta=m_fondo * a.coeff_trasformazione,
                risparmio_annuo_busta=risparmio, capitale_finale=m_fondo)


# ----------------------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------------------

def tabella(rows: list[dict], anni_chiave: list[int]) -> str:
    keys = [k for k in rows[0] if k != "anno"]
    out = ["anno    " + "  ".join(f"{k[:18]:>18s}" for k in keys)]
    for r in rows:
        if r["anno"] in anni_chiave:
            out.append(f"{r['anno']}  " + "  ".join(f"{r[k]:>18,.1f}" for k in keys))
    return "\n".join(out)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=None, help="directory per i CSV")
    args = p.parse_args()
    a = Assumptions()
    anni = [2018, 2028, 2033, 2040, 2048, 2063, 2078, 2093]

    leg = comparto_legacy(a)
    print("\n=== COMPARTO 1 — LEGACY (EUR mld) ===")
    print(tabella(leg, anni))
    picco = max(r["stock_btp"] for r in leg)
    anno_picco = next(r["anno"] for r in leg if r["stock_btp"] == picco)
    print(f"\nPicco BTP: {picco:,.0f} mld nel {anno_picco} "
          f"({picco / a.pil_iniziale * 100:.0f} punti di PIL iniziale)")

    for sc, nome in [("A", "TETTO 2500 NETTI"), ("B", "ECCESSO MISURATO (mid-range)")]:
        ric = comparto_riconoscimento(a, sc)
        print(f"\n=== COMPARTO 2 — RICONOSCIMENTO, SCENARIO {sc}: {nome} ===")
        print(tabella(ric, anni))
        scoperto_tot = sum(r["scoperto"] for r in ric)
        print(f"Scoperto cumulato (su BTP/fiscalita): {scoperto_tot:,.0f} mld")

    print("\n=== PROFILI LAVORATORE (EUR reali, nozionale 0% reale) ===")
    for nome, ral in [("mediano", a.ral_mediana), ("top10", a.ral_top10)]:
        w = profilo_lavoratore(a, ral)
        print(f"{nome:8s} RAL {ral:>8,.0f} | PAYG {w['pensione_payg']:>9,.0f} | "
              f"proposta {w['pensione_proposta']:>9,.0f} "
              f"({w['pensione_proposta'] / w['pensione_payg'] - 1:+.0%}) | "
              f"in busta {w['risparmio_annuo_busta']:>7,.0f}/anno | "
              f"capitale {w['capitale_finale']:>9,.0f}")

    if args.csv:
        import csv
        d = Path(args.csv); d.mkdir(parents=True, exist_ok=True)
        for nome, rows in [("comparto_legacy", leg),
                           ("comparto2_scenarioA", comparto_riconoscimento(a, "A")),
                           ("comparto2_scenarioB", comparto_riconoscimento(a, "B"))]:
            with open(d / f"{nome}.csv", "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader(); w.writerows(rows)
        print(f"\nCSV salvati in {d}/")


if __name__ == "__main__":
    main()
