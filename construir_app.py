"""Construye la app «Hànzì de Pablo» a partir del Excel «Vocabulario Chino.xlsx».

Uso:  python3 construir_app.py "Vocabulario Chino.xlsx"
Genera, en la carpeta «app/»:
  - index.html      → la app completa, lista para subir a cualquier web (GitHub Pages, Netlify…)
  - strokes/*.json  → los trazos de los caracteres (para el modo Escribir)
  - hanzi-writer.min.js
y además «artifact_body.html» (la versión para publicar como Artifact de Claude).

Necesita: Python 3 con openpyxl (pip install openpyxl). Internet solo si hay caracteres nuevos
sin trazos (los descarga de cdn.jsdelivr.net/npm/hanzi-writer-data@2.0.1).
"""
import hashlib, json, os, re, shutil, sys, urllib.request
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = {"Verbo": "Verbos", "Sustantivo": "Sustantivos", "Adjetivo": "Adjetivos", "Adverbio / expresión": "Adverbios",
       "Pronombre": "Pronombres", "Clasificador": "Clasificadores", "Frase": "Oraciones", "Frase generada": "Generadas"}
CJK = re.compile(r"[㐀-鿿]")

def level(txt):
    txt = (txt or "").strip()
    if txt == "HSK 7-9": return 7
    m = re.match(r"HSK (\d)", txt)
    return int(m.group(1)) if m else 0

def lesson(txt):
    m = re.search(r"Lecci[oó]n (\d+)", txt or "")
    return f"L{m.group(1)}" if m else ""

def read_excel(path):
    ws = load_workbook(path, read_only=True)["Vocabulario"]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h or "").strip() for h in rows[0]]
    col = {name: head.index(name) for name in head}
    cards, seen = [], set()
    for r in rows[1:]:
        g = lambda k: (str(r[col[k]]).strip() if k in col and r[col[k]] is not None else "")
        h, es = g("Hànzì"), g("Español")
        if not h or not es: continue
        cat = CAT.get(g("Categoría"), "Adverbios")
        cid = g("ID (no tocar)") or hashlib.md5(f"{cat}|{h}|{es}".encode()).hexdigest()[:8]
        if cid in seen: continue
        seen.add(cid)
        cards.append([cid, cat, h, g("Pinyin"), es, level(g("Nivel HSK")), lesson(g("Lección")),
                      1 if g("Nivel: cómo se asignó") == "Lista oficial" else 0,
                      g("Tipo") if "Tipo" in col else ""])
    return cards

def build_strokes(cards, out_dir):
    """Carga los trazos existentes (strokes/ junto a este script) y descarga los que falten."""
    src = os.path.join(HERE, "app", "strokes")
    known = {}
    if os.path.isdir(src):
        for f in os.listdir(src):
            known.update(json.load(open(os.path.join(src, f), encoding="utf-8")))
    chars = sorted({ch for c in cards for ch in c[2] if CJK.match(ch)})
    for ch in chars:
        if ch in known: continue
        url = "https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0.1/" + urllib.request.quote(ch) + ".json"
        try:
            d = json.load(urllib.request.urlopen(url, timeout=20))
            known[ch] = {"strokes": d["strokes"], "medians": d["medians"]}
            print("  trazos descargados:", ch)
        except Exception as e:
            print("  sin trazos para", ch, "→ en modo Escribir usará la pizarra libre")
    chunks = {i: {} for i in range(64)}
    have = []
    for ch in chars:
        if ch in known:
            chunks[ord(ch) % 64][ch] = known[ch]; have.append(ch)
    os.makedirs(out_dir, exist_ok=True)
    for i, c in chunks.items():
        with open(os.path.join(out_dir, f"s{i:x}.json"), "w", encoding="utf-8") as fh:
            json.dump(c, fh, ensure_ascii=False, separators=(",", ":"))
    return "".join(have)

def main():
    xlsx = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "Vocabulario Chino.xlsx")
    cards = read_excel(xlsx)
    lessons = sorted({c[6] for c in cards if c[6]}, key=lambda l: int(l[1:]))
    tmp = os.path.join(HERE, "_strokes_nuevos")
    stroke_chars = build_strokes(cards, tmp)
    tpl = open(os.path.join(HERE, "plantilla.html"), encoding="utf-8").read()
    body = (tpl.replace("__CARDS__", json.dumps(cards, ensure_ascii=False, separators=(",", ":")))
               .replace("__STROKECHARS__", json.dumps(stroke_chars, ensure_ascii=False))
               .replace("__LESSONS__", json.dumps({l: "Lección " + l[1:] for l in lessons}, ensure_ascii=False)))
    open(os.path.join(HERE, "artifact_body.html"), "w", encoding="utf-8").write(body)
    app = os.path.join(HERE, "app")
    if os.path.isdir(os.path.join(app, "strokes")): shutil.rmtree(os.path.join(app, "strokes"))
    os.makedirs(app, exist_ok=True)
    shutil.move(tmp, os.path.join(app, "strokes"))
    standalone = body.replace("https://cdn.jsdelivr.net/npm/hanzi-writer@3.5.0/dist/hanzi-writer.min.js", "hanzi-writer.min.js")
    page = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<link rel="manifest" href="manifest.json"><link rel="apple-touch-icon" href="icon-180.png">'
            '<meta name="theme-color" content="#237A64"><meta name="apple-mobile-web-app-capable" content="yes">'
            '<style>[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0}</style>'
            '</head><body>' + standalone + '</body></html>')
    open(os.path.join(app, "index.html"), "w", encoding="utf-8").write(page)
    print(f"Listo: {len(cards)} tarjetas, {len(lessons)} lecciones, {len(stroke_chars)} caracteres con trazos.")
    print("Sube la carpeta «app» a tu web, o publica «artifact_body.html» como Artifact.")

if __name__ == "__main__":
    main()
