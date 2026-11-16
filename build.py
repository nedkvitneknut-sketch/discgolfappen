"""Byggjer Discbaggen frå kjeldefila.

Bruk:  python build.py            (byggjer discbag.html og discbag-demo.html)
       python build.py --bilete   (lagar også bilete/innebygde-bilete.json på nytt frå .webp-filene, krev Pillow)
"""
import base64, io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src.html"
IMG_DIR = ROOT / "bilete"
IMG_JSON = IMG_DIR / "innebygde-bilete.json"
DISCS = ["aviar", "tl", "beast"]  # filnamn i bilete/ og nøklar i appen


def lag_bilete():
    from PIL import Image, ImageStat
    out = {}
    for key in DISCS:
        im = Image.open(IMG_DIR / f"{key}.webp").convert("RGB")
        w, h = im.size
        s = min(w, h)
        i = int(s * 0.012)  # skjer bort den kvite kanten rundt disken
        im = im.crop((i, i, s - i, s - i)).resize((512, 512), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=86)
        rim = [int(x) for x in ImageStat.Stat(im.crop((20, 240, 50, 270))).mean]
        out[key] = {
            "src": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
            "rim": "#%02x%02x%02x" % tuple(rim),
        }
        print(f"  {key}: {len(buf.getvalue()) // 1024} KB, kantfarge {out[key]['rim']}")
    IMG_JSON.write_text(json.dumps(out), encoding="utf-8")


def bygg():
    src = SRC.read_text(encoding="utf-8")
    imgs = json.loads(IMG_JSON.read_text(encoding="utf-8"))
    b64 = lambda f: "data:image/png;base64," + base64.b64encode((IMG_DIR / f).read_bytes()).decode()
    app = (src.replace("__IMGS__", json.dumps(imgs))
              .replace("__ICON180__", b64("ikon-180.png"))
              .replace("__ICON32__", b64("ikon-32.png")))
    (ROOT / "discbag.html").write_text(app, encoding="utf-8")

    meta = '<meta name="claude:viewport-fit-sides" content="cover">'
    demo = (app.replace(meta, meta + "\n<script>window.DISC_DEMO=100</script>", 1)
               .replace("<title>Discbaggen</title>", "<title>Discbaggen demo</title>", 1))
    (ROOT / "discbag-demo.html").write_text(demo, encoding="utf-8")

    # GitHub Pages: frittståande sider med eige dokumentskal
    head = ('<!doctype html>\n<html lang="nn">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<meta name="theme-color" content="#f2f2f7">\n'
            '<meta name="apple-mobile-web-app-capable" content="yes">\n'
            '<meta name="apple-mobile-web-app-title" content="Discbaggen">\n'
            '<link rel="manifest" href="manifest.webmanifest">\n'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
    foot = '\n</body>\n</html>\n'
    for f in ("ikon-180.png", "ikon-512.png"):
        (ROOT / f).write_bytes((IMG_DIR / f).read_bytes())
    (ROOT / "manifest.webmanifest").write_text(json.dumps({
        "name": "Discbaggen", "short_name": "Discbaggen", "start_url": "./", "display": "standalone",
        "background_color": "#f2f2f7", "theme_color": "#f2f2f7",
        "icons": [{"src": "ikon-180.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "ikon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "index.html").write_text(head + app + foot, encoding="utf-8")
    (ROOT / "demo.html").write_text(head + demo + foot, encoding="utf-8")
    print("Bygd: discbag.html, discbag-demo.html, index.html og demo.html")


if __name__ == "__main__":
    if "--bilete" in sys.argv:
        print("Lagar innebygde bilete …")
        lag_bilete()
    bygg()
