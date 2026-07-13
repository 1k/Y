/* 梓航城市发现之旅 · 交互脚本 (null-safe) */
(function () {
  'use strict';

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---- sticky header shadow ---- */
  var header = $('#siteHeader');
  function onScroll() {
    if (header) header.classList.toggle('scrolled', window.scrollY > 30);
    var btt = $('#back-to-top');
    if (btt) btt.classList.toggle('show', window.scrollY > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- back to top ---- */
  var btt = $('#back-to-top');
  if (btt) btt.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---- city directory drawer ---- */
  var dir = $('#cityDirectory');
  var toggle = $('#navToggle');
  var closeBtn = $('#directoryClose');
  var backdrop = $('#directoryBackdrop');

  function openDir() {
    if (!dir) return;
    dir.classList.add('open');
    dir.setAttribute('aria-hidden', 'false');
    if (toggle) toggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
  function closeDir() {
    if (!dir) return;
    dir.classList.remove('open');
    dir.setAttribute('aria-hidden', 'true');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
  if (toggle) toggle.addEventListener('click', openDir);
  if (closeBtn) closeBtn.addEventListener('click', closeDir);
  if (backdrop) backdrop.addEventListener('click', closeDir);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeDir(); closeSearch(); }
  });

  /* drawer links now point to real pages — just close on click */
  if (dir) {
    $all('a', dir).forEach(function (a) {
      a.addEventListener('click', function () { closeDir(); });
    });
  }

  /* ---- global search (typeahead) ---- */
  var searchInput = $('#siteSearch');
  var searchResults = $('#searchResults');
  var INDEX = window.SEARCH_INDEX || [];
  var activeIdx = -1;
  var current = [];

  function closeSearch() {
    if (searchResults) { searchResults.hidden = true; searchResults.innerHTML = ''; }
    if (searchInput) { searchInput.setAttribute('aria-expanded', 'false'); }
    activeIdx = -1;
  }

  function renderResults(q) {
    if (!searchResults) return;
    q = q.trim().toLowerCase();
    if (!q) { closeSearch(); return; }
    var scored = [];
    for (var i = 0; i < INDEX.length; i++) {
      var it = INDEX[i];
      var hay = (it.name + ' ' + (it.sub || '') + ' ' + (it.city || '') + ' ' + (it.region || '')).toLowerCase();
      var pos = hay.indexOf(q);
      if (pos === -1) continue;
      var rank = (it.name.toLowerCase().indexOf(q) === 0) ? 0 : (it.t === 'city' ? 1 : 2);
      scored.push({ it: it, rank: rank });
    }
    scored.sort(function (a, b) { return a.rank - b.rank; });
    current = scored.slice(0, 8).map(function (s) { return s.it; });

    if (!current.length) {
      searchResults.innerHTML = '<div class="search-empty">未找到相关城市或景点</div>';
      searchResults.hidden = false;
      searchInput.setAttribute('aria-expanded', 'true');
      return;
    }
    var html = '';
    for (var j = 0; j < current.length; j++) {
      var r = current[j];
      var type = r.t === 'city' ? '城市' : '景点';
      var sub = r.t === 'city' ? (r.region || '') : (r.city || '');
      html += '<a class="search-result" role="option" href="' + r.url + '">' +
        '<span class="sr-type">' + type + '</span>' +
        '<span class="sr-name">' + r.name + '</span>' +
        '<span class="sr-sub">' + (sub || '') + '</span></a>';
    }
    searchResults.innerHTML = html;
    searchResults.hidden = false;
    searchInput.setAttribute('aria-expanded', 'true');
    activeIdx = -1;
  }

  function setActive(idx) {
    var nodes = searchResults ? $all('.search-result', searchResults) : [];
    if (!nodes.length) return;
    if (idx < 0) idx = nodes.length - 1;
    if (idx >= nodes.length) idx = 0;
    nodes.forEach(function (n, i) { n.classList.toggle('active', i === idx); });
    activeIdx = idx;
  }

  if (searchInput && searchResults) {
    searchInput.addEventListener('input', function () { renderResults(this.value); });
    searchInput.addEventListener('focus', function () { if (this.value.trim()) renderResults(this.value); });
    searchInput.addEventListener('keydown', function (e) {
      if (searchResults.hidden) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(activeIdx + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(activeIdx - 1); }
      else if (e.key === 'Enter') {
        var nodes = $all('.search-result', searchResults);
        if (activeIdx >= 0 && nodes[activeIdx]) { e.preventDefault(); window.location.href = nodes[activeIdx].getAttribute('href'); }
      }
    });
    // close when clicking outside
    document.addEventListener('click', function (e) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) closeSearch();
    });
  }

  /* ---- reveal on scroll ---- */
  var reveals = $all('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }
})();
