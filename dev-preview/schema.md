---
layout: dev-preview
title: Batch Data Schema (prototype)
description: Batch Data Schema (prototype)
---

[← Back to Dev Preview](./)

**Prototype (see [steering notes](FEEDBACK.html)):** this page documents the structured
front-matter shape used by the [sample batch pages](demo-batch/) and consumed by the
[all-batches index](batches/) — the reference a human (or a future cycle) needs to add another
sample batch, or to judge what a real migration would ask a batch page to declare. Nothing on
this page is new behavior; it's a write-up of the shape that's already in use across all four
sample batches, kept in one place instead of only being discoverable by diffing front matter
across pages.

## Front matter fields

A batch page opts into the structured-data rendering by setting these three top-level front
matter keys. Everything not listed here (Brewing Notes, tasting commentary, any other narrative)
stays plain Markdown in the page body, per [FEEDBACK.md](FEEDBACK.html)'s guidance not to force
prose into structured fields.

### `batch:` — Overview table

| Field         | Type   | Required? | Notes |
|---------------|--------|-----------|-------|
| `type`        | string | required  | e.g. `Metheglin`, `Melomel`, `Pyment`. Free text — whatever category the batch is. |
| `start_date`  | string | required  | Human-readable date (e.g. `July 20, 2026`). Also parsed by Liquid's `date` filter for the all-batches index's timestamp sort, so keep it in a normal, unambiguous date format. |
| `bottling_date` | string | optional | **Omit entirely** while the batch hasn't been bottled yet — don't fill in a placeholder. Both the Overview table and the all-batches index render "In progress" automatically when this key is absent. |
| `abv`         | string | optional  | Free-text display value, e.g. `"~13%"`. Omit while in progress, same as `bottling_date`. |
| `abv_percent` | number | optional  | Plain number (e.g. `13`), used *only* for the all-batches index's numeric ABV sort — Liquid can't parse `"~13%"` as a number. Omit while `abv` is omitted; there's nothing to sort yet. |

### `recipe:` — Recipe list

A list of ingredient entries, each a `label`/`detail` pair:

```yaml
recipe:
  - label: "Honey"
    detail: "3 lbs Sample Wildflower"
  - label: "Nutrient"
    detail:
```

- `label` (string, required) — the ingredient category (`Honey`, `Water`, `Yeast`, `Nutrient`,
  `Fruit / Spice`, …).
- `detail` (string, optional) — the specifics. Leave it blank (as with `Nutrient` above) for an
  ingredient that's a known part of the recipe but not yet decided/measured — it renders as just
  `Label:` with nothing after the colon, matching how a real in-progress batch page looks.

Every `label`/`detail` pair also feeds the [all-batches index](batches/)'s search box, which
matches against ingredient text as well as batch name — e.g. searching "cinnamon" finds every
batch whose recipe mentions it, across all batches at once, which a hand-typed recipe list
buried in each page's own Markdown could never do.

### `gravity_log:` — Gravity & Fermentation Log

A list of readings, each a `date`/`reading` pair:

```yaml
gravity_log:
  - date: July 20, 2026
    reading: "1.090 OG"
```

- `date` (string, required) — human-readable, same conventions as `batch.start_date`.
- `reading` (string, required) — the gravity value as you'd write it by hand, including any
  suffix like `OG`/`FG` (this stays a display string, not a parsed number — see
  [FEEDBACK.md](FEEDBACK.html) on why a second in-page gravity chart/calculator isn't wanted).

## Adding a new sample batch

**Option A — scaffold script.** Run
`python3 dev-preview/_scripts/new_sample_batch.py --name "TRM Sample Batch N" --type Melomel
--start-date "August 19, 2026"` (add `--bottling-date`/`--abv`/`--abv-percent` for a finished
batch instead of an in-progress one — see `--help` for the full flag list). It creates the new
folder with a correct `batch:` block and a byte-identical copy of `_includes/batch-data.html`
for you; `recipe:`/`gravity_log:` are left as empty-detail placeholder lists (variable-length,
so not worth a flag each) for you to fill in by hand afterwards, same as step 2 below. The script
lives in a leading-underscore directory so Jekyll doesn't publish it as a static file on the
preview site, the same reason `_includes/` is nested per batch (see the
[changelog](CHANGELOG.html)'s take-1 scope note).

**Option B — copy by hand:**

1. Copy an existing sample batch's whole folder (e.g. `demo-batch-4/`) to a new
   `dev-preview/<your-batch-name>/` directory.
2. In the new `index.md`, update `title`/`description` and the `batch:`/`recipe:`/`gravity_log:`
   fields above to the new batch's data.
3. Leave `_includes/batch-data.html` exactly as copied — it's byte-identical across every sample
   batch (see the [changelog](CHANGELOG.html)'s take-1 scope note for why each batch folder needs
   its own copy rather than one shared partial).
4. Write the free-form "Brewing Notes" section below the `{% raw %}{% include_relative
   _includes/batch-data.html %}{% endraw %}` line as normal Markdown, same as any other page.

Either way, that's it — no other page needs editing. The [all-batches index](batches/)
auto-discovers any page under `dev-preview/` with a `batch:` field via `site.pages`, so the new
batch appears there (and is sortable/filterable/searchable) without any manual list to update.
