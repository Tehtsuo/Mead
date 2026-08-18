---
layout: dev-preview
title: Dev Preview Changelog
description: Dev Preview Changelog
---

[← Back to Dev Preview](./)

One entry per dev cycle: what changed, why, and any asset sources/licenses used.

## 2026-08-18 — Structured batch data, take 6: search box for the all-batches table

- **What:** Added a text search input above the [all-batches table](batches/) that filters rows by
  name as you type, composing with the existing type filter chips rather than replacing them (e.g.
  filter to "Melomel", then search "ember" to narrow further within just that type). Reworked the
  chip click-handler and the new search input to share one `applyFilters()` function that checks
  both conditions (`data-type` match AND `data-name` substring match) before showing/hiding each
  row, instead of the chip handler directly setting `row.style.display` on its own. Also added a
  "No batches match your search and filter." message that appears only when a search/filter
  combination leaves zero visible rows, so an empty result doesn't look like a broken/loading table.
  Grouped the new `<input type="search">` and the existing filter chips under one
  `.batches-toolbar` flex row in `assets/css/dev-preview.scss`, styled to match the chips'
  teak/cream/sand palette.
- **Why:** This is FEEDBACK.md's step 3, "iterate on ergonomics," and a direct extension of take 4
  (click-to-filter by type). Type filtering narrows by category, but once there are more batches
  than fit on screen, finding one specific batch by name is a different, equally common need that
  chips alone don't solve — a quick substring search is the natural complement, and composing it
  with the existing filter (rather than being a separate, exclusive mode) keeps both tools usable
  together the way real users would want ("show me the Melomels named X").
- **Assets:** None — the search input is a plain styled `<input>`, no new icon files.
- **Scope:** Edited `dev-preview/batches/index.md` (search input markup, empty-state message
  markup, and the `applyFilters()` JS rework) and `assets/css/dev-preview.scss` (added
  `.batches-toolbar`/`.batch-search`/`.batches-empty` rules, wrapped inside the sanctioned
  stylesheet anchor file) — both in scope.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors and no `_includes/` or build
  artifact leakage. Used headless Chromium (Playwright) to click through: typing a search query
  hides non-matching rows and leaves matching ones visible; searching a query that matches nothing
  shows the empty-state message and hides it again once cleared; combining a type-chip filter with
  a search query correctly ANDs both conditions (narrowing to Melomel then searching still shows
  only matching Melomel rows, and a further non-matching search under that filter also triggers the
  empty message); clearing the search and resetting to "All" restores every row; and column sorting
  still works correctly with the search box present and non-empty. Scratch build/server artifacts
  were removed after.

## 2026-08-18 — Structured batch data, take 5: batch name as its own column

- **What:** The [all-batches table](batches/) previously had no way to tell rows apart except by
  Type/ABV/dates — the only identifier was a generic "View" link at the end of each row. Added a
  new, sortable "Name" column (first in the table) using each batch page's own `page.title`
  (already set by every batch page, real and demo — no new front-matter field needed), and made it
  the row's link, dropping the redundant trailing "View" column. The column reuses the table's
  existing teak/cream "label" styling (`.main-content tr td:first-child`) that already highlighted
  the leftmost cell; added an `a` override in that same rule so the link renders in the existing
  cream color instead of the theme's default teal link color, which had weak contrast against the
  teak-gradient background.
- **Why:** This is FEEDBACK.md's step 3, "iterate on ergonomics." A table you can't identify rows
  in without clicking through isn't very ergonomic — once there are more than a couple of batches,
  "which row is which" matters as much as sorting/filtering. Real batch pages already name
  themselves via `title` (e.g. "TRM Grotto Ember" in `2026/TRM Grotto Ember/index.md`), so this
  also demonstrates the structured-data payoff needs no new field for something this basic — it's
  already there, just unused by the index page until now.
