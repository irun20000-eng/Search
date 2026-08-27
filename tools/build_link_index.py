#!/usr/bin/env python3
"""
7개 갤러리 manifest → 루트 link-index.json

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
  blog      blog/#b=<slug>
  cardnews  cardnews/#c=<folder>
  concept   concept/#n=<slug>

■ 허브도 이 파일을 쓴다
  루트 index.html(허브)의 통합 검색과 '최근' 목록이 entries 를 그대로 읽는다.
  그래서 각 항목에 날짜를 함께 싣는다. alias 맵은 허브가 쓰지 않는다.

■ 검색어 — 제목만으로는 서가를 가로지르지 못한다
  허브 검색이 제목 문자열만 보던 때, '수학'으로 찾으면 블로그 7편만 나왔다.
  수학사 노트 제목이 '적분법'·'무한급수'라 '수학'이 들어 있지 않기 때문이다.
  서가를 합쳐 놓고도 교차점을 못 찾는 셈이라, 각 항목에 서가별 태그를 모아
  `검색어` 한 줄로 싣는다. 태그 정본은 각 갤러리 manifest 이고 이건 사본이다.
  ★ 리스트가 아니라 공백으로 이은 문자열인 이유: 이 파일은 모든 페이지가 받아 가는데
  indent=1 로 덤프하면 태그 하나가 한 줄씩 차지해 파일이 배로 부푼다.
  검색은 부분일치라 문자열이면 충분하다.
  카드뉴스는 태그가 없어 시리즈 이름과 앵글 문구를 대신 쓴다.

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


def hay(*parts):
    """태그·문구를 공백으로 이어 검색용 한 줄로. 중복은 순서를 지키며 지운다."""
    out, seen = [], set()
    for part in parts:
        if not part:
            continue
        for w in (part if isinstance(part, (list, tuple)) else [part]):
            w = str(w).strip()
            if w and w.lower() not in seen:
                seen.add(w.lower())
                out.append(w)
    return " ".join(out)


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
                            검색어=hay(r.get("tags"), r.get("cat")),
                            url="research/#r=" + r["slug"]))
        add(len(entries) - 1, M.aliases_for_report(r["title"], r["slug"]))

    # ── guides ──
    for g in load("guides/manifest.json").get("guides", []):
        entries.append(dict(제목=g["title"], 섹션="guides", 유형=None,
                            슬러그=g["slug"], 날짜=g.get("date", ""),
                            검색어=hay(g.get("tags"), g.get("level")),
                            url="guides/#g-" + g["slug"]))
        add(len(entries) - 1, M.aliases_for_report(g["title"], g["slug"]))

    # ── videos ──
    for v in load("videos/manifest.json").get("videos", []):
        entries.append(dict(제목=v["title"], 섹션="videos", 유형=None,
                            슬러그=v["id"], 날짜=v.get("added") or v.get("published", ""),
                            검색어=hay(v.get("tags"), v.get("cat"), v.get("channel")),
                            url="videos/#post-" + v["id"]))
        add(len(entries) - 1, {M.norm(v["title"]), v["id"]})

    # ── blog ──
    for b in load("blog/manifest.json").get("posts", []):
        entries.append(dict(제목=b["title"], 섹션="blog", 유형=None,
                            슬러그=b["slug"], 날짜=b.get("date", ""),
                            검색어=hay(b.get("tags"), b.get("pillar_ko")),
                            url="blog/#b=" + b["slug"]))
        add(len(entries) - 1, {M.norm(b["title"]), b["slug"]})

    # 개념노트를 카드뉴스보다 먼저 등록한다 — 이름이 같으면 먼저 등록된 쪽이 이긴다.
    # 카드뉴스 '생존자 편향'(그림 10장)과 개념노트 '생존자 편향'(이해편 5,800자)이
    # 같은 이름을 갖는데, 글 속의 [[생존자 편향]] 은 설명이 있는 쪽을 가리켜야 한다.
    # 카드뉴스는 폴더명 별칭(숫자노트_02_생존자편향)으로 그대로 닿는다.
    # ── concept (개념노트) ──
    for n in load("concept/manifest.json").get("notes", []):
        entries.append(dict(제목=n["title"], 섹션="concept", 유형=None,
                            슬러그=n["slug"], 날짜=n.get("date", ""),
                            검색어=hay(n.get("tags"), n.get("level")),
                            url="concept/#n=" + n["slug"]))
        # 제목이 '최적 정지(Optimal Stopping) — 이해편(입문·딥)' 꼴이라
        # 본문의 [[최적 정지]] 가 안 잡힌다. 짧은 이름을 별칭으로 함께 넣는다.
        short = n["title"].split(" — ")[0]
        base = short.split("(")[0].strip()
        add(len(entries) - 1, {M.norm(n["title"]), M.norm(short), M.norm(base), n["slug"]})

    # ── cardnews ──
    # 카드뉴스만 태그가 없다. 시리즈 키(discovery)는 검색어로 쓸모가 없으니
    # 사람이 부르는 이름('발견 노트')으로 바꿔 앵글 문구와 함께 싣는다.
    cardnews_man = load("cardnews/manifest.json")
    series_label = {s["key"]: s.get("label", "") for s in cardnews_man.get("series", [])}
    for c in cardnews_man.get("episodes", []):
        entries.append(dict(제목=c["title"], 섹션="cardnews", 유형=None,
                            슬러그=c["folder"], 날짜=c.get("date", ""),
                            검색어=hay(series_label.get(c.get("series")), c.get("angle")),
                            url="cardnews/#c=" + c["folder"]))
        add(len(entries) - 1, {M.norm(c["title"]), c["folder"]})

    # ── math ──
    math_man = load("math/manifest.json")
    math_gen = math_man.get("generated", "")
    for n in math_man.get("notes", []):
        entries.append(dict(제목=n["제목"], 섹션="math", 유형=n.get("유형"),
                            슬러그=n["슬러그"], 날짜=math_gen,
                            검색어=hay(n.get("태그"), n.get("분야"), n.get("교과")),
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
    rc = build()
    # 백로그는 별칭이 정해진 뒤라야 뜻이 생긴다 - 따로 돌리게 두면 반드시 잊는다.
    # (--no-backlog 로 끌 수 있다. 백로그가 깨져도 링크 인덱스는 이미 나온 뒤다.)
    if rc == 0 and "--no-backlog" not in sys.argv:
        try:
            import build_backlog
            print()
            build_backlog.build()
        except Exception as e:
            print("! 백로그 갱신 실패(링크 인덱스는 정상): %s" % e)
    sys.exit(rc)
