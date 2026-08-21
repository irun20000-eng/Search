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

■ URL 규약 (루트 기준 상대경로)
  research  research/#r=<slug>    갤러리는 research/, 마크다운 데이터는 reports/ 에 남는다
  guides    guides/#g-<slug>
  videos    videos/#post-<id>
  math      math/#n=<slug>

■ 허브도 이 파일을 쓴다
  루트 index.html(허브)의 통합 검색과 '최근' 목록이 entries 를 그대로 읽는다.
  그래서 각 항목에 날짜를 함께 싣는다. alias 맵은 허브가 쓰지 않는다.

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
        # 별칭은 집합으로 만들어지는데 파이썬 집합의 순회 순서는 실행마다 달라진다.
        # 정렬해서 넣지 않으면 내용이 같아도 매번 수백 줄짜리 diff 가 난다.
        for a in sorted(names):
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

    # ── reports (갤러리는 research/, 데이터는 reports/ 에 남는다) ──
    for r in load("reports/manifest.json").get("reports", []):
        entries.append(dict(제목=r["title"], 섹션="research", 유형=None,
                            슬러그=r["slug"], 날짜=r.get("date", ""),
                            url="research/#r=" + r["slug"]))
        add(len(entries) - 1, M.aliases_for_report(r["title"], r["slug"]))

    # ── guides ──
    for g in load("guides/manifest.json").get("guides", []):
        entries.append(dict(제목=g["title"], 섹션="guides", 유형=None,
                            슬러그=g["slug"], 날짜=g.get("date", ""),
                            url="guides/#g-" + g["slug"]))
        add(len(entries) - 1, M.aliases_for_report(g["title"], g["slug"]))

    # ── videos ──
    for v in load("videos/manifest.json").get("videos", []):
        entries.append(dict(제목=v["title"], 섹션="videos", 유형=None,
                            슬러그=v["id"], 날짜=v.get("added") or v.get("published", ""),
                            url="videos/#post-" + v["id"]))
        add(len(entries) - 1, {M.norm(v["title"]), v["id"]})

    # ── math ──
    math_man = load("math/manifest.json")
    math_gen = math_man.get("generated", "")
    for n in math_man.get("notes", []):
        entries.append(dict(제목=n["제목"], 섹션="math", 유형=n.get("유형"),
                            슬러그=n["슬러그"], 날짜=math_gen,
                            url="math/#n=" + n["슬러그"]))
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
