#!/usr/bin/env python3
"""Scaffold a new mead batch folder with a randomly generated, non-duplicate name."""
import os
import random
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORDLIST_DIR = Path(__file__).resolve().parent / "wordlists"
MAX_ATTEMPTS = 500
SITE_URL = "https://tehtsuo.github.io/Mead"

BATCH_TEMPLATE = """---
title: {name}
---

[← Back to {year} Batches](../)

## Overview

| | |
|---|---|
| **Type** | |
| **Start date** | |
| **Bottling date** | |
| **ABV** | |
| **Fermentrack** | |

![QR code linking to this page](qr.svg)

[Print label](../../print/?batch={url_path})

## Recipe

- Honey:
- Water:
- Yeast:
- Nutrient:
- Fruit / Spice:

## Gravity & Fermentation Log

## Brewing Notes

-
"""

YEAR_INDEX_TEMPLATE = """---
title: {year} Batches
---

[← Back to Mead Log](../)

## {year} Batches

<!-- BATCH_LIST_START -->
No batches logged yet.
<!-- BATCH_LIST_END -->
"""


def load_words(filename):
    path = WORDLIST_DIR / filename
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def existing_batch_names(year_dir: Path):
    if not year_dir.exists():
        return set()
    return {p.name for p in year_dir.iterdir() if p.is_dir() and p.name.startswith("TRM ")}


def generate_unique_name(year_dir: Path):
    words_a = load_words("tropical.txt")
    words_b = load_words("mead.txt")
    taken = existing_batch_names(year_dir)

    total_combos = len(words_a) * len(words_b)
    if len(taken) >= total_combos:
        sys.exit(
            f"Exhausted all {total_combos} name combinations for {year_dir.name}. "
            "Add more words to scripts/wordlists/tropical.txt or mead.txt."
        )

    for _ in range(MAX_ATTEMPTS):
        name = f"TRM {random.choice(words_a)} {random.choice(words_b)}"
        if name not in taken:
            return name
    sys.exit("Could not find a unique batch name after many attempts. Add more words to the word lists.")


def ensure_year_index(year_dir: Path, year: str):
    index_path = year_dir / "index.md"
    if not index_path.exists():
        year_dir.mkdir(parents=True, exist_ok=True)
        index_path.write_text(YEAR_INDEX_TEMPLATE.format(year=year), encoding="utf-8")


def add_batch_link(year_dir: Path, name: str):
    index_path = year_dir / "index.md"
    content = index_path.read_text(encoding="utf-8")
    encoded = name.replace(" ", "%20")
    link_line = f"- [{name}]({encoded}/)"

    if "<!-- BATCH_LIST_START -->" not in content:
        sys.exit(f"{index_path} is missing batch list markers; add them manually and re-run.")

    start = content.index("<!-- BATCH_LIST_START -->") + len("<!-- BATCH_LIST_START -->")
    end = content.index("<!-- BATCH_LIST_END -->")
    body = content[start:end].strip()

    new_body = link_line if body == "No batches logged yet." or not body else f"{body}\n{link_line}"
    new_content = f"{content[:start]}\n{new_body}\n{content[end:]}"
    index_path.write_text(new_content, encoding="utf-8")


def write_qr_code(batch_dir: Path, year: str, name: str):
    import segno

    encoded = name.replace(" ", "%20")
    url = f"{SITE_URL}/{year}/{encoded}/"
    segno.make(url).save(batch_dir / "qr.svg", scale=6)


def main():
    year = os.environ.get("BATCH_YEAR", "").strip() or str(datetime.now().year)
    if not re.fullmatch(r"\d{4}", year):
        sys.exit(f"Invalid year: {year!r}")

    year_dir = REPO_ROOT / year
    ensure_year_index(year_dir, year)

    name = generate_unique_name(year_dir)
    batch_dir = year_dir / name
    batch_dir.mkdir(parents=True, exist_ok=False)

    batch_path = f"{year}/{name}"
    batch_url_path = f"{year}/{name.replace(' ', '%20')}"

    (batch_dir / "index.md").write_text(
        BATCH_TEMPLATE.format(name=name, year=year, url_path=batch_url_path), encoding="utf-8"
    )
    write_qr_code(batch_dir, year, name)

    add_batch_link(year_dir, name)

    print(f"Created {batch_path}")

    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as f:
            f.write(f"batch_name={name}\n")
            f.write(f"batch_path={batch_path}\n")
            f.write(f"batch_url_path={batch_url_path}\n")


if __name__ == "__main__":
    main()