- **Assets:** None — reused the existing teak/cream color pair, no new icon files.
- **Scope:** Edited `dev-preview/batches/index.md` (Name column markup, `data-name` sort
  attribute, dropped the "View" column) and `assets/css/dev-preview.scss` (added the `a` color
  override inside the existing `tr td:first-child` rule) — both in scope.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors, correct `data-name` values,
  and no `_includes/` or build artifact leakage. Used headless Chromium (Playwright) to click
  through: default load still shows rows pre-sorted by type; clicking "Name" sorts alphabetically
  ascending/descending; each name links to its own batch page; the type filter chips still work
  against the reordered rows; and the link color renders as the intended cream against the teak
  background (confirmed via computed style and a screenshot). Scratch build/server artifacts were
  removed after.

## 2026-08-17 — Structured batch data, take 4: click-to-filter by type

- **What:** Added a row of type filter chips ("All", "Melomel", "Metheglin", "Traditional", each
  labeled with a live count) above the [all-batches table](batches/). Clicking a chip hides every
  row whose `data-type` doesn't match, complementing the existing click-to-sort headers rather than
  replacing them — sorting and filtering compose freely (e.g. filter to Melomel, then sort what's
  left by ABV). Chips are `{% raw %}{{ group.name }} ({{ group.items.size }}){% endraw %}` derived
  from `all_batches | group_by_exp: "p", "p.batch.type"`, so the chip list and counts are entirely
  data-driven — adding a fourth batch of a new type would add a fourth chip automatically, no
  hand-maintained list. Styled as pill buttons (`.filter-chips`/`.filter-chip` in
  `assets/css/dev-preview.scss`) matching the existing sunset-gradient active state used elsewhere
  on the site, with `aria-pressed` on each chip for accessibility. Same progressive-enhancement
  approach as the sort feature: with JavaScript disabled, all rows show and the chips render but do
  nothing, so the table degrades gracefully rather than breaking.
- **Why:** This is FEEDBACK.md's step 3, "iterate on ergonomics." With three batches the table is
  small enough to scan, but the whole point of the structured-data direction is that this scales —
  once there are a dozen+ real batches, being able to narrow to "just the Melomels" is a much bigger
  ergonomic win than sorting alone, and it was a natural next increment on the take-3 sortable table
  rather than a new mechanism.
- **Assets:** None — chips are plain HTML/CSS, no new icon files.
- **Scope:** Edited `dev-preview/batches/index.md` (filter chip markup + JS) and
  `assets/css/dev-preview.scss` (added `.filter-chips`/`.filter-chip` rules) — both in scope.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors, correct chip labels/counts
  (`All (3)`, `Melomel (1)`, `Metheglin (1)`, `Traditional (1)`), and no `_includes/` or build
  artifact leakage. Used headless Chromium (Playwright) to click through: clicking a type chip hides
  the other rows and sets `aria-pressed`/`.is-active` correctly, sorting still works correctly on
  the filtered subset, and clicking "All" restores every row. Scratch build/server artifacts were
  removed after.

## 2026-08-17 — Structured batch data, take 3: click-to-sort batches table

- **What:** Replaced the [all-batches index](batches/)'s two separate pre-sorted tables (one
  sorted by type, one by ABV) with a single table sortable by any column — Type, ABV, Start date,
  or Bottling date — via clickable column headers. Each `<th>` header is a `<button>` with
  `data-sort-key`/`data-sort-type`; a small vanilla-JS snippet (inline in the page, no new files
  or dependencies) re-orders the existing `<tr>` rows in the DOM on click and toggles
  ascending/descending via `aria-sort`, with a matching `▲`/`▼`/`⇅` indicator added to
  `assets/css/dev-preview.scss`. Server-side rendering is unchanged — Liquid still emits the table
  pre-sorted by type (and now stamps each row with `data-start`/`data-bottling` Unix-timestamp
  attributes via the `date` filter, so date columns sort correctly even though the display text
  stays a human-readable string) — so the page still works with JavaScript disabled, sorting is
  just a client-side enhancement on top.
- **Why:** This is FEEDBACK.md's step 3, "iterate on ergonomics," and directly closes the "Not
  done" item flagged in the prior entry: "interactive (click-to-sort) tables... could be a
  follow-up." One sortable table is also a better demonstration of the structured-data payoff than
  two hardcoded tables — any column becomes sortable for free once the data is structured, not
  just the two columns a cycle happened to hand-code a sort for.
- **Assets:** None — the sort indicators are plain Unicode characters (`▲`/`▼`/`⇅`) in CSS
  `content`, no new icon files.
