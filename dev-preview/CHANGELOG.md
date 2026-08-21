---
layout: dev-preview
title: Dev Preview Changelog
description: Dev Preview Changelog
---

[← Back to Dev Preview](./)

One entry per dev cycle: what changed, why, and any asset sources/licenses used.

## 2026-08-21 — Structured batch data, take 14: computed Duration column

- **What:** Added a **Duration** column to the [all-batches index](batches/)'s sortable table,
  showing how many days each finished batch spent from `start_date` to `bottling_date`, plus a
  fifth "Avg. days to bottle" stat tile alongside the existing four. Neither is a new front-matter
  field — both are computed at build time from the `start_date`/`bottling_date` strings every
  batch already declares, via Liquid's `date: '%s'` filter (already used for the timestamp-sort
  attributes) subtracted and divided by 86400. The column plugs into the existing generic
  `data-sort-key`/`data-sort-type="number"` sort mechanism with no new JS — it already handles
  missing values (the in-progress sample batch's empty `data-duration`) by sorting them last in
  either direction, the same as the ABV/Bottling date columns. Updated the page's intro text and
  [`schema.md`](schema.html) to note Duration is derived, not a field to add when writing a new
  batch.
- **Why:** FEEDBACK.md's own rationale for the whole direction names "no way to compute stats
  across batches" as one of hand-typed Markdown's core limits. Take 11 covered that with an
  average-ABV stat, but every computed value since has drawn only from `abv_percent` — the two
  date fields (`start_date`/`bottling_date`) have been rendered and sorted individually across
  thirteen takes but never combined into a new fact the way `abv_percent` was. A duration/
  time-to-bottle figure is a natural, useful cross-batch stat (mirrors what a mead-maker would
  actually want to know — "how long did this batch take") that falls entirely out of data already
  present, with zero new front-matter to maintain. This is explicitly *not* a gravity/ABV
  visualization or calculator (the thing FEEDBACK.md flagged as not wanted) — it's a plain date
  difference on the two Overview-table date fields, unrelated to gravity readings.
- **Assets:** None — reused the existing `.batch-stat`/`.sortable-table`/`.batch-in-progress` CSS
  and sort JS, no new icon files or style rules.
- **Scope:** Edited `dev-preview/batches/index.md` (Duration column markup, `data-duration`
  attribute, per-row and stat-tile Liquid duration calculations, intro text) and
  `dev-preview/schema.md` (one clarifying paragraph) — both under `dev-preview/**`. No CSS changes
  needed since the new column/tile reuse existing classes.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair (`liquid`
  pinned to 4.0.4, matching prior takes), built the full site to a scratch directory, confirmed no
  Liquid/build errors, correct `data-duration` values on each row (demo-batch: 59, demo-batch-2:
  125, demo-batch-3: 151, demo-batch-4 in-progress: empty), correct table cells ("59 days" etc. vs.
  "In progress"), and the "Avg. days to bottle" tile computing 111 (the integer-divided mean of
  59/125/151). No `_includes:`/`_scripts:` leakage into `_site/`. Installed a local, uncommitted
  `playwright` pip package (browsers were already present in this environment) and used headless
  Chromium against the served scratch build to click through: clicking the Duration header sorts
  ascending then descending correctly with the in-progress row always last; searching "cinnamon"
  and filtering to the Pyment type chip still work exactly as before, composing correctly with the
  new column present. The scratch build/server artifacts, local gem install, and temporary
  `playwright` pip package were all removed after.

## 2026-08-20 — Structured batch data, take 13: ingredient search on the all-batches index

- **What:** Extended the [all-batches index](batches/)'s existing name-search box (take 6) to also
  match against recipe ingredients — searching "cinnamon" or "wildflower" now finds any batch whose
  `recipe:` `label`/`detail` pairs mention it, composing with the existing type-filter chips and
  name search exactly as before (same `applyFilters()` function, one more OR'd condition). Each row
  gets a new `data-ingredients` attribute built by a small Liquid loop that concatenates every
  recipe item's `label` and `detail` into one lowercased string per batch; the JS `matchesSearch`
  check now tests the search query against `data-name` *or* `data-ingredients`. Updated the search
  input's placeholder/`aria-label` ("Search by name or ingredient…") and the page's intro text to
  describe the new behavior, and added a paragraph to [`schema.md`](schema.html)'s Recipe section
  documenting that `label`/`detail` now feeds this search.
- **Why:** Take 8 split each recipe entry into structured `label`/`detail` fields specifically so
  ingredient data would be "queryable, not just display text sitting in YAML instead of Markdown" —
  but nothing since then actually queried it across batches: every later take (schema page, scaffold
  script, stat tiles, JSON export) built on the `batch:` fields (type, ABV, dates) or exposed
  `recipe:` verbatim in the JSON export, never searched/filtered *by* it. Letting the search box
  match ingredients as well as batch names is the natural, minimal way to demonstrate that payoff —
  "which batches use cinnamon" is exactly the kind of cross-batch question a hand-typed recipe list
  buried in each page's own Markdown could never answer, and it reuses the existing search UI rather
  than adding a new control.
- **Assets:** None — reused the existing search input and `.batches-toolbar`/`.batch-search` CSS,
  no new icon files or style rules.
- **Scope:** Edited `dev-preview/batches/index.md` (intro text, placeholder/aria-label,
  `data-ingredients` attribute + Liquid loop, `matchesSearch` JS) and `dev-preview/schema.md` (one
  documentation paragraph) — both under `dev-preview/**`, in scope. No CSS changes, no other files
  touched.
- **Verified:** Installed a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair (confirmed
  `liquid` pins to 4.0.4, same as prior takes), built the full site to a scratch directory,
  confirmed no Liquid/build errors, correct `data-ingredients` values for all four sample batches
  (spot-checked demo-batch's row includes "cinnamon, cloves"), and no `_includes/`/`_scripts/`
  leakage into `_site/`. Installed a local, uncommitted `playwright` pip package (browsers were
  already present in this environment) and used headless Chromium against the served scratch build
  to click through: searching "cinnamon" (present only in an ingredient, not any batch name) shows
  exactly the one matching batch; searching "raspberries" (a recipe `detail`) and "nutrient" (a
  `label` common to all four batches) work the same way; a query matching neither name nor
  ingredient shows the existing empty-state message; composing a type-chip filter with an ingredient
  search still ANDs both conditions correctly (Metheglin + "cinnamon" → demo-batch only; Pyment +
  "grape" → demo-batch-4 only); and search is case-insensitive ("CINNAMON" still matches). Clearing
  the search restores all rows. The scratch build/server artifacts, local gem install, and the
  temporary `playwright` pip package were all removed after.

## 2026-08-19 — Structured batch data, take 12: JSON export of the batch collection

- **What:** Added [`dev-preview/batches/data.json`](batches/data.json), a Jekyll page (front
  matter `layout: null`, no HTML wrapper) that renders the same `all_batches` collection the
  index table/stat tiles already use as a plain JSON array — one object per batch with `name`,
  `url`, and the three structured front-matter blocks (`batch`, `recipe`, `gravity_log`), each run
  through Jekyll's `jsonify` filter so nesting/escaping is handled for free rather than hand-built
  with string concatenation. Linked it from the [all-batches index](batches/) two ways: a sentence
  in the intro text, and a small "⬇ Export as JSON" pill (`.export-link` in
  `assets/css/dev-preview.scss`) pinned to the right end of the existing search/filter-chip
  toolbar row, with a `download="batches.json"` attribute so clicking it saves the file instead of
  just navigating to it.
- **Why:** FEEDBACK.md's own opening rationale for the whole structured-data direction names
  three things hand-typed Markdown can't do: "no way to compute stats across batches, build a
  sortable/filterable batch index, or feed the data anywhere else." Take 11 covered the first
  ("compute stats"); ten takes before that covered the second (the sortable/filterable/searchable
  index). This is the only one of the three still undemonstrated — a JSON export is the simplest,
  most direct way to show the data can leave the page entirely (script access, a spreadsheet
  import, a future non-Jekyll tool) instead of being trapped in either a Markdown table or an
  HTML page's DOM.
- **Assets:** None — plain Liquid/JSON output and a CSS pill reusing the existing chip/search
  palette tokens, no new icon files.
- **Scope:** Added `dev-preview/batches/data.json`; edited `dev-preview/batches/index.md` (intro
  sentence + toolbar export link) and `assets/css/dev-preview.scss` (added `.export-link`) — all
  in scope. No other files touched.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors and no `_includes/`/
  `_scripts/` leakage. Validated `data.json`'s output directly with `python3 -m json.tool` (parses
  cleanly) and by eye: all four sample batches present, the in-progress batch's `batch` object
  correctly omits `bottling_date`/`abv`/`abv_percent` entirely (matching the schema's "omit, don't
  placeholder" rule) rather than emitting `null`/empty-string placeholders, and `recipe`/
  `gravity_log` round-trip as proper arrays of objects. Served the scratch build locally and
  confirmed the file responds `200` with `Content-Type: application/json`. Used headless Chromium
  (Playwright) to load the built index page and confirm the toolbar's export link renders with the
  correct href/label at the intended position. Scratch build/server artifacts, the local gem
  install, and the temporary Playwright pip package used only for this verification were all
  removed after.

## 2026-08-19 — Structured batch data, take 11: quick-stats tiles on the all-batches index

- **What:** Added a row of four stat tiles ("Total batches", "Finished", "In progress",
  "Avg. ABV (finished)") above the toolbar on the [all-batches index](batches/), computed
  entirely from the same `all_batches` Liquid collection the table already builds — no new data
  source, no hand-typed numbers. `finished_batches` is `all_batches` filtered to pages with an
  `abv_percent` (the same "does this batch have a real value yet" check the Overview
  table/index already use for "In progress"); the average ABV sums `abv_percent` across those via
  a plain Liquid `for` loop with a running `plus` total (not the `sum` filter — confirmed against
  the actual installed `liquid` gem, 4.0.4, that GitHub Pages' Jekyll pins, which predates
  `sum`'s addition in Liquid 5.4), then `divided_by` the count and `round: 1`, with an em dash
  fallback if there are zero finished batches yet. Styled as small rounded tiles
  (`.batch-stats`/`.batch-stat*` in `assets/css/dev-preview.scss`) reusing the existing sand/cream
  gradient and rust/teak palette tokens, matching the filter chips and search box already on the
  page. The tiles summarize the *whole* collection regardless of the active type filter/search —
  confirmed deliberately, not a bug: they're a stats overview, not a filtered subtotal.
- **Why:** FEEDBACK.md's own opening rationale for the whole structured-data direction names two
  payoffs data trapped in hand-typed Markdown can't deliver: "no way to compute stats across
  batches, build a sortable/filterable batch index, or feed the data anywhere else." Ten prior
  takes fully delivered the second half (the sortable/filterable/searchable index) but nothing yet
  demonstrated the first half — computing a stat *across* batches, not just listing them. A small
  summary row is the natural, minimal way to show that off without duplicating what the type
  filter chips already do (per-type counts) or reintroducing the gravity/ABV chart FEEDBACK.md
  explicitly flagged as not wanted.
- **Assets:** None — plain HTML/CSS tiles reusing existing palette tokens and the existing
  "Super Funky" font-face, no new icon files.
- **Scope:** Edited `dev-preview/batches/index.md` (new Liquid assigns + `.batch-stats` markup,
  above the existing toolbar) and `assets/css/dev-preview.scss` (added `.batch-stats`/
  `.batch-stat`/`.batch-stat-value`/`.batch-stat-label` rules) — both in scope. No other files
  touched.
- **Verified:** Installed a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair (confirmed
  the pinned `liquid` version is 4.0.4, informing the `sum`-filter-avoidance decision above), built
  the full site to a scratch directory, confirmed no Liquid/build errors and no `_includes/`/
  `_scripts/` leakage. Checked the rendered stat values directly: 4 total, 3 finished, 1 in
  progress, 12.8% average ABV (the correct mean of 13/11/14.5 across the three finished sample
  batches — demo-batch-4 excluded as in-progress). Used headless Chromium (Playwright) to confirm
  the tiles render correctly against the live palette (screenshot), and that they stay
  visually/functionally independent of the existing sort/filter/search controls — clicking a type
  chip and searching still correctly narrows the *table* while the stat tiles keep showing the
  whole-collection totals, and the tiles don't interfere with sort/filter/search still working
  together as before. Scratch build/server artifacts and the local gem install were removed after.

## 2026-08-19 — Structured batch data, take 10: scaffold script for new sample batches

- **What:** Added [`dev-preview/_scripts/new_sample_batch.py`](https://github.com/Tehtsuo/Mead/blob/main/dev-preview/_scripts/new_sample_batch.py),
  a small CLI script that scaffolds a new sample batch folder — front matter (`batch:` fully
  filled in from flags, `recipe:`/`gravity_log:` seeded as empty-detail placeholder lists) plus a
  byte-identical copy of `_includes/batch-data.html` — instead of copy-pasting an existing batch
  folder by hand. It takes `--name`/`--type`/`--start-date` (required) and
  `--bottling-date`/`--abv`/`--abv-percent` (optional, for a finished vs. in-progress batch,
  enforcing the same "abv requires a bottling date" invariant the schema already documents),
  slugifies the name into a folder, and refuses to overwrite an existing folder. Lives in a
  leading-underscore directory (`dev-preview/_scripts/`, not `dev-preview/scripts/`) so Jekyll
  doesn't publish the `.py` file as a static asset on the preview site — confirmed by a full site
  build before and after the rename (the un-prefixed name leaked into `_site/dev-preview/scripts/`;
  the underscore-prefixed one didn't), the same reasoning take 1 used for nesting `_includes/`
  inside each batch folder rather than a shared root one. Updated
  [`dev-preview/schema.md`](schema.html)'s "Adding a new sample batch" section to present the
  script as Option A (fast path) alongside the existing manual copy steps as Option B.
- **Why:** FEEDBACK.md's step 3 explicitly suggests this: "iterate on ergonomics... or
  scriptable the way `scripts/new_batch.py` already scaffolds new batches." Nine prior takes built
  the schema, the rendering partial, and the pages that consume it, but every one of them still
  required manually copying a folder and hand-editing YAML to add a new sample batch — the exact
  kind of repetitive setup `scripts/new_batch.py` already automates for real batches. This mirrors
  that pattern for the prototype's sample batches specifically (real batches and `scripts/**` are
  untouched, per the sandbox's file scope and FEEDBACK.md's explicit "do not migrate real batch
  data" instruction) — `recipe:`/`gravity_log:` are deliberately left as manual follow-up since
  they're variable-length lists that don't map cleanly onto a fixed set of CLI flags the way the
  three-or-four Overview fields do.
- **Assets:** None — a plain Python script, no new icon files.
- **Scope:** Added `dev-preview/_scripts/new_sample_batch.py`; edited `dev-preview/schema.md`
  (added the "Option A — scaffold script" paragraph, restructured the existing steps as
  "Option B") — both under `dev-preview/**`. No CSS or partial changes.
- **Verified:** Ran the script directly (both in a scratch copy of `dev-preview/` and, briefly,
  for a real build check, uncommitted inside the repo itself before deleting it) to confirm: an
  in-progress batch (no `--bottling-date`) scaffolds correctly; a finished batch with
  `--bottling-date`/`--abv`/`--abv-percent` scaffolds correctly; passing `--abv` without
  `--bottling-date` is rejected with a clear error; running twice for the same name is rejected
  ("already exists") rather than overwriting; and the generated `_includes/batch-data.html` is
  byte-identical (`diff` confirmed) to the canonical copy in `demo-batch-4/`. Reinstalled a local,
  uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the full site to a scratch directory
  with a scaffolded test batch present, confirmed: the batch page renders its Overview table
  correctly from the generated front matter (including the "In progress" case), it appears
  automatically on the all-batches index with no other page edited, `dev-preview/_scripts/` does
  **not** leak into the built `_site/` output (verified by first testing with the un-prefixed
  `dev-preview/scripts/` name, seeing it leak, then confirming the underscore-prefixed rename
  fixes it), and the updated `schema.md` section renders correctly. The test batch folder, scratch
  build artifacts, and the local gem install were all removed after — the repo's working tree has
  only the two files listed under Scope.

## 2026-08-19 — Structured batch data, take 9: batch data schema reference page

- **What:** Added [`dev-preview/schema.md`](schema.html), a reference page documenting the
  `batch:`/`recipe:`/`gravity_log:` front-matter shape used by every sample batch — what each
  field is, its type, and whether it's required or safe to omit (e.g. `bottling_date`/`abv`/
  `abv_percent` while a batch is still in progress) — plus a numbered "Adding a new sample batch"
  walkthrough (copy an existing batch folder, edit front matter, leave `_includes/batch-data.html`
  untouched, no other page needs editing since the all-batches index auto-discovers via
  `site.pages`). Linked it from `dev-preview/index.md`'s bullet list alongside the other prototype
  pages.
- **Why:** FEEDBACK.md's step 3 asks to "iterate on ergonomics — what would make this pleasant to
  maintain by hand." Eight prior takes built the schema and the pages that consume it, but the
  shape itself was only ever discoverable by reading front matter across four different pages and
  cross-referencing changelog entries for the "why" (e.g. why each batch folder needs its own
  copy of the partial). That's exactly the kind of friction "pleasant to maintain by hand" is
  meant to catch — a single reference page removes it, and doubles as the spec a human would want
  before deciding whether to migrate real batch pages to this pattern.
- **Assets:** None — plain Markdown (a table and two fenced YAML snippets), no new icon files.
- **Scope:** Added `dev-preview/schema.md`; edited `dev-preview/index.md` (added one bullet
  linking the new page) — both under `dev-preview/**`. No CSS or partial changes.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors, `dev-preview/schema.html`
  renders (table and YAML code blocks present, no `_includes/` leakage), and the new index.md
  bullet links to it correctly. Scratch build artifacts and the local gem install (including
  transitive dependency gems) were removed after.

## 2026-08-18 — Structured batch data, take 8: recipe items as label/detail pairs

- **What:** Recipe items in front matter were still a list of one hand-formatted string per line
  (e.g. `"Honey: 3 lbs Sample Wildflower"`) — genuinely structured for the Overview table and
  Gravity log, but not for Recipe, where the label ("Honey") and its detail were still baked
  together as display text rather than separate fields. Split each recipe entry into a `label`/
  `detail` pair (e.g. `label: Honey`, `detail: 3 lbs Sample Wildflower`) across all four sample
  batches, and updated all four `batch-data.html` partial copies to render
  `<li><strong>{{ item.label }}:</strong> {{ item.detail }}</li>`. For entries with no detail yet
  (demo-batch-4's `Nutrient` and `Fruit / Spice`, which were already deliberately blank to mirror
  a real in-progress batch), the detail simply renders empty rather than needing a placeholder —
  matching exactly how the real "TRM Grotto Ember" page's own blank `Nutrient:`/`Fruit / Spice:`
  lines look (confirmed by comparing rendered output to `2026/TRM Grotto Ember/index.md`, read
  only for reference, not modified).
- **Why:** This is still FEEDBACK.md's primary direction — "recipe ingredients" is explicitly
  named as one of the fact-like fields to structure — and take 1 only partly delivered on it: the
  Overview/Gravity fields became real structured data, but Recipe items stayed pre-formatted
  strings, the same category of problem the whole effort exists to move away from (not queryable,
  not filterable, just display text sitting in YAML instead of Markdown). Splitting `label` from
  `detail` closes that gap and keeps every structured field at the same granularity, without
  touching the free-form Brewing Notes prose, which stays exactly as-is per FEEDBACK.md's
  narrative-text guidance.
- **Assets:** None — no markup changes beyond the existing `<strong>`/`<li>` structure, no new
  icon files.
- **Scope:** Edited `recipe:` front matter in all four sample batches
  (`dev-preview/demo-batch{,-2,-3,-4}/index.md`) and the Recipe loop in all four
  `_includes/batch-data.html` copies; also updated `demo-batch/index.md`'s intro text to describe
  the new shape and fix a stale "one of three" batch count (there are now four sample batches,
  since take 7 added a fourth) — all under `dev-preview/**`, in scope. No CSS changes.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors and no `_includes/` leakage.
  Checked the rendered HTML directly (this change is pure server-side Liquid with no JS behavior,
  so no browser automation was needed): all four batches' Recipe sections render
  `<strong>Label:</strong> detail` correctly, and demo-batch-4's two detail-less entries render as
  `<strong>Nutrient:</strong>`/`<strong>Fruit / Spice:</strong>` with nothing after the colon,
  matching the real Grotto Ember page's equivalent blank lines. Scratch build artifacts and the
  local gem install were removed after.

## 2026-08-18 — Structured batch data, take 7: handling in-progress batches

- **What:** Every sample batch so far had a complete, finished record — Type, both dates, and a
  final ABV. Real batches don't start that way: looking at the live site, several real pages
  (e.g. "TRM Grotto Ember") only have a Type and start date logged so far, with Bottling date and
  ABV genuinely blank because the batch just hasn't gotten there yet. That's a gap in the
  prototype's schema handling, not an edge case to ignore, so this cycle made missing fields a
  first-class, deliberately-modeled case instead of an unhandled one:
  - Added a fourth sample, [demo-batch-4](demo-batch-4/) ("TRM Sample Batch 4 (fake data, in
    progress)", Pyment, only `start_date` and a single OG gravity reading set) — `bottling_date`,
    `abv`, and `abv_percent` are simply absent from its front matter, the same way a real
    in-progress batch's page would look, rather than being filled with a placeholder value.
  - Updated the `batch-data.html` partial (all four sample batches' copies, since the pattern
    isn't shared) so the Overview table renders `<em class="batch-in-progress">In progress</em>`
    for `bottling_date`/`abv` when absent, instead of a silently blank table cell.
  - Updated the [all-batches index](batches/) to match: the Bottling date/ABV columns show the
    same "In progress" label instead of blank, and the sort comparator (`data-abv`/`data-bottling`
    are empty strings for a missing value, which parsed as `NaN` before) now explicitly sorts rows
    with no value to the *end* of the list in both ascending and descending order, rather than
    comparing as `NaN` and leaving their position among sorted rows undefined/inconsistent.
- **Why:** This is still FEEDBACK.md's step 3, "iterate on ergonomics" — a schema that only
  demos the tidy, complete-record case isn't validated against how batches actually get created
  and updated over weeks/months. Handling "no value yet" cleanly (a readable label, not a raw
  blank cell; a sane, stable sort position) is exactly the kind of ergonomics gap that would bite
  immediately if this pattern were ever applied to real batch pages, so it's worth surfacing and
  fixing in the prototype now rather than after a real migration.
- **Assets:** None — `.batch-in-progress` is a plain italic text style reusing the existing
  `$blockquote-text-color` token, no new icon files.
- **Scope:** Added `dev-preview/demo-batch-4/` (`index.md` + `_includes/batch-data.html`); edited
  the other three sample batches' `_includes/batch-data.html` files, `dev-preview/batches/index.md`
  (table cell markup, `data-abv`/`data-bottling` attributes, JS sort comparator, and intro text),
  and `assets/css/dev-preview.scss` (added the `.batch-in-progress` rule) — all in scope.
- **Verified:** Reinstalled a local, uncommitted `jekyll`/`jekyll-theme-cayman` gem pair, built the
  full site to a scratch directory, confirmed no Liquid/build errors, correct `data-abv=""`/
  `data-bottling=""` attributes on the in-progress row, and no `_includes/` or build artifact
  leakage. Used headless Chromium (Playwright) to confirm: the in-progress row shows "In progress"
  in both columns; sorting by ABV or Bottling date (ascending and descending) always places the
  in-progress row last; filtering to its type ("Pyment") via the chip correctly isolates just that
  row; and combining that filter with a non-matching search still triggers the existing empty-state
  message. Scratch build/server artifacts and the local gem install were removed after.

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
