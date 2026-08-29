# -*- coding: utf-8 -*-
"""개념 한 장 v2 — 1536×1024 가로 인포그래픽 빌더.

v1(2026-08-04) 대비 바뀐 것 — 2026-08-22 사용자 지시로 확정한 규격:
  · 단계 카드에 **설명 2단**(요지 + 구분선 아래 상세)을 둔다. v1은 요지 한 덩어리라
    카드 아래 절반이 비었다.
  · **정리부를 확대**한다. v1의 얇은 띠 대신 좌(세 줄 정리 3칸 + 흐름 칩) /
    우(다크 패널: 한 줄 정리 + 부연 + 실전 질문) 2단 구성.
  · 우측 하단에 **aftermath 낙관**을 고정으로 넣는다 (`brand_signature.py`).
  · device_scale_factor=2 로 렌더 → 실제 파일은 3072×2048, 논리 규격은 1536×1024.

이미지 생성 모델은 한글을 정확히 못 쓴다. 카드뉴스 엔진과 같은
HTML → Playwright 스크린샷 경로를 쓰면 한글이 100% 정확하게 나온다.

--- spec 스키마 ---------------------------------------------------------
{
 "title","en","tag",
 "hook","hooksub",
 "data": {"label", "head":[4칸], "rows":[[셀×4, ...]], "note"},
 "steps": [ {"c":색, "t":제목, "d":요지, "kv":상세, "extra":하단블록HTML} × 4 ],
 "points": [ (라벨, 색, 문장) × 3 ],
 "flow": [ (칩글자, 색) × 4 ],
 "take": {"big","sub","ask"},
 "foot": 출처 한 줄,
 "h_r1": 1행 높이(기본 250) · 표 행 수에 맞춰 조정,
 "h_r2": 2행 높이(기본 330) · 단계 카드 분량에 맞춰 조정,
}
"""
import os, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import brand_signature as bs

# 개념 한 장 공통 팔레트 (심슨·최적정지 공용)
INK = "#1E2430"; RED = "#D6452C"; BLU = "#2F6BE0"
ORG = "#E0871F"; GRN = "#2E9E6B"; YEL = "#FFD24A"
STEP_COLORS = [BLU, ORG, GRN, RED]

