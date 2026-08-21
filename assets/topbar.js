/* 이룬 서재 — 공통 상단바 렌더러
 *
 * 각 페이지에서 이렇게 부른다:
 *   <link rel="stylesheet" href="../assets/topbar.css">
 *   <script src="../assets/topbar.js" data-section="research" data-root="../"></script>
 *
 *   data-section : home | research | videos | guides | math   (현재 위치 표시)
 *   data-root    : 이 페이지에서 저장소 루트까지의 상대경로 ("./" 또는 "../")
 *
 * 스크립트는 자기 자신의 data-* 를 읽으므로 페이지마다 설정을 따로 두지 않는다.
 */
(function () {
  "use strict";

  var me = document.currentScript;
  if (!me) return;

  var section = me.dataset.section || "";
  var root = me.dataset.root || "./";

  var TABS = [
    { key: "home",     label: "홈",       href: "" },
    { key: "research", label: "리서치",   href: "research/" },
    { key: "videos",   label: "영상노트", href: "videos/" },
    { key: "guides",   label: "가이드",   href: "guides/" },
    { key: "math",     label: "수학사",   href: "math/" }
  ];

  function build() {
    var bar = document.createElement("div");
    bar.className = "itb";

    var inner = document.createElement("div");
    inner.className = "itb-in";

    var brand = document.createElement("a");
    brand.className = "itb-brand";
    brand.href = root;
    brand.innerHTML = '이룬 <span>서재</span>';
    inner.appendChild(brand);

    var nav = document.createElement("nav");
    nav.className = "itb-tabs";
    nav.setAttribute("aria-label", "서가");
    TABS.forEach(function (t) {
      var a = document.createElement("a");
      a.href = root + t.href;
      a.textContent = t.label;
      if (t.key === section) {
        a.className = "on";
        a.setAttribute("aria-current", "page");
      }
      nav.appendChild(a);
    });
    inner.appendChild(nav);

    /* 오른쪽 끝 '만든 사람' 마크. 서재 이름(왼쪽)과 역할이 다르므로
       색 계열도 일부러 다르다 — 자세한 규칙은 assets/brand.css 머리말. */
    var sig = document.createElement("a");
    sig.className = "itb-sig";
    sig.href = "https://github.com/irun20000-eng";
    sig.target = "_blank";
    sig.rel = "noopener";
    sig.title = "aftermath — 만든 사람";
    sig.innerHTML = '<span class="sig"><span class="af">after</span>'
                  + '<span class="m">math</span><span class="q"></span></span>';
    inner.appendChild(sig);

    bar.appendChild(inner);
    document.body.insertBefore(bar, document.body.firstChild);

    /* 페이지의 sticky 하위 바(리서치 .stickybar, 수학사 .viewbar)가
       상단바 바로 아래에 붙도록 높이를 CSS 변수로 알린다.
       모바일에서 탭이 다음 줄로 내려가면 높이가 달라지므로 리사이즈에도 갱신한다. */
    function measure() {
      document.documentElement.style.setProperty(
        "--itb-h", Math.round(bar.getBoundingClientRect().height) + "px");
    }
    measure();
    if (window.ResizeObserver) new ResizeObserver(measure).observe(bar);
    else window.addEventListener("resize", measure);
    // 웹폰트가 늦게 오면 높이가 한 번 더 바뀐다
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);

    // 스크롤하면 아래쪽 경계선을 드러낸다
    window.addEventListener("scroll", function () {
      bar.classList.toggle("stuck", window.scrollY > 4);
    }, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
