---
layout: dev-preview
title: Dev Preview Changelog
description: Dev Preview Changelog
---

[← Back to Dev Preview](./)

One entry per dev cycle: what changed, why, and any asset sources/licenses used.

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
