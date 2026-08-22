# -*- coding: utf-8 -*-
"""
셀렉터 (Stage 3) — 한 줄 규약을 (브랜드 토큰 × 레이아웃 플랜)으로 해석.
  spec:  "주제: ... / 브랜드: bold_social / 레이아웃: B"
  - 브랜드 생략 → 주제 키워드로 자동 선택
  - 레이아웃 생략/auto → auto_plan(회전)
"""
import re, pathlib
try:
    import layout_archive as L
    import carousel_engine as base
except Exception:
    import factory2 as L
    import factory as base

PLANS = L.PLANS
THEME_BY_ID = base.THEME_BY_ID

# 주제 키워드 → 브랜드 자동 매핑
BRAND_AUTO = {
 "dark_tech":           ["ai","인공지능","개발","코딩","코드","테크","데이터","자동화","프로그래밍","gpt","llm","머신러닝"],
 "bold_social":         ["sns","인스타","릴스","숏폼","유튜브","크리에이터","마케팅","브랜딩","팔로워","콘텐츠","바이럴"],
 "magazine_noir":       ["뷰티","패션","럭셔리","향수","라이프","감성","여행","인테리어","와인","호텔","미니멀"],
 "instructional_clean": ["방법","하는 법","가이드","입문","기초","튜토리얼","노하우","공부","정리법","단계","활용법"],
 "newsletter_modern":   ["트렌드","이슈","뉴스","시장","최신","동향","전망","리포트","분석"],
 "editorial_ink":       ["비즈니스","전략","경영","투자","금융","생산성","업무","커리어","리더십","협상"],
}
DEFAULT_BRAND = "editorial_ink"

def pick_brand(topic: str) -> str:
    t = (topic or "").lower()
    best, score = DEFAULT_BRAND, 0
    for bid, kws in BRAND_AUTO.items():
        s = sum(1 for k in kws if k in t)
        if s > score: best, score = bid, s
    return best

def parse_spec(text: str) -> dict:
    out = {"topic":"", "brand":None, "layout":None, "extra":{}}
    for raw in (text or "").splitlines():
        m = re.match(r"\s*([가-힣A-Za-z]+)\s*[:：]\s*(.+)", raw)
        if not m: continue
        key, val = m.group(1).strip(), m.group(2).strip()
        if key in ("주제","토픽"):        out["topic"]  = val
        elif key in ("브랜드","테마"):     out["brand"]  = val
        elif key in ("레이아웃","구성"):   out["layout"] = val
        else:                              out["extra"][key] = val
    return out

def resolve(brand=None, layout=None, topic="", seed=None):
    bid = brand if (brand and brand in THEME_BY_ID and brand!="auto") else pick_brand(topic)
    lay = (layout or "auto").strip()
    if lay.upper() in PLANS:           plan, lname = PLANS[lay.upper()], lay.upper()
    else:                              plan, lname = L.auto_plan(seed), "auto"
    return THEME_BY_ID[bid], plan, bid, lname

def make_from_spec(text, content=None, outdir="out", prefix="card", slides=range(1,11), seed=None):
    content = content or base.CONTENT
    s = parse_spec(text)
    theme, plan, bid, lname = resolve(s["brand"], s["layout"], s["topic"], seed)
    paths = L.render_v2(content, theme, plan, slides, outdir, prefix)
    return {"brand":bid, "layout":lname, "topic":s["topic"], "paths":paths}

if __name__ == "__main__":
    tests = [
        "주제: AI로 업무시간 줄이기",                          # 브랜드 자동(dark_tech), 레이아웃 auto
        "주제: 프리랜서가 단가를 낮추면 안 되는 이유\n브랜드: bold_social\n레이아웃: B",
        "주제: 미니멀 향수 입문 가이드",                        # 자동(magazine_noir)
        "주제: 2026 콘텐츠 마케팅 트렌드\n레이아웃: C",          # 자동(bold_social/newsletter), C
    ]
    for t in tests:
        s = parse_spec(t); th, pl, bid, ln = resolve(s["brand"], s["layout"], s["topic"], seed=1)
        print(f"입력: {t.splitlines()[0]:35s} → 브랜드={bid:20s} 레이아웃={ln:5s} (cover={pl['cover']}, steps={pl['steps']})")
