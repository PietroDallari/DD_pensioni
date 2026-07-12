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
    # ============ CONTRIBUTI IVS — DECOMPOSIZIONE UFFICIALE DEGLI SGRAVI ============
    # INPS PUBBLICA la decomposizione dei 33,5 mld di sgravi: non serviva ricostruirla.
    # Fonte: Rendiconto generale 2024, Allegato 24 (GIAS), ALLEGATO 15 "Poste correttive
    # e compensative delle entrate correnti", pp.164-167. Totale 33.537.246.069,82 —
    # coincide esattamente con la Nota integrativa p.106.
    #
    # Limite superiore IVS (Nota integr. Tab.19 p.49: 136,963 uniemens pensionistici
    # + 106,496 non-uniemens contato tutto come IVS) = 243,459 mld, LORDO sgravi.
    #
    # Decomposizione dei 33,537:
    #   IVS CERTO     18,374 (54,8%) — cuneo lavoratore 17,206 + lavoratrici madri
    #                                  1,100 + coltivatori under40 0,067 + altri
    #   NON-IVS CERTO  8,987 (26,8%) — prestazioni temporanee (L.266/2005, L.388/2000,
    #                                  L.296/2006), Fondo garanzia TFR, riduzione CIG
    #   MISTA          6,175 (18,4%) — Decontribuzione Sud 3,748, esonero giovani 1,877,
    #                                  donne 0,102, marittimi 0,313... esoneri sui
    #                                  contributi datoriali COMPLESSIVI: la ripartizione
    #                                  IVS/non-IVS al loro interno NON e' pubblicata.
    #   => quota IVS degli sgravi: 54,8% (mista=0) - 73,2% (mista=100%)
    #
    # CORREZIONE IMPORTANTE: l'esonero cuneo a CONSUNTIVO INPS vale 17,206 mld, non i
    # 13,535 della relazione tecnica LdB 2024. La RT e' una PREVISIONE ed e' costruita
    # su un perimetro diverso. Per il conto contributivo vale il consuntivo.
    #
    # VINTAGE 2024 (consuntivo)  : 243,459 - [18,4 ... 24,5] = 218,9 - 225,1
    # VINTAGE 2025+ (STRUTTURALE): l'esonero cuneo (17,206, IVS al 100%) e' MIGRATO AL
    #   FISCO (L.207/2024 c.4-9: somma esente + detrazione IRPEF; la RT — Camera
    #   A.C.2112-bis pp.13-17 — espone solo minori entrate TRIBUTARIE e maggiori spese
    #   correnti, NESSUNA voce contributiva). Quei 17,2 mld tornano contributi versati.
    #   => 243,459 - [1,2 ... 7,3] = 236,1 - 242,3
    #
    # SOTTOCONTRIBUZIONI (Allegato 16, 7.332 mln): NON vanno sottratte. Sarebbe un
    # DOPPIO CONTEGGIO. Sgravi e sottocontribuzioni sono contabilizzati in modo diverso:
    #   - SGRAVI: l'aliquota di COMPUTO resta al 33% (il diritto pensionistico e' pieno,
    #     lo Stato rimborsa). INPS iscrive il contributo PIENO nelle entrate contributive
    #     e poi corregge con le poste correttive -> sono DENTRO i 284,047 -> si sottraggono.
    #   - SOTTOCONTRIBUZIONI: l'aliquota e' davvero RIDOTTA. Si iscrive il contributo
    #     ridotto, e la GIAS integra con un TRASFERIMENTO separato -> NON sono dentro i
    #     284,047 -> NON si sottraggono.
    # PROVA nel bilancio del FPLD (Gestione n.2):
    #   aliquote contributive          138.688 mln  <- entrate contributive
    #   trasferimenti da GIAS            5.816 mln  <- voce SEPARATA, di cui 4.998 di
    #                                                  "copertura mancato gettito contributivo"
    #   Allegato 16, quota FPLD          4.996,3 mln  -> COINCIDE con i 4.998.
    # Le entrate contributive sono quindi gia' al netto delle aliquote ridotte: INPS
    # scrive che i trasferimenti sono "ad INTEGRAZIONE DI MINORI ENTRATE per riduzione
    # di aliquote contributive" — minori entrate, cioe' gia' ridotte.
    #
    # Punto di rottura del ponte: 212,2 mld. Tutto il vintage 2025+ e' 24-30 mld sopra.
    contributi_ivs: float = 237.3     # vintage 2025+, centrale. Intervallo 236,1-242,3.
    contributi_contributivi: float = 99.0   # quota dirottabile, scalata sulla base
    aliquota_piena: float = 0.33
    aliquota_carveout: float = 0.25   # quanto dirottano; 8 punti restano in PAYG
    tfr_flusso_netto: float = 24.0    # 30 lordi - 6 Fondo Tesoreria perso

    # --- CLAUSOLA DI SALVAGUARDIA (punto 3) ---
    # L'autoammortamento del ponte NON e' una proprieta' del piano: e' condizionato agli
    # IVS effettivi (punto di rottura ~212 mld, dentro l'intervallo di incertezza 210-223).
    # La salvaguardia rende l'esito robusto invece che sperato: se lo stock BTP sfora la
    # traiettoria di rientro, il carve-out RALLENTA temporaneamente (25% -> 27%), cioe'
    # restano piu' punti in PAYG, finche' il saldo del Comparto 1 rientra.
    # NOTA SULLA DIREZIONE. Le istruzioni dicevano "carve-out 25% -> 27%". Nel modello
    # aliquota_carveout e' QUANTO SI DIROTTA ai fondi (25%, e i restanti 8 punti su 33
    # restano in PAYG). Portarla a 27% dirotterebbe DI PIU', lasciando solo 6 punti in
    # PAYG: peggiorerebbe il disavanzo invece di correggerlo (verificato: a IVS=205 lo
    # stock finale passava da 1.395 a 2.233). La direzione voluta e' l'opposta:
    # RIDURRE il carve-out a 23%, cosi' restano 10 punti in PAYG invece di 8.
    # Costo per il lavoratore: 2 punti in meno versati al proprio fondo, per gli anni
    # di attivazione. E' il prezzo esplicito della garanzia.
    salvaguardia_attiva: bool = False
    salv_soglia_stock_pil: float = 0.15   # attiva se stock BTP > 15% del PIL iniziale
    salv_carveout_ridotto: float = 0.23   # si dirotta MENO: 10 punti restano in PAYG
    salv_isteresi_pil: float = 0.10       # disattiva sotto il 10%: evita l'on/off

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
    # RICALIBRATO su serie salariali storiche vere (analisi/scenarioB_serie_salariali.py).
    # La stima precedente (5,5-7,3 lordo / 3,1-4,1 netto) era SBAGLIATA: il calcolatore
    # assumeva salari a +2% NOMINALE fisso su carriere 1970-2002, quando l'inflazione era
    # ~10%/anno e i tassi di capitalizzazione 15-22%. Montante gonfiato -> eccesso ~zero.
    #
    # Sentiero salariale ora ancorato ad AMECO (Commissione UE), ITA.1.0.0.0.HWCDW
    # "Nominal compensation per employee, total economy", annuale dal 1960.
    # Crescita nominale: 1970-90 = 14,6%/anno | 1990-2010 = 3,1% | 2010-24 = 1,3%.
    #
    # ANCORA DI VALIDAZIONE SUPERATA: su carriera piena (40 anni, uscita a 65) il metodo
    # produce un tasso di sostituzione contributivo del 75,6% (atteso 60-75%); a 38 anni
    # e 63 anni, 63,2%. Il metodo non e' rotto.
    # Il 41% del pensionato uscito a 58 anni con 33 di contributi e' quindi il RISULTATO,
    # non un bug: 66% erogato contro 41% finanziato. E' il regalo retributivo.
    #
    # DUE IPOTESI-CHIAVE, dichiarate:
    #   1. PREMIO DI CARRIERA (0/+1/+2 punti sopra l'aggregato). ATTENZIONE ALLA DIREZIONE:
    #      poiche' il controfattuale e' ancorato alla RETRIBUZIONE FINALE (che l'inversione
    #      retributiva ci da'), un premio piu' alto implica salari iniziali PIU' BASSI ->
    #      montante piu' basso -> eccesso PIU' ALTO. Il premio quindi ALZA l'eccesso, non
    #      lo abbassa. Premio 0 e' il bordo BASSO.
    #   2. TASSI DI CAPITALIZZAZIONE PRE-1996: sono un controfattuale COSTRUITO dai livelli
    #      di PIL nominale, non un dato osservato (il contributivo nasce nel 1996).
    #
    # Prelievo = min(eccesso, pensione - franchigia di 2.500 netti garantiti).
    # Sotto ~5.700-7.900 EUR/mese morde la FRANCHIGIA; sopra, morde l'ECCESSO.
    gettito_eccesso_min: float = 13.2  # NETTO (premio 0). Lordo 24,0
    gettito_eccesso_max: float = 15.5  # NETTO (premio +2). Lordo 28,2
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
    allarme = False          # stato della salvaguardia (con isteresi)
    anni_salvaguardia = 0
    n = a.orizzonte - a.anno_avvio + 1
    for i in range(n):
        anno = a.anno_avvio + i
        quota_residua = max(0.0, 1 - i / a.anni_estinzione_legacy)
        spesa_lorda = a.spesa_ivs_lorda * quota_residua
        clawback = a.clawback_irpef * quota_residua

        # --- salvaguardia: feedback annuale con isteresi ---
        carveout = a.aliquota_carveout
        if a.salvaguardia_attiva:
            soglia_on = a.salv_soglia_stock_pil * a.pil_iniziale
            soglia_off = a.salv_isteresi_pil * a.pil_iniziale
            if not allarme and btp > soglia_on:
                allarme = True
            elif allarme and btp < soglia_off:
                allarme = False
            if allarme:
                carveout = a.salv_carveout_ridotto
                anni_salvaguardia += 1
        # entrate che restano in PAYG:
        # - contributi dei non-contributivi (misti/retributivi al lavoro), che si
        #   estinguono con la loro uscita (~stessa scala del legacy, semplificazione)
        # - gli 8 punti dei contributivi (aliquota piena - carveout)
        # - effetto TFR (meno IVS da dirottare)
        contrib_altri = (a.contributi_ivs - a.contributi_contributivi) * quota_residua
        otto_punti = a.contributi_contributivi * (1 - carveout / a.aliquota_piena)
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
                         clawback_irpef=clawback, saldo_corrente=saldo, stock_btp=btp,
                         carveout=carveout, salvaguardia=int(allarme)))
    return rows   # anni di salvaguardia: sum(r["salvaguardia"] for r in rows)


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
