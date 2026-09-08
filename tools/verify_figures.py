#!/usr/bin/env python3
"""도해(SVG)가 실제로 그려지는지 브라우저로 잰다 — math/assets/figures/*.svg.

왜 브라우저인가.
    좌표만 읽어서는 「지면 밖으로 나갔는가」밖에 못 본다. 글자 폭을 모르기 때문이다.
    이 파일이 생기기 전에는 세션에서 그때그때 어림 계산(글자당 0.62 × font-size)을
    썼는데 — 리포에 있던 도구가 아니라 일회용 스크립트였다 — 라틴 문자엔 맞지만
    한글은 실측 약 0.99 배라 글자당 38% 짧게 잡혔고, 실제로 46px 잘려 있던 캡션을
    「경계 밖 0건」으로 통과시켰다(leibniz-characteristic-triangle, 2026-09-08).
    갤러리는 브라우저로 그리므로 재는 것도 브라우저여야 한다 —
    `getBBox()` + `getCTM()` 이 정본이다.

    cairosvg 로도 그림은 볼 수 있지만 **판정에는 쓰지 말 것.** `text-anchor="middle"`
    인 글자가 `<tspan>` 으로 나뉘면 조각마다 따로 가운데 정렬해서, 멀쩡한 수식을
    겹쳐 그린다(vibrating-string-initial-shape 에서 `u(x, 0) = …` 이
    `)u(xa · sin…` 으로 보였다). 없는 결함을 만들어 낸다.

무엇을 재나.
    1. 넘침 — 글자의 실제 경계상자가 viewBox 밖으로 나가는가.
    2. 겹침 — 글자끼리 경계상자가 겹치는가(가로·세로 각각 하한, 회전 라벨 포함).
    3. 관통 — 그려진 잉크가 글자 상자 **안쪽**을 지나는가. 2026-09-09 에
       접선과 할선이 `P` 라벨 한복판을 지나갔는데 1·2 만 보던 이 검사기가 통과시켰다.
       상자 가장자리를 스치는 것은 정상(라벨은 대개 선 옆에 붙는다)이므로 안쪽으로
       INSET 만큼 줄여서 잰다.
       ⚠ **기하만으로는 오탐이 난다.** 뒤에 그린 불투명 도형에 가려 화면에는 안 보이는
       선이 있다(라이프니츠의 확대 상자가 지시선을 덮는다). 그래서 교차점에서
       `elementsFromPoint` 로 **그 선이 실제로 맨 위에 그려지는지**까지 확인한다.
       그 히트 테스트에는 함정이 셋 있고 셋 다 실제로 물렸다 —
       ① 글자는 상자 전체가 걸리므로 스택에서 걷어내야 한다(안 그러면 진짜를 못 잡는다),
       ② 점선은 **틈**에서 아무것도 안 걸린다 → 잴 때만 `stroke-dasharray` 를 끈다
          (안 그러면 위상 운으로 놓친다 — `5 4` 에서 offset 6·8 이 통째로 빗나갔다),
       ③ 반투명 도형은 **가리지 못한다** → 실효 알파 0.5 미만은 차단으로 세지 않는다.
       그리고 `line`·`polyline` 만 보면 리포 잉크의 절반을 놓친다(`dice-sum-grid` 는
       전부 `<rect>`, `descartes` 의 컴퍼스는 `<path>`) → 기하 요소를 **길이로 훑는다**.
    4. 가려짐 — 불투명 도형이 글자 **위**에 그려졌는가. 3 의 거울상이고, 2026-09-08 에
       라이프니츠의 확대 상자가 곡선을 21px 덮은 것과 같은 유형이다(그때는 곡선이었다).
       ⚠ **그 점에 글자가 실제로 그려져 있을 때만 판정한다.** 「글자보다 앞에 불투명 도형이
       있나」만 보면, 표본이 글자에 안 닿는 자리에서 스택에 글자가 아예 없어 **배경 rect** 가
       맨 앞으로 잡힌다 — 처음에 그렇게 짜서 11장 라벨 124개가 전부 걸렸다.

       마지막으로 **옅은 잉크는 세지 않는다.** 배경과 대비가 낮은 격자선이 라벨 밑을
       지나는 것은 정상 배치다(`descartes` 의 #EDE4D4 격자). 지면색과의 명암비가
       MIN_CONTRAST 미만이면 건너뛴다 — 안 그러면 정상 도해가 FAIL 로 뜬다.
    회전·translate 는 `getCTM()` 으로 루트 좌표계에 옮겨 놓고 잰다. 이걸 빼먹으면
    회전 라벨이 전부 오탐으로 뜬다(getBBox 는 변환 전 좌표를 준다).

못 재는 것.
    그림이 **옳은가**는 못 잰다. 컴퍼스 두 다리가 둘 다 중심에서 나오거나, 「확대도」의
    삼각형 비가 원본과 다르거나, **할선과 접선의 대소가 본문 주장과 반대**인 것은
    사람이 봐야 한다. 마지막 것은 2026-09-09 에 실제로 났다 — 곡선을 오목으로 그리면
    할선이 접선보다 **언제나** 완만해지는데, 본문은 `2x+e > 2x` 를 계산하고 있었다.
    이 검사기는 그 앞단의 값싼 그물이지 대신이 아니다.

쓰기.
    python3 tools/verify_figures.py            # math/assets/figures/*.svg 전부
    python3 tools/verify_figures.py <파일…>    # 지정한 것만
    python3 tools/verify_figures.py --allow-skip  # 브라우저가 없어도 exit 0
    브라우저가 없으면 **exit 2** 로 나간다 — 「검사를 안 했다」와 「검사해서 통과했다」는
    다르고, exit 0 으로 나가면 그 둘이 같아진다. 정말 건너뛰어도 좋은 자리에서만
    `--allow-skip` 을 준다(그때는 exit 0).
"""
import glob
import pathlib
import re
import sys

