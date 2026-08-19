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
Type the search box to narrow further by name — search and the type filter compose (e.g. filter to
Melomel, then search "ember" within just that type). Each batch's own page title (e.g. "TRM Grotto
Ember", matching the real site's naming) is now the first column and the row's link, so a row
identifies itself without needing to click through. A fourth sample batch,
[demo-batch-4](../demo-batch-4/), is still **in progress** — no bottling date or ABV yet, just like
several real batches on the live site — so those columns show "In progress" instead of a blank
cell, and sort after every batch that has a real value.

The stat tiles below are the other half of FEEDBACK.md's original rationale for this whole
direction — "no way to compute stats across batches" — rendered entirely from the same
`all_batches` collection the table already uses, no separate data source.

{% assign all_batches = site.pages | where_exp: "p", "p.batch" | sort: "batch.type" %}
{% assign batch_type_groups = all_batches | group_by_exp: "p", "p.batch.type" | sort: "name" %}
{% assign finished_batches = all_batches | where_exp: "p", "p.batch.abv_percent" %}
{% assign in_progress_count = all_batches.size | minus: finished_batches.size %}
{% assign abv_total = 0 %}
{% for p in finished_batches %}{% assign abv_total = abv_total | plus: p.batch.abv_percent %}{% endfor %}
{% if finished_batches.size > 0 %}{% assign avg_abv = abv_total | plus: 0.0 | divided_by: finished_batches.size | round: 1 %}{% endif %}

<div class="batch-stats">
  <div class="batch-stat">
    <span class="batch-stat-value">{{ all_batches.size }}</span>
    <span class="batch-stat-label">Total batches</span>
  </div>
  <div class="batch-stat">
    <span class="batch-stat-value">{{ finished_batches.size }}</span>
    <span class="batch-stat-label">Finished</span>
  </div>
  <div class="batch-stat">
    <span class="batch-stat-value">{{ in_progress_count }}</span>
    <span class="batch-stat-label">In progress</span>
  </div>
  <div class="batch-stat">
    <span class="batch-stat-value">{% if avg_abv %}{{ avg_abv }}%{% else %}—{% endif %}</span>
    <span class="batch-stat-label">Avg. ABV (finished)</span>
  </div>
</div>

<div class="batches-toolbar">
  <input type="search" id="batch-search" class="batch-search" placeholder="Search batches by name…" aria-label="Search batches by name">

  <div class="filter-chips" role="group" aria-label="Filter batches by type">
    <button type="button" class="filter-chip is-active" data-filter-type="all" aria-pressed="true">All ({{ all_batches.size }})</button>
{% for group in batch_type_groups %}
    <button type="button" class="filter-chip" data-filter-type="{{ group.name | downcase }}" aria-pressed="false">{{ group.name }} ({{ group.items.size }})</button>
{% endfor %}
  </div>
</div>

<table class="sortable-table" id="batches-table">
  <thead>
    <tr>
      <th scope="col" aria-sort="none"><button type="button" data-sort-key="name">Name</button></th>
      <th scope="col" aria-sort="ascending"><button type="button" data-sort-key="type">Type</button></th>
      <th scope="col" aria-sort="none"><button type="button" data-sort-key="abv" data-sort-type="number">ABV</button></th>
      <th scope="col" aria-sort="none"><button type="button" data-sort-key="start" data-sort-type="number">Start date</button></th>
      <th scope="col" aria-sort="none"><button type="button" data-sort-key="bottling" data-sort-type="number">Bottling date</button></th>
    </tr>
  </thead>
  <tbody>
{% for p in all_batches %}
    <tr data-type="{{ p.batch.type | downcase }}" data-name="{{ p.title | downcase }}" data-abv="{{ p.batch.abv_percent }}" data-start="{{ p.batch.start_date | date: '%s' }}" data-bottling="{% if p.batch.bottling_date %}{{ p.batch.bottling_date | date: '%s' }}{% endif %}">
      <td><a href="{{ p.url | relative_url }}">{{ p.title }}</a></td>
      <td>{{ p.batch.type }}</td>
      <td>{% if p.batch.abv %}{{ p.batch.abv }}{% else %}<em class="batch-in-progress">In progress</em>{% endif %}</td>
      <td>{{ p.batch.start_date }}</td>
      <td>{% if p.batch.bottling_date %}{{ p.batch.bottling_date }}{% else %}<em class="batch-in-progress">In progress</em>{% endif %}</td>
    </tr>
{% endfor %}
  </tbody>
</table>

<p id="batches-empty-msg" class="batches-empty" hidden>No batches match your search and filter.</p>

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
          // Missing values (in-progress batches: no ABV/bottling date yet) always sort
          // last, in either sort direction, instead of comparing as NaN.
          var aMissing = a === '';
          var bMissing = b === '';
          if (aMissing && bMissing) return 0;
          if (aMissing) return 1;
          if (bMissing) return -1;
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
  var searchInput = document.getElementById('batch-search');
  var emptyMsg = document.getElementById('batches-empty-msg');
  var activeType = 'all';

  function applyFilters() {
    var query = searchInput ? searchInput.value.trim().toLowerCase() : '';
    var visibleCount = 0;

    var rows = tbody.querySelectorAll('tr');
    rows.forEach(function (row) {
      var matchesType = activeType === 'all' || row.getAttribute('data-type') === activeType;
      var matchesSearch = !query || row.getAttribute('data-name').indexOf(query) !== -1;
      var show = matchesType && matchesSearch;
      row.style.display = show ? '' : 'none';
      if (show) visibleCount++;
    });

    if (emptyMsg) emptyMsg.hidden = visibleCount !== 0;
  }

  filterChips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      activeType = chip.getAttribute('data-filter-type');

      filterChips.forEach(function (c) {
        c.classList.remove('is-active');
        c.setAttribute('aria-pressed', 'false');
      });
      chip.classList.add('is-active');
      chip.setAttribute('aria-pressed', 'true');

      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }
})();
</script>
