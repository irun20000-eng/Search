/* 담기함 — 서가를 넘나드는 공용 모듈
 *
 * 왜 서가를 넘나드나: GitHub Pages 는 리포가 달라도 오리진이 하나라
 * (irun20000-eng.github.io) localStorage 가 전부 공유된다. 테마(stTheme)가
 * 이미 그 방식으로 서가를 넘나들고 있다. 그래서 리서치 3편 + 수학사 2편 +
 * 블로그 1편을 한 담기함에 담아 한 번에 인쇄할 수 있다.
 *
 * 쓰는 법 (각 갤러리에서):
 *   <link rel="stylesheet" href="../assets/basket.css">
 *   <script src="../assets/basket.js"></script>
 *   Basket.init({section:"blog", root:"../"});
 *   Basket.button({k:slug, t:title, p:"blog/notes/x.md", kind:"md"})  → 버튼 HTML
 *
 * 항목 모양 — 저장 용량을 아끼려고 짧은 키를 쓴다.
 *   k 식별자 · t 제목 · s 서가 · u 열람 URL(루트 기준) · p 본문 경로(루트 기준) · kind 렌더 방식
 */
(function (global) {
  "use strict";

  var KEY = "stBasket";
  var MAX = 60;                    // 인쇄 한 장에 담을 만한 상한
  var LABEL = {
    research: "리서치", videos: "영상노트", guides: "가이드", math: "수학사",
    blog: "블로그", cardnews: "카드뉴스", concept: "개념노트"
  };

  var cfg = { section: "", root: "./" };
  var items = [];
  var listeners = [];

  function load() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }
  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {}
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function idOf(it) { return it.s + "::" + it.k; }
  function indexOf(it) {
    var id = idOf(it);
    for (var i = 0; i < items.length; i++) if (idOf(items[i]) === id) return i;
    return -1;
  }

  function emit() {
    listeners.forEach(function (fn) { try { fn(items.slice()); } catch (e) {} });
    paint();
  }

  /* ── 공개 API ── */

  function has(k) { return indexOf({ s: cfg.section, k: k }) >= 0; }

  function toggle(it) {
    it = Object.assign({ s: cfg.section }, it);
    var i = indexOf(it);
    if (i >= 0) { items.splice(i, 1); }
    else {
      if (items.length >= MAX) { toast("담기함이 가득 찼습니다 (" + MAX + "개)"); return false; }
      items.push(it);
    }
    persist(); emit();
    return i < 0;
  }

  function clear() { items = []; persist(); emit(); }

  function button(it) {
    /* 카드 안에 넣는 버튼. 카드 전체가 클릭 대상인 경우가 많아
       stopPropagation 은 호출부가 아니라 여기서 처리한다. */
    var on = has(it.k);
    return '<button type="button" class="bskt-add' + (on ? " on" : "") +
      '" data-bk="' + esc(it.k) + '" title="담기함에 넣기" aria-pressed="' + on + '">' +
      (on ? "담김" : "담기") + "</button>";
  }

  function wire(container, lookup) {
    /* lookup(k) → {t, p, u, kind} 를 돌려주는 함수 */
    (container || document).querySelectorAll(".bskt-add").forEach(function (b) {
      if (b.__bskt) return;
      b.__bskt = 1;
      b.addEventListener("click", function (ev) {
        ev.preventDefault(); ev.stopPropagation();
        var k = b.dataset.bk, meta = lookup(k);
        if (!meta) return;
        var added = toggle(Object.assign({ k: k }, meta));
        b.classList.toggle("on", added);
        b.setAttribute("aria-pressed", String(added));
        b.textContent = added ? "담김" : "담기";
        toast(added ? "담았습니다" : "뺐습니다");
      });
    });
  }

  /* 카드 안에 담기 버튼을 넣으려면 카드가 <button> 이면 안 된다 —
     HTML 파서가 중첩 <button> 을 만나면 바깥 버튼을 닫아 버려서 담기 버튼이
     카드 밖으로 튕겨 나간다(2026-08-22 에 실제로 이렇게 깨졌다).
     그래서 카드를 div[role=button] 으로 두고, 잃어버린 키보드 동작을 여기서 되돌린다. */
  function keyable(root, sel) {
    (root || document).querySelectorAll(sel).forEach(function (el) {
      if (el.__kb) return;
      el.__kb = 1;
      el.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); el.click(); }
      });
    });
  }

  /* ── 떠 있는 담기함 ── */

  function ensureUI() {
    if (document.getElementById("bskt-fab")) return;
    var fab = document.createElement("button");
    fab.id = "bskt-fab"; fab.className = "bskt-fab";
    fab.innerHTML = '🧺 담기함 <span class="n" id="bskt-n">0</span>';
    fab.addEventListener("click", function () {
      document.getElementById("bskt-panel").classList.toggle("open");
    });
    var panel = document.createElement("div");
    panel.id = "bskt-panel"; panel.className = "bskt-panel";
    panel.innerHTML =
      '<div class="bskt-h"><b>담기함</b><span id="bskt-sum"></span></div>' +
      '<div class="bskt-list" id="bskt-list"></div>' +
      '<div class="bskt-foot">' +
      '  <button class="bskt-btn" id="bskt-print">인쇄·모아보기</button>' +
      '  <button class="bskt-btn ghost" id="bskt-clear">비우기</button>' +
      "</div>";
    document.body.appendChild(fab);
    document.body.appendChild(panel);
    document.getElementById("bskt-clear").addEventListener("click", function () {
      if (items.length && !confirm("담기함을 비울까요?")) return;
      clear();
    });
    document.getElementById("bskt-print").addEventListener("click", function () {
      if (!items.length) { toast("담기함이 비어 있습니다"); return; }
      location.href = cfg.root + "print.html";
    });
    /* 다른 탭·다른 서가에서 담으면 여기도 따라간다 */
    global.addEventListener("storage", function (e) {
      if (e.key === KEY) { items = load(); emit(); }
    });
  }

  function paint() {
    var n = document.getElementById("bskt-n");
    if (!n) return;
    n.textContent = items.length;
    document.getElementById("bskt-fab").classList.toggle("has", items.length > 0);
    var by = {};
    items.forEach(function (i) { by[i.s] = (by[i.s] || 0) + 1; });
    document.getElementById("bskt-sum").textContent =
      items.length
        ? Object.keys(by).map(function (s) { return (LABEL[s] || s) + " " + by[s]; }).join(" · ")
        : "";
    document.getElementById("bskt-list").innerHTML = items.length
      ? items.map(function (i, idx) {
          return '<div class="bskt-row"><span class="sec">' + esc(LABEL[i.s] || i.s) +
            '</span><span class="t">' + esc(i.t) + "</span>" +
            '<button class="rm" data-i="' + idx + '" aria-label="빼기">✕</button></div>';
        }).join("")
      : '<p class="bskt-empty">서가에서 <b>담기</b>를 눌러 모아 보세요.<br>서가가 달라도 한곳에 담깁니다.</p>';
    document.querySelectorAll("#bskt-list .rm").forEach(function (b) {
      b.addEventListener("click", function () {
        items.splice(+b.dataset.i, 1); persist(); emit();
        document.querySelectorAll(".bskt-add").forEach(function (x) {
          var on = has(x.dataset.bk);
          x.classList.toggle("on", on);
          x.textContent = on ? "담김" : "담기";
        });
      });
    });
  }

  var toastEl = null, toastT = null;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "bskt-toast";
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add("on");
    clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove("on"); }, 1600);
  }

  function init(o) {
    cfg = Object.assign(cfg, o || {});
    items = load();
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () { ensureUI(); emit(); });
    } else { ensureUI(); emit(); }
  }

  global.Basket = {
    init: init, has: has, toggle: toggle, clear: clear,
    button: button, wire: wire, keyable: keyable,
    all: function () { return items.slice(); },
    onChange: function (fn) { listeners.push(fn); },
    LABEL: LABEL, KEY: KEY
  };
})(window);