CSS = bs.CSS + r"""
*{box-sizing:border-box;margin:0;padding:0}
body{width:1536px;height:1024px;background:#EFEDE8;--h1:250px;--h2:330px;
  /* 지금 있는 다섯 장은 전부 이 폰트 순서로, 같은 PC 에서 그려졌다.
     Noto Sans CJK KR 이 있는 환경(예: GitHub Actions)에서 그리면 글자가 달라진다.
     아래 FONT_FINGERPRINT 가 그 경우를 막는다. */
  font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;color:#1E2430;
  word-break:keep-all;-webkit-font-smoothing:antialiased}
.sheet{padding:28px 34px;height:100%;display:flex;flex-direction:column;gap:12px}
.hd{display:flex;align-items:baseline;gap:13px;flex:0 0 46px}
.hd h1{font-size:37px;font-weight:900;letter-spacing:-.02em}
.hd .en{font-size:16px;color:#7A8394;font-weight:600}
.hd .tag{margin-left:auto;font-size:13px;font-weight:700;color:#fff;
  background:#1E2430;padding:6px 14px;border-radius:99px}
.row{display:flex;gap:12px}
.r1{flex:0 0 var(--h1)}
.r2{flex:0 0 var(--h2)}
.r3{flex:1;min-height:0}
.card{background:#fff;border:2px solid #1E2430;border-radius:13px;padding:15px 18px;
  box-shadow:0 2px 0 rgba(30,36,48,.10)}
/* 1행 */
.intro{background:#1E2430;color:#fff;flex:0 0 520px;display:flex;flex-direction:column;
  justify-content:center}
.intro .q{font-size:29px;font-weight:900;line-height:1.3}
.intro .q b{color:#FFD24A}
.intro .s{font-size:14.5px;color:#B9C0CE;margin-top:10px;line-height:1.6}
.datacard{flex:1;display:flex;flex-direction:column}
.dt{font-size:14px;font-weight:800;color:#7A8394;margin-bottom:7px}
table{width:100%;border-collapse:collapse;font-size:15px}
th{font-size:12.5px;color:#7A8394;font-weight:700;text-align:right;padding:0 0 5px}
th:first-child{text-align:left}
td{padding:3.6px 0;border-top:1px solid #E2E0DA;text-align:right;font-weight:700;
  font-variant-numeric:tabular-nums}
td:first-child{text-align:left;font-weight:800}
.win{color:#D6452C}
.dim{color:#9AA2B0;font-weight:600}
.note{margin-top:auto;padding-top:7px;font-size:12.5px;color:#4A5262;line-height:1.52}
.note b{color:#D6452C}
/* 2행 단계 카드 */
.step{flex:1;position:relative;padding-top:21px;display:flex;flex-direction:column}
.num{position:absolute;top:-15px;left:18px;width:36px;height:36px;border-radius:50%;
  color:#fff;font-weight:900;font-size:18px;display:flex;align-items:center;
  justify-content:center;border:2px solid #1E2430}
.st{font-size:19px;font-weight:900;margin-bottom:6px;line-height:1.26}
.sd{font-size:13.5px;color:#3D4553;line-height:1.6}
.sd b{color:#1E2430;font-weight:800}
.sd .r{color:#D6452C;font-weight:800}
.hr{height:1px;background:#E2E0DA;margin:8px 0}
.kv{font-size:12.5px;color:#4A5262;line-height:1.52}
.kv b{color:#1E2430}
.bars{margin-top:auto;padding-top:12px;display:flex;flex-direction:column;gap:6px}
.bar{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:700}
.bar i{display:block;height:14px;border-radius:3px}
.bar span.l{width:48px;color:#4A5262}
.box{margin-top:auto;background:#F6F5F2;border-radius:9px;padding:9px 10px;
  font-size:12.5px;font-weight:700;line-height:1.7;color:#4A5262;text-align:center}
.box .k{color:#D6452C;font-weight:900}
.box.lft{text-align:left}
.calc{margin-top:auto;background:#F6F5F2;border-radius:9px;padding:9px 12px;
  font-size:12px;line-height:1.75;color:#4A5262;font-weight:700;
  font-variant-numeric:tabular-nums}
.calc b{color:#1E2430}
.calc .r{color:#D6452C;font-weight:900}
/* 3행 정리부 */
.sumL{flex:1;display:flex;flex-direction:column}
.lb{font-size:12.5px;font-weight:800;color:#7A8394;letter-spacing:.06em;margin-bottom:9px}
.pts{display:flex;gap:11px;flex:1}
.pt{flex:1;background:#F6F5F2;border-radius:10px;padding:12px 13px;display:flex;
  flex-direction:column;justify-content:center}
.pt .h{font-size:13px;font-weight:900;color:#fff;padding:2px 9px;border-radius:6px;
  align-self:flex-start;margin-bottom:7px}
.pt .b{font-size:13px;line-height:1.58;color:#3D4553;font-weight:600}
.pt .b b{color:#1E2430;font-weight:800}
.flow{display:flex;align-items:center;gap:7px;margin-top:auto;padding-top:13px}
.chip{font-size:13px;font-weight:800;color:#fff;padding:7px 13px;border-radius:8px;
  border:2px solid #1E2430}
.arw{font-size:15px;color:#7A8394;font-weight:900}
.sumR{flex:0 0 494px;background:#1E2430;color:#fff;display:flex;flex-direction:column;
  justify-content:center}
.sumR .t{font-size:12.5px;font-weight:800;color:#8B93A2;letter-spacing:.08em}
.sumR .big{font-size:29px;font-weight:900;line-height:1.33;margin-top:8px}
.sumR .big b{color:#FFD24A}
.sumR .sub{font-size:13.5px;color:#B9C0CE;line-height:1.58;margin-top:10px;
  border-top:1px solid #39414F;padding-top:10px}
.sumR .ask{margin-top:9px;background:#D6452C;border-radius:9px;padding:9px 14px;
  font-size:18px;font-weight:900;text-align:center}
.ft{flex:0 0 24px;font-size:12px;color:#8B93A2;display:flex;align-items:center;
  justify-content:space-between;gap:20px}
.ft .src{flex:1;min-width:0}
"""


