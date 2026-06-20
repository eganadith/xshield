#!/usr/bin/env python3
"""Remove em dashes (—) from site HTML and snippets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def remove_em_dashes(text: str) -> str:
    # Title / meta: use pipe instead of dash
    text = text.replace("XShield — To Protect", "XShield | To Protect")
    text = text.replace("To Protect and Prevent —", "To Protect and Prevent")
    text = text.replace("To Protect and Prevent <span>— ", "To Protect and Prevent <span>")
    # Footer / hours (match existing middle-dot rhythm)
    text = text.replace("Free Inspection — ", "Free Inspection · ")
    text = text.replace("Open 24/7 — ", "Open 24/7. ")
    # Line breaks in headings
    text = text.replace(" —<br>", "<br>")
    text = text.replace("—<br>", "<br>")
    # Mid-sentence em dashes
    text = text.replace(" — ", ", ")
    text = text.replace("—", ", ")
    # Cleanup template leftovers and double punctuation
    text = text.replace("Germany , </li>", "</li>")
    text = text.replace("Germany,</li>", "</li>")
    text = text.replace(", ,", ",")
    text = text.replace(",.", ".")
    text = text.replace(" ,", ",")
    return text


def main():
    paths = list(ROOT.glob("*.html"))
    paths += list((ROOT / "_snippets").glob("*.html"))
    for path in paths:
        original = path.read_text(encoding="utf-8")
        updated = remove_em_dashes(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
