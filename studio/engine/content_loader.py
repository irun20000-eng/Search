# -*- coding: utf-8 -*-
"""
콘텐츠 로더 (Stage 4) — 카피를 JSON 데이터로 규격화.
  load(json)      : 검증 + 기본 kicker 채움
  render_deck(...) : JSON 콘텐츠 → 브랜드×레이아웃 적용 → PNG 10장
새 주제 = 이 스키마(JSON)만 채우면 같은 라인으로 찍힌다.
"""
import json, pathlib
try:
    import layout_archive as L
except Exception:
    import factory2 as L

# 슬라이드별 기본 kicker (생략 시 자동)
DEFAULT_KICKS = {"s1":"도입","s2":"궁금증","s3":"문제","s4":"전환","s5":"전환",
                 "s6":"핵심","s7":"적용","s8":"통찰","s9":"실행","s10":"마무리"}

# 슬라이드별 필수 필드 (기능별 스키마)
REQUIRED = {
 "s1":["head","sub"],                                  # 커버
 "s2":["head","body","lead"],                          # 텍스트
 "s3":["head","lead","body"],                          # 텍스트
 "s4":["head","body"],                                 # 텍스트
 "s5":["head","colA_t","colA","colB_t","colB"],        # 대비
 "s6":["head","steps"],                                # 단계
 "s7":["head","rows"],                                 # 적용/행
 "s8":["head","lead","body"],                          # 텍스트
 "s9":["head","checks"],                               # 체크리스트
 "s10":["head","sub","cta_l","cta_s","next","foot"],   # 마무리
}

def validate(c: dict):
    errs = []
    if not c.get("series"): errs.append("series(시리즈명) 누락")
    for sid, fields in REQUIRED.items():
        if sid not in c:
            errs.append(f"{sid} 슬라이드 누락"); continue
        for f in fields:
            v = c[sid].get(f)
            if v in (None, "", []): errs.append(f"{sid}.{f} 누락/빈값")
        if sid == "s6":
            for i, st in enumerate(c[sid].get("steps", [])):
                if not (isinstance(st, (list, tuple)) and len(st) == 3):
                    errs.append(f"s6.steps[{i}]는 [번호,제목,설명] 3개여야 함")
        if sid == "s7":
            for i, r in enumerate(c[sid].get("rows", [])):
                if not (isinstance(r, (list, tuple)) and len(r) == 2):
                    errs.append(f"s7.rows[{i}]는 [라벨,설명] 2개여야 함")
        for lk in ("colA", "colB", "checks"):
            if lk in REQUIRED.get(sid, []) and not isinstance(c[sid].get(lk), list):
                errs.append(f"{sid}.{lk}는 리스트여야 함")
    return errs

def load(src):
    """src: JSON 파일 경로 또는 dict → 검증된 콘텐츠 dict."""
    c = json.loads(pathlib.Path(src).read_text("utf-8")) if isinstance(src, str) else dict(src)
    c.setdefault("series", "")
    for sid, k in DEFAULT_KICKS.items():
        if isinstance(c.get(sid), dict): c[sid].setdefault("kick", k)
    errs = validate(c)
    if errs:
        raise ValueError("콘텐츠 검증 실패:\n- " + "\n- ".join(errs))
    return c

def render_deck(src, brand, layout="auto", outdir="out", prefix="card", seed=None):
    import selector as S
    c = load(src)
    theme, plan, bid, lname = S.resolve(brand, layout, c.get("series", ""), seed)
    paths = L.render_v2(c, theme, plan, range(1, 11), outdir, prefix)
    return {"brand": bid, "layout": lname, "slides": len(paths), "paths": paths}
