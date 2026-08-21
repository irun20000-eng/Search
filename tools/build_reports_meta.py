#!/usr/bin/env python3
"""reports/manifest.json 에 카테고리(cat)와 짝문서(pair)를 채운다.

■ 왜 필요한가
  · 태그 333종은 분류로 쓸 수 없다. 62편에 333개면 대부분 한 번만 쓰인 태그다.
    영상 갤러리가 이미 쓰는 방식대로 명시적 카테고리를 얹는다.
  · 이해편/확장편이 각각 별개 카드로 나열돼 62장 중 절반이 중복 인상을 준다.
    짝을 한 카드로 묶으려면 manifest 에 짝 정보가 있어야 한다.

■ 짝문서를 정하는 순서
  1) 원문 frontmatter 의 '짝문서' (정본, 9쌍만 갖고 있다)
  2) 슬러그 유추: X-advanced <-> X
  3) 수동 예외 — 슬러그가 어긋나는 두 쌍
       jacobian-advanced           <-> jacobian-transformation
       matrix-multivariable-advanced <-> matrix-multivariable-intro

새 보고서를 추가하면 CATS 에 한 줄 넣고 이 스크립트를 다시 돌린다.
분류되지 않은 보고서가 있으면 알려주고 '기타'로 둔다.

사용: python3 tools/build_reports_meta.py
"""
import sys
import io
import json
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M          # noqa: E402

MAN = M.ROOT / "reports" / "manifest.json"

CATEGORIES = [
    {"key": "math",    "label": "수학"},
    {"key": "ai",      "label": "AI·에이전트"},
    {"key": "auto",    "label": "자동화·생산성"},
    {"key": "science", "label": "과학·공학"},
    {"key": "society", "label": "사회·시사"},
    {"key": "culture", "label": "인문"},
]

CATS = {
    # ── 수학 ──
    "benford-law": "math", "benford-law-advanced": "math",
    "calculus-discovery": "math", "calculus-discovery-advanced": "math",
    "infinity-set-theory": "math", "infinity-set-theory-advanced": "math",
    "jacobian-transformation": "math", "jacobian-advanced": "math",
    "leslie-matrix": "math", "leslie-matrix-advanced": "math",
    "lhopital-rule": "math", "lhopital-rule-advanced": "math",
    "math-function-terms": "math", "math-function-terms-advanced": "math",
    "matrix-diagonalization": "math", "matrix-diagonalization-advanced": "math",
    "matrix-multivariable-intro": "math", "matrix-multivariable-advanced": "math",
    "mean-value-theorem": "math", "mean-value-theorem-advanced": "math",
    "polynomial-functions": "math", "polynomial-functions-advanced": "math",
    "shear-polynomial": "math", "shear-polynomial-advanced": "math",
    "spherical-geometry-curvature": "math", "spherical-geometry-curvature-advanced": "math",
    "vector": "math", "vector-advanced": "math",
    # ── AI·에이전트 ──
    "ai-engineering-evolution-graph": "ai",
    "ai-models-2026-comparison": "ai",
    "claude-cowork-mobile": "ai",
    "claude-extension-ecosystem": "ai",
    "claude-mcp-guide": "ai",
    "claude-plugins-build": "ai",
    "claude-plugins-guide": "ai",
    "claude-plugins-workflows": "ai",
    "domain-literacy-ai-era": "ai",
    "gemini-spark-agent": "ai",
    "google-flow": "ai",
    "google-flow-practice": "ai",
    "hermes-agent-deep": "ai",
    "hermes-agent-quick": "ai",
    "hermes-agent-windows": "ai",
    "higgsfield-mcp-claude": "ai",
    "orca-agent-ide": "ai",
    # ── 자동화·생산성 ──
    "chrome-extensions-work": "auto",
    "n8n-automation-guide": "auto",
    "slack-ai-bot": "auto",
    "slack-bot-build": "auto",
    "slack-solo-developer": "auto",
    "video-editing-capcut-gom": "auto",
    "zapier-automation-guide": "auto",
    # ── 과학·공학 ──
    "aerodynamic-lift": "science", "aerodynamic-lift-advanced": "science",
    "semiconductor-communication": "science", "semiconductor-communication-advanced": "science",
    "milk-yogurt-history": "science",
    # ── 사회·시사 ──
    "iran-us-conflict-timeline": "society",
    "korea-college-admission-2032": "society",
    "prosecution-reform-2026": "society",
    # ── 인문 ──
    "hesse-demian": "culture",
    "hesse-siddhartha": "culture",
}

# 슬러그로 유추할 수 없는 짝
PAIR_OVERRIDE = {
    "jacobian-advanced": "jacobian-transformation",
    "jacobian-transformation": "jacobian-advanced",
    "matrix-multivariable-advanced": "matrix-multivariable-intro",
    "matrix-multivariable-intro": "matrix-multivariable-advanced",
}


def frontmatter_pair(slug):
    p = M.ROOT / "reports" / slug / "report.md"
    if not p.exists():
        return None
    try:
        fm, _ = M.split_frontmatter(p.read_text(encoding="utf-8"), strict=False)
    except Exception:
        return None
    v = fm.get("짝문서")
    return v.strip() if isinstance(v, str) and v.strip() else None


def main():
    man = json.loads(MAN.read_text(encoding="utf-8"))
    reports = man.get("reports", [])
    by_slug = {r["slug"] for r in reports}

    unclassified, paired, tracks = [], 0, {}
    for r in reports:
        slug = r["slug"]

        # 카테고리
        cat = CATS.get(slug)
        if not cat:
            unclassified.append(slug)
            cat = "etc"
        r["cat"] = cat

        # 짝문서 — frontmatter → 수동 예외 → 슬러그 유추
        pair = frontmatter_pair(slug) or PAIR_OVERRIDE.get(slug)
        if not pair:
            guess = slug[:-9] if slug.endswith("-advanced") else slug + "-advanced"
            pair = guess if guess in by_slug else None
        if pair and pair in by_slug:
            r["pair"] = pair
            paired += 1
        else:
            r.pop("pair", None)

        # 트랙 — 확장편인지 이해편인지. 카드를 묶을 때 어느 쪽을 앞면으로 둘지 정한다.
        r["track"] = "advanced" if slug.endswith("-advanced") else "intro"
        tracks[r["track"]] = tracks.get(r["track"], 0) + 1

        # 자수 — 깊이 필터(61/62가 deep 이라 죽어 있다)를 대신해 '읽기 N분'을 보여준다.
        # 본문만 센다. 측정 방식은 verify_math.py 와 같다.
        p = M.ROOT / "reports" / slug / "report.md"
        if p.exists():
            r["chars"] = len(M.body_of(p.read_text(encoding="utf-8")))

    man["categories"] = CATEGORIES
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = {}
    for r in reports:
        counts[r["cat"]] = counts.get(r["cat"], 0) + 1
    print("reports/manifest.json 갱신: %d편" % len(reports))
    for c in CATEGORIES:
        print("   %-16s %d편" % (c["label"], counts.get(c["key"], 0)))
    if counts.get("etc"):
        print("   %-16s %d편" % ("(미분류)", counts["etc"]))
    print("짝문서 %d편(%d쌍) · 이해편 %d / 확장편 %d"
          % (paired, paired // 2, tracks.get("intro", 0), tracks.get("advanced", 0)))
    if unclassified:
        print("\n! 분류되지 않은 보고서 — CATS 에 추가할 것:")
        for s in unclassified:
            print("   ", s)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