FIGURE_DIR = 'math/assets/figures'
# 브라우저 경로를 버전에 못 박지 않는다. 이 러너의 이미지가 올라가면 디렉터리 이름이
# 바뀌는데(chromium-1194 → …), 못 박아 두면 그날부터 검사기가 조용히 건너뛴다.
CHROME_GLOBS = (
    '/opt/pw-browsers/chromium-*/chrome-linux/chrome',
    '/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell',
)
# 겹침으로 셀 최소 폭·높이(px). 가로·세로 **둘 다** 넘을 때만 센다.
#   면적 하나로 재면 감도가 균일하지 않다 — 긴 캡션 둘이 스치기만 해도 면적이 커지고,
#   짧은 라벨 둘이 진짜로 겹쳐도 면적이 작다. 서로 다른 <text> 사이에는 커닝이 없으므로
#   이 여유는 커닝이 아니라 글자 상자의 사이드베어링(실제 잉크보다 넓은 AABB) 몫이다.
OVERLAP_MIN_W = 1.5
OVERLAP_MIN_H = 1.5
# 관통 판정에서 글자 상자를 안쪽으로 줄이는 양. 라벨은 대개 선 옆에 붙으므로 가장자리를
# 스치는 것은 정상이고, 「한복판을 지나는가」만 결함으로 센다.
#   비율만 쓰면 감도가 라벨 크기에 좌우된다 — 408px 캡션은 가장자리에서 114px 안쪽까지
#   들어와야 잡히고 7px 라벨은 2px 만 비켜도 통과한다. 그래서 둘 중 **작은 쪽**을 쓴다.
TEXT_INSET_RATIO = 0.25
TEXT_INSET_MAX = 2.0
# 관통으로 셀 최소 명암비(WCAG, 지면색 대비). 옅은 격자선이 라벨 밑을 지나는 것은
# 읽기를 해치지 않는 정상 배치다 — #EDE4D4 격자가 지면 #FFFDF7 대비 1.24 다.
#   문턱을 1.5 로 두면 격자만이 아니라 **구조선**까지 빠진다 — 확대 상자 테두리 #DED3C0(1.46),
#   패널 구분선 #E2DACB(1.37). 그것들은 배경이 아니라 구역을 나누는 선이라 라벨이 걸치면
#   눈에 띈다. 1.30 이면 격자(1.24)만 빠지고 둘은 감시 안에 남는다.
MIN_CONTRAST = 1.30

