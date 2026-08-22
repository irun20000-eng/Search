# -*- coding: utf-8 -*-
"""
레이아웃 아카이브 (Stage 2)
- 슬라이드를 '기능'으로 보고 기능마다 배치 변형을 보유.
- build_html_v2(content, theme, plan)  → 같은 브랜드도 구성을 바꿔 렌더.
- 플랜(PLANS): 변형들을 일관되게 묶은 구성 프리셋 (정렬형/센터/구조).
"""
import pathlib, random
try:
    import carousel_engine as base
except Exception:
    import factory as base

C_DEFAULT = base.CONTENT
THEME_BY_ID = base.THEME_BY_ID
_dots = base._dots

# ── 기능별 변형 목록 ─────────────────────────────────────────────
LAYOUT_VARIANTS = {
 "cover":    ["left", "center", "fullbleed"],
 "text":     ["left", "center"],
 "contrast": ["cols", "stack", "vs"],
 "steps":    ["vertical", "timeline", "cards"],
 "rows":     ["divider", "numbered"],
 "check":    ["box", "numbered", "toggle"],
 "cta":      ["box", "center"],
}

# ── 레이아웃 플랜 (구성 프리셋) ──────────────────────────────────
PLANS = {
 "A": {"name":"정렬형","cover":"left","text":"left","contrast":"cols",
       "steps":"vertical","rows":"divider","check":"box","cta":"box"},
 "B": {"name":"센터 임팩트","cover":"center","text":"center","contrast":"stack",
       "steps":"cards","rows":"numbered","check":"numbered","cta":"center"},
 "C": {"name":"구조 강조","cover":"fullbleed","text":"left","contrast":"vs",
       "steps":"timeline","rows":"numbered","check":"toggle","cta":"box"},
}

def auto_plan(seed=None):
    """시드별로 변형을 무작위 회전 → 생성마다 다른 구성."""
    r = random.Random(seed)
    return {k: r.choice(v) for k, v in LAYOUT_VARIANTS.items()}

EXTRA_CSS = r"""
.tick{display:block}
.tickwrap{display:flex;justify-content:flex-start}
.ctr{align-items:center !important;text-align:center}
.ctr .tickwrap{justify-content:center}
.cv-fb{flex:1;display:flex;flex-direction:column;justify-content:flex-end}
.cv-rule{height:3px;background:var(--accent);width:100%;margin-top:30px}
.stack-row{padding:34px 0}
.stack-div{height:1px;background:var(--hair)}
.chiprow{display:flex;gap:20px;flex-wrap:wrap;margin-top:22px}
.pill{font-weight:600;font-size:40px;border:2px solid var(--hair);border-radius:999px;padding:14px 34px}
.vsrow{display:flex;align-items:stretch;margin-top:54px}
.vsbox{flex:1;border:2px solid var(--hair);border-radius:calc(var(--radius) + 12px);padding:44px 40px}
.vsbox .vt{font-weight:800;font-size:44px;margin-bottom:26px}
.vsbox ul li{list-style:none;font-weight:500;font-size:42px;line-height:1.7}
.vsmid{display:flex;align-items:center;justify-content:center;width:96px}
.vscircle{width:88px;height:88px;border-radius:50%;background:var(--accent);color:var(--bg);
  display:flex;align-items:center;justify-content:center;font-size:46px;font-weight:800}
.tl{display:flex;justify-content:space-between;position:relative;margin-top:80px}
.tl::before{content:"";position:absolute;left:9%;right:9%;top:43px;height:3px;background:var(--hair)}
.tlcol{flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;position:relative;z-index:1;padding:0 14px}
.tlnum{width:88px;height:88px;border-radius:50%;background:var(--accent);color:var(--bg);
  display:flex;align-items:center;justify-content:center;font-weight:900;font-size:40px}
.tlt{font-weight:800;font-size:44px;margin-top:32px}
.tld{font-weight:400;font-size:32px;color:var(--muted);margin-top:12px;line-height:1.4}
.scards{display:flex;flex-direction:column;gap:28px;margin-top:50px}
.scard{display:flex;gap:34px;align-items:center;border:2px solid var(--hair);
  border-radius:calc(var(--radius) + 12px);padding:36px 40px}
.scard .sb{min-width:98px;height:98px;border-radius:calc(var(--radius) + 6px);background:var(--accent);
  color:var(--bg);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:46px}
.scard .stt{font-weight:800;font-size:50px}
.scard .sdd{font-weight:400;font-size:36px;color:var(--muted);margin-top:8px}
.rnum{display:flex;gap:36px;align-items:baseline;padding:34px 0;border-top:1px solid var(--hair)}
.rnum:last-child{border-bottom:1px solid var(--hair)}
.rnum .rn{font-weight:900;font-size:50px;color:var(--accent);min-width:88px}
.rnum .rl{font-weight:800;font-size:46px;letter-spacing:-.01em}
.rnum .rd{font-weight:400;font-size:38px;color:var(--muted);margin-top:10px}
.cnum{display:flex;gap:30px;align-items:center;padding:32px 0;border-top:1px solid var(--hair)}
.cnum:last-child{border-bottom:1px solid var(--hair)}
.cbadge{min-width:62px;height:62px;border-radius:50%;background:var(--accent);color:var(--bg);
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:32px;flex:none}
.tog{display:flex;align-items:center;justify-content:space-between;
  border:2px solid var(--hair);border-radius:999px;padding:26px 42px;margin-bottom:24px}
.tog .tgt{font-weight:600;font-size:45px}
.tog .tgr{width:46px;height:46px;border-radius:50%;border:4px solid var(--accent);flex:none}
.ctac{align-items:center;text-align:center}
.ac-div{width:92px;height:6px;background:var(--accent);border-radius:3px;margin:36px auto 4px}
"""

