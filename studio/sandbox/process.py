# -*- coding: utf-8 -*-
"""프로세스 인포그래픽 — 1536×1024, 도입 + 단계 N + 마무리.

이 판형은 **이미지 생성 프롬프트를 렌더러 스펙으로 옮긴 것**이다.

원 프롬프트는 텍스트→이미지 모델에게 주는 것이었는데, 최우선 규칙이
"모든 보이는 글자를 정확한 한글로, 모든 글자를 완전히 렌더링" 이었다.
그건 생성 모델이 원리적으로 못 하는 일이고, 이 저장소는 이미 그 결론에 도달해
규칙으로 박아 두었다(`studio/CLAUDE.md` — "개념 한 장을 이미지 생성 모델로 만들지
말 것. 한글이 깨진다"). 그래서 프롬프트를 버리는 대신 **읽는 쪽을 바꿨다.**

프롬프트가 지시한 것은 전부 결정적 조판이다 — 1536×1024 · 지면 #F4F2EF ·
4행 그리드 · 16px 라운드 · 1.5px 외곽 · 24px 패딩 · 원형번호→제목→문장→도해 ·
악센트 4색 회전 · 하단 프로세스 맵. 사람이 눈대중할 것이 하나도 없다.
HTML/SVG 는 이것을 정확히 그리고, **한글은 애초에 깨지지 않는다.**

--- 글자수 상한을 코드가 잰다 -------------------------------------------------
프롬프트는 "제목 12자, 문장 28자" 처럼 상한을 적어 두었지만 이미지 모델은 그것을
지켰는지 알 수 없다. 여기서는 **렌더러가 센다.** 넘으면 몇 자 넘었는지 짚는다 —
주장이 아니라 측정이다.

--- 인물을 쓰지 않는다 --------------------------------------------------------
원 프롬프트도 "주제가 사람을 다룰 때만" 이라고 단서를 달았다. 이 판형은 과정이
주인공이라 도해로 충분하고, 덤으로 **QED프렌즈 컷아웃(비공개 자산)이 들어가지
않아** 산출물을 그대로 공유할 수 있다. 컷툰·카드뉴스와 갈리는 지점이다.
"""
import os
import pathlib

from cuttoon import esc

