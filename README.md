# Discbaggen

Mobilapp (éi HTML-side) for å halde styr på frisbeegolf-discane i baggen: 3D-visning av kvar disc, forklarte flygetal, simulert flygelinje og samanlikning av discar.

## Nettside (GitHub Pages)

- Appen: https://nedkvitneknut-sketch.github.io/discgolfappen/
- Demo: https://nedkvitneknut-sketch.github.io/discgolfappen/demo.html

På nettsida blir discane lagra i nettlesaren (localStorage), så kvar eining har sin eigen bag.

## Publiserte sider på claude.ai (private)

- Appen: https://claude.ai/artifact/3nsbnu9AQ5c835kWZyKwR8
- Demo med 100 oppdikta discar: https://claude.ai/artifact/6GjfCDVyNCpKFwGrGB23PK

Discane i appen er lagra i artifact-databasen (samlinga `discs`), ikkje i desse filene.

## Filer

| Fil | Kva |
| --- | --- |
| `src.html` | Kjeldefila. Alle endringar blir gjorde her. |
| `discbag.html` | Ferdig bygd app, klar til publisering. |
| `discbag-demo.html` | Same app i demomodus med 100 dummy-discar. |
| `index.html`, `demo.html` | Same sider som frittståande nettsider for GitHub Pages. |
| `build.py` | Byggjer alle sidene frå `src.html`. |
| `bilete/*.webp` | Originalbileta av Aviar, TL og Beast. |
| `bilete/innebygde-bilete.json` | Bileta beskorne og komprimerte, slik dei blir bygde inn i appen. |

## Bygg

```bash
python build.py
```

Har du byta eller lagt til eit startbilete i `bilete/`, køyr `python build.py --bilete` (krev Pillow).

Opnar du `discbag.html` direkte i nettlesaren, køyrer appen i lokal modus og lagrar berre i den nettlesaren.
