#!/usr/bin/env python3
"""미해결 위키링크 → 콘텐츠 백로그.

`[[X]]` 를 썼는데 X 가 아직 없으면 갤러리에서 점선으로 렌더된다. 그건 결함이 아니라
**아직 안 쓴 글**이다. 여러 문서가 반복해서 부르는 이름일수록 먼저 쓸 값이 있다.
`verify_math.py --backlog` 이 math/ 안에서 하던 일을 일곱 서가 전부로 넓힌 것이다.

두 무더기로 나눈다 — 섞어 두면 목록이 쓸모없어진다.

  · 백로그   아직 문서가 없다. 새로 써야 한다.
  · 별칭구멍 문서는 있는데 이름이 안 맞아 못 찾는다. **글을 쓸 게 아니라
             `build_link_index.py` 의 별칭을 고쳐야 한다.**

또 짝 문서(`X 확장편`)는 따로 표시한다. 새 개념을 파는 것과 이미 쓴 글의 심화편을
쓰는 것은 드는 품이 다르다.

산출: backlog.json (루트) — backlog.html 이 읽는다.
사용: python tools/build_backlog.py [--print]
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "backlog.json"

WIKI_RE = re.compile(r"\[\[([^\]\[|]+?)(?:\|([^\]\[]*))?\]\]")

# 어떤 서가의 어떤 파일을 훑고, 그 문서를 무엇으로 부를지.
# manifest 를 그대로 쓰면 갤러리에 실제로 뜨는 문서만 훑게 된다 — 초안·삭제분이 안 섞인다.
SHELVES = [
    ("research", "reports/manifest.json", "reports", "title", "slug",
     lambda r: r["path"], lambda r: "research/#r=" + r["slug"]),
    ("guides", "guides/manifest.json", "guides", "title", "slug",
     lambda g: "guides/" + g["path"], lambda g: "guides/#g=" + g["slug"]),
    ("videos", "videos/manifest.json", "videos", "title", "id",
     lambda v: "videos/" + v["path"], lambda v: "videos/#post-" + v["id"]),
    ("concept", "concept/manifest.json", "notes", "title", "slug",
     lambda n: n["path"], lambda n: "concept/#n=" + n["slug"]),
]

LABEL = {"research": "리서치", "videos": "영상노트", "guides": "가이드", "math": "수학사",
         "blog": "블로그", "cardnews": "카드뉴스", "concept": "개념노트"}


def loose(s: str) -> str:
    """이름이 '사실상 같은지' 보는 헐거운 열쇠.

    별칭구멍을 찾는 데만 쓴다 — 띄어쓰기·괄호병기·문장부호만 다른 경우를 잡는다.
    """
    s = M.strip_gloss(M.norm(s)).lower()
    return re.sub(r"[^0-9a-z가-힣]+", "", s)


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def iter_docs():
    """(섹션, 제목, url, 본문) 을 하나씩 내놓는다."""
    for sec, man, key, tkey, skey, pathf, urlf in SHELVES:
        for it in load(man).get(key, []):
            f = ROOT / pathf(it)
            if not f.exists():
                continue
            yield sec, it[tkey], urlf(it), f.read_text(encoding="utf-8")

    # math 는 노트 구조가 달라 따로 (mathlib 이 이미 아는 길이 있다)
    for slug, path in M.iter_notes():
        try:
            fm, body = M.read_note(path)
        except ValueError:
            continue
        yield "math", fm.get("제목", slug), "math/#n=" + slug, body


def build(verbose=False):
    idx = M.load_link_index()                    # 별칭 -> 아무 값 (존재 여부만 본다)
    by_loose = {}
    for a in idx:
        by_loose.setdefault(loose(a), a)

    count = Counter()
    refs = {}
    scanned = resolved = 0

    for sec, title, url, body in iter_docs():
        scanned += 1
        seen_here = Counter()
        for m in WIKI_RE.finditer(body):
            t = M.norm(m.group(1))
            if not t:
                continue
            if t in idx:
                resolved += 1
                continue
            count[t] += 1
            seen_here[t] += 1
        for t, n in seen_here.items():
            refs.setdefault(t, []).append({"t": title, "u": url, "s": sec, "n": n})

    items = []
    for t, c in count.most_common():
        lk = loose(t)
        # 짝 문서인가 — 'X 확장편' 에서 X 가 이미 있으면 심화편을 쓰라는 뜻
        base = re.sub(r"\s*(확장편|이해편)\s*$", "", t).strip()
        companion = base != t and (base in idx or loose(base) in by_loose)
        # 별칭구멍인가 — 이름만 안 맞고 문서는 있다
        gap = by_loose.get(lk) if not companion else None
        items.append({
            "name": t,
            "count": c,
            "kind": "gap" if gap else ("companion" if companion else "new"),
            "target": gap,
            "base": base if companion else None,
            "refs": sorted(refs.get(t, []), key=lambda r: -r["n"]),
        })

    data = {
        "generated": datetime.date.today().isoformat(),
        "scanned": scanned,
        "resolved": resolved,
        "pending": sum(count.values()),
        "counts": {k: sum(1 for i in items if i["kind"] == k) for k in ("new", "companion", "gap")},
        "items": items,
    }
    M.dump_json(OUT, data)

    print("[OK] 훑은 문서 %d · 해결 %d회 · 미해결 %d종 %d회"
          % (scanned, resolved, len(items), data["pending"]))
    print("     새로 쓸 것 %d · 짝 문서 %d · 별칭구멍 %d"
          % (data["counts"]["new"], data["counts"]["companion"], data["counts"]["gap"]))

    if data["counts"]["gap"]:
        print("\n! 별칭구멍 — 문서는 있는데 이름이 안 맞는다. 글이 아니라 별칭을 고칠 것:")
        for i in items:
            if i["kind"] == "gap":
                print("   %3d회  %-28s → %s" % (i["count"], i["name"][:28], i["target"]))

    if verbose:
        print("\n── 새로 쓸 것 (참조가 많은 순) ──")
        for i in items:
            if i["kind"] != "new":
                continue
            src = ", ".join("%s" % r["t"][:18] for r in i["refs"][:2])
            print("  %3d회  %-30s  ← %s" % (i["count"], i["name"][:30], src))
    return 0


if __name__ == "__main__":
    raise SystemExit(build(verbose="--print" in sys.argv))
