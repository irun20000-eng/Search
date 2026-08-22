# -*- coding: utf-8 -*-
"""
카드뉴스 공장 엔진 (carousel factory)
- 콘텐츠(CONTENT)와 브랜드(THEMES)를 분리.
- 같은 콘텐츠에 테마만 바꾸면 다른 브랜드 디자인이 나온다.
- build_html(content, theme) -> HTML  /  render_pngs(...) -> 1080x1350 PNG
"""
import json, pathlib

# ──────────────────────────────────────────────────────────────────────────
# 1) 콘텐츠 (주제/카피)  ── 주제를 바꾸려면 이 dict의 텍스트만 교체
#    <span class="ac">...</span> = 포인트 컬러 강조
# ──────────────────────────────────────────────────────────────────────────
CONTENT = {
 "series": "AI 업무 시리즈",
 "s1": {"kick":"도입","head":'빨라진 건 일,<br>줄지 않은 건<br><span class="ac">시간</span>이다',
        "sub":"AI를 써도 여전히 바쁜 진짜 이유"},
 "s2": {"kick":"궁금증","head":"문제는<br>도구가 아니다",
        "body":"같은 AI를 써도<br>누구는 두 시간을 벌고<br>누구는 그대로다.",
        "lead":'차이는 <span class="ac">쓰는 방식</span>에서 갈린다.'},
 "s3": {"kick":"문제","head":"가장 흔한 실수",
        "lead":"하던 일을 그대로<br>AI에게 떠넘긴다.",
        "body":"빨라진 만큼<br>더 많은 일이 돌아온다."},
 "s4": {"kick":"전환","head":'속도보다<br><span class="ac">제거</span>가 먼저다',
        "body":"AI의 진짜 쓸모는<br>더 빨리 하는 게 아니라<br>안 해도 될 일을 골라내는 것."},
 "s5": {"kick":"전환","head":"반복은 맡기고<br>판단은 쥔다",
        "colA_t":"AI에 맡긴다","colA":["요약","정리","초안","분류"],
        "colB_t":"내가 쥔다","colB":["방향","선택","책임"]},
 "s6": {"kick":"핵심","head":"시간을 버는<br>3단계",
        "steps":[["01","비우기","없앨 일을 먼저 고른다"],
                 ["02","맡기기","반복 작업을 AI에 넘긴다"],
                 ["03","다듬기","결과를 내 기준으로 고친다"]]},
 "s7": {"kick":"적용","head":"오늘부터<br>이렇게",
        "rows":[["이메일","초안은 AI에게, 나는 다듬기만"],
                ["회의록","녹음을 요약본으로 받아 정리"],
                ["반복 문서","템플릿을 만들고 빈칸만 AI로"]]},
 "s8": {"kick":"통찰","head":"AI는 시간을<br>만들지 않는다",
        "lead":"단지 옮겨줄 뿐이다.",
        "body":'비운 자리를 <span class="ac" style="font-weight:700">무엇으로</span> 채울지,<br>그게 진짜 차이를 만든다.'},
 "s9": {"kick":"실행","head":"이번 주<br>실행 체크",
        "checks":["반복 업무 3가지 적어보기","그중 1가지를 AI에 맡기기",
                  "사람이 할 일과 분리하기","번 시간을 미리 정해두기"]},
 "s10":{"kick":"마무리","head":"바쁨은<br>줄지 않는다","sub":"구조를 바꾸기 전까지는.",
        "cta_l":"도움이 됐다면 저장해두세요.","cta_s":"필요할 때 다시 꺼내 쓰도록.",
        "next":"다음 편 · 실제로 쓰는 AI 업무 루틴","foot":"반복 업무는 댓글로 →"},
}

# ──────────────────────────────────────────────────────────────────────────
# 2) 브랜드 템플릿 (테마 토큰)  ── 새 브랜드 = 아래에 dict 하나 추가
# ──────────────────────────────────────────────────────────────────────────
SANS  = "'Noto Sans CJK KR'"
SERIF = "'Noto Serif CJK KR'"
MONO  = "'Noto Sans Mono CJK KR'"