# ── 헬퍼 ────────────────────────────────────────────────────────
def _meta(kick, i): return f'<div class="meta"><span class="kicker">{kick}</span><span class="pageno">{i:02d} / 10</span></div>'
def _foot(i, right): return f'<div class="foot">{_dots(i)}{right}</div>'
def _tk(t, cover=False):
    return f'<div class="tickwrap {t["tick"]}{" cv" if cover else ""}"><span class="tick"></span></div>'
def _dark(i, t):
    if t["all_dark"]: return False
    return t["cover_dark"] and i in (1, 10)
def _wrap(i, t, inner, cover=False):
    cls = "slide dark" if _dark(i, t) else "slide"
    ghost = "" if cover else f'<div class="ghost">{i:02d}</div>'
    return f'<div class="{cls}" id="s{i}"><div class="bgfx"></div>{ghost}<div class="pad">{inner}</div></div>'

# ── 슬라이드 렌더러 ──────────────────────────────────────────────
def _cover(C, t, v):
    c = C["s1"]; m = _meta(c["kick"], 1); f = _foot(1, '<span class="swipe">넘겨보기 →</span>')
    if v == "center":
        b = f'<div class="center ctr">{_tk(t,True)}<div class="h" style="font-size:138px;margin-top:46px">{c["head"]}</div><div class="lead subln" style="margin-top:48px">{c["sub"]}</div></div>'
    elif v == "fullbleed":
        b = f'<div class="cv-rule"></div><div class="cv-fb"><div class="lead subln" style="margin-bottom:28px">{c["sub"]}</div><div class="h" style="font-size:172px">{c["head"]}</div></div>'
    else:
        b = f'<div class="center">{_tk(t,True)}<div class="h" style="font-size:148px;margin-top:46px">{c["head"]}</div><div class="lead subln" style="margin-top:52px">{c["sub"]}</div></div>'
    return _wrap(1, t, m + b + f, cover=True)

def _text(C, t, v, i, key, hsize, parts):
    c = C[key]; align = "ctr" if v == "center" else ""
    inner = _tk(t) + f'<div class="h" style="font-size:{hsize}px;margin-top:34px">{c["head"]}</div>'
    for cls, field in parts:
        mt = "44px" if cls == "lead" else "40px"
        inner += f'<div class="{cls}" style="margin-top:{mt}">{c[field]}</div>'
    b = f'<div class="center {align}">{inner}</div>'
    return _wrap(i, t, m_text(c, i) + b + _foot(i, f'<span class="series">{C["series"]}</span>'))
