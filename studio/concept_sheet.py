# -*- coding: utf-8 -*-
"""개념 한 장 - 만들기·검사·목록.

카드뉴스가 `cardnews.py` 를 갖듯, 학습자료(개념노트)의 그림 한 장도 같은 자리를 갖는다.
카피는 `concepts/<슬러그>.py` 한 파일에 `SPEC` 하나로 두고, 렌더·검사는 여기가 맡는다.

    python concept_sheet.py list                 지금 있는 스펙
    python concept_sheet.py build <슬러그>        한 장 렌더 + 균형 검사
    python concept_sheet.py build --all          전부
    python concept_sheet.py check <슬러그>        렌더하지 않고 스키마만 본다

산출물은 `out/개념한장_<파일키>.png`. 학습자료 폴더로 옮기면
`tools/ingest_concept.py` 가 제목과 짝지어 서가로 반입한다.

**기준 환경은 러너다**(`.github/workflows/concept-sheet-render.yml`). 여기서 그려도
되지만 폰트가 달라 글자 굵기가 다르게 나온다 — 서가에 올릴 그림은 러너가 그린 것을 쓴다.
처음 두 장(심슨·최적정지)은 스펙이 없어 다시 그릴 수 없으므로 테스트분으로 남는다.

왜 스펙을 따로 두나 - 처음 두 장(심슨·최적정지)은 스펙이 대화 안에만 있었고
파일로 남지 않았다. 그래서 같은 양식으로 한 장 더 만들려면 레이아웃을 처음부터
다시 설명해야 했다. 스펙이 파일이면 다음 편은 복사해서 고치면 된다.
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SPECS = HERE / "concepts"
OUT = HERE / "out"

sys.path.insert(0, str(HERE / "engine"))
import build_concept_sheet as sheet  # noqa: E402

# 스펙이 반드시 갖춰야 하는 것. 빠지면 렌더 도중이 아니라 여기서 멈춘다.
REQUIRED = ["title", "en", "tag", "hook", "hooksub", "data", "steps",
            "points", "flow", "take", "foot", "file_key"]


def load(slug):
    p = SPECS / (slug + ".py")
    if not p.exists():
        raise SystemExit("스펙이 없다: %s" % p)
    spec = importlib.util.spec_from_file_location("spec_" + slug, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "SPEC"):
        raise SystemExit("%s 에 SPEC 이 없다" % p.name)
    return mod.SPEC


def check(s, slug):
    """렌더 전에 걸러 낼 수 있는 것은 여기서 다 거른다."""
    bad = [k for k in REQUIRED if k not in s]
    if bad:
        raise SystemExit("[%s] 빠진 항목: %s" % (slug, ", ".join(bad)))
    if len(s["steps"]) != 4:
        raise SystemExit("[%s] 단계 카드는 4개여야 한다 (지금 %d개)" % (slug, len(s["steps"])))
    if len(s["points"]) != 3:
        raise SystemExit("[%s] 세 줄 정리는 3칸이어야 한다 (지금 %d개)" % (slug, len(s["points"])))
    if len(s["flow"]) != 4:
        raise SystemExit("[%s] 흐름 칩은 4개여야 한다 (지금 %d개)" % (slug, len(s["flow"])))
    for i, st in enumerate(s["steps"], 1):
        for k in ("t", "d", "kv"):
            if not st.get(k):
                raise SystemExit("[%s] %d번 카드에 '%s' 가 비었다" % (slug, i, k))
    head = s["data"]["head"]
    for r in s["data"]["rows"]:
        if len(r) != len(head):
            raise SystemExit("[%s] 표의 칸 수가 머리글과 다르다: %s" % (slug, r))
    print("[%s] 스키마 통과 - 단계 4 · 정리 3 · 흐름 4 · 표 %d행"
          % (slug, len(s["data"]["rows"])))
    return True


def build(slug):
    s = load(slug)
    check(s, slug)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / ("개념한장_%s.png" % s["file_key"])
    sheet.build(s, out)
    print("[%s] 그림 -> %s" % (slug, out))
    return out


def main():
    ap = argparse.ArgumentParser(description="개념 한 장 만들기")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    b = sub.add_parser("build"); b.add_argument("slug", nargs="?"); b.add_argument("--all", action="store_true")
    c = sub.add_parser("check"); c.add_argument("slug", nargs="?"); c.add_argument("--all", action="store_true")
    a = ap.parse_args()

    slugs = sorted(p.stem for p in SPECS.glob("*.py") if not p.stem.startswith("_"))

    if a.cmd == "list":
        if not slugs:
            print("스펙이 없다. concepts/ 에 <슬러그>.py 를 만들고 SPEC 을 둘 것.")
            return 0
        for s in slugs:
            spec = load(s)
            print("  %-20s %s" % (s, spec.get("title", "")))
        return 0

    targets = slugs if a.all else ([a.slug] if a.slug else [])
    if not targets:
        raise SystemExit("슬러그를 주거나 --all 을 쓸 것. 목록은 `list`.")

    for s in targets:
        (build if a.cmd == "build" else lambda x: check(load(x), x))(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