THEMES = [
 {"id":"editorial_ink","name":"에디토리얼 잉크","tag":"프리미엄 리포트",
  "fd":SANS,"fb":SANS,"fl":SANS,"dw":900,"radius":13,"tick":"bar","bg_fx":"ghost",
  "cover_dark":True,"all_dark":False,
  "bg":"#F2EEE6","ink":"#15171C","accent":"#2742E0","muted":"#5C5F69","hair":"rgba(20,22,28,.14)","subln":"#5C5F69",
  "dbg":"#15171C","dink":"#F2EEE6","dac":"#6E86FF","dmut":"#9AA2B0","dhair":"rgba(255,255,255,.16)","dsubln":"#C9CCD6"},

 {"id":"bold_social","name":"볼드 소셜","tag":"크리에이터/SNS",
  "fd":SANS,"fb":SANS,"fl":SANS,"dw":900,"radius":8,"tick":"bar","bg_fx":"flat",
  "cover_dark":True,"all_dark":False,
  "bg":"#F2F0EC","ink":"#0B0B0C","accent":"#FF3B2F","muted":"#5A5A5C","hair":"rgba(10,10,12,.14)","subln":"#5A5A5C",
  "dbg":"#0B0B0C","dink":"#F2F0EC","dac":"#FF5B4D","dmut":"#9A9A9C","dhair":"rgba(255,255,255,.16)","dsubln":"#CFCFCF"},

 {"id":"magazine_noir","name":"매거진 누아르","tag":"럭셔리/감성",
  "fd":SERIF,"fb":SANS,"fl":SANS,"dw":900,"radius":0,"tick":"thin","bg_fx":"flat",
  "cover_dark":True,"all_dark":False,
  "bg":"#ECE7DE","ink":"#1C1A17","accent":"#9A7B3F","muted":"#6B6256","hair":"rgba(28,26,23,.16)","subln":"#6B6256",
  "dbg":"#211E1B","dink":"#ECE7DE","dac":"#C9A24B","dmut":"#A39A8B","dhair":"rgba(255,255,255,.16)","dsubln":"#CFC8BD"},

 {"id":"instructional_clean","name":"인스트럭셔널 클린","tag":"교육/가이드",
  "fd":SANS,"fb":SANS,"fl":SANS,"dw":800,"radius":22,"tick":"none","bg_fx":"dots",
  "cover_dark":False,"all_dark":False,
  "bg":"#FFFFFF","ink":"#16243B","accent":"#2D7CF5","muted":"#5A6B86","hair":"rgba(20,40,80,.13)","subln":"#5A6B86",
  "dbg":"#16243B","dink":"#FFFFFF","dac":"#5E9CFF","dmut":"#9FB0CC","dhair":"rgba(255,255,255,.18)","dsubln":"#CFD9EC"},

 {"id":"newsletter_modern","name":"뉴스레터 모던","tag":"트렌드/이슈",
  "fd":SANS,"fb":SANS,"fl":MONO,"dw":900,"radius":4,"tick":"bar","bg_fx":"grid",
  "cover_dark":True,"all_dark":False,
  "bg":"#F4EFE4","ink":"#14130F","accent":"#B5402B","muted":"#5F584C","hair":"rgba(20,19,15,.14)","subln":"#5F584C",
  "dbg":"#1A1813","dink":"#F4EFE4","dac":"#E0795F","dmut":"#9C9486","dhair":"rgba(255,255,255,.15)","dsubln":"#CDC6B8"},

 {"id":"dark_tech","name":"다크 테크","tag":"AI/테크",
  "fd":SANS,"fb":SANS,"fl":MONO,"dw":900,"radius":10,"tick":"bar","bg_fx":"grid",
  "cover_dark":False,"all_dark":True,
  "bg":"#0E1116","ink":"#E9EEF5","accent":"#3DE0C2","muted":"#8A94A6","hair":"rgba(255,255,255,.10)","subln":"#8A94A6",
  "dbg":"#0E1116","dink":"#E9EEF5","dac":"#3DE0C2","dmut":"#8A94A6","dhair":"rgba(255,255,255,.10)","dsubln":"#8A94A6"},
]
THEME_BY_ID = {t["id"]: t for t in THEMES}