MEASURE_JS = """({ vb, RATIO, MAXIN, MINC }) => {
  const [X0, Y0, W, H] = vb;
  const X1 = X0 + W, Y1 = Y0 + H;
  const svg = document.querySelector('svg');
  const root = svg.getScreenCTM().inverse();
  const boxes = [], textEls = [];
  for (const el of svg.querySelectorAll('text')) {
    const t = (el.textContent || '').replace(/\\s+/g, ' ').trim();
    if (!t) continue;
    const b = el.getBBox();
    const m = root.multiply(el.getScreenCTM());   // 루트 viewBox 좌표계로
    const pts = [[b.x, b.y], [b.x + b.width, b.y],
                 [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]]
      .map(([x, y]) => ({ x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f }));
    textEls.push(el);
    boxes.push({
      t: t.slice(0, 30),
      x0: Math.min(...pts.map(p => p.x)), x1: Math.max(...pts.map(p => p.x)),
      y0: Math.min(...pts.map(p => p.y)), y1: Math.max(...pts.map(p => p.y)),
    });
  }
  const over = boxes.filter(b => b.x0 < X0 - 0.5 || b.x1 > X1 + 0.5
                            || b.y0 < Y0 - 0.5 || b.y1 > Y1 + 0.5);
  const hits = [];
  for (let i = 0; i < boxes.length; i++)
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], c = boxes[j];
      const w = Math.min(a.x1, c.x1) - Math.max(a.x0, c.x0);
      const h = Math.min(a.y1, c.y1) - Math.max(a.y0, c.y0);
      if (w > 0 && h > 0) hits.push({ a: a.t, b: c.t, w: w, h: h, area: w * h });
    }
  // 관통 — 그려진 잉크가 글자 상자 안쪽을 지나는가.
  //   line/polyline 만 보면 리포 잉크의 절반을 놓치므로 기하 요소를 전부 훑고,
  //   세그먼트 수식 대신 getTotalLength()/getPointAtLength() 로 윤곽을 표본한다.
  //   (rect 는 윤곽 = 테두리이므로 배경 rect 가 안쪽 글자를 「관통」으로 잡지 않는다.)
  const geoms = [];
  for (const el of svg.querySelectorAll('line, polyline, polygon, path, rect, circle, ellipse')) {
    let L = 0;
    try { L = el.getTotalLength(); } catch (e) { continue; }
    if (!(L > 0)) continue;
    const cs0 = getComputedStyle(el);
    if (cs0.visibility === 'hidden' || cs0.display === 'none') continue;
    if (cs0.stroke === 'none' && cs0.fill === 'none') continue;
    const m = root.multiply(el.getScreenCTM());
    // 표본 「개수」에 상한을 두면 긴 경로에서 간격이 벌어져 좁은 상자를 통과한다.
    // 간격을 0.5px 로 고정하고, 총 작업량에만 상한을 둔다.
    const n = Math.min(40000, Math.max(40, Math.ceil(L / 0.5)));
    const pts = [];
    for (let k = 0; k <= n; k++) {
      const q = el.getPointAtLength(L * k / n);
      pts.push({ x: m.a * q.x + m.c * q.y + m.e, y: m.b * q.x + m.d * q.y + m.f });
    }
    // 굵은 선은 중심선이 상자 밖이어도 잉크가 안에 들어온다. 반폭만큼 넓혀서 잰다.
    const hw = (parseFloat(cs0.strokeWidth) || 0) / 2;
    geoms.push({ el, pts, hw });
  }
  const scr = svg.getScreenCTM();   // 루트 viewBox → client 좌표. elementsFromPoint 가
                                    // 쓰는 좌표계와 같다(스크롤·확대까지 반영된다).
  // 지면색 — 첫 <rect> 의 fill 을 지면으로 본다(도해 11장 모두 그 형태다).
  // 없으면 math 서가의 지면색으로 떨어지는데, 그 값이 지금 지면색과 같아 실패가 조용하다.
  const bgEl = svg.querySelector('rect');
  const parseRGB = (c) => {
    const m = /rgba?\(([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?/.exec(c || '');
    return m ? [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]] : null;
  };
  const BG = (bgEl && parseRGB(getComputedStyle(bgEl).fill)) || [255, 253, 247, 1];
  const lum = (c) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
  };
  const inkContrast = (el) => {
    const cs = getComputedStyle(el);
    const useStroke = cs.stroke && cs.stroke !== 'none';
    const c = parseRGB(useStroke ? cs.stroke : cs.fill);
    if (!c) return 0;
    // 읽은 쪽의 불투명도를 곱해야 한다. fill 을 읽고 strokeOpacity 를 곱하면
    // 채움만 반투명한 도형(hyperbola 의 음영: fill-opacity 0.16, stroke none)이
    // 완전 불투명 잉크로 채점된다.
    const own = parseFloat(useStroke ? cs.strokeOpacity : cs.fillOpacity);
    const a = c[3] * (isNaN(own) ? 1 : own) * (parseFloat(cs.opacity) || 1);
    const over = [0, 1, 2].map(i => c[i] * a + BG[i] * (1 - a));   // 지면 위에 합성
    const l1 = Math.max(lum(over), lum(BG)), l2 = Math.min(lum(over), lum(BG));
    return (l1 + 0.05) / (l2 + 0.05);
  };
  const opaqueEnough = (e) => {
    const cs = getComputedStyle(e);
    if (cs.fill === 'none' || !cs.fill) return false;
    const a = (parseFloat(cs.fillOpacity) || 0) * (parseFloat(cs.opacity) || 0);
    return a >= 0.5;   // 반투명은 아래 잉크를 가리지 못한다
  };
  const crossed = [];
  for (const b of boxes) {
    const iw = Math.min((b.x1 - b.x0) * RATIO, MAXIN);
    const ih = Math.min((b.y1 - b.y0) * RATIO, MAXIN);
    const r = { x0: b.x0 + iw, x1: b.x1 - iw, y0: b.y0 + ih, y1: b.y1 - ih };
    if (r.x1 <= r.x0 || r.y1 <= r.y0) continue;
    let done = false;
    for (const g of geoms) {
      if (done) break;
      const h = g.hw;
      const inside = g.pts.filter(q => q.x >= r.x0 - h && q.x <= r.x1 + h
                                    && q.y >= r.y0 - h && q.y <= r.y1 + h);
      if (!inside.length) continue;
      if (inkContrast(g.el) < MINC) continue;   // 옅은 격자선은 읽기를 해치지 않는다
      // 화면에서도 보이나 — 점선의 틈에서는 아무것도 안 걸리므로 잴 때만 실선으로 둔다
      const keep = g.el.style.strokeDasharray;
      g.el.style.strokeDasharray = 'none';
      const step = Math.max(1, Math.floor(inside.length / 16));
      for (let k = 0; k < inside.length && !done; k += step) {
        const u = inside[k];
        const cx = scr.a * u.x + scr.c * u.y + scr.e;
        const cy = scr.b * u.x + scr.d * u.y + scr.f;
        let blocked = false, seen = false;
        for (const e of document.elementsFromPoint(cx, cy)) {
          if (e === g.el) { seen = true; break; }
          if (e.tagName === 'text' || e.tagName === 'tspan') continue;
          if (opaqueEnough(e)) { blocked = true; break; }
        }
        if (seen && !blocked) { crossed.push({ t: b.t, by: g.el.tagName }); done = true; }
      }
      g.el.style.strokeDasharray = keep;
    }
  }
  // 가려짐 — 불투명 도형이 글자 **위**에 그려졌는가 (관통의 거울상)
  //   ⚠ 「글자보다 앞에 불투명 도형이 있나」만 보면 안 된다. 표본이 글자에 안 닿는
  //   자리(상자 가장자리)에서는 스택에 글자가 아예 없고, 그러면 **배경 rect** 가 맨 앞에
  //   잡혀 전부 가려진 것으로 센다(처음에 그렇게 짜서 11장 124건이 떴다).
  //   그 점에 **글자가 실제로 그려져 있을 때만** 판정한다.
  const covered = [];
  for (let bi = 0; bi < boxes.length; bi++) {
    const b = boxes[bi], tEl = textEls[bi];
    let hit = false;
    // 가장자리까지 훑는다 — 테두리대만 덮인 글자를 놓치지 않기 위해서다.
    // 가장자리 표본은 글자에 안 닿기 쉬운데, 그 자리는 아래에서 걸러진다.
    for (let i = 0; i <= 8 && !hit; i++)
      for (let j = 0; j <= 5 && !hit; j++) {
        const ux = b.x0 + (b.x1 - b.x0) * (i / 8);
        const uy = b.y0 + (b.y1 - b.y0) * (j / 5);
        const cx = scr.a * ux + scr.c * uy + scr.e;
        const cy = scr.b * ux + scr.d * uy + scr.f;
        const stack = document.elementsFromPoint(cx, cy);
        const ti = stack.indexOf(tEl);
        if (ti < 0) continue;                 // 이 점에는 글자가 없다 — 판정하지 않는다
        for (let k = 0; k < ti; k++) {
          const e = stack[k];
          if (e.tagName === 'text' || e.tagName === 'tspan') continue;
          if (opaqueEnough(e)) { covered.push({ t: b.t, by: e.tagName }); hit = true; break; }
        }
      }
  }
  return { over, hits, crossed, covered, n: boxes.length };
}"""