# --- 판형(plan) -------------------------------------------------------------
# 같은 스펙을 세 가지 지면으로 그린다. 카드뉴스가 `layout_archive.PLANS` 로
# A/B/C 를 돌리는 것과 같은 생각이다 — 카피를 다시 쓰지 않고 인상만 바꿔 본다.
#
# **A 는 빈 문자열이어야 한다.** 이미 발행된 일곱 장이 A 로 그려졌고, 여기에
# 한 글자라도 더 붙으면 HTML 이 달라져 그림이 미묘하게 바뀐다. A 의 산출물이
# 이 변경 전후로 바이트까지 같은지는 `studio/sandbox/render.py --same` 이 본다.
PLAN_CSS = {
    # A — 기준형. 지금 서가에 올라간 일곱 장이 이 판형이다.
    "A": "",

    # B — 센터 임팩트. 후크를 붉은 면에 가운데로 세우고, 한 줄 정리를 왼쪽으로
    #     옮겨 시선이 '질문 → 답' 순서로 지면을 한 바퀴 돌게 한다.
    "B": r"""
.hd h1{font-size:41px}
.intro{background:#D6452C;text-align:center;align-items:center}
.intro .q{font-size:32px}
.intro .q b{color:#FFE08A}
.intro .s{color:#F8DBD4;border-top:1px solid rgba(255,255,255,.28);padding-top:10px}
.dt{color:#D6452C}
.step{background:#FFFDFA}
.st{font-size:20px}
.r3{flex-direction:row-reverse}
.sumR{flex:0 0 548px}
.sumR .big{font-size:32px}
.pt{text-align:center;align-items:center}
.pt .h{align-self:center}
.flow{justify-content:center}
""",

    # C — 구조 강조. 색면을 걷어내고 선·격자로만 위계를 만든다. 표와 단계의
    #     순서가 먼저 읽히는 판형이라 절차·비교형 주제에 맞는다.
    "C": r"""
body{background:#F4F2ED}
.card{border-width:1.5px;border-radius:4px;box-shadow:none}
.intro{background:#fff;color:#1E2430;border-left:9px solid #1E2430}
.intro .q b{color:#D6452C}
.intro .s{color:#4A5262}
tr:nth-child(even) td{background:#F7F6F3}
.num{top:-13px;left:16px;width:30px;height:30px;border-radius:5px;font-size:16px}
.pt{background:#fff;border:1.5px solid #E2E0DA;border-radius:4px}
.chip{border-radius:4px;border-width:1.5px}
.sumR{background:#fff;color:#1E2430;border-left:9px solid #D6452C}
.sumR .t{color:#7A8394}
.sumR .big b{color:#D6452C}
.sumR .sub{color:#4A5262;border-top-color:#E2E0DA}
.sumR .ask{background:#1E2430;color:#fff}
""",
}


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{th}</tr>{tr}</table>"


# --- 한글이 읽히는가 --------------------------------------------------------
# 2026-08-22 초안은 "기존 다섯 장과 폰트 환경이 같은가"를 봤다. 그런데 그렇게 잠그면
# 되돌릴 수 없는 두 장(스펙 없는 심슨·최적정지) 때문에 나머지 전부가 열등한 폴백 폰트에
# 묶인다. 사용자 판단(같은 날): **양식만 같으면 되고, 낙관이 찍히고 읽을 수 있으면 된다.**
#
# 그래서 조건을 바꿨다 - 폰트가 '같은지' 가 아니라 한글이 '읽히는지' 만 본다.
# 진짜 사고는 리눅스처럼 한글 폰트가 아예 없는 환경에서 글자가 두부(□)로 나오는 것이다.
# 없는 코드포인트(사용자 영역)와 폭이 같으면 한글도 두부로 그려지고 있는 것이다.
TOFU_JS = """() => {
  const c = document.createElement('canvas').getContext('2d');
  c.font = "100px 'Noto Sans CJK KR','Malgun Gothic',sans-serif";
  const ko   = Math.round(c.measureText('가나다라마바사').width);
  const tofu = Math.round(c.measureText('').width);
  return { ko: ko, tofu: tofu };
}"""


def check_hangul(pg):
    r = pg.evaluate(TOFU_JS)
    if r["ko"] == r["tofu"]:
        raise SystemExit(
            "[개념 한 장] 이 환경에는 한글 폰트가 없다 - 글자가 두부(네모)로 그려진다." + '\n' +
            "  리눅스라면 fonts-noto-cjk 를 설치할 것.")