# ──────────────────────────────────────────────────────────────────────────
# 3) 렌더 엔진
# ──────────────────────────────────────────────────────────────────────────
BULK_CSS = r"""
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
html,body{background:#3a3a3a}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;word-break:keep-all;line-break:strict;
  background:var(--bg);color:var(--ink)}
.slide.dark{background:var(--bg);color:var(--ink)}
.bgfx{position:absolute;inset:0;pointer-events:none;z-index:0}
.pad{position:absolute;inset:0;z-index:1;padding:104px 96px;display:flex;flex-direction:column}
.meta{display:flex;justify-content:space-between;align-items:center}
.kicker{font-weight:700;font-size:29px;letter-spacing:.22em}
.pageno{font-weight:700;font-size:29px;letter-spacing:.12em;color:var(--muted)}
.tick{background:var(--accent);border-radius:5px}
.h{letter-spacing:-.025em;line-height:1.07}
.ac{color:var(--accent)}
.body{font-weight:400;font-size:45px;line-height:1.6;color:var(--muted)}
.lead{font-weight:500;font-size:50px;line-height:1.5}
.subln{color:var(--subln)}
.center{flex:1;display:flex;flex-direction:column;justify-content:center}
.foot{display:flex;justify-content:space-between;align-items:center}
.dots{display:flex;gap:13px;align-items:center}
.dot{width:15px;height:15px;border-radius:50%;background:var(--hair)}
.dot.on{background:var(--accent);width:40px;border-radius:8px}
.swipe{font-weight:700;font-size:28px;letter-spacing:.05em;color:var(--muted)}
.series{font-weight:700;font-size:27px;letter-spacing:.16em;color:var(--muted)}
.step{display:flex;gap:40px;align-items:flex-start;padding:34px 0;border-top:1px solid var(--hair)}
.step:last-child{border-bottom:1px solid var(--hair)}
.step .num{font-weight:900;font-size:60px;color:var(--accent);line-height:1;min-width:96px}
.step .st{font-weight:800;font-size:50px;letter-spacing:-.01em}
.step .sd{font-weight:400;font-size:38px;color:var(--muted);margin-top:12px;line-height:1.45}
.row{padding:36px 0;border-top:1px solid var(--hair)}
.row:last-child{border-bottom:1px solid var(--hair)}
.row .rl{font-weight:800;font-size:46px;letter-spacing:-.01em}
.row .rd{font-weight:400;font-size:38px;color:var(--muted);margin-top:10px}
.cols{display:flex;margin-top:14px}
.col{flex:1}
.col.b{border-left:1px solid var(--hair);padding-left:52px}
.col.a{padding-right:52px}
.chip{font-weight:800;font-size:38px;margin-bottom:30px}
.chip .d{display:inline-block;width:18px;height:18px;border-radius:50%;background:var(--accent);margin-right:16px;vertical-align:middle}
.col li{list-style:none;font-weight:500;font-size:44px;line-height:1.8}
.check{display:flex;gap:30px;align-items:center;padding:32px 0;border-top:1px solid var(--hair)}
.check:last-child{border-bottom:1px solid var(--hair)}
.bx{width:52px;height:52px;border:3px solid var(--ink);border-radius:var(--radius);flex:none}
.ct{font-weight:500;font-size:47px;letter-spacing:-.01em}
.ctabox{border:2px solid var(--hair);border-radius:calc(var(--radius) + 14px);padding:48px 52px;margin-top:8px}
.ctabox .cl{font-weight:800;font-size:46px;line-height:1.45}
.ctabox .cs{font-weight:400;font-size:38px;color:var(--muted);margin-top:14px}
.next{font-weight:700;font-size:34px;color:var(--accent);margin-top:48px;letter-spacing:-.01em}
.ghost{position:absolute;font-weight:900;font-size:640px;color:var(--hair);right:-40px;bottom:-180px;
  line-height:.8;letter-spacing:-.04em;display:none}
/* tick variants */
.tickwrap.bar .tick{width:76px;height:9px}
.tickwrap.bar.cv .tick{width:120px}
.tickwrap.thin .tick{width:130px;height:2px;border-radius:0}
.tickwrap.thin.cv .tick{width:170px}
.tickwrap.none .tick{display:none}
/* background fx */
.fx-grid .bgfx{background-image:
  linear-gradient(var(--hair) 1px,transparent 1px),
  linear-gradient(90deg,var(--hair) 1px,transparent 1px);
  background-size:135px 135px;opacity:.6}
.fx-dots .bgfx{background-image:radial-gradient(var(--hair) 2.5px,transparent 2.6px);
  background-size:60px 60px;opacity:.7}
.fx-ghost .ghost{display:block}
"""

