#!/usr/bin/env python3
"""마크다운 표가 **실제로 그려지는지** 재는 공용 모듈.

■ 왜 이 파일이 따로 있나 (2026-09-03)

  자수·절수·**시각화** 게이트는 표를 *세기만* 하고 표가 **그려지는지는 보지 않는다.**
  셀 안의 `|` 는 셀 구분자로 읽히므로 한 칸이 행 전체를 쪼개는데, 그래도 게이트는
  전부 통과한다. 실측(2026-09-03)에서 저장소 4건이 나왔고 그중 둘은 **이미 발행돼
  있었다**(`reports/derivative-rate-of-change-advanced` 의 `|∇f|`).

  절댓값·노름·논리합·집합조건제시법처럼 **수학 글이 자주 쓰는 기호가 전부 `|`** 라
  재발하기 쉽다. 그래서 규칙을 문서가 아니라 여기에 둔다.

■ 규칙이 하나가 아니다 — 서가마다 렌더러가 다르다

  실측으로 확인한 것이지 추정이 아니다.

  · "gfm"   — `research/` · `concept/` · `math/` 는 marked@12.0.2 를 쓴다.
              셀 안의 `|` 는 **`\\|` 로 이스케이프하면** 살릴 수 있다.
              ⚠ 코드 스팬(`` `…` ``) 안에 넣어도 **보호되지 않는다.**

  · "plain" — `videos/` · `guides/` 는 손으로 쓴 파서를 쓴다:
                  s.trim().replace(/^\\|/,'').replace(/\\|$/,'').split('|')
              **이스케이프 처리가 아예 없다.** `\\|` 를 써도 셀이 쪼개지고
              백슬래시만 화면에 남는다 → **셀 안에 `|` 를 쓸 방법이 없다.**
              낱말로 풀어 적어야 한다("이중 세로선", "절댓값 기호").

  `blog/` 는 본문을 마크다운으로 그리지 않고(원문을 그대로 넣는다) 표도 0건이라
  대상이 아니다. `cardnews/` 도 본문 렌더가 없다.
"""
import re

RULES = ("gfm", "plain")


def split_cells(line, rule="gfm"):
    """한 행을 렌더러와 같은 방식으로 셀로 가른다."""
    s = line.strip()
    s = re.sub(r"^\|", "", s)
    s = re.sub(r"\|$", "", s)
    if rule == "gfm":
        return re.split(r"(?<!\\)\|", s)
    return s.split("|")           # plain: 이스케이프가 없다


def is_separator(line, rule="gfm"):
    cs = split_cells(line, rule)
    return bool(cs) and all(re.fullmatch(r":?\s*-{2,}\s*:?", c.strip()) for c in cs)


def defects(text, rule="gfm"):
    """(줄번호, 머리행 칸수, 이 행 칸수, 행 원문) 목록. 코드펜스 안은 건너뛴다."""
    out, in_fence, i = [], False, 0
    lines = text.split("\n")
    while i < len(lines):
        if lines[i].strip().startswith("```"):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            i += 1
            continue
        head = lines[i].strip()
        if head.startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1], rule):
            ncol, j = len(split_cells(head, rule)), i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                n = len(split_cells(lines[j], rule))
                if n != ncol:
                    out.append((j + 1, ncol, n, lines[j].strip()))
                j += 1
            i = j
        else:
            i += 1
    return out


def advice(rule):
    if rule == "gfm":
        return "셀 안의 `|` 는 코드 스팬 안에서도 구분자로 읽힌다. `\\|` 로 이스케이프할 것"
    return ("이 서가의 파서는 이스케이프를 모른다 — `\\|` 도 통하지 않는다. "
            "셀 안에서 `|` 를 아예 빼고 낱말로 적을 것")
