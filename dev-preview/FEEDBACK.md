---
layout: dev-preview
title: Dev Preview Steering Notes
description: Dev Preview Steering Notes
---

[← Back to Dev Preview](./)

This is the current direction for the automated dev cycle. **Read this file first, every run.**
Edit it any time (via "Edit on GitHub" or by telling Claude directly) to steer future cycles —
things to focus on, things to avoid, or "spend the next N cycles refining idea X."

## Current direction

**Primary focus, spend multiple cycles on this: structured data storage for batch content.**

Real batch pages currently store everything — Type, dates, ABV, recipe, gravity log, notes — as
hand-formatted Markdown (a table plus bullet lists) directly in `2026/<batch>/index.md`. That's
opaque to anything except a human reading that one page: no way to compute stats across batches,
build a sortable/filterable batch index, or feed the data anywhere else.

The direction: prototype storing the **structured, fact-like fields** (Type, start/bottling date,
ABV, recipe ingredients, gravity readings) in data files — Jekyll's native `_data/` directory
(YAML or JSON) is the idiomatic fit — with the page template rendering the Overview table, Recipe
list, and Gravity log *from* that data via Liquid, instead of the values being hand-typed into
markdown. **Free-form prose** (Brewing Notes narrative, tasting commentary) should stay as plain
markdown in the page body — don't try to force narrative text into structured fields, it belongs
as text.

Suggested shape, roughly one idea per cycle:
1. Design the data schema (what fields, what a `_data/` file for one batch looks like) and update
   the [demo batch page](demo-batch/) to render its Overview/Recipe/Gravity sections from a data
   file instead of hardcoded markdown, using a Liquid include.
2. Once that pattern is solid, prototype an "all batches" index page fed by the data collection
   (e.g. sortable by type or ABV) — this is the kind of thing that's basically impossible with the
   current markdown-only approach, and demonstrates why the structured version is worth it.
3. Iterate on ergonomics — e.g. what would make this pleasant to maintain by hand (or scriptable
   the way `scripts/new_batch.py` already scaffolds new batches).

**Do NOT attempt to migrate real batch data** (`2026/**`) to this pattern — that's out of scope
for the sandbox anyway, but worth stating explicitly: this is prototype-only until the human
reviews the pattern and decides to migrate real content themselves.

**Not wanted right now:** gravity/ABV visualization widgets (charts, calculators). Real gravity
tracking is handled by iSpindel + BrewSpy, which already produces graphs to be added manually once
a batch finishes — a second, redundant in-page chart/calculator isn't useful. (The gravity trend
chart from 2026-08-16 was a reasonable idea but isn't a direction to keep building on.)

## Standing preferences

- Both cosmetic and functional ideas are wanted — don't limit yourself to visual polish.
- One meaningful, scoped improvement per run. Small and reviewable beats big and sprawling.
- Sourced assets: only genuinely no-attribution-required, open-source resources (the UXWing
  pattern already used on the live site — see `assets/icons/CREDITS.md`). Log every new asset.
- Don't repeat an idea already logged as tried/rejected in the changelog.
