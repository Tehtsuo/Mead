---
layout: dev-preview
title: All Batches (demo)
description: All Batches Index (prototype)
---

[← Back to Dev Preview](../)

**Prototype (see [steering notes](../FEEDBACK.html)):** step 2 of the structured-data direction —
an index page fed entirely by each [sample batch](../demo-batch/) page's own structured front
matter (`page.batch`), with no hand-typed table anywhere on this page. It collects every page
under `dev-preview/` that has a `batch:` field via `site.pages`, then renders it two ways below.
This is the kind of view that's basically impossible to keep in sync by hand once there's more
than a couple of batches — with structured data it's just a Liquid `sort`.

*(Real batch pages aren't structured this way yet — see the [scope note](../CHANGELOG.html) on
why this prototype lives here instead of a site-wide `_data/` collection.)*

{% assign all_batches = site.pages | where_exp: "p", "p.batch" %}

## By type

<table>
  <thead>
    <tr><th>Type</th><th>ABV</th><th>Start date</th><th>Bottling date</th><th></th></tr>
  </thead>
  <tbody>
{% assign by_type = all_batches | sort: "batch.type" %}
{% for p in by_type %}
    <tr>
      <td>{{ p.batch.type }}</td>
      <td>{{ p.batch.abv }}</td>
      <td>{{ p.batch.start_date }}</td>
      <td>{{ p.batch.bottling_date }}</td>
      <td><a href="{{ p.url | relative_url }}">View</a></td>
    </tr>
{% endfor %}
  </tbody>
</table>

## By ABV, highest first

<table>
  <thead>
    <tr><th>ABV</th><th>Type</th><th>Start date</th><th>Bottling date</th><th></th></tr>
  </thead>
  <tbody>
{% assign by_abv = all_batches | sort: "batch.abv_percent" | reverse %}
{% for p in by_abv %}
    <tr>
      <td>{{ p.batch.abv }}</td>
      <td>{{ p.batch.type }}</td>
      <td>{{ p.batch.start_date }}</td>
      <td>{{ p.batch.bottling_date }}</td>
      <td><a href="{{ p.url | relative_url }}">View</a></td>
    </tr>
{% endfor %}
  </tbody>
</table>