W, H = 1536, 1024
INK = "#1F2937"
BG = "#F4F2EF"
LIMITS = {"title": 12, "sent": 28, "bubble": 10, "takeaway": 40}

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;forced-color-adjust:none;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{width:{W}px}}
body{{height:{H}px;background:{BG};color:{INK};
  font-family:"Pretendard","Noto Sans CJK KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  display:flex;flex-direction:column;gap:14px;padding:28px;word-break:keep-all}}

/* 패널 공통 — 흰 카드, 16px 라운드, 1.5px 외곽, 번짐 없는 단색 그림자.
   그라디언트를 쓰지 않는 것이 이 판형의 규약이다. */
.p{{background:#fff;border:1.5px solid {INK};border-radius:16px;
  box-shadow:5px 5px 0 rgba(31,41,55,.11);padding:24px;position:relative}}

/* 1행 — 도입. 유일하게 짙은 판이라 시선이 여기서 시작한다. */
.intro{{flex:0 0 186px;background:#22303F;border-color:#22303F;color:#fff;
  display:flex;align-items:center;gap:28px}}
.intro .txt{{flex:1}}
.intro .kicker{{font-size:16px;font-weight:700;letter-spacing:.14em;opacity:.62;
  margin-bottom:10px}}
.intro h1{{font-size:52px;font-weight:800;letter-spacing:-1.5px;line-height:1.05}}
.intro .def{{margin-top:12px;font-size:23px;font-weight:600;opacity:.92}}
.intro .hero{{flex:0 0 452px;height:130px}}
.intro .hero svg{{width:100%;height:100%;display:block}}

/* 2~3행 — 단계. 행마다 패널 수가 달라도 한 행 안에서는 고르게 눕는다. */
.row{{flex:1;display:flex;gap:14px;min-height:0}}
.step{{flex:1;display:flex;flex-direction:column;min-width:0}}
.step .no{{width:44px;height:44px;border-radius:50%;color:#fff;font-weight:800;
  font-size:23px;display:flex;align-items:center;justify-content:center;flex:0 0 auto}}
.step h3{{margin-top:12px;font-size:25px;font-weight:800;letter-spacing:-.6px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.step .s{{margin-top:7px;font-size:17px;font-weight:500;line-height:1.45;color:#43505F}}
.step .fig{{flex:1;margin-top:12px;min-height:0}}
.step .fig svg{{width:100%;height:100%;display:block}}

/* 말풍선 — 전체 다섯 중 둘에만 둔다. 모든 패널에 달면 리듬이 죽는다. */
.bub{{position:absolute;top:18px;right:18px;background:#fff;border:1.5px solid {INK};
  border-radius:999px;padding:6px 15px;font-size:15px;font-weight:700;
  box-shadow:2px 2px 0 rgba(31,41,55,.14)}}

/* 4행 — 마무리. 단계와 같은 흰 카드지만 악센트가 하나 따로라 결론으로 읽힌다. */
.sum{{flex:0 0 132px;display:flex;align-items:center;gap:26px}}
.map{{display:flex;align-items:center;gap:9px;flex:0 0 auto}}
.chip{{display:flex;align-items:center;gap:7px;border:1.5px solid {INK};
  border-radius:999px;padding:6px 13px 6px 6px;font-size:15px;font-weight:700;
  background:#fff}}
.chip i{{width:23px;height:23px;border-radius:50%;color:#fff;font-style:normal;
  font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center}}
.arw{{font-size:18px;color:#8A93A0;font-weight:800}}
.take{{flex:1;font-size:22px;font-weight:800;letter-spacing:-.5px;line-height:1.35}}
.credit{{position:absolute;right:24px;bottom:9px;font-size:12px;color:#98A0AC}}
"""


# ── 도해 ────────────────────────────────────────────────────────────────
# 전부 평면 도형이다. 그라디언트·질감·3D 를 쓰지 않는 것이 이 판형의 규약이고,
# 글자가 필요한 자리는 SVG 텍스트로 쓴다 — 생성 모델이 못 하는 바로 그 부분이다.

def _svg(w, h, inner):
    return (f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg>')


def fig_papers(a):
    s = [f'<rect x="18" y="96" width="228" height="9" rx="4" fill="{INK}" opacity=".16"/>']
    for i, (x, n) in enumerate(((36, 7), (110, 5), (176, 6))):
        for k in range(n):
            s.append(f'<rect x="{x}" y="{92 - k * 6}" width="60" height="5" rx="1.5" '
                     f'fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    # 촛불 — 밤샘의 유일한 광원.
    # 첫 판에는 몸통 위에 타원 하나를 얹었더니 촛불이 아니라 빨간 알약으로 읽혔다.
    # 불꽃은 물방울 모양(뾰족한 위 + 둥근 아래)이어야 불로 보이고, 옅은 빛무리와
    # 심지가 있어야 '켜져 있다'가 된다.
    s += [f'<circle cx="252" cy="46" r="22" fill="{a}" opacity=".13"/>',
          f'<rect x="245" y="56" width="14" height="40" rx="3" fill="#fff" '
          f'stroke="{INK}" stroke-width="1.5"/>',
          f'<rect x="241" y="93" width="22" height="6" rx="3" fill="#fff" '
          f'stroke="{INK}" stroke-width="1.5"/>',
          f'<path d="M252 50 V56" stroke="{INK}" stroke-width="1.6"/>',
          f'<path d="M252 30 C259 40 258 50 252 50 C246 50 245 40 252 30 Z" fill="{a}"/>']
    # 지친 숫자 — 여덟 자리
    s.append(f'<text x="18" y="28" font-size="17" font-weight="700" fill="{INK}" '
             f'opacity=".55" font-family="monospace">83,192,447</text>')
    return _svg(280, 110, "".join(s))


def fig_pairing(a):
    xs = [30, 96, 162, 228]
    top, bot = [2, 4, 8, 16], [1, 2, 3, 4]
    s = [f'<defs><marker id="m{a[1:]}" viewBox="0 0 10 10" refX="8" refY="5" '
         f'markerWidth="4.5" markerHeight="4.5" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 z" fill="{a}"/></marker></defs>']
    for x, v in zip(xs, top):
        s.append(f'<text x="{x}" y="30" text-anchor="middle" font-size="26" '
                 f'font-weight="800" fill="{INK}">{v}</text>')
    for x, v in zip(xs, bot):
        s.append(f'<text x="{x}" y="102" text-anchor="middle" font-size="26" '
                 f'font-weight="800" fill="{INK}">{v}</text>')
    for x in xs:
        s.append(f'<path d="M{x} 44 V78" stroke="{a}" stroke-width="2.6" '
                 f'marker-end="url(#m{a[1:]})"/>')
    for i in range(3):
        mx = (xs[i] + xs[i + 1]) / 2
        s.append(f'<text x="{mx}" y="24" text-anchor="middle" font-size="13" '
                 f'font-weight="700" fill="{a}">×2</text>')
        s.append(f'<text x="{mx}" y="110" text-anchor="middle" font-size="13" '
                 f'font-weight="700" fill="{a}">+1</text>')
    return _svg(280, 118, "".join(s))


def fig_book(a):
    cx, top = 140, 14
    s = [f'<path d="M{cx} 96 L{cx - 104} 84 V{top} L{cx} 26 Z" fill="#fff" '
         f'stroke="{INK}" stroke-width="1.8"/>',
         f'<path d="M{cx} 96 L{cx + 104} 84 V{top} L{cx} 26 Z" fill="#fff" '
         f'stroke="{INK}" stroke-width="1.8"/>',
         f'<path d="M{cx} 26 V96" stroke="{INK}" stroke-width="1.8"/>',
         f'<rect x="{cx - 112}" y="96" width="224" height="7" rx="3" fill="{a}"/>']
    for i in range(5):                       # 설명 면 — 성긴 줄
        s.append(f'<rect x="{cx - 92}" y="{36 + i * 10}" width="72" height="2.4" '
                 f'rx="1" fill="{INK}" opacity=".34"/>')
    for r in range(7):                       # 표 면 — 빽빽한 격자
        for c in range(4):
            s.append(f'<rect x="{cx + 16 + c * 22}" y="{34 + r * 8}" width="16" '
                     f'height="3" rx="1" fill="{INK}" opacity=".46"/>')
    s.append(f'<text x="{cx - 56}" y="118" text-anchor="middle" font-size="13" '
             f'font-weight="700" fill="{INK}" opacity=".62">설명 57쪽</text>')
    s.append(f'<text x="{cx + 58}" y="118" text-anchor="middle" font-size="13" '
             f'font-weight="700" fill="{a}">표 90쪽</text>')
    return _svg(280, 124, "".join(s))


def fig_base10(a):
    s = [f'<circle cx="58" cy="58" r="46" fill="{a}" opacity=".16"/>',
         f'<circle cx="58" cy="58" r="46" fill="none" stroke="{INK}" stroke-width="2"/>',
         f'<text x="58" y="74" text-anchor="middle" font-size="46" font-weight="800" '
         f'fill="{INK}">10</text>']
    for k in range(3):                       # 떠맡은 방대한 계산 — 두께로만
        x, y = 152 + k * 5, 20 + k * 28
        s.append(f'<rect x="{x}" y="{y}" width="104" height="24" rx="3" fill="#fff" '
                 f'stroke="{INK}" stroke-width="1.6"/>')
        for r in range(2):
            s.append(f'<rect x="{x + 9}" y="{y + 7 + r * 7}" width="86" height="2.4" '
                     f'rx="1" fill="{INK}" opacity=".4"/>')
    return _svg(280, 116, "".join(s))


def fig_swap(a):
    s = [f'<rect x="10" y="16" width="112" height="34" rx="8" fill="#fff" '
         f'stroke="{INK}" stroke-width="1.8"/>',
         f'<text x="66" y="39" text-anchor="middle" font-size="18" font-weight="800" '
         f'fill="{INK}">곱셈 23</text>',
         f'<rect x="158" y="16" width="112" height="34" rx="8" fill="{a}"/>',
         f'<text x="214" y="39" text-anchor="middle" font-size="18" font-weight="800" '
         f'fill="#fff">덧셈 23</text>',
         f'<path d="M126 33 H152" stroke="{INK}" stroke-width="2.4" '
         f'marker-end="url(#sw)"/>',
         f'<defs><marker id="sw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
         f'markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/>'
         f'</marker></defs>']
    # 걸린 시간 — 길이로만 말한다
    s += [f'<rect x="10" y="70" width="112" height="13" rx="6" fill="{INK}" opacity=".72"/>',
          f'<rect x="158" y="70" width="26" height="13" rx="6" fill="{a}"/>',
          f'<text x="10" y="104" font-size="13" font-weight="700" fill="{INK}" '
          f'opacity=".55">하룻밤</text>',
          f'<text x="158" y="104" font-size="13" font-weight="700" fill="{a}">몇 분</text>']
    return _svg(280, 112, "".join(s))


FIGS = {"papers": fig_papers, "pairing": fig_pairing, "book": fig_book,
        "base10": fig_base10, "swap": fig_swap}


def hero_svg(kind, a):
    """도입 판의 그림 — 개념 한 줄을 그림으로 되풀이한다."""
    s = [f'<rect x="14" y="30" width="150" height="62" rx="14" fill="#fff" opacity=".10"/>',
         f'<text x="89" y="70" text-anchor="middle" font-size="34" font-weight="800" '
         f'fill="#fff">A × B</text>',
         f'<path d="M182 61 H236" stroke="{a}" stroke-width="3.4" marker-end="url(#h)"/>',
         f'<defs><marker id="h" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.6" '
         f'markerHeight="4.6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{a}"/>'
         f'</marker></defs>',
         f'<rect x="252" y="30" width="186" height="62" rx="14" fill="{a}"/>',
         f'<text x="345" y="70" text-anchor="middle" font-size="30" font-weight="800" '
         f'fill="#fff">log A + log B</text>']
    return _svg(452, 122, "".join(s))


def check(spec):
    """글자수 상한을 사람이 눈대중하지 않게 한다. 넘으면 몇 자 넘었는지 말한다."""
    bad = []
    for i, st in enumerate(spec["steps"], 1):
        for k in ("title", "sent", "bubble"):
            v = st.get(k)
            if v and len(v) > LIMITS[k]:
                bad.append("%d번 %s %d자 (상한 %d)" % (i, k, len(v), LIMITS[k]))
    t = spec.get("takeaway", "")
    if len(t) > LIMITS["takeaway"]:
        bad.append("마무리 %d자 (상한 %d)" % (len(t), LIMITS["takeaway"]))
    n = len(spec["steps"])
    if not 4 <= n <= 6:
        bad.append("단계 %d개 — 4~6 이 아니면 1536×1024 에서 글이 안 읽힌다" % n)
    if sum(spec.get("rows") or []) != n:
        bad.append("rows 합 %d ≠ 단계 %d" % (sum(spec.get("rows") or []), n))
    return bad


def build(spec, out_png, scale=1):
    bad = check(spec)
    acc = spec["accents"]
    steps = spec["steps"]

    rows_html = ""
    idx = 0
    for cnt in spec["rows"]:
        cells = ""
        for _ in range(cnt):
            st = steps[idx]
            a = acc[idx % len(acc)]
            fig = FIGS.get(st["fig"])
            cells += (
                f'<div class="p step">'
                f'<div class="no" style="background:{a}">{idx + 1}</div>'
                f'<h3>{esc(st["title"])}</h3>'
                f'<div class="s">{esc(st["sent"])}</div>'
                f'<div class="fig">{fig(a) if fig else ""}</div>'
                + (f'<div class="bub">{esc(st["bubble"])}</div>' if st.get("bubble") else "")
                + '</div>')
            idx += 1
        rows_html += f'<div class="row">{cells}</div>'

    sa = spec["accent_sum"]
    chips = ('<span class="arw">→</span>').join(
        f'<span class="chip"><i style="background:{acc[i % len(acc)]}">{i + 1}</i>'
        f'{esc(c)}</span>' for i, c in enumerate(spec["chips"]))

    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
 <div class="p intro">
  <div class="txt">
   <div class="kicker">{esc(spec.get('kicker',''))}</div>
   <h1>{esc(spec['title'])}</h1>
   <div class="def">{esc(spec['define'])}</div>
  </div>
  <div class="hero">{hero_svg(spec.get('hero'), sa)}</div>
 </div>
 {rows_html}
 <div class="p sum" style="border-left:9px solid {sa}">
  <div class="map">{chips}</div>
  <div class="take">{esc(spec['takeaway'])}</div>
  <div class="credit">{esc(spec.get('credit_r',''))}</div>
 </div>
</body></html>"""

    p = pathlib.Path(out_png).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    h = p.with_suffix(".html")
    h.write_text(doc, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        exe = os.environ.get("CONCEPT_CHROMIUM")
        b = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
        pg.goto(h.as_uri())
        pg.wait_for_timeout(350)
        r = pg.evaluate("""()=>{const c=document.createElement('canvas').getContext('2d');
          c.font="100px 'Noto Sans CJK KR','Malgun Gothic',sans-serif";
          return {ko:Math.round(c.measureText('가나다라마바사').width),
                  tofu:Math.round(c.measureText('').width)}}""")
        if r["ko"] == r["tofu"]:
            b.close()
            raise SystemExit("[프로세스] 한글 폰트가 없다 — fonts-noto-cjk 를 설치할 것.")
        over = pg.evaluate("()=>document.body.scrollHeight - %d" % H)
        # 제목 한 줄 규약 — 넘치면 CSS 가 말줄임으로 감춰 버리므로 그 전에 잡는다.
        cut = pg.evaluate("""()=>[...document.querySelectorAll('.step h3')]
          .map((e,i)=>({i:i+1,t:e.textContent,over:e.scrollWidth-e.clientWidth}))
          .filter(x=>x.over>1)""")
        pg.screenshot(path=str(p))
        b.close()

    print("[프로세스] %d단계 · %d×%d -> %s" % (len(steps), W, H, p))
    if over > 1:
        bad.append("지면 %dpx 넘침" % over)
    for c in cut:
        bad.append("%d번 제목이 한 줄을 넘어 잘렸다 — '%s'" % (c["i"], c["t"]))
    if bad:
        for x in bad:
            print("   [주의] %s" % x)
    else:
        print("   [OK] 글자수 상한·한 줄 제목·지면 전부 통과")
    return 0
