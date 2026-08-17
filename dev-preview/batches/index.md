---
layout: dev-preview
title: All Batches (demo)
description: All Batches Index (prototype)
---

[← Back to Dev Preview](../)

**Prototype (see [steering notes](../FEEDBACK.html)):** step 2 of the structured-data direction —
an index page fed entirely by each [sample batch](../demo-batch/) page's own structured front
matter (`page.batch`), with no hand-typed table anywhere on this page. It collects every page
under `dev-preview/` that has a `batch:` field via `site.pages`, then renders one table below.
This is the kind of view that's basically impossible to keep in sync by hand once there's more
than a couple of batches — with structured data it's just a Liquid `sort`.

*(Real batch pages aren't structured this way yet — see the [scope note](../CHANGELOG.html) on
why this prototype lives here instead of a site-wide `_data/` collection.)*

Click a column header to sort by it; click again to reverse. This replaces the previous prototype's
two separate pre-sorted tables (by type, by ABV) with one table sortable by any column — the
server still renders it pre-sorted by type, so the page is still useful with JavaScript off.
Click a type chip below to narrow the table to just that type; click "All" to clear the filter.

{% assign all_batches = site.pages | where_exp: "p", "p.batch" | sort: "batch.type" %}
{% assign batch_type_groups = all_batches | group_by_exp: "p", "p.batch.type" | sort: "name" %}

<div class="filter-chips" role="group" aria-label="Filter batches by type">
  <button type="button" class="filter-chip is-active" data-filter-type="all" aria-pressed="true">All ({{ all_batches.size }})</button>
{% for group in batch_type_groups %}
  <button type="button" class="filter-chip" data-filter-type="{{ group.name | downcase }}" aria-pressed="false">{{ group.name }} ({{ group.items.size }})</button>
{% endfor %}
</div>

<table class="sortable-table" id="batches-table">
  <thead>
    <tr>
      <th scope="col" aria-sort="ascending"><button type="button" data-sort-key="type">Type</button></th>
      <th scope="col" aria-sort="none"><button type="button" data-sort-key="abv" data-sort-type="number">ABV</button></th>
      <th scope="col" aria-sort="none"><button type="button" data-sort-key="start" data-sort-type="number">Start date</button></th>
      <th scope="col" aria-sort="none"><button type="button" data-sort-key="bottling" data-sort-type="number">Bottling date</button></th>
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
{% for p in all_batches %}
    <tr data-type="{{ p.batch.type | downcase }}" data-abv="{{ p.batch.abv_percent }}" data-start="{{ p.batch.start_date | date: '%s' }}" data-bottling="{{ p.batch.bottling_date | date: '%s' }}">
      <td>{{ p.batch.type }}</td>
      <td>{{ p.batch.abv }}</td>
      <td>{{ p.batch.start_date }}</td>
      <td>{{ p.batch.bottling_date }}</td>
      <td><a href="{{ p.url | relative_url }}">View</a></td>
    </tr>
{% endfor %}
  </tbody>
</table>

<script>
(function () {
  var table = document.getElementById('batches-table');
  if (!table) return;
  var tbody = table.tBodies[0];
  var headers = table.querySelectorAll('th button[data-sort-key]');

  headers.forEach(function (button) {
    button.addEventListener('click', function () {
      var key = button.getAttribute('data-sort-key');
      var isNumber = button.getAttribute('data-sort-type') === 'number';
      var th = button.closest('th');
      var wasAscending = th.getAttribute('aria-sort') === 'ascending';
      var ascending = !wasAscending;

      var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
      rows.sort(function (rowA, rowB) {
        var a = rowA.getAttribute('data-' + key);
        var b = rowB.getAttribute('data-' + key);
        if (isNumber) {
          a = parseFloat(a);
          b = parseFloat(b);
        }
        if (a < b) return ascending ? -1 : 1;
        if (a > b) return ascending ? 1 : -1;
        return 0;
      });
      rows.forEach(function (row) { tbody.appendChild(row); });

      headers.forEach(function (otherButton) {
        otherButton.closest('th').setAttribute('aria-sort', 'none');
      });
      th.setAttribute('aria-sort', ascending ? 'ascending' : 'descending');
    });
  });

  var filterChips = document.querySelectorAll('.filter-chip[data-filter-type]');
  filterChips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var filterType = chip.getAttribute('data-filter-type');

      filterChips.forEach(function (c) {
        c.classList.remove('is-active');
        c.setAttribute('aria-pressed', 'false');
      });
      chip.classList.add('is-active');
      chip.setAttribute('aria-pressed', 'true');

      var rows = tbody.querySelectorAll('tr');
      rows.forEach(function (row) {
        var show = filterType === 'all' || row.getAttribute('data-type') === filterType;
        row.style.display = show ? '' : 'none';
      });
    });
  });
})();
</script>
