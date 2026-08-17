---
layout: dev-preview
title: TRM Sample Batch (fake data)
description: TRM Sample Batch (fake data)
batch:
  type: Metheglin
  start_date: January 1, 2026
  bottling_date: March 1, 2026
  abv: "~13%"
  abv_percent: 13
recipe:
  - "Honey: 3 lbs Sample Wildflower"
  - "Water: Fill to 1 gallon"
  - "Yeast: Sample Yeast Strain"
  - "Nutrient: Sample Nutrient"
  - "Spice: Cinnamon, cloves"
gravity_log:
  - date: January 1, 2026
    reading: "1.100 OG"
  - date: February 1, 2026
    reading: "1.010"
  - date: March 1, 2026
    reading: "0.998"
---

[← Back to Dev Preview](../)

This page mimics the structure of a real batch page, using made-up data, so dev-cycle runs have
a realistic canvas to improve without ever touching real batch content.

**Prototype (see [steering notes](../FEEDBACK.html)):** the Overview, Recipe, and Gravity Log
sections below are rendered from structured fields in this page's front matter — not hand-typed
Markdown — via a shared partial, [`_includes/batch-data.html`](https://github.com/Tehtsuo/Mead/blob/main/dev-preview/demo-batch/_includes/batch-data.html).
Open ["Edit on GitHub"](https://github.com/Tehtsuo/Mead/edit/main/dev-preview/demo-batch/index.md)
to see the data shape. Brewing Notes below stays free-form prose, as before. This is now one of
three sample batches feeding the [all-batches index](../batches/).

{% include_relative _includes/batch-data.html %}

## Brewing Notes

- January 15, 2026 : Racked to secondary
- March 1, 2026 : Bottled