def build(spec, out_png, scale=2, plan="A"):
    steps = "".join(f'''<div class="card step">
      <div class="num" style="background:{s.get('c', STEP_COLORS[i])}">{i+1}</div>
      <div class="st">{s['t']}</div>
      <div class="sd">{s['d']}</div>
      <div class="hr"></div>
      <div class="kv">{s['kv']}</div>
      {s.get('extra','')}
    </div>''' for i, s in enumerate(spec["steps"]))

    pts = "".join(f'<div class="pt"><div class="h" style="background:{c}">{h}</div>'
                  f'<div class="b">{b}</div></div>' for h, c, b in spec["points"])

    chips = '<span class="arw">→</span>'.join(
        f'<span class="chip" style="background:{c}">{t}</span>' for t, c in spec["flow"])

    d = spec["data"]
    tk = spec["take"]
    sig = bs.signature(h=19, tone="light")

    hvar = f"body{{--h1:{spec.get('h_r1',250)}px;--h2:{spec.get('h_r2',330)}px}}"

    if plan not in PLAN_CSS:
        raise SystemExit("[개념 한 장] 없는 판형: %s (있는 것: %s)"
                         % (plan, ", ".join(PLAN_CSS)))
    pcss = PLAN_CSS[plan]

    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>{CSS}
{hvar}{pcss}</style></head><body><div class="sheet">
 <div class="hd"><h1>{spec['title']}</h1><span class="en">{spec['en']}</span>
  <span class="tag">{spec['tag']}</span></div>

 <div class="row r1">
  <div class="card intro">
   <div class="q">{spec['hook']}</div>
   <div class="s">{spec['hooksub']}</div>
  </div>
  <div class="card datacard">
   <div class="dt">{d['label']}</div>
   {table(d['head'], d['rows'])}
   <div class="note">{d['note']}</div>
  </div>
 </div>

 <div class="row r2">{steps}</div>

 <div class="row r3">
  <div class="card sumL">
   <div class="lb">세 줄 정리</div>
   <div class="pts">{pts}</div>
   <div class="flow">{chips}</div>
  </div>
  <div class="card sumR">
   <div class="t">한 줄 정리</div>
   <div class="big">{tk['big']}</div>
   <div class="sub">{tk['sub']}</div>
   <div class="ask">{tk['ask']}</div>
  </div>
 </div>

 <div class="ft"><span class="src">{spec['foot']}</span>{sig}</div>
