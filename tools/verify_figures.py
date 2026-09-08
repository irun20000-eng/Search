#!/usr/bin/env python3
"""도해(SVG)가 실제로 그려지는지 브라우저로 잰다 — math/assets/figures/*.svg.

왜 브라우저인가.
    좌표만 읽는 검사는 「지면 밖으로 나갔는가」밖에 못 본다. 글자 폭을 모르기
    때문이다. 손으로 잡은 어림값(글자당 0.62 × font-size)은 라틴 문자엔 맞지만
    한글엔 40% 가까이 모자라서, 실제로 46px 잘려 있던 캡션을 통과시켰다
    (leibniz-characteristic-triangle, 2026-09-08). 갤러리는 브라우저로 그리므로
    재는 것도 브라우저여야 한다 — `getBBox()` + `getCTM()` 이 정본이다.

    cairosvg 로도 그림은 볼 수 있지만 **판정에는 쓰지 말 것.** `text-anchor="middle"`
    인 글자가 `<tspan>` 으로 나뉘면 조각마다 따로 가운데 정렬해서, 멀쩡한 수식을
    겹쳐 그린다(vibrating-string-initial-shape 에서 `u(x, 0) = …` 이
    `)u(xa · sin…` 으로 보였다). 없는 결함을 만들어 낸다.

무엇을 재나.
    1. 넘침 — 글자의 실제 경계상자가 viewBox 밖으로 나가는가.
    2. 겹침 — 글자끼리 경계상자가 겹치는가(면적 기준, 회전 라벨 포함).
    회전·translate 는 `getCTM()` 으로 루트 좌표계에 옮겨 놓고 잰다. 이걸 빼먹으면
    회전 라벨이 전부 오탐으로 뜬다(getBBox 는 변환 전 좌표를 준다).

못 재는 것.
    그림이 **옳은가**는 못 잰다. 컴퍼스 두 다리가 둘 다 중심에서 나오거나, 접선이
    할선보다 완만하거나, 「확대도」의 삼각형 비가 원본과 다른 것은 사람이 봐야 한다.
    이 검사기는 그 앞단의 값싼 그물이지 대신이 아니다.

쓰기.
    python3 tools/verify_figures.py            # math/assets/figures/*.svg 전부
    python3 tools/verify_figures.py <파일…>    # 지정한 것만
    브라우저가 없는 환경에서는 건너뛰고 exit 0 (검사 없음을 분명히 찍는다).
"""
import glob
import pathlib
import re
import sys

FIGURE_DIR = 'math/assets/figures'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
# 겹침으로 셀 최소 면적(px²). 글자 사이 미세한 커닝 겹침을 결함으로 세지 않는다.
OVERLAP_MIN_AREA = 6.0

MEASURE_JS = """(vb) => {
  const [ , , W, H] = vb;
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
  const over = boxes.filter(b => b.x0 < -0.5 || b.x1 > W + 0.5 || b.y0 < -0.5 || b.y1 > H + 0.5);
  const hits = [];
  for (let i = 0; i < boxes.length; i++)
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], c = boxes[j];
      const w = Math.min(a.x1, c.x1) - Math.max(a.x0, c.x0);
      const h = Math.min(a.y1, c.y1) - Math.max(a.y0, c.y0);
      if (w > 0 && h > 0) hits.push({ a: a.t, b: c.t, area: w * h });
    }
  return { over, hits, n: boxes.length };
}"""


def main(argv):
    files = argv[1:] or sorted(glob.glob(f'{FIGURE_DIR}/*.svg'))
    if not files:
        print(f'검사할 SVG 가 없다: {FIGURE_DIR}')
        return 0

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('[건너뜀] playwright 가 없다 — 도해 렌더 검사를 하지 않았다.')
        print('         설치: pip install playwright  (브라우저는 이미 있다면 받지 않아도 된다)')
        return 0
    if not pathlib.Path(CHROME).exists():
        print(f'[건너뜀] 브라우저가 없다 ({CHROME}) — 도해 렌더 검사를 하지 않았다.')
        return 0

    fails = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME)
        page = browser.new_page()
        for f in files:
            src = pathlib.Path(f).read_text(encoding='utf-8')
            m = re.search(r'viewBox="([^"]+)"', src)
            name = pathlib.Path(f).stem
            if not m:
                print(f'{name:34s} FAIL — viewBox 가 없다')
                fails += 1
                continue
            vb = [float(v) for v in m.group(1).split()]
            page.set_viewport_size({'width': int(vb[2]), 'height': int(vb[3])})
            page.set_content(
                '<style>html,body{margin:0;padding:0}svg{display:block}</style>'
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
                '?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap">' + src,
                wait_until='networkidle')
            r = page.evaluate(MEASURE_JS, vb)
            hits = [h for h in r['hits'] if h['area'] >= OVERLAP_MIN_AREA]
            bad = len(r['over']) + len(hits)
            fails += bad
            flag = 'OK  ' if not bad else 'FAIL'
            print(f'{name:34s} {flag} {int(vb[2])}x{int(vb[3])} · 글자 {r["n"]:2d} '
                  f'· 넘침 {len(r["over"])} · 겹침 {len(hits)}')
            for d in r['over']:
                print(f'    넘침 "{d["t"]}"  x {d["x0"]:.1f}~{d["x1"]:.1f}'
                      f'  y {d["y0"]:.1f}~{d["y1"]:.1f}')
            for h in hits:
                print(f'    겹침 "{h["a"]}" × "{h["b"]}"  {h["area"]:.1f}px²')
        browser.close()

    print(f'\n{len(files)}장 · 지적 {fails}건.')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
