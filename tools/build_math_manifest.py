#!/usr/bin/env python3
"""
math/notes/<슬러그>/note.md → math/manifest.json

역인덱스를 빌드 시점에 만들어 클라이언트를 가볍게 유지한다.
(세기 뷰·역링크 패널이 런타임에 전체 노트를 훑지 않아도 되게 한다.)

■ 세기 인덱스는 '세기' 필드와 '발전단계[].세기' 의 합집합으로 만든다.
  개념 문서 하나가 여러 세기에 걸치는 것이 수학사의 기본이고
  (미분법 = 17세기 태동 + 19세기 엄밀화), 발전단계가 그 사실의 원본이다.
  세기 필드만 믿으면 연표에서 문서가 누락된다.

사용: python3 tools/build_math_manifest.py
"""
import sys
import re
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M          # noqa: E402

OUT = M.MATH / "manifest.json"

# manifest 에 실을 frontmatter 필드 (본문은 싣지 않는다)
CARD_FIELDS = [
    "유형", "제목", "슬러그", "별칭", "볼트파일명", "트랙", "짝문서",
    "세기", "분야", "교과", "난이도", "요약", "태그",
    "발전단계", "선행개념", "후속개념", "기여인물",
    "생몰", "기여개념", "관련일화",
    "사실성", "사실성근거", "관련인물", "관련개념",
    "연대", "시대이슈", "세계사사건",
    "이미지", "출처",
]

# 다른 노트를 가리키는 참조 필드 (역링크 계산에 쓴다)
REF_FIELDS = ["선행개념", "후속개념", "기여인물", "기여개념",
              "관련일화", "관련인물", "관련개념", "짝문서"]


def centuries_of(fm):
    out = set(fm.get("세기") or [])
    for st in (fm.get("발전단계") or []):
        if isinstance(st, dict) and isinstance(st.get("세기"), int):
            out.add(st["세기"])
    return sorted(out)


def main():
    notes, errors = [], []
    alias2slug = {}

    # ── 1차: 노트 적재 + 별칭 표 ──
    for slug, path in M.iter_notes():
        try:
            fm, body = M.read_note(path, strict=True)
        except ValueError as e:
            errors.append("%s: %s" % (slug, e))
            continue

        card = {k: fm[k] for k in CARD_FIELDS if fm.get(k) is not None}
        card["슬러그"] = slug
        card["path"] = "notes/%s/note.md" % slug
        card["세기전체"] = centuries_of(fm)
        card["자수"] = M.count_chars(body)
        card["시각화"] = M.count_visuals(body)
        notes.append(card)

        for a in M.aliases_for_math(fm):
            alias2slug.setdefault(a, slug)

    if errors:
        for e in errors:
            print("✗ %s" % e)
        print("\nfrontmatter 오류가 있어 manifest를 만들지 않았다.")
        return 1

    by_slug = {n["슬러그"]: n for n in notes}

    # ── 2차: 역링크 ──
    backlinks = defaultdict(list)
    seen = set()

    def link(src, dst, how):
        if dst not in by_slug or dst == src:
            return
        key = (dst, src)
        if key in seen:
            return
        seen.add(key)
        s = by_slug[src]
        backlinks[dst].append({
            "슬러그": src, "제목": s["제목"], "유형": s["유형"], "경로": how,
        })

    for slug, path in M.iter_notes():
        if slug not in by_slug:
            continue
        fm, body = M.read_note(path, strict=True)
        # frontmatter 참조 필드
        for f in REF_FIELDS:
            v = fm.get(f)
            for target in ([v] if isinstance(v, str) else (v or [])):
                if isinstance(target, str):
                    link(slug, alias2slug.get(M.norm(target), target), f)
        # 본문 위키링크
        for target, _label in M.extract_wikilinks(body):
            t = alias2slug.get(M.norm(target))
            if t:
                link(slug, t, "본문")

    # ── 3차: 분류 인덱스 ──
    idx = {k: defaultdict(list) for k in ("세기", "분야", "교과", "유형", "태그")}
    for n in notes:
        for c in n["세기전체"]:
            idx["세기"][str(c)].append(n["슬러그"])
        for f in (n.get("분야") or []):
            idx["분야"][f].append(n["슬러그"])
        for f in (n.get("교과") or []):
            idx["교과"][f].append(n["슬러그"])
        for f in (n.get("태그") or []):
            idx["태그"][f].append(n["슬러그"])
        idx["유형"][n["유형"]].append(n["슬러그"])

    # 인물별: 그 인물을 참조하는 노트 (기여인물·관련인물·발전단계.인물)
    by_person = defaultdict(list)
    for n in notes:
        names = list(n.get("기여인물") or []) + list(n.get("관련인물") or [])
        names += [st.get("인물") for st in (n.get("발전단계") or [])
                  if isinstance(st, dict) and st.get("인물")]
        for nm in {M.norm(x) for x in names if isinstance(x, str)}:
            p = alias2slug.get(nm, nm)
            if n["슬러그"] not in by_person[p]:
                by_person[p].append(n["슬러그"])

    notes.sort(key=lambda n: (min(n["세기전체"] or [9999]),
                              {"세기": 0, "개념": 1, "인물": 2, "일화": 3}.get(n["유형"], 9),
                              n["슬러그"]))

    gen = ""
    try:
        import subprocess
        gen = subprocess.run(["git", "log", "-1", "--format=%cs"], cwd=str(M.ROOT),
                             capture_output=True, text=True).stdout.strip()
    except Exception:
        pass

    M.dump_json(OUT, {
        "generated": gen,
        "notes": notes,
        "index": {
            "세기": {k: v for k, v in sorted(idx["세기"].items(), key=lambda x: int(x[0]))},
            "분야": dict(idx["분야"]),
            "교과": dict(idx["교과"]),
            "유형": dict(idx["유형"]),
            "태그": dict(idx["태그"]),
            "인물": dict(by_person),
            "역링크": {k: v for k, v in backlinks.items()},
        },
        "별칭": alias2slug,
    })

    cents = ", ".join("%s세기 %d편" % (k, len(v))
                      for k, v in sorted(idx["세기"].items(), key=lambda x: int(x[0])))
    print("math/manifest.json: %d편  [%s]" % (len(notes), cents or "없음"))
    print("역링크 %d건 · 별칭 %d개" % (sum(len(v) for v in backlinks.values()), len(alias2slug)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