def find_chrome():
    """설치된 브라우저 중 버전이 가장 높은 것. 사전순으로 고르면 안 된다 —
    chromium-999 가 chromium-1234 를 이긴다."""
    def version(path):
        m = re.search(r'-(\d+)/', path)
        return int(m.group(1)) if m else -1
    for pattern in CHROME_GLOBS:
        found = glob.glob(pattern)
        if found:
            return max(found, key=version)
    return None


def main(argv):
    args = [a for a in argv[1:] if a != '--allow-skip']
    allow_skip = '--allow-skip' in argv[1:]
    skip = 0 if allow_skip else 2

    files = args or sorted(glob.glob(f'{FIGURE_DIR}/*.svg'))
    if not files:
        print(f'검사할 SVG 가 없다: {FIGURE_DIR}')
        return 0
    missing = [f for f in files if not pathlib.Path(f).is_file()]
    if missing:
        print('FAIL — 파일이 없다: ' + ', '.join(missing))
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('[건너뜀] playwright 가 없다 — 도해 렌더 검사를 하지 않았다.')
        print('         설치: pip install playwright  (브라우저가 이미 있으면 받지 않아도 된다)')
        return skip
    chrome = find_chrome()
    if chrome is None:
        print('[건너뜀] 브라우저를 찾지 못했다 — 도해 렌더 검사를 하지 않았다.')
        print('         찾은 자리: ' + ' · '.join(CHROME_GLOBS))
        return skip

    fails = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome)
        page = browser.new_page()
        for f in files:
            src = pathlib.Path(f).read_text(encoding='utf-8')
            m = re.search(r'viewBox="([^"]+)"', src)
            name = pathlib.Path(f).stem
            if not m:
                print(f'{name:34s} FAIL — viewBox 가 없다')
                fails += 1
                continue
            vb = [float(v) for v in re.split(r'[\s,]+', m.group(1).strip())]
            if len(vb) != 4:
                print(f'{name:34s} FAIL — viewBox 를 읽을 수 없다: {m.group(1)!r}')
                fails += 1
                continue
            page.set_viewport_size({'width': int(vb[2]), 'height': int(vb[3])})
            # 웹폰트를 일부러 심지 않는다 — 노트는 `![](…svg)` 즉 <img> 로 임베드하고,
            # <img> 안의 SVG 는 격리 모드라 외부 폰트를 못 받고 부모의 폰트도 상속하지
            # 않는다. 여기서 <link> 로 폰트를 받아 재면 발행 화면과 다른 자가 된다.
            page.set_content(
                '<style>html,body{margin:0;padding:0}svg{display:block}</style>' + src,
                wait_until='domcontentloaded')
            r = page.evaluate(MEASURE_JS, {'vb': vb, 'RATIO': TEXT_INSET_RATIO,
                                           'MAXIN': TEXT_INSET_MAX,
                                           'MINC': MIN_CONTRAST})
            hits = [h for h in r['hits']
                    if h['w'] >= OVERLAP_MIN_W and h['h'] >= OVERLAP_MIN_H]
            bad = len(r['over']) + len(hits) + len(r['crossed']) + len(r['covered'])
            fails += bad
            flag = 'OK  ' if not bad else 'FAIL'
            print(f'{name:34s} {flag} {int(vb[2])}x{int(vb[3])} · 글자 {r["n"]:2d} '
                  f'· 넘침 {len(r["over"])} · 겹침 {len(hits)} · 관통 {len(r["crossed"])}'
                  f' · 가려짐 {len(r["covered"])}')
            for d in r['over']:
                print(f'    넘침 "{d["t"]}"  x {d["x0"]:.1f}~{d["x1"]:.1f}'
                      f'  y {d["y0"]:.1f}~{d["y1"]:.1f}')
            for d in r['crossed']:
                print(f'    관통 "{d["t"]}"  — <{d["by"]}> 가 글자 상자 안쪽을 지난다')
            for d in r['covered']:
                print(f'    가려짐 "{d["t"]}"  — <{d["by"]}> 가 글자 위를 덮는다')
            for h in hits:
                print(f'    겹침 "{h["a"]}" × "{h["b"]}"  '
                      f'{h["w"]:.1f}×{h["h"]:.1f} = {h["area"]:.1f}px²')
        browser.close()

    print(f'\n{len(files)}장 · 지적 {fails}건.')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
