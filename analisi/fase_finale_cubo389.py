"""
FASE FINALE — punti 1 e 2, dal cubo INPS 389 "Pensioni per regime di liquidazione".

L'API si sblocca con un campo non documentato: "zip": true nel payload di
getDatiOsservatorio. Senza, il server risponde "The input is not a valid Base-64
string" — errore fuorviante, che non c'entra con l'encoding dei filtri.

PUNTO 1: quota retributivo+misto sulla massa pensionistica, ultimo anno (sostituisce
         il 98,9% calcolato su dati 2017).
PUNTO 2: cross-check del bordo basso dello Scenario B, confrontando gli importi medi
         delle coorti di decorrenza VECCHIE (dove vive lo stock legacy) con quelle
         RECENTI usate nella griglia del punto 4.
         FILTRO CATEGORIA = VECCHIAIA: senza, il confronto e' contaminato dal mix
         (le "retributive" con decorrenza recente sono in larga parte REVERSIONI,
         non dirette — un lavoratore non puo' maturare una diretta retributiva pura
         con decorrenza 2016).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path
import ssl
import urllib.request

OUT = Path(__file__).resolve().parent / "output"
B = "https://servizi2.inps.it/servizi/osservatoristatistici/api"
CTX = ssl.create_default_context()


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        B + path, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0",
                 "Accept": "application/json"})
    raw = urllib.request.urlopen(req, context=CTX, timeout=300).read()
    if raw[:2] == bytes([0x1F, 0x8B]):
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def struttura(oid: str) -> dict:
    return post("/getStrutturaOsservatorio/", {"id_osservatorio": oid, "language": "it"})


def query(oid: str, s: dict, rows: list[str], cols: list[str],
          meas: list[tuple[str, str]], filters: dict[str, list[str]] | None = None) -> dict:
    d = s["definition"]
    hier = lambda l: next(h for h in d["Hierarchy"] if h["label"] == l)
    fld = lambda i: next(f for f in d["fields"] if f["id"] == i)
    p = {"id_osservatorio": oid, "nome_osservatorio": s["nome_osservatorio"], "language": "",
         "totalRow": True, "totalColumn": True, "subtotalRow": True, "subtotalColumn": True,
         "zip": True,   # <-- IL CAMPO CHE SBLOCCA TUTTO
         "selections": {"rows": [], "cols": [], "measures": [], "filters": []}}
    for n, l in enumerate(rows):
        h = hier(l)
        p["selections"]["rows"].append({
            "id": h["Name"], "label": h["Name"], "order": n + 1,
            "aggregate": fld(h["Component"][0]["id"])["aggregate"], "expand": "", "hide": False})
    for n, l in enumerate(cols):
        h = hier(l)
        p["selections"]["cols"].append({
            "id": h["Name"], "label": h["Name"], "order": n + 1,
            "aggregate": fld(h["Component"][0]["id"])["aggregate"], "expand": "", "hide": False})
    for mid, st in meas:
        f = fld(mid)
        p["selections"]["measures"].append({
            "id": mid, "logicalName": f["logicalName"], "label": f["label"],
            "statistic": st, "format": f.get("format", ""), "order": 1})
    for lab, vals in (filters or {}).items():
        h = hier(lab)
        p["selections"]["filters"].append({
            "id": h["Component"][0]["id"], "label": h["Name"], "values": vals})
    return post("/getDatiOsservatorio/", p)


def main() -> None:
    s = struttura("389")
    d = s["definition"]
    print("dimensioni:", [h["label"] for h in d["Hierarchy"]])
    print("misure    :", [(f["id"], f["label"]) for f in d["fields"] if f.get("isMeasure")])
    Path(OUT / "cubo389_struttura.json").write_text(
        json.dumps(s, ensure_ascii=False)[:2000], encoding="utf-8")


if __name__ == "__main__":
    main()


def estrai() -> None:
    s = struttura("389")
    d = s["definition"]
    cat = next(h for h in d["Hierarchy"] if h["label"] == "Categoria")
    print("valori Categoria:", [v for v in cat.get("values", [])][:6])
