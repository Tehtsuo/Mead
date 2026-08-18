---
layout: dev-preview
title: TRM Sample Batch 4 (fake data, in progress)
description: TRM Sample Batch 4 (fake data, in progress)
batch:
  type: Pyment
  start_date: July 20, 2026
recipe:
  - "Honey: 2 lbs Sample Wildflower"
  - "Fruit: ~90 oz Sample Grape Juice"
  - "Yeast: Sample Bread Yeast"
  - "Nutrient:"
  - "Fruit / Spice:"
gravity_log:
  - date: July 20, 2026
    reading: "1.090 OG"
---

[← Back to Dev Preview](../)

This page mimics the structure of a real batch page, using made-up data, so dev-cycle runs have
a realistic canvas to improve without ever touching real batch content.

**Prototype (see [steering notes](../FEEDBACK.html)):** a fourth sample batch, deliberately
**still in progress** — like several real batches on the live site (e.g. "TRM Grotto Ember"),
this one only has a start date logged so far; `bottling_date` and `abv` are simply absent from
its front matter rather than filled in with placeholder values. This is the case the first three
samples didn't cover: every real batch starts this way and stays this way for weeks or months, so
the structured-data prototype needs to render it sensibly, not just the tidy "finished" case.

{% include_relative _includes/batch-data.html %}

## Brewing Notes

- July 20, 2026 : Pitched yeast, fermentation active within 24 hours
