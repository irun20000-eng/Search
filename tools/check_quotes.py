#!/usr/bin/env python3
"""check_quotes.py — 영상 노트의 「핵심 인용」이 실제 자막에 있는지 대조한다.

    python3 tools/check_quotes.py videos/notes/<id>.md /tmp/brief/<id>.md

brief 는 yt-inbox 브랜치의 `briefs/<video_id>.md` (schema: yt-brief/v1) 다.
2026-10-15 스파크 → Aside brief 전환과 함께 도입. 스파크 시절에는 원본 자막이 없어
보증 범위가 「노트 = 스파크 원본」까지였다. brief 는 자막 전문을 싣고 오므로
「인용 = 실제 발화(자막)」까지 기계로 확인할 수 있다.

판정 — 인용문과 자막을 각각 한글·영숫자만 남겨 정규화한 뒤, 인용문의 글자 3-gram 이
자막에 얼마나 들어 있는지(포함률)를 잰다. 띄어쓰기·문장부호 정리는 점수에 영향이 없다.

  포함률 ≥ 0.90  PASS   자막 그대로(띄어쓰기·부호만 정리)
  0.75 ~ 0.90   WARN   일부 손질 — 눈으로 확인
  < 0.75        FAIL   자막에 없는 문장(의역·창작) — 자막에서 다시 옮겨 적을 것

FAIL 이 하나라도 있으면 종료코드 1. 함께 가장 가까운 자막 위치(타임스탬프)를 보여 준다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

QUOTE_RE = re.compile(r"^\s*-\s*\*\*핵심 인용\*\*\s*:\s*(.+?)\s*$")
TS_RE = re.compile(r"^\[(\d{1,2}(?::\d{2}){1,2})\]\s*(.*)$")
KEEP = re.compile(r"[^0-9A-Za-z\uac00-\ud7a3]")


def norm(s: str) -> str:
    return KEEP.sub("", s).lower()


def grams(s: str, n: int = 3) -> list[str]:
    return [s[i:i + n] for i in range(max(0, len(s) - n + 1))]


def load_transcript(brief: Path) -> list[tuple[str, str]]:
    text = brief.read_text(encoding="utf-8")
    if "schema: yt-brief/v1" not in text:
        sys.exit(f"brief 형식이 아니다(schema: yt-brief/v1 없음): {brief}")
    part = text.split("\n## 자막", 1)
    if len(part) < 2:
        sys.exit("brief 에 '## 자막' 절이 없다")
    rows = []
    for line in part[1].splitlines():
        m = TS_RE.match(line.strip())
        if m:
            rows.append((m.group(1), m.group(2)))
    if not rows:
        sys.exit("brief 자막이 비어 있다")
    return rows


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    note, brief = Path(sys.argv[1]), Path(sys.argv[2])
    rows = load_transcript(brief)
    # 자막 전체 정규화 문자열 + 각 글자가 어느 줄에서 왔는지
    full, owner = [], []
    for i, (_, t) in enumerate(rows):
        n = norm(t)
        full.append(n)
        owner.extend([i] * len(n))
    tx = "".join(full)
    tx_grams = set(grams(tx))

    quotes = []
    for line in note.read_text(encoding="utf-8").splitlines():
        m = QUOTE_RE.match(line)
        if m:
            quotes.append(m.group(1).strip().strip('"“”'))
    if not quotes:
        print("핵심 인용을 찾지 못했다")
        return 1

    fails = 0
    print(f"자막 {len(rows)}줄 · 인용 {len(quotes)}개")
    for k, qt in enumerate(quotes, 1):
        g = grams(norm(qt))
        if not g:
            print(f"  [{k}] SKIP (빈 인용)")
            continue
        score = sum(1 for x in g if x in tx_grams) / len(g)
        verdict = "PASS" if score >= 0.90 else ("WARN" if score >= 0.75 else "FAIL")
        fails += verdict == "FAIL"
        # 가장 가까운 위치: 인용 첫 6글자 → 없으면 가장 많이 겹치는 3-gram 위치
        head = norm(qt)[:6]
        pos = tx.find(head) if head else -1
        if pos < 0:
            for x in g:
                pos = tx.find(x)
                if pos >= 0:
                    break
        where = rows[owner[pos]][0] if 0 <= pos < len(owner) else "?"
        print(f"  [{k}] {verdict} {score:.2f} @{where}  {qt[:60]}{'…' if len(qt) > 60 else ''}")
    print("결과:", "FAIL" if fails else "OK", f"(FAIL {fails}건)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
