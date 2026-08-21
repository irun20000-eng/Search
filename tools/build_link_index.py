#!/usr/bin/env python3
"""
4개 갤러리 manifest → 루트 link-index.json

본문의 [[위키링크]]를 실제 링크로 바꾸려면 갤러리 경계를 넘는 조회표가 필요하다.
([[미적분의 발견]] 은 math/ 문서에서 reports/ 문서를 가리킨다.)
각 페이지는 이 파일 하나만 더 받아오면 상호 링크가 성립한다.

■ 매칭 원칙
  추측 매칭(부분일치·유사도)을 쓰지 않는다. 틀린 링크가 미해결 링크보다 나쁘다.
  자동 정규화로 안 잡히는 것은 link-aliases.json 에 손으로 적는다.
  무엇을 적어야 하는지는 verify_math.py --backlog 가 알려준다.

■ URL 규약 (각 갤러리 index.html 에서 실측)
  reports  ./#r=<slug>          index.html:225  openBySlug
  guides   guides/#g-<slug>     guides/index.html:282
  videos   videos/#post-<id>    videos/index.html:274
  math     math/#n=<slug>

사용: python3 tools/build_link_index.py
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M          # noqa: E402

ROOT = M.ROOT
OUT = ROOT / "link-index.json"
MANUAL = ROOT / "link-aliases.json"


def load(p):
    p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def build():
    entries = []          # [{제목, 섹션, 유형, 슬러그, url}]
    alias = {}            # 별칭 -> entries 인덱스
    collide = []

    def add(idx, names):
        for a in names:
            a = M.norm(a)
            if not a:
                continue
            if a in alias and alias[a] != idx:
                prev = entries[alias[a]]
                cur = entries[idx]
                # reports 안에서의 이해편/확장편 충돌은 이해편을 택한다
                if prev["섹션"] == cur["섹션"] == "reports":
                    win = M.prefer_intro(prev["슬러그"], cur["슬러그"])
                    alias[a] = idx if win == cur["슬러그"] else alias[a]
                else:
                    collide.append((a, prev["슬러그"], cur["슬러그"]))
                continue
            alias.setdefault(a, idx)

    # ── reports ──
    for r in load("reports/manifest.json").get("reports", []):
        entries.append(dict(제목=r["title"], 섹션="reports", 유형=None,
                            슬러그=r["slug"], url="./#r=" + r["slug"]))
        add(len(entries) - 1, M.aliases_for_report(r["title"], r["slug"]))

    # ── guides ──
    for g in load("guides/manifest.json").get("guides", []):
        entries.append(dict(제목=g["title"], 섹션="guides", 유형=None,
                            슬러그=g["slug"], url="guides/#g-" + g["slug"]))
        add(len(entries) - 1, M.aliases_for_report(g["title"], g["slug"]))

    # ── videos ──
    for v in load("videos/manifest.json").get("videos", []):
        entries.append(dict(제목=v["title"], 섹션="videos", 유형=None,
                            슬러그=v["id"], url="videos/#post-" + v["id"]))
        add(len(entries) - 1, {M.norm(v["title"]), v["id"]})

    # ── math ──
    for n in load("math/manifest.json").get("notes", []):
        entries.append(dict(제목=n["제목"], 섹션="math", 유형=n.get("유형"),
                            슬러그=n["슬러그"], url="math/#n=" + n["슬러그"]))
        add(len(entries) - 1, M.aliases_for_math(n))

    # ── 수동 별칭 (자동 정규화로 안 잡히는 것) ──
    manual = load("link-aliases.json").get("별칭", {})
    by_slug = {e["슬러그"]: i for i, e in enumerate(entries)}
    unknown = []
    for a, slug in manual.items():
        if slug not in by_slug:
            unknown.append((a, slug))
            continue
        alias[M.norm(a)] = by_slug[slug]      # 수동이 자동을 덮어쓴다

    M.dump_json(OUT, {
        "generated": load("reports/manifest.json").get("generated", ""),
        "entries": entries,
        "alias": alias,
    })

    print("link-index.json: 항목 %d · 별칭 %d (수동 %d)"
          % (len(entries), len(alias), len(manual)))
    if collide:
        print("\n! 별칭 충돌 %d건 — 먼저 등록된 쪽을 유지했다:" % len(collide))
        for a, p, c in collide[:15]:
            print("   %-34s %s ← %s" % (a[:34], p, c))
    if unknown:
        print("\n! link-aliases.json 의 슬러그를 찾을 수 없다:")
        for a, s in unknown:
            print("   %r -> %r" % (a, s))
    return 0


if __name__ == "__main__":
    sys.exit(build())