def _root(t):
    return (f":root{{--bg:{t['bg']};--ink:{t['ink']};--accent:{t['accent']};--muted:{t['muted']};"
            f"--hair:{t['hair']};--subln:{t['subln']};--radius:{t['radius']}px}}"
            f".slide.dark{{--bg:{t['dbg']};--ink:{t['dink']};--accent:{t['dac']};--muted:{t['dmut']};"
            f"--hair:{t['dhair']};--subln:{t['dsubln']}}}"
            f".slide{{font-family:{t['fb']},sans-serif}}"
            f".h{{font-family:{t['fd']},serif;font-weight:{t['dw']}}}"
            f".kicker,.pageno,.series,.swipe{{font-family:{t['fl']},sans-serif}}")

def _dots(active):
    return '<div class="dots">'+''.join(
        f'<span class="dot{" on" if i==active else ""}"></span>' for i in range(1,11))+'</div>'

def _slide(i, theme, inner, dark, cover=False):
    cls = "slide dark" if dark else "slide"
    tw = f'tickwrap {theme["tick"]}{" cv" if cover else ""}'
    ghost = f'<div class="ghost">{i:02d}</div>' if not cover else ''
    return (f'<div class="{cls}" id="s{i}"><div class="bgfx"></div>{ghost}'
            f'<div class="pad">{inner.replace("@TICK@", f"<div class=\'{tw}\'><span class=\'tick\'></span></div>")}'
            f'</div></div>')

