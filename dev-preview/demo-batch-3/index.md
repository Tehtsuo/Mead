---
layout: dev-preview
title: TRM Sample Batch 3 (fake data)
description: TRM Sample Batch 3 (fake data)
batch:
  type: Melomel
  start_date: March 3, 2026
  bottling_date: August 1, 2026
  abv: "~14.5%"
  abv_percent: 14.5
recipe:
  - "Honey: 4 lbs Sample Clover"
  - "Fruit: 3 lbs Sample Raspberries (secondary)"
  - "Water: Fill to 1 gallon"
  - "Yeast: Sample High-ABV Strain"
  - "Nutrient: Sample Nutrient (staggered)"
gravity_log:
  - date: March 3, 2026
    reading: "1.110 OG"
  - date: April 20, 2026
    reading: "1.012"
  - date: August 1, 2026
    reading: "0.994"
---

[← Back to Dev Preview](../)

This page mimics the structure of a real batch page, using made-up data, so dev-cycle runs have
a realistic canvas to improve without ever touching real batch content.

**Prototype (see [steering notes](../FEEDBACK.html)):** a third sample batch, giving the
[all-batches index](../batches/) a spread of types and ABVs worth sorting.

{% include_relative _includes/batch-data.html %}

## Brewing Notes

- March 20, 2026 : Racked onto raspberries for secondary
- May 5, 2026 : Racked off fruit, back to bulk aging
- August 1, 2026 : Bottled
