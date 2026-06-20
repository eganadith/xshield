#!/usr/bin/env python3
"""Convert live-site images to WebP, update references, remove unused assets."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

LIVE_HTML = [
    ROOT / "index.html",
    ROOT / "about.html",
    ROOT / "service.html",
    ROOT / "contact.html",
    ROOT / "_snippets/inquiry-page.template.html",
]

LIVE_SCSS = list((ROOT / "assets/sass").rglob("*.scss"))
LIVE_JSON = [ROOT / "assets/data/services-inquiry.json"]

RASTER_EXT = {".jpg", ".jpeg", ".png", ".gif"}
KEEP_SVG = True
VIDEO_FILES = {
    "assets/images/0619.mp4",
    "assets/images/0619.webm",
}

REF_PATTERNS = [
    re.compile(r"""((?:\.\./)?assets/(?:images|logo)/[^\s"'<>]+?)\.(jpg|jpeg|png|gif)""", re.I),
    re.compile(r"""url\((["']?)([^"')]+?)\.(jpg|jpeg|png|gif)\1\)""", re.I),
]


def collect_referenced_paths() -> set[str]:
    refs: set[str] = set()
    sources = LIVE_HTML + LIVE_SCSS + LIVE_JSON

    for path in sources:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")

        for m in re.finditer(r"""["']((?:\.\./)?assets/(?:images|logo)/[^"']+)["']""", text, re.I):
            refs.add(normalize_ref(m.group(1)))

        for m in re.finditer(r"""url\(["']?([^"')]+)["']?\)""", text, re.I):
            p = m.group(1)
            if p.startswith("../images/"):
                refs.add("assets/images/" + p[len("../images/"):])
            elif "assets/" in p:
                idx = p.index("assets/")
                refs.add(normalize_ref(p[idx:]))

    data = json.loads((ROOT / "assets/data/services-inquiry.json").read_text(encoding="utf-8"))
    for item in data:
        refs.add(normalize_ref(item["image"]))

    refs.update(VIDEO_FILES)
    return refs


def normalize_ref(ref: str) -> str:
    ref = ref.split("?")[0]
    return ref.replace("\\", "/").lstrip("./").replace("../", "")


def to_webp_path(path: str) -> str:
    p = Path(path)
    return str(p.with_suffix(".webp")).replace("\\", "/")


def convert_to_webp(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        img.save(dst, "WEBP", quality=82, method=6)


def replace_in_file(path: Path, mapping: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    refs = collect_referenced_paths()

    raster_refs = sorted(
        r for r in refs if Path(r).suffix.lower() in RASTER_EXT and (ROOT / r).exists()
    )
    svg_refs = sorted(r for r in refs if Path(r).suffix.lower() == ".svg" and (ROOT / r).exists())
    missing = sorted(r for r in refs if not (ROOT / r).exists() and not r.endswith((".mp4", ".webm")))

    print(f"Referenced assets: {len(refs)}")
    print(f"Raster to convert: {len(raster_refs)}")
    print(f"SVG kept: {len(svg_refs)}")
    if missing:
        print(f"WARNING missing refs: {missing}")

    mapping: dict[str, str] = {}
    converted = 0
    for ref in raster_refs:
        src = ROOT / ref
        webp_ref = to_webp_path(ref)
        dst = ROOT / webp_ref
        convert_to_webp(src, dst)
        mapping[ref] = webp_ref
        converted += 1
        print(f"  ✓ {ref} → {webp_ref}")

    # Update source files
    update_paths = LIVE_HTML + LIVE_JSON + LIVE_SCSS
    updated_files = 0
    for path in update_paths:
        # Build replacements including ../ prefixed paths
        file_mapping: dict[str, str] = {}
        for old, new in mapping.items():
            file_mapping[old] = new
            file_mapping[f"../{old}"] = f"../{new}"
            old_name = Path(old).name
            new_name = Path(new).name
            file_mapping[old_name] = new_name
        if replace_in_file(path, file_mapping):
            updated_files += 1
            print(f"  updated {path.relative_to(ROOT)}")

    # favicon mime type
    for html in LIVE_HTML:
        text = html.read_text(encoding="utf-8")
        new_text = text.replace('type="image/png" href="assets/logo/favicon.webp"', 'type="image/webp" href="assets/logo/favicon.webp"')
        new_text = new_text.replace('type="image/png" href="../assets/logo/favicon.webp"', 'type="image/webp" href="../assets/logo/favicon.webp"')
        if new_text != text:
            html.write_text(new_text, encoding="utf-8")

    # Remove original raster files that were converted
    for ref in raster_refs:
        (ROOT / ref).unlink(missing_ok=True)

    # Delete unreferenced files under assets/images and assets/logo
    keep_paths = set(mapping.values()) | set(svg_refs) | VIDEO_FILES
    # Also keep converted webp keys values and any svg from refs
    for ref in refs:
        if ref.endswith(".svg") or ref.endswith((".mp4", ".webm")):
            keep_paths.add(ref)

    deleted = 0
    for base in [ASSETS / "images", ASSETS / "logo"]:
        if not base.exists():
            continue
        for f in sorted(base.rglob("*")):
            if not f.is_file():
                continue
            rel = str(f.relative_to(ROOT)).replace("\\", "/")
            if rel in keep_paths:
                continue
            if f.suffix.lower() in RASTER_EXT | {".webp"}:
                # delete orphan raster/webp not in keep set
                f.unlink()
                deleted += 1
                print(f"  deleted {rel}")
            elif f.name == ".DS_Store":
                f.unlink()

    # Remove empty directories
    for base in [ASSETS / "images", ASSETS / "logo"]:
        for d in sorted(base.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
                print(f"  removed empty dir {d.relative_to(ROOT)}")

    print(f"\nConverted: {converted} images")
    print(f"Updated: {updated_files} source files")
    print(f"Deleted: {deleted} unused raster/webp files")


if __name__ == "__main__":
    main()