</div></body></html>"""

    # 상대경로를 그대로 두면 아래 as_uri() 가 터진다(윈도우에서 드라이브가 없다).
    p = pathlib.Path(out_png).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    h = p.with_suffix(".html")
    h.write_text(html, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        # 이 컨테이너의 playwright 패키지가 기대하는 브라우저 빌드와
        # /opt/pw-browsers 에 깔린 빌드가 달라 기본 launch() 가 실패한다.
        # 러너에는 이 변수가 없으니 기존 동작 그대로다.
        _exe = os.environ.get("CONCEPT_CHROMIUM")
        b = pw.chromium.launch(**({"executable_path": _exe} if _exe else {}))
        pg = b.new_page(viewport={"width": 1536, "height": 1024}, device_scale_factor=scale)
        pg.goto(h.as_uri()); pg.wait_for_timeout(500)
        check_hangul(pg)
        over = pg.evaluate("()=>document.body.scrollHeight - 1024")
        clip = pg.evaluate("""()=>[...document.querySelectorAll('.card,.step,.pt')]
            .filter(e=>e.scrollHeight>e.clientHeight+1)
            .map(e=>(e.className+' +'+(e.scrollHeight-e.clientHeight)))""")
        gaps = pg.evaluate(MEASURE_JS)
        pg.screenshot(path=str(p))
        b.close()
    if over > 0 or clip:
        raise SystemExit(f"[개념 한 장] 넘침 감지 — 지면 +{over}px, 잘린 블록 {clip}\n"
                         f"카피를 줄이거나 행 높이(.r1/.r2)를 조정할 것.")
    report_balance(gaps)
    return p


# --- 카드 내 균형 ---------------------------------------------------------
# v1 의 결함이 "요지 한 덩어리라 카드 아래 절반이 비었다" 였다. v2 에서 2단 설명을
# 넣어 완화했지만, 하단 블록(.box/.calc/.bars)이 margin-top:auto 로 바닥에 붙는 구조라
# 본문이 짧은 카드는 여전히 가운데가 텅 빈다. 렌더를 눈으로 봐야만 보이는 결함이라
# 매번 놓친다. 그래서 그 빈 공간을 픽셀로 재서 보고한다.
#
# 재는 것 - 단계 카드마다 '본문이 끝난 자리'와 '하단 블록이 시작하는 자리' 사이 간격.
# 이 값이 카드마다 크게 다르면 한 줄이 들쭉날쭉해 보인다.
BALANCE_SPREAD_MAX = 26      # 카드 사이 여백 차이 상한(px) - 대략 두 줄
BALANCE_GAP_MAX = 52         # 한 카드가 혼자 비어 보이기 시작하는 여백(px)
POINT_FILL_MIN = 0.55        # 세 줄 정리 칸이 이보다 덜 차면 허전해 보인다

MEASURE_JS = """()=>{
  const gapOf = (card) => {
    const t = [...card.querySelectorAll('.kv, .sd')].pop();
    if (!t) return null;
    const foot = card.querySelector('.box,.calc,.bars');
    const cb = card.getBoundingClientRect();
    const end = foot ? foot.getBoundingClientRect().top
                     : cb.bottom - parseFloat(getComputedStyle(card).paddingBottom);
    return Math.round(end - t.getBoundingClientRect().bottom);
  };
  return {
    steps: [...document.querySelectorAll('.step')].map((c,i)=>({
      n: i+1,
      title: (c.querySelector('.st') || {}).textContent || '',
      gap: gapOf(c),
      foot: !!c.querySelector('.box,.calc,.bars')
    })),
    points: [...document.querySelectorAll('.pt')].map((c)=>{
      const st = getComputedStyle(c);
      const inner = c.getBoundingClientRect().height
                  - parseFloat(st.paddingTop) - parseFloat(st.paddingBottom);
      const used = [...c.children].reduce((a,e)=>a + e.getBoundingClientRect().height, 0)
                 + (c.children.length > 1 ? 7 : 0);
      return { box: Math.round(inner), used: Math.round(used) };
    })
  };
}"""


def report_balance(m):
    """카드 내 균형을 픽셀로 보고한다.

    넘침처럼 실패시키지는 않는다 - 빈 곳은 '줄이면 되는 문제'가 아니라
    '채워야 하는 문제'라 카피 판단이 필요하기 때문이다. 대신 어느 카드를
    얼마나 늘려야 하는지까지 짚어 준다.
    """
    steps = [s for s in m["steps"] if s["gap"] is not None]
    if not steps:
        return True
    gaps = [s["gap"] for s in steps]
    spread = max(gaps) - min(gaps)
    print("[개념 한 장] 카드 내 균형 - 본문 끝과 하단 블록 사이 여백")
    for s in steps:
        mark = "" if s["gap"] <= BALANCE_GAP_MAX else "   <- 비어 보임"
        print("  %d. %-20s %4dpx%s" % (s["n"], s["title"][:20], s["gap"], mark))
    pts = m.get("points") or []
    pt_thin = []
    if pts:
        fills = [p["used"] / p["box"] if p["box"] else 1.0 for p in pts]
        print("  세 줄 정리 칸 채움 %s"
              % " · ".join("%d%%" % round(f * 100) for f in fills))
        pt_thin = [i + 1 for i, f in enumerate(fills) if f < POINT_FILL_MIN]
    ok = (spread <= BALANCE_SPREAD_MAX and max(gaps) <= BALANCE_GAP_MAX
          and not pt_thin)
    if ok:
        print("  [OK] 균형 통과 - 여백 차이 %dpx" % spread)
        return True
    if spread > BALANCE_SPREAD_MAX or max(gaps) > BALANCE_GAP_MAX:
        worst = max(steps, key=lambda s: s["gap"])
        print("  [X] 단계 카드 - 여백 차이 %dpx (상한 %d), 최대 여백 %dpx (상한 %d)"
              % (spread, BALANCE_SPREAD_MAX, max(gaps), BALANCE_GAP_MAX))
        print("      가장 빈 카드는 %d번 '%s'. 그 카드의 상세(kv)를 %d줄쯤 늘릴 것."
              % (worst["n"], worst["title"][:20], max(1, round(worst["gap"] / 21))))
    if pt_thin:
        print("  [X] 세 줄 정리 - %s번 칸이 %d%% 미만으로 비었다. 문장을 한 줄씩 늘릴 것."
              % (", ".join(str(i) for i in pt_thin), round(POINT_FILL_MIN * 100)))
    return ok