def m_text(c, i): return _meta(c["kick"], i)

def _contrast(C, t, v):
    c = C["s5"]; head = _tk(t) + f'<div class="h" style="font-size:96px;margin-top:34px">{c["head"]}</div>'
    liA = "".join(f"<li>{x}</li>" for x in c["colA"]); liB = "".join(f"<li>{x}</li>" for x in c["colB"])
    if v == "stack":
        pA = "".join(f'<span class="pill">{x}</span>' for x in c["colA"])
        pB = "".join(f'<span class="pill">{x}</span>' for x in c["colB"])
        body = (f'<div style="margin-top:48px">'
                f'<div class="stack-row"><div class="chip"><span class="d"></span>{c["colA_t"]}</div><div class="chiprow">{pA}</div></div>'
                f'<div class="stack-div"></div>'
                f'<div class="stack-row"><div class="chip"><span class="d"></span>{c["colB_t"]}</div><div class="chiprow">{pB}</div></div></div>')
    elif v == "vs":
        body = (f'<div class="vsrow"><div class="vsbox"><div class="vt">{c["colA_t"]}</div><ul>{liA}</ul></div>'
                f'<div class="vsmid"><div class="vscircle">↔</div></div>'
                f'<div class="vsbox"><div class="vt">{c["colB_t"]}</div><ul>{liB}</ul></div></div>')
    else:
        body = (f'<div class="cols" style="margin-top:56px">'
                f'<div class="col a"><div class="chip"><span class="d"></span>{c["colA_t"]}</div><ul>{liA}</ul></div>'
                f'<div class="col b"><div class="chip"><span class="d"></span>{c["colB_t"]}</div><ul>{liB}</ul></div></div>')
    return _wrap(5, t, _meta(c["kick"],5) + f'<div class="center">{head}{body}</div>' + _foot(5, f'<span class="series">{C["series"]}</span>'))

def _steps(C, t, v):
    c = C["s6"]; head = _tk(t) + f'<div class="h" style="font-size:90px;margin-top:34px">{c["head"]}</div>'
    if v == "timeline":
        cols = "".join(f'<div class="tlcol"><div class="tlnum">{n}</div><div class="tlt">{ti}</div><div class="tld">{d}</div></div>' for n,ti,d in c["steps"])
        content = f'<div class="tl">{cols}</div>'
    elif v == "cards":
        cards = "".join(f'<div class="scard"><div class="sb">{n}</div><div><div class="stt">{ti}</div><div class="sdd">{d}</div></div></div>' for n,ti,d in c["steps"])
        content = f'<div class="scards">{cards}</div>'
    else:
        content = "".join(f'<div class="step"><div class="num">{n}</div><div><div class="st">{ti}</div><div class="sd">{d}</div></div></div>' for n,ti,d in c["steps"])
    inner = _meta(c["kick"],6) + f'<div style="margin-top:22px">{head}</div><div class="center">{content}</div>' + _foot(6, '<span class="series" style="color:var(--accent)">저장 포인트</span>')
    return _wrap(6, t, inner)

def _rows(C, t, v):
    c = C["s7"]; head = _tk(t) + f'<div class="h" style="font-size:90px;margin-top:34px">{c["head"]}</div>'
    if v == "numbered":
        content = "".join(f'<div class="rnum"><div class="rn">{i+1:02d}</div><div><div class="rl">{l}</div><div class="rd">{d}</div></div></div>' for i,(l,d) in enumerate(c["rows"]))
    else:
        content = "".join(f'<div class="row"><div class="rl">{l}</div><div class="rd">{d}</div></div>' for l,d in c["rows"])
    inner = _meta(c["kick"],7) + f'<div style="margin-top:22px">{head}</div><div class="center">{content}</div>' + _foot(7, f'<span class="series">{C["series"]}</span>')
    return _wrap(7, t, inner)