- **Scope:** Edited `dev-preview/batches/index.md` (table markup + inline script) and
  `assets/css/dev-preview.scss` (added `.sortable-table` rules) — both in scope.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors and correct `data-*` timestamp
  values on each row, then used a headless Chromium (Playwright, already available in this
  environment) to load the built page and click through: default load renders sorted by type;
  clicking ABV sorts ascending then descending on a second click; clicking Start date sorts
  chronologically. All matched expectations. Scratch build/server artifacts were removed after.

## 2026-08-17 — Structured batch data, take 2: all-batches index, sortable by type/ABV

- **What:** Added [`dev-preview/batches/`](batches/), a prototype "all batches" index page that
  collects every page with a `batch:` front-matter field via `{% raw %}site.pages | where_exp{% endraw %}`
  and renders two tables from it — one sorted by `batch.type`, one sorted by a new
  `batch.abv_percent` numeric field (descending) — with no hand-typed row anywhere on the page.
  To give the index something to sort, added two more sample batches,
  [`demo-batch-2`](demo-batch-2/) (Traditional, ~11%) and [`demo-batch-3`](demo-batch-3/)
  (Melomel, ~14.5%), alongside the existing [`demo-batch`](demo-batch/) (Metheglin, ~13%), each
  using the same structured-front-matter pattern and its own copy of the `batch-data.html`
  partial (`include_relative` can't traverse out of a page's own directory, per the note in the
  prior entry). Also added `batch.abv_percent: <number>` to all three sample batches' front
  matter — the existing `batch.abv` stays a free-text display string (e.g. `"~13%"`), while
  `abv_percent` is a plain number used only for the `sort` filter, since Liquid's `sort` can't
  parse `"~13%"` numerically. Linked the new page from `dev-preview/index.md`.
- **Why:** This is step 2 of FEEDBACK.md's primary direction — "prototype an all batches index
  page fed by the data collection (e.g. sortable by type or ABV) — this is the kind of thing
  that's basically impossible with the current markdown-only approach." With three batches now
  carrying structured front matter, the index page proves that out: no per-batch table to
  maintain by hand, just a Liquid `sort` over whatever pages declare a `batch:` field.
- **Scope note — same deviation as the prior entry, still applies:** this uses `site.pages` plus
  each page's own front matter (not a real `_data/` collection or a shared root `_includes/`)
  because the sandbox's hard file-scope limit doesn't cover root `_data/**` or `_includes/**`.
  That's the mechanism a genuine site-wide version would need — flagged again here now that a
  second cycle has leaned on the same constraint, in case the human wants to widen scope for a
  future cycle instead of continuing to work around it with page-scoped front matter.
- **Not done:** interactive (click-to-sort) tables — this cycle used two pre-sorted static
  sections instead, to keep the change small; client-side sorting could be a follow-up per
  FEEDBACK.md's "iterate on ergonomics" suggestion, if wanted.
- **Assets:** None.
- **Scope:** Added `dev-preview/batches/index.md`, `dev-preview/demo-batch-2/` (`index.md` +
  `_includes/batch-data.html`), `dev-preview/demo-batch-3/` (`index.md` +
  `_includes/batch-data.html`); edited `dev-preview/demo-batch/index.md` (added `abv_percent`,
  updated intro text) and `dev-preview/index.md` (added link) — all under `dev-preview/**`.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built
  the full site to a scratch directory, and confirmed: both sorted tables render in the correct
  order (type: Melomel/Metheglin/Traditional; ABV descending: 14.5%/13%/11%), all three sample
  batch pages render correctly from their own front matter, and no `_includes/` directory or
  build artifact leaked into the output or the repo.

## 2026-08-17 — Structured batch data, take 1: front matter + Liquid partial

- **What:** Reworked the [demo batch page](demo-batch/) so its Overview table, Recipe list, and
  Gravity & Fermentation Log are no longer hand-typed Markdown — they're now structured fields
  (`batch:`, `recipe:`, `gravity_log:`) in the page's own YAML front matter, rendered by a new
  Liquid partial, `dev-preview/demo-batch/_includes/batch-data.html`, using Jekyll's
  `include_relative` tag.
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
