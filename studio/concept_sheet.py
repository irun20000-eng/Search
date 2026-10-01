# -*- coding: utf-8 -*-
"""개념 한 장 - 만들기·검사·목록.

카드뉴스가 `cardnews.py` 를 갖듯, 학습자료(개념노트)의 그림 한 장도 같은 자리를 갖는다.
카피는 `concepts/<슬러그>.py` 한 파일에 `SPEC` 하나로 두고, 렌더·검사는 여기가 맡는다.

    python concept_sheet.py list                 지금 있는 스펙
    python concept_sheet.py build <슬러그>        한 장 렌더 + 균형 검사
    python concept_sheet.py build --all          전부
    python concept_sheet.py check <슬러그>        렌더하지 않고 스키마만 본다

산출물은 `out/개념한장_<파일키>.png`. 서가 반영은 러너의 `concept-sheet-render.yml` 이
`concept/assets/<슬러그>.png` 로 옮겨 넣는다(반입 단계는 2026-08-22 에 없어졌다).

    python concept_sheet.py check <슬러그>  은 렌더 없이 돈다 — **루틴은 push 전에 이것을 돌린다.**
    분량 경고가 뜨면 줄이고 다시 잰다. 러너 왕복 한 번을 아낀다(아래 COPY_MAX).

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

# 렌더 결과와 실패 메시지가 로그에서 어긋나지 않게 한다. stdout 은 기본이 블록 버퍼라
# 끝에 한꺼번에 나오고 실패 메시지(stderr)만 제때 나와서, 2026-10-01 에 brooks-law 의
# 넘침이 로그상 base-rate-fallacy 자리에 찍혔다.
try:
    sys.stdout.reconfigure(line_buffering=True)
except AttributeError:          # 파이프가 아닌 특수 스트림
    pass

# 한 줄 정리(take) 블록과 바닥 출처 줄의 글자수(태그 제외) 관측 최대.
# 2026-10-01 에 러너에서 넘침 없이 렌더된 12종을 실측한 값이다 — verify_concept.py 가
# 하한을 정하는 방식과 같다. **경고만 한다**: 진짜 제약은 픽셀이고 글자수는 근사다
# (big 은 <br> 위치에 따라, sub 은 줄바꿈 위치에 따라 같은 글자수도 높이가 다르다).
# 근거: 같은 날 brooks-law 첫 스펙이 sub 113 · ask 38 로 렌더되어 `card sumR +13` 넘침.
COPY_MAX = {
    ("take", "big"): 23,    # size-bias
    ("take", "sub"): 100,   # base-rate-fallacy
    ("take", "ask"): 31,    # parkinsons-law
    ("foot",): 264,         # benfords-law
}

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
    for msg in copy_warnings(s):
        print("[%s] 분량 경고 - %s" % (slug, msg))
    return True


def _plain(html):
    import re
    return re.sub(r"<[^>]+>", "", html or "")


def copy_warnings(s):
    """관측 최대를 넘은 칸을 돌려준다. 실패시키지 않는다(COPY_MAX 머리말)."""
    out = []
    for path, cap in COPY_MAX.items():
        v = s
        for k in path:
            v = v.get(k, "") if isinstance(v, dict) else ""
        n = len(_plain(v))
        if n > cap:
            out.append("%s %d자 > 관측 최대 %d자 — 넘칠 수 있다. 줄이고 다시 잴 것"
                       % (".".join(path), n, cap))
    return out


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

    # 한 장이 실패해도 나머지는 계속 그린다. 2026-10-01 에는 13종 중 4번째에서
    # SystemExit 가 터져 뒤의 9종이 돌지 않았고, 메시지에 슬러그가 없어 어느 장인지
    # 로그 순서로 짐작해야 했다. 엔진 변경 때 전부 다시 그리는 `--all` 범위는 그대로 둔다.
    failed = []
    for s in targets:
        try:
            (build if a.cmd == "build" else lambda x: check(load(x), x))(s)
        except SystemExit as e:
            msg = str(e.code) if e.code not in (None, 0, 1) else "실패"
            print("[%s] 실패 - %s" % (s, msg))
            failed.append(s)
    if failed:
        print()
        print("[X] %d/%d장 실패: %s" % (len(failed), len(targets), ", ".join(failed)))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
