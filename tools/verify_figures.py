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
    3. 관통 — `<line>`·`<polyline>` 이 글자 상자 **안쪽**을 지나는가. 2026-09-09 에
       접선과 할선이 `P` 라벨 한복판을 지나갔는데 1·2 만 보던 이 검사기가 통과시켰다.
       상자 가장자리를 스치는 것은 정상(라벨은 대개 선 옆에 붙는다)이므로 안쪽으로
       INSET 만큼 줄여서 잰다.
       ⚠ **기하만으로는 오탐이 난다.** 뒤에 그린 불투명 도형에 가려 화면에는 안 보이는
       선이 있다(라이프니츠의 확대 상자가 지시선을 덮는다). 그래서 교차점에서
       `elementsFromPoint` 로 **그 선이 실제로 맨 위에 그려지는지**까지 확인한다.
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
# 관통 판정에서 글자 상자를 안쪽으로 줄이는 비율. 라벨은 대개 선 옆에 붙으므로
# 가장자리를 스치는 것은 정상이고, 「한복판을 지나는가」만 결함으로 센다.
TEXT_INSET = 0.28

MEASURE_JS = """({ vb, INSET }) => {
  const [X0, Y0, W, H] = vb;
  const X1 = X0 + W, Y1 = Y0 + H;
  const svg = document.querySelector('svg');
  const root = svg.getScreenCTM().inverse();
  const boxes = [];
  for (const el of svg.querySelectorAll('text')) {
    const t = (el.textContent || '').replace(/\\s+/g, ' ').trim();
    if (!t) continue;
    const b = el.getBBox();
    const m = root.multiply(el.getScreenCTM());   // 루트 viewBox 좌표계로
    const pts = [[b.x, b.y], [b.x + b.width, b.y],
                 [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]]
      .map(([x, y]) => ({ x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f }));
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
  // 관통 — 직선이 글자 상자 안쪽을 지나는가
  const segs = [];
  for (const el of svg.querySelectorAll('line, polyline')) {
    const m = root.multiply(el.getScreenCTM());
    const T = (x, y) => ({ x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f });
    let raw = [];
    if (el.tagName === 'line')
      raw = [[+el.getAttribute('x1') || 0, +el.getAttribute('y1') || 0],
             [+el.getAttribute('x2') || 0, +el.getAttribute('y2') || 0]];
    else
      raw = (el.getAttribute('points') || '').trim().split(/[\s,]+/).map(Number)
              .reduce((a, v, i) => (i % 2 ? a[a.length - 1].push(v) : a.push([v]), a), []);
    const p = raw.filter(q => q.length === 2 && q.every(Number.isFinite)).map(q => T(q[0], q[1]));
    for (let i = 0; i + 1 < p.length; i++) segs.push([p[i], p[i + 1], el]);
  }
  const crossed = [];
  for (const b of boxes) {
    const iw = (b.x1 - b.x0) * INSET, ih = (b.y1 - b.y0) * INSET;
    const r = { x0: b.x0 + iw, x1: b.x1 - iw, y0: b.y0 + ih, y1: b.y1 - ih };
    if (r.x1 <= r.x0 || r.y1 <= r.y0) continue;
    for (const [a, c, el0] of segs) {
      // Liang-Barsky
      let t0 = 0, t1 = 1;
      const dx = c.x - a.x, dy = c.y - a.y;
      const P = [-dx, dx, -dy, dy];
      const Q = [a.x - r.x0, r.x1 - a.x, a.y - r.y0, r.y1 - a.y];
      let ok = true;
      for (let i = 0; i < 4; i++) {
        if (P[i] === 0) { if (Q[i] < 0) { ok = false; break; } continue; }
        const t = Q[i] / P[i];
        if (P[i] < 0) { if (t > t1) { ok = false; break; } if (t > t0) t0 = t; }
        else { if (t < t0) { ok = false; break; } if (t < t1) t1 = t; }
      }
      if (!ok || t1 <= t0) continue;
      // 기하로는 지나간다. 화면에서도 보이는지 — 뒤에 그린 불투명 도형에 가리면 아니다.
      const scr = svg.getScreenCTM();
      let visible = false;
      for (let k = 0; k <= 12 && !visible; k++) {
        const t = t0 + (t1 - t0) * (k / 12);
        const ux = a.x + dx * t, uy = a.y + dy * t;
        const cx = scr.a * ux + scr.c * uy + scr.e;
        const cy = scr.b * ux + scr.d * uy + scr.f;
        // 글자는 상자 전체가 히트 테스트에 걸리므로 걷어낸다 — 우리가 알고 싶은 것은
        // 「그 선이 다른 **도형**에 가려졌는가」다. 남은 것 중 맨 앞이 이 선이면 보인다.
        const stack = document.elementsFromPoint(cx, cy)
          .filter(e => e.tagName !== 'text' && e.tagName !== 'tspan');
        if (stack[0] === el0) visible = true;
      }
      if (visible) { crossed.push({ t: b.t }); break; }
    }
  }
  return { over, hits, crossed, n: boxes.length };
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
            r = page.evaluate(MEASURE_JS, {'vb': vb, 'INSET': TEXT_INSET})
            hits = [h for h in r['hits']
                    if h['w'] >= OVERLAP_MIN_W and h['h'] >= OVERLAP_MIN_H]
            bad = len(r['over']) + len(hits) + len(r['crossed'])
            fails += bad
            flag = 'OK  ' if not bad else 'FAIL'
            print(f'{name:34s} {flag} {int(vb[2])}x{int(vb[3])} · 글자 {r["n"]:2d} '
                  f'· 넘침 {len(r["over"])} · 겹침 {len(hits)} · 관통 {len(r["crossed"])}')
            for d in r['over']:
                print(f'    넘침 "{d["t"]}"  x {d["x0"]:.1f}~{d["x1"]:.1f}'
                      f'  y {d["y0"]:.1f}~{d["y1"]:.1f}')
            for d in r['crossed']:
                print(f'    관통 "{d["t"]}"  — 직선이 글자 상자 안쪽을 지난다')
            for h in hits:
                print(f'    겹침 "{h["a"]}" × "{h["b"]}"  '
                      f'{h["w"]:.1f}×{h["h"]:.1f} = {h["area"]:.1f}px²')
        browser.close()

    print(f'\n{len(files)}장 · 지적 {fails}건.')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