def _check(C, t, v):
    c = C["s9"]; head = _tk(t) + f'<div class="h" style="font-size:90px;margin-top:34px">{c["head"]}</div>'
    if v == "numbered":
        content = "".join(f'<div class="cnum"><div class="cbadge">{i+1}</div><span class="ct">{x}</span></div>' for i,x in enumerate(c["checks"]))
    elif v == "toggle":
        content = "".join(f'<div class="tog"><span class="tgt">{x}</span><span class="tgr"></span></div>' for x in c["checks"])
    else:
        content = "".join(f'<div class="check"><span class="bx"></span><span class="ct">{x}</span></div>' for x in c["checks"])
    inner = _meta(c["kick"],9) + f'<div style="margin-top:22px">{head}</div><div class="center">{content}</div>' + _foot(9, '<span class="series" style="color:var(--accent)">저장 포인트</span>')
    return _wrap(9, t, inner)

def _cta(C, t, v):
    c = C["s10"]; foot = _foot(10, f'<span class="swipe subln">{c["foot"]}</span>')
    if v == "center":
        b = (f'<div class="center ctac">{_tk(t,True)}<div class="h" style="font-size:96px;margin-top:40px">{c["head"]}</div>'
             f'<div class="lead subln" style="margin-top:26px">{c["sub"]}</div><div class="ac-div"></div>'
             f'<div style="font-weight:800;font-size:46px;margin-top:34px">{c["cta_l"]}</div>'
             f'<div style="font-weight:400;font-size:38px;color:var(--muted);margin-top:12px">{c["cta_s"]}</div>'
             f'<div class="next">{c["next"]}</div></div>')
    else:
        b = (f'<div class="center">{_tk(t,True)}<div class="h" style="font-size:92px;margin-top:34px">{c["head"]}</div>'
             f'<div class="lead subln" style="margin-top:30px">{c["sub"]}</div>'
             f'<div class="ctabox" style="margin-top:60px"><div class="cl">{c["cta_l"]}</div><div class="cs">{c["cta_s"]}</div></div>'
             f'<div class="next">{c["next"]}</div></div>')
    return _wrap(10, t, _meta(c["kick"],10) + b + foot)

# ── 빌드 ────────────────────────────────────────────────────────
def build_html_v2(C, t, plan):
    S = [
        _cover(C, t, plan["cover"]),
        _text(C, t, plan["text"], 2, "s2", 100, [("body","body"),("lead","lead")]),
        _text(C, t, plan["text"], 3, "s3", 100, [("lead","lead"),("body","body")]),
        _text(C, t, plan["text"], 4, "s4", 104, [("body","body")]),
        _contrast(C, t, plan["contrast"]),
        _steps(C, t, plan["steps"]),
        _rows(C, t, plan["rows"]),
        _text(C, t, plan["text"], 8, "s8", 104, [("lead","lead"),("body","body")]),
        _check(C, t, plan["check"]),
        _cta(C, t, plan["cta"]),
    ]
    style = base._root(t) + base.BULK_CSS + EXTRA_CSS
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{style}</style>'
            f'</head><body class="fx-{t["bg_fx"]}">{"".join(S)}</body></html>')

def render_v2(C, t, plan, slides, outdir, prefix, scale=1):
    from playwright.sync_api import sync_playwright
    pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
    html = build_html_v2(C, t, plan)
    f = pathlib.Path(outdir)/f"_{prefix}.html"; f.write_text(html, encoding="utf-8")
    out=[]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=scale)
        pg.goto(f.as_uri()); pg.wait_for_timeout(350)
        for i in slides:
            p=f"{outdir}/{prefix}_{i:02d}.png"; pg.query_selector(f"#s{i}").screenshot(path=p); out.append(p)
        b.close()
    return out

if __name__ == "__main__":
    TMP="/home/claude/render2"
    # 검증: 같은 브랜드(editorial_ink)로 플랜 A/B/C, 핵심 슬라이드만
    for k in ("A","B","C"):
        render_v2(C_DEFAULT, THEME_BY_ID["editorial_ink"], PLANS[k], [1,5,6,9], TMP, f"plan{k}")
    print("DONE")
