---
layout: dev-preview
title: Dev Preview
description: Dev Preview Sandbox
---

This is a sandbox where an automated dev-cycle proposes improvements — cosmetic and
functional — to the Tiki Room Meadery site, every 6 hours. Nothing here is live; it's all
proposals for review. Nothing outside this `dev-preview/` folder (plus its two anchor files,
`_layouts/dev-preview.html` and `assets/css/dev-preview.scss`) is ever touched by the automation.

- [Changelog](CHANGELOG.html) — what's been tried, run by run
- [Steering notes](FEEDBACK.html) — current direction/guidance for the automation (editable any time)
- [Demo batch page](demo-batch/) — a sample page (fake data) the automation uses as a canvas
- [All batches (demo)](batches/) — a prototype index page, sortable by type/ABV, fed by the
  structured data on the sample batch pages
- [Batch data schema](schema.html) — reference docs for the `batch`/`recipe`/`gravity_log` front
  matter fields, and steps for adding another sample batch

To apply something you like to the real site, just tell Claude which change/run to promote.
