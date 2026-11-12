"""
NORDWAY — Brand assets : reconstruit la bibliothèque à partir du dossier ../ASSETS.

À relancer après avoir ajouté, renommé ou retiré un fichier dans ASSETS :
    python build_assets.py          (depuis ce dossier, Pillow requis : pip install pillow)

Ce que le script écrit (les fichiers d'ASSETS ne sont jamais modifiés) :
  · web/<id>.webp     image 1080 px de large, légère : vignettes, aperçu, Image matrice
  · thumb/<id>.webp   image 540 px pour la grille
  · assets.js         le manifeste lu par index.html (un script, pas du JSON : la page
                      s'ouvre aussi en double-cliquant, sans serveur)
  · ../image-matrice/brand-images.json   la liste lue par le bouton « Brand images »

Les rubriques suivent les dossiers d'ASSETS, dans l'ordre de FOLDERS ci-dessous.
"""
from pathlib import Path
import json, re, unicodedata

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "ASSETS"

# (dossier dans ASSETS, identifiant court, nom affiché, description)
FOLDERS = [
    ("LOGO", "logo", "Logo",
     "Wordmark and seal. Keep a clear space equal to the height of the ® around the wordmark."),
    ("ASSETS/ASSETS CAMPAGNE", "campagne", "Campaign",
     "Four image families: Relief, Signal, Ritual. 4:5, 1080 × 1350."),
    ("ASSETS/ASSETS GRAPHICS", "graphics", "Graphics",
     "Coordinates band, marker grid, seal plan, Climber sign."),
    ("ASSETS/ASSETS PRODUCT", "product", "Product",
     "X-ray product shots on Glacier, Granite and Night backgrounds."),
    ("ASSETS/OBJECT", "object", "Object",
     "Printed objects: the Climber sign in relief."),
    ("ASSETS/vidéo", "video", "Motion",
     "Short films, 8 to 12 s. The logo only appears at the end, in Signal green."),
    ("TYPO", "typo", "Type",
     "Two families, one weight. Nord Pro carries the story, Roboto Mono carries the data."),
]
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".webm"}
FONT_EXT = {".ttf", ".otf", ".woff", ".woff2"}


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def natural(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def save_webp(img, dest, width, quality):
    im = img.copy()
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    has_alpha = im.mode in ("RGBA", "LA") and im.getextrema()[-1][0] < 255
    im = im.convert("RGBA" if has_alpha else "RGB")
    im.save(dest, "WEBP", quality=quality, method=6)
    return has_alpha


def main():
    (HERE / "web").mkdir(exist_ok=True)
    (HERE / "thumb").mkdir(exist_ok=True)
    groups, matrice = [], []
    for folder, gid, label, desc in FOLDERS:
        d = SRC / folder
        if not d.is_dir():
            continue
        items = []
        for f in sorted((p for p in d.iterdir() if p.is_file()), key=lambda p: natural(p.name)):
            ext = f.suffix.lower()
            rel = "../ASSETS/" + f.relative_to(SRC).as_posix()
            item = {"name": f.stem, "file": f.name, "src": rel, "ext": ext[1:].upper(), "bytes": f.stat().st_size}
            if ext in IMAGE_EXT:
                aid = f"{gid}-{slug(f.stem)}"
                with Image.open(f) as img:
                    item.update(kind="image", id=aid, w=img.width, h=img.height,
                                web=f"web/{aid}.webp", thumb=f"thumb/{aid}.webp")
                    item["alpha"] = save_webp(img, HERE / item["web"], 1080, 84)
                    save_webp(img, HERE / item["thumb"], 540, 78)
                # le poster d'une vidéo n'est pas une image de marque pour la Matrice
                if gid in ("campagne", "graphics", "product", "object"):
                    matrice.append(f"{aid}.webp")
            elif ext in VIDEO_EXT:
                item.update(kind="video", id=f"{gid}-{slug(f.stem)}")
            elif ext in FONT_EXT:
                item.update(kind="font", id=f"{gid}-{slug(f.stem)}")
            else:
                continue
            items.append(item)
        groups.append({"id": gid, "label": label, "folder": folder, "desc": desc, "items": items})
        print(f"{label:10} {len(items):3} files")

    js = ("// Généré par build_assets.py — ne pas modifier à la main, relancer le script.\n"
          "window.NORDWAY_ASSETS = " + json.dumps(groups, ensure_ascii=False, indent=1) + ";\n")
    (HERE / "assets.js").write_text(js, encoding="utf-8")
    (ROOT / "image-matrice" / "brand-images.json").write_text(json.dumps(matrice, indent=1), encoding="utf-8")
    print(f"assets.js written, {len(matrice)} images for Image matrice")


if __name__ == "__main__":
    main()
