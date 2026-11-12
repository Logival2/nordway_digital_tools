# NORDWAY Digital tools

Five browser tools from *Digital tools* (MULTI-DIGITAL TOOLS), restyled to the NORDWAY identity, plus the brand library. The UX of each tool is unchanged.

| N° | Folder | Origin |
|----|--------|--------|
| 01 | `image-matrice/` | tools_Matrice_images_002 |
| 02 | `cairn-generator/` | tools_kinetic_v2_000 |
| 03 | `gradient-body/` | tools_gradient_body_001 |
| 04 | `mockup/` | tools_mockup_000 |
| 05 | `card-ring/` | tools_DA_cercle_002 |
| 06 | `brand-assets/` | new: library of the files in `ASSETS/` |

`index.html` at the root is the entry point: the seal works as the navigation (six points, six tools).

## Run

Some tools load files with `fetch` (Image matrice: brand images and Mont Blanc terrain), so serve the folder:

```
python -m http.server 8000
```

then open http://localhost:8000/.

## Shared files

- `ui/nordway.css`, `ui/nordway.js`: the tools' interface (from `ui_001`, same selectors). Paper / Ink, square controls, 2 px and 1 px rules, Nord Pro + Roboto Mono, the Signal green only on the export point, keyboard focus and the hand skeleton.
- `ui/site.css`: the scrolling pages (home, Brand assets).
- `ui/wordmark.png`, `ui/sceau.png`: black-on-transparent marks, coloured with CSS masks.
- `fonts/`: `Nord_pro_regular` (= MingLiU Prop), `Nord_pro_mono` (= MingLiU-01), `Nord_pro_SemiBold`, Roboto Mono.
- `apercu/`: 4:5 previews used by the home page.

## Adding brand files

Put the file in the matching `ASSETS/` folder, then:

```
cd brand-assets
python build_assets.py
```

This rewrites the web copies (`web/`, `thumb/`), the manifest `assets.js` and `image-matrice/brand-images.json` (the **Brand images** button). The originals in `ASSETS/` are never changed.
