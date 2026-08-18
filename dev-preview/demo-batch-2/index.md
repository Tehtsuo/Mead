---
layout: dev-preview
title: TRM Sample Batch 2 (fake data)
description: TRM Sample Batch 2 (fake data)
batch:
  type: Traditional
  start_date: February 10, 2026
  bottling_date: June 15, 2026
  abv: "~11%"
  abv_percent: 11
recipe:
  - label: "Honey"
    detail: "3.5 lbs Sample Orange Blossom"
  - label: "Water"
    detail: "Fill to 1 gallon"
  - label: "Yeast"
    detail: "Sample Champagne Strain"
  - label: "Nutrient"
    detail: "Sample Nutrient (staggered)"
gravity_log:
  - date: February 10, 2026
    reading: "1.090 OG"
  - date: March 24, 2026
    reading: "1.005"
  - date: June 15, 2026
    reading: "0.996"
---

[← Back to Dev Preview](../)

This page mimics the structure of a real batch page, using made-up data, so dev-cycle runs have
a realistic canvas to improve without ever touching real batch content.

**Prototype (see [steering notes](../FEEDBACK.html)):** a second sample batch, alongside
[the first](../demo-batch/), so the [all-batches index](../batches/) has more than one row to
sort. Same structured-front-matter pattern as the first sample.

{% include_relative _includes/batch-data.html %}

## Brewing Notes

- February 24, 2026 : Degassed and added second nutrient dose
- April 10, 2026 : Racked to secondary
- June 15, 2026 : Bottled