def build_html(C, t):
    # 슬라이드별 다크 여부
    def isdark(i):
        if t["all_dark"]: return False  # all_dark는 light 팔레트를 어둡게 정의 → dark 클래스 불필요
        return t["cover_dark"] and i in (1,10)

    S=[]
    # 1 cover
    S.append(_slide(1,t,
      f'<div class="meta"><span class="kicker">{C["s1"]["kick"]}</span><span class="pageno">01 / 10</span></div>'
      f'<div class="center"><div style="margin-bottom:46px">@TICK@</div>'
      f'<div class="h" style="font-size:148px">{C["s1"]["head"]}</div>'
      f'<div class="lead subln" style="margin-top:52px">{C["s1"]["sub"]}</div></div>'
      f'<div class="foot">{_dots(1)}<span class="swipe">넘겨보기 →</span></div>',
      isdark(1), cover=True))
    # 2
    S.append(_slide(2,t,
      f'<div class="meta"><span class="kicker">{C["s2"]["kick"]}</span><span class="pageno">02 / 10</span></div>'
      f'<div class="center"><div style="margin-bottom:38px">@TICK@</div>'
      f'<div class="h" style="font-size:100px">{C["s2"]["head"]}</div>'
      f'<div class="body" style="margin-top:46px">{C["s2"]["body"]}</div>'
      f'<div class="lead" style="margin-top:44px">{C["s2"]["lead"]}</div></div>'
      f'<div class="foot">{_dots(2)}<span class="series">{C["series"]}</span></div>', isdark(2)))
    # 3
    S.append(_slide(3,t,
      f'<div class="meta"><span class="kicker">{C["s3"]["kick"]}</span><span class="pageno">03 / 10</span></div>'
      f'<div class="center"><div style="margin-bottom:38px">@TICK@</div>'
      f'<div class="h" style="font-size:100px">{C["s3"]["head"]}</div>'
      f'<div class="lead" style="margin-top:46px">{C["s3"]["lead"]}</div>'
      f'<div class="body" style="margin-top:40px">{C["s3"]["body"]}</div></div>'
      f'<div class="foot">{_dots(3)}<span class="series">{C["series"]}</span></div>', isdark(3)))
    # 4
    S.append(_slide(4,t,
      f'<div class="meta"><span class="kicker">{C["s4"]["kick"]}</span><span class="pageno">04 / 10</span></div>'
      f'<div class="center"><div style="margin-bottom:38px">@TICK@</div>'
      f'<div class="h" style="font-size:104px">{C["s4"]["head"]}</div>'
      f'<div class="body" style="margin-top:48px">{C["s4"]["body"]}</div></div>'
      f'<div class="foot">{_dots(4)}<span class="series">{C["series"]}</span></div>', isdark(4)))
    # 5 two col
    colA="".join(f"<li>{x}</li>" for x in C["s5"]["colA"])
    colB="".join(f"<li>{x}</li>" for x in C["s5"]["colB"])
    S.append(_slide(5,t,
      f'<div class="meta"><span class="kicker">{C["s5"]["kick"]}</span><span class="pageno">05 / 10</span></div>'
      f'<div class="center"><div style="margin-bottom:38px">@TICK@</div>'
      f'<div class="h" style="font-size:96px">{C["s5"]["head"]}</div>'
      f'<div class="cols" style="margin-top:60px">'
      f'<div class="col a"><div class="chip"><span class="d"></span>{C["s5"]["colA_t"]}</div><ul>{colA}</ul></div>'
      f'<div class="col b"><div class="chip"><span class="d"></span>{C["s5"]["colB_t"]}</div><ul>{colB}</ul></div>'
      f'</div></div><div class="foot">{_dots(5)}<span class="series">{C["series"]}</span></div>', isdark(5)))
    # 6 steps
    steps="".join(f'<div class="step"><div class="num">{n}</div><div><div class="st">{ti}</div><div class="sd">{d}</div></div></div>' for n,ti,d in C["s6"]["steps"])
    S.append(_slide(6,t,
      f'<div class="meta"><span class="kicker">{C["s6"]["kick"]}</span><span class="pageno">06 / 10</span></div>'
      f'<div style="margin-top:30px"><div style="margin-bottom:34px">@TICK@</div>'
      f'<div class="h" style="font-size:90px">{C["s6"]["head"]}</div></div>'
      f'<div style="margin-top:52px">{steps}</div>'
      f'<div class="foot" style="margin-top:auto">{_dots(6)}<span class="series" style="color:var(--accent)">저장 포인트</span></div>', isdark(6)))
    # 7 rows
    rows="".join(f'<div class="row"><div class="rl">{l}</div><div class="rd">{d}</div></div>' for l,d in C["s7"]["rows"])
    S.append(_slide(7,t,
      f'<div class="meta"><span class="kicker">{C["s7"]["kick"]}</span><span class="pageno">07 / 10</span></div>'
      f'<div style="margin-top:30px"><div style="margin-bottom:34px">@TICK@</div>'
      f'<div class="h" style="font-size:90px">{C["s7"]["head"]}</div></div>'
      f'<div style="margin-top:50px">{rows}</div>'
      f'<div class="foot" style="margin-top:auto">{_dots(7)}<span class="series">{C["series"]}</span></div>', isdark(7)))
    # 8
    S.append(_slide(8,t,
      f'<div class="meta"><span class="kicker">{C["s8"]["kick"]}</span><span class="pageno">08 / 10</span></div>'
      f'<div class="center"><div style="margin-bottom:38px">@TICK@</div>'
      f'<div class="h" style="font-size:104px">{C["s8"]["head"]}</div>'
      f'<div class="lead" style="margin-top:44px">{C["s8"]["lead"]}</div>'
      f'<div class="body" style="margin-top:46px">{C["s8"]["body"]}</div></div>'
      f'<div class="foot">{_dots(8)}<span class="series">{C["series"]}</span></div>', isdark(8)))
    # 9 checklist
    checks="".join(f'<div class="check"><span class="bx"></span><span class="ct">{x}</span></div>' for x in C["s9"]["checks"])
    S.append(_slide(9,t,
      f'<div class="meta"><span class="kicker">{C["s9"]["kick"]}</span><span class="pageno">09 / 10</span></div>'
      f'<div style="margin-top:30px"><div style="margin-bottom:34px">@TICK@</div>'
      f'<div class="h" style="font-size:90px">{C["s9"]["head"]}</div></div>'
      f'<div style="margin-top:48px">{checks}</div>'
      f'<div class="foot" style="margin-top:auto">{_dots(9)}<span class="series" style="color:var(--accent)">저장 포인트</span></div>', isdark(9)))
    # 10 cta
    S.append(_slide(10,t,
      f'<div class="meta"><span class="kicker">{C["s10"]["kick"]}</span><span class="pageno">10 / 10</span></div>'
      f'<div class="center"><div style="margin-bottom:44px">@TICK@</div>'
      f'<div class="h" style="font-size:92px">{C["s10"]["head"]}</div>'
      f'<div class="lead subln" style="margin-top:30px">{C["s10"]["sub"]}</div>'
      f'<div class="ctabox" style="margin-top:60px"><div class="cl">{C["s10"]["cta_l"]}</div><div class="cs">{C["s10"]["cta_s"]}</div></div>'
      f'<div class="next">{C["s10"]["next"]}</div></div>'
      f'<div class="foot">{_dots(10)}<span class="swipe subln">{C["s10"]["foot"]}</span></div>',
      isdark(10), cover=True))

    bodycls=f'fx-{t["bg_fx"]}'
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{_root(t)}{BULK_CSS}</style>'
            f'</head><body class="{bodycls}">{"".join(S)}</body></html>')

def render_pngs(C, t, slides, outdir, prefix, scale=1):
    from playwright.sync_api import sync_playwright
    pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
    html = build_html(C, t)
    f = pathlib.Path(outdir)/f"_{t['id']}.html"; f.write_text(html, encoding="utf-8")
    paths=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch()
        pg=b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=scale)
        pg.goto(f.as_uri()); pg.wait_for_timeout(350)
        for i in slides:
            p=f"{outdir}/{prefix}_{i:02d}.png"
            pg.query_selector(f"#s{i}").screenshot(path=p); paths.append(p)
        b.close()
    return paths

if __name__ == "__main__":
    OUT="/mnt/user-data/outputs"
    TMP="/home/claude/render"
    # (A) 전체 브랜드: 커버(1) + 핵심(6) 렌더 → 라인업용
    for t in THEMES:
        render_pngs(CONTENT, t, [1,6], TMP, t["id"])
    # (B) 적용 증명: 신규 브랜드 '다크 테크' 풀세트 10장
    render_pngs(CONTENT, THEME_BY_ID["dark_tech"], list(range(1,11)), OUT, "다크테크")
    print("DONE")
