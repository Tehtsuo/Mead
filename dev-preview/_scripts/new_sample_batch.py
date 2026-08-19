#!/usr/bin/env python3
"""Scaffold a new dev-preview sample batch folder from the structured-data schema.

Prototype-only tooling for this sandbox (see dev-preview/FEEDBACK.md and
dev-preview/schema.md) — mirrors what scripts/new_batch.py does for real batches, but
for the fake sample batches under dev-preview/ that the structured-data prototype uses
as its canvas. It only fills in the Overview fields (batch:); recipe: and gravity_log:
are left as empty lists for you to fill in by hand afterwards, since they're variable-
length lists that don't map cleanly onto CLI flags.

Usage:
    python3 dev-preview/_scripts/new_sample_batch.py \\
        --name "TRM Sample Batch 5" --type Melomel --start-date "August 19, 2026" \\
        [--bottling-date "September 30, 2026"] [--abv "~12%"] [--abv-percent 12]

Omit --bottling-date/--abv/--abv-percent for an in-progress sample batch, same as a
real batch that hasn't finished yet (see schema.md's "In progress" handling).
"""
import argparse
import re
import sys
from pathlib import Path

DEV_PREVIEW_DIR = Path(__file__).resolve().parent.parent

# Kept byte-identical to every other sample batch's copy, per schema.md's "Adding a new
# sample batch" step 3 — include_relative can't traverse out of a page's own directory,
# so each batch folder needs its own copy rather than one shared partial.
BATCH_DATA_PARTIAL = """<!-- Renders Overview/Recipe/Gravity Log from this page's front matter (page.batch / page.recipe / page.gravity_log). See dev-preview/CHANGELOG.md for why it lives here. -->
## Overview

<table>
  <tbody>
    <tr><td><strong>Type</strong></td><td>{{ page.batch.type }}</td></tr>
    <tr><td><strong>Start date</strong></td><td>{{ page.batch.start_date }}</td></tr>
    <tr><td><strong>Bottling date</strong></td><td>{% if page.batch.bottling_date %}{{ page.batch.bottling_date }}{% else %}<em class="batch-in-progress">In progress</em>{% endif %}</td></tr>
    <tr><td><strong>ABV</strong></td><td>{% if page.batch.abv %}{{ page.batch.abv }}{% else %}<em class="batch-in-progress">In progress</em>{% endif %}</td></tr>
  </tbody>
</table>

## Recipe

<ul>
{% for item in page.recipe %}
  <li><strong>{{ item.label }}:</strong>{% if item.detail %} {{ item.detail }}{% endif %}</li>
{% endfor %}
</ul>

## Gravity & Fermentation Log

<ul>
{% for entry in page.gravity_log %}
  <li>{{ entry.date }} : {{ entry.reading }}</li>
{% endfor %}
</ul>
"""

INDEX_TEMPLATE = """---
layout: dev-preview
title: {name}
description: {name}
batch:
  type: {type}
  start_date: {start_date}{bottling_date_line}{abv_line}{abv_percent_line}
recipe:
  - label: "Honey"
    detail:
  - label: "Water"
    detail:
  - label: "Yeast"
    detail:
  - label: "Nutrient"
    detail:
  - label: "Fruit / Spice"
    detail:
gravity_log:
  - date: {start_date}
    reading:
---

[← Back to Dev Preview](../)

This page mimics the structure of a real batch page, using made-up data, so dev-cycle runs have
a realistic canvas to improve without ever touching real batch content.

**Prototype (see [steering notes](../FEEDBACK.html)):** scaffolded by
`dev-preview/_scripts/new_sample_batch.py`. Fill in the `recipe:`/`gravity_log:` entries above
and this Brewing Notes section with sample data, per [the schema reference](../schema.html).

{{% include_relative _includes/batch-data.html %}}

## Brewing Notes

-
"""


def slugify(name):
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    if not slug:
        sys.exit(f"Could not derive a folder name from {name!r}.")
    return slug


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--name", required=True, help='Sample batch title, e.g. "TRM Sample Batch 5"')
    parser.add_argument("--type", required=True, help="e.g. Melomel, Metheglin, Pyment, Traditional")
    parser.add_argument("--start-date", required=True, help='Human-readable date, e.g. "August 19, 2026"')
    parser.add_argument("--bottling-date", default=None, help="Omit for an in-progress sample batch")
    parser.add_argument("--abv", default=None, help='Free-text ABV, e.g. "~12%%". Omit if --bottling-date is omitted')
    parser.add_argument("--abv-percent", default=None, type=float, help="Plain number for sorting, e.g. 12")
    args = parser.parse_args()

    if (args.abv or args.abv_percent is not None) and not args.bottling_date:
        sys.exit("--abv/--abv-percent require --bottling-date — an in-progress batch has neither yet.")

    slug = slugify(args.name)
    batch_dir = DEV_PREVIEW_DIR / slug
    if batch_dir.exists():
        sys.exit(f"{batch_dir} already exists.")

    bottling_date_line = f"\n  bottling_date: {args.bottling_date}" if args.bottling_date else ""
    abv_line = f"\n  abv: {args.abv}" if args.abv else ""
    abv_percent_line = f"\n  abv_percent: {args.abv_percent:g}" if args.abv_percent is not None else ""

    includes_dir = batch_dir / "_includes"
    includes_dir.mkdir(parents=True)
    (batch_dir / "index.md").write_text(
        INDEX_TEMPLATE.format(
            name=args.name,
            type=args.type,
            start_date=args.start_date,
            bottling_date_line=bottling_date_line,
            abv_line=abv_line,
            abv_percent_line=abv_percent_line,
        ),
        encoding="utf-8",
    )
    (includes_dir / "batch-data.html").write_text(BATCH_DATA_PARTIAL, encoding="utf-8")

    print(f"Created dev-preview/{slug}/")
    print("Next steps:")
    print("  - Fill in the recipe: and gravity_log: entries in its index.md front matter")
    print("  - Write the Brewing Notes section")
    print("  - It will appear on the all-batches index automatically, no other page to edit")


if __name__ == "__main__":
    main()
