#!/usr/bin/env python3
"""
개념노트(이해편) 품질 게이트 — 측정이지 판단이 아니다.

카드뉴스 한 편의 짝으로 쓰는 학습자료다. reports/ 의 이해편과 절차는 같고
(수집 → fact-ledger → 합성 → 측정 게이트 → 별도 검수, PIPELINE.md) **눈금만 다르다** —
카드 10장의 범위를 설명하므로 주제 하나를 통째로 다루는 리서치 이해편보다 짧다.

■ 하한의 근거
기존 5편(simpsons-paradox · optimal-stopping · size-bias · square-cube-law ·
survivorship-bias)을 실측한 **관측 최저값**이다. verify_video.py 가 73편 코퍼스로
한 방식과 같다. 따라서 **이미 합격한 노트가 이 게이트에 걸리면 그것은 게이트 산정
오류**이지 노트의 결함이 아니다. LESSONS.md "근거 없는 숫자를 쓰지 말 것".

    항목        실측 최저 / 중앙 / 최고      하한
    글자(공백제외)  5,428 / 5,804 / 6,362     5,400
    줄            166 /   210 /   220        165
    섹션(##)       13 /    14 /    16         12
    시각화(표행+코드) 14 /    21 /    35         12
    출처 국내         2 /     3 /     4          2
    출처 해외         3 /     6 /     7          3

■ 이 게이트가 잡는 진짜 사고
  · 본문에 [n] 을 달아 놓고 출처 목록에 그 번호가 없는 것 (무환각의 핵심)
  · 검증 메모 누락 — 어떤 수치가 '설명용으로 지어낸 것'인지 밝히지 않은 글
  · 부모 노트로 학습자료를 만든 것 (studio/CLAUDE.md 금지 규칙)
  · 짝 카드뉴스가 실재하지 않는 것

사용:
    python tools/verify_concept.py                     # concept/notes/*.md 전부
    python tools/verify_concept.py concept/notes/x.md  # 지정
    python tools/verify_concept.py --vault <폴더>       # 볼트 원고(프론트매터 포함)도 본다
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdtables as MT          # noqa: E402  표 렌더 검사(서가 공용)

ROOT = Path(__file__).resolve().parent.parent

# ── 게이트 (기존 5편 실측 최저값) ──────────────────────────────
G = {
    "chars_min": 5400,     # 실측 min 5,428 (공백 제외)
    "lines_min":  165,     # 실측 min 166
    "secs_min":    12,     # 실측 min 13
    "visual_min":  12,     # 실측 min 14 (표 행 + 코드블록)
    "src_dom_min":  2,     # 실측 min 2
    "src_fgn_min":  3,     # 실측 min 3
}

MUST_HAVE = ["TL;DR", "핵심 포인트", "다음 읽을 것", "출처", "검증 메모"]

# 부모 노트는 학습자료를 만들지 않는다 — 경험 기반 조언 · 심리 연구 재현성 문제
# (studio/CLAUDE.md "하지 말 것"). 짝 카드뉴스의 시리즈로 판정한다.
FORBIDDEN_SERIES = {"parent"}


def parse(path: Path):
    txt = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    if not m:
        return {}, txt          # concept/notes/*.md 는 프론트매터가 벗겨져 있다
    fm, body = m.groups()
    meta = {}
    for line in fm.split("\n"):
        if ": " in line:
            k, v = line.split(": ", 1)
            meta[k.strip()] = v.strip()
    return meta, body


def sources(body: str):
    """출처 목록을 국내/해외로 나눠 세고, 번호 체계를 함께 돌려준다.

    두 형식이 실제로 공존한다(2026-08-22 발견):
      A  연속 번호 + 접두어    `1. (국내) …`  `5. (해외) …`   ← 4편
      B  구획마다 번호 재시작   **국내** 1.2. / **해외** 1.2.  ← 1편
    B 형식은 본문의 [n] 이 어느 목록의 n 인지 기계가 가릴 수 없다. 그래서
    **A 를 정본으로 두고 B 는 경고**한다(기존 글을 탈락시키지는 않는다).
    """
    tail = body.split("## 출처", 1)[-1]
    dom_pre = re.findall(r"(?m)^(\d+)\. \(국내\)", tail)
    fgn_pre = re.findall(r"(?m)^(\d+)\. \(해외\)", tail)
    if dom_pre or fgn_pre:
        nums = {int(n) for n in dom_pre + fgn_pre}
        return len(dom_pre), len(fgn_pre), nums, "A"

    # B 형식 — **국내** / **해외** 구획을 잘라 각각 센다
    def block(label):
        m = re.search(r"\*\*%s\*\*(.*?)(?=\*\*(?:국내|해외)\*\*|^>|\Z)" % label,
                      tail, re.S | re.M)
        return re.findall(r"(?m)^(\d+)\.", m.group(1)) if m else []

    d, f = block("국내"), block("해외")
    # 번호가 겹치므로 [n] 대조는 못 한다 — 빈 집합을 주고 형식을 B 로 알린다
    return len(d), len(f), set(), "B"


def check(path: Path, cardnews_series=None):
    meta, body = parse(path)
    slug = path.stem
    errs, warns, stat = [], [], {}

    stat["글자"] = len(re.sub(r"\s", "", body))
    stat["줄"] = body.count("\n") + 1
    stat["섹션"] = len(re.findall(r"(?m)^## ", body))
    stat["시각화"] = len(re.findall(r"(?m)^\|", body)) + len(re.findall(r"(?m)^```", body)) // 2
    # 표가 실제로 그려지는가. concept/index.html 은 marked 라 "gfm" 규칙이다
    # (셀 안의 `|` 는 `\\|` 로 이스케이프하면 살릴 수 있다). 자세한 것은 mdtables.py
    for _ln, want, got, row in MT.defects(body, "gfm"):
        errs.append("표 행이 머리행과 칸 수가 다름 (%d칸이어야 하는데 %d칸): %s — %s"
                    % (want, got, row[:60], MT.advice("gfm")))

    dom, fgn, src_nums, fmt = sources(body)
    stat["국내"], stat["해외"] = dom, fgn

    for key, label, gate in (("글자", "글자수", "chars_min"), ("줄", "줄수", "lines_min"),
                             ("섹션", "섹션수", "secs_min"), ("시각화", "시각화", "visual_min"),
                             ("국내", "국내 출처", "src_dom_min"), ("해외", "해외 출처", "src_fgn_min")):
        if stat[key] < G[gate]:
            errs.append("%s %d < %d" % (label, stat[key], G[gate]))

    for h in MUST_HAVE:
        if h not in body:
            errs.append("'%s' 절 없음" % h)

    # 무환각 핵심 — 본문에 단 [n] 이 출처 목록에 실제로 있는가
    if fmt == "A":
        cited = {int(n) for n in re.findall(r"\[(\d+)(?:\(국내\))?\]", body)}
        dangling = sorted(cited - src_nums)
        if dangling:
            errs.append("출처 없는 인용 번호 %s" % dangling)
        unused = sorted(src_nums - cited)
        if unused:
            warns.append("본문에서 안 쓴 출처 %s" % unused)
    else:
        warns.append("출처 번호가 국내/해외마다 재시작한다(B형식) — "
                     "[n] 대조를 못 한다. '1. (국내) …' 연속 번호로 고칠 것")

    # 짝 카드뉴스가 실재하는가 · 부모 노트는 아닌가
    if cardnews_series is not None:
        pair = meta.get("카드뉴스", "")
        if not pair and "🔗 짝 카드뉴스" not in body and "짝 카드뉴스" not in body:
            warns.append("짝 카드뉴스 표기 없음")
        for folder, series in cardnews_series.items():
            if series in FORBIDDEN_SERIES and slug in folder:
                errs.append("부모 노트는 학습자료를 만들지 않는다 (studio/CLAUDE.md)")

    return errs, warns, stat


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    vault = None
    if "--vault" in sys.argv:
        i = sys.argv.index("--vault")
        vault = Path(sys.argv[i + 1]) if i + 1 < len(sys.argv) else None

    if vault:
        paths = sorted(p for p in vault.glob("*.md") if not p.name.startswith("_"))
    elif args:
        paths = [Path(a) for a in args]
    else:
        paths = sorted((ROOT / "concept" / "notes").glob("*.md"))

    if not paths:
        print("볼 파일이 없다.")
        return 0

    # 짝 카드뉴스 판정용
    series = {}
    man = ROOT / "cardnews" / "manifest.json"
    if man.exists():
        d = json.loads(man.read_text(encoding="utf-8"))
        series = {e["folder"]: e.get("series", "") for e in d.get("episodes", [])}

    print("개념노트 게이트 — 하한은 기존 5편 실측 최저값 (PIPELINE.md 방식)")
    print("%-22s %6s %5s %4s %5s %4s %4s  %s"
          % ("노트", "글자", "줄", "절", "시각화", "국내", "해외", "판정"))

    failed = 0
    all_warns = []
    for p in paths:
        errs, warns, s = check(p, series)
        mark = "OK" if not errs else "X"
        if errs:
            failed += 1
        print("%-22s %6d %5d %4d %5d %4d %4d  %s"
              % (p.stem[:22], s["글자"], s["줄"], s["섹션"], s["시각화"],
                 s["국내"], s["해외"], mark))
        for e in errs:
            print("      X %s" % e)
        for w in warns:
            all_warns.append((p.stem, w))

    if all_warns:
        print()
        print("경고 — 막지는 않지만 고쳐야 할 것:")
        for slug, w in all_warns:
            print("  ! %-22s %s" % (slug[:22], w))

    print()
    if failed:
        print("[X] %d/%d편 미달 — 본문을 보강한 뒤 다시 잴 것. 머지 금지." % (failed, len(paths)))
        return 1
    print("[OK] %d편 전부 통과." % len(paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
