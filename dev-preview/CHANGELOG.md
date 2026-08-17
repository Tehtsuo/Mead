---
layout: dev-preview
title: Dev Preview Changelog
description: Dev Preview Changelog
---

[← Back to Dev Preview](./)

One entry per dev cycle: what changed, why, and any asset sources/licenses used.

## 2026-08-17 — Structured batch data, take 1: front matter + Liquid partial

- **What:** Reworked the [demo batch page](demo-batch/) so its Overview table, Recipe list, and
  Gravity & Fermentation Log are no longer hand-typed Markdown — they're now structured fields
  (`batch:`, `recipe:`, `gravity_log:`) in the page's own YAML front matter, rendered by a new
  Liquid partial, `dev-preview/demo-batch/_includes/batch-data.html`, via `{% include_relative %}`.
  Free-form prose (Brewing Notes) is untouched, still plain Markdown in the page body, per
  FEEDBACK.md's "don't force narrative text into structured fields" guidance. Also removed the
  gravity trend chart added 2026-08-16 and its now-unused `.gravity-chart*` CSS, since
  FEEDBACK.md flagged it as "not wanted right now" — the Gravity Log is back to a plain rendered
  list (now data-driven instead of hand-typed).
- **Why:** This is step 1 of FEEDBACK.md's primary direction: prototype structured, fact-like
  batch fields (Type, dates, ABV, recipe, gravity readings) living in data instead of buried in
  a markdown table + bullet lists, with the page template rendering from that data via Liquid.
- **Scope note — deviation from FEEDBACK.md's suggested shape:** FEEDBACK.md suggests Jekyll's
  native `_data/` directory and a `_includes/` partial, both of which are root-level Jekyll
  directories. This sandbox's hard file-scope limit only covers `dev-preview/**`,
  `_layouts/dev-preview.html`, `assets/css/dev-preview.scss`, and `assets/icons/dev-preview/**` —
  it does not list root `_data/` or `_includes/`, and the task instructions are explicit that
  file scope is a hard limit ("never touch anything else... if unsure, don't touch it"), so this
  cycle did not create either. Instead: the structured fields live in the page's own front
  matter (still genuinely structured/queryable via Liquid, just page-scoped rather than a
  site-wide `_data/` collection), and the rendering partial lives at
  `dev-preview/demo-batch/_includes/batch-data.html` — a leading-underscore directory *nested
  inside* `dev-preview/`, not the root one. Jekyll's `include_relative` tag can't traverse `../`
  out of a page's own directory (confirmed by a local test build — it raises an error), which is
  why the partial sits beside `demo-batch/index.md` rather than in a shared
  `dev-preview/_includes/`; a nested leading-underscore directory is excluded from Jekyll's own
  Pages/StaticFiles listing at any depth, so it's readable via `include_relative` without also
  being published as a stray page. **If a future cycle (or the human) wants the real `_data/`
  idiom** — a genuine site-wide data collection and a reusable root `_includes/` partial, which
  would matter more once cycle 2's "all batches" index page needs to read every batch's data at
  once — the sandbox's hard file-scope list would need to be widened to include root `_data/**`
  and `_includes/**`. Flagging that here rather than acting on it unilaterally.
- **Assets:** None.
- **Scope:** Touched `dev-preview/demo-batch/index.md`, added
  `dev-preview/demo-batch/_includes/batch-data.html` (both under `dev-preview/**`), and edited
  `assets/css/dev-preview.scss` (removed the now-unused gravity-chart rules only).
- **Verified:** Installed a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair to build
  the site and confirm: the page renders correctly from front matter, no Liquid/build errors, and
  the `_includes/` partial is not leaked as a stray output file.

## Scaffold created

- Set up the sandbox: `_layouts/dev-preview.html`, `assets/css/dev-preview.scss` (forked from
  the live theme), this changelog, [steering notes](FEEDBACK.html), and a
  [demo batch page](demo-batch/) with sample data to work against.
- No proposals yet — the first scheduled run picks the first idea.

## 2026-08-16 — Gravity trend chart

- **What:** Added a small inline-SVG line chart under "Gravity & Fermentation Log" on the
  [demo batch page](demo-batch/), plotting the existing bullet-list gravity readings (OG → FG
  over time) as a proper trend line instead of leaving them as plain text. Styled to match the
  existing tiki palette (teal line/area, rust dots, sand card background) and added matching
  rules (`.gravity-chart*`) to `assets/css/dev-preview.scss`.
- **Why:** Real batch pages already log several gravity readings over the course of
  fermentation, but the data is easy to skim past as a flat list. A small chart makes the
  fermentation progress (and when it stalls or finishes) visible at a glance. This is a
  functional/UX idea, not just decoration — if liked, the pattern could be hand-applied to
  real batch pages that have 3+ gravity readings.
- **Assets:** None — the chart is hand-authored inline SVG (lines/polyline/polygon/text), no
  new icon files needed.
- **Scope:** Touched only `dev-preview/demo-batch/index.md` and `assets/css/dev-preview.scss`
  (the sanctioned stylesheet anchor file). No other files modified.
