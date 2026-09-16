#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROADMAP §11 의 「다음에 쓸 것」 판단이 서가보다 낡았는가.

왜 이 검사기가 있나
-------------------
`math/ROADMAP.md` §11 은 **다음 세션이 무엇을 할지 읽는 자리**다. 그런데 거기 후보로
이름을 올려 둔 노트를 쓰고 나서 그 줄을 「완료」로 고치는 것을 **반복해서 빠뜨렸다**.

  - 2026-08-31 「지금 상태」가 자동 측정 블록 **바로 위에서** 낡아 있었다(#144·#173).
  - 2026-09-05 「다음에 할 것」의 낡은 판단을 통째로 정정했다(과제 #47).
  - 2026-09-16 다시 재어 보니 **후보 표의 일곱 줄**이 이미 쓴 노트를 아직
    「권고(집필)」·「판단 필요」·「보류」·「차선」으로 달고 있었다.

숫자는 `build_math_status.py` 가 자동으로 맞춰 주지만 **판단 문장은 사람이 적는다** —
그래서 노후가 숫자에 가려지지 않고 그대로 남는다. 세 번 같은 일이 났으면 문서가 아니라
게이트에 적을 자리다(`.github/workflows/gates.yml` 머리말과 같은 이유).

무엇을 재나
-----------
§11 안의 표에서 **첫 칸에 슬러그가 적힌 줄**만 본다(둘째 칸 이후에 나오는 슬러그는
근거·겹침 대상으로 언급된 것이라 후보가 아니다).

  1. **쓴 것을 아직 후보로 두었나** — 슬러그에 해당하는 노트가 `math/notes/` 에 있는데
     그 줄이 완료 표시가 아니면 지적한다.

완료 표시는 이 파일의 기존 관례를 그대로 따른다 — 첫 칸에 취소선(`~~`)을 긋거나
마지막 칸에 「완료」를 적은 줄.

무엇을 못 재나 (중요)
---------------------
  - **`<details>` 안과 취소선 그은 제목 아래 구간은 건너뛴다.** 「이행한 옛 권고 (기록)」처럼 **일부러 남겨 둔 archive** 라
    거기 적힌 「권고」는 낡은 것이 아니라 그때의 기록이다. 이것을 안 건너뛰면 지적 셋이 거짓으로
    뜨고, **정상인데 FAIL 이 뜨면 다음 사람이 게이트를 무시한다**(LESSONS 2026-09-09).
    ⚠ 아카이브는 `<details>` 로만 표시되지 않는다 — `#### ~~다음 대상 …~~ → **썼다**` 처럼
    **제목에 취소선을 그어** 그 아래를 통째로 기록으로 두는 관례가 있다. 처음 판에서 이것을
    놓쳐 **아카이브 두 줄을 「완료」로 고쳐 버렸다**(= 게이트를 통과시키려고 역사를 고친 것).
    되돌리고 취소선 제목 구간도 건너뛰게 했다.
  - **펜스 코드블록 안은 건너뛴다.** §11 에 예시 코드가 있고 그 안의 표 비슷한 줄이 걸렸다.
  - **반대 방향(없는 노트가 완료)은 안 본다.** 후보는 **쓰지 않기로 하고도** 닫힌다 —
    `concept-real-analysis` 가 「새 문서로 쓸 일이 아니다」로 해소된 것이 그 예다.
    그것까지 지적하면 「안 쓰기로 함」을 표현할 방법이 없어진다.
  - **판단이 옳은가는 안 본다.** 「아직 이르다」가 타당한지, 근거로 적은 수가 맞는지는
    사람이 볼 일이다. 이 검사기는 **「이미 썼는데 아직 쓸 것으로 적혀 있다」** 하나만 잡는다.
  - **첫 칸에 백틱 슬러그가 없는 후보 줄은 못 본다.** §11 은 후보를 슬러그로도 적고
    한글 이름으로도 적는다(「카발리에리 (17세기)」). 그런 줄은 세지 못하므로 **몇 줄을
    못 봤는지 함께 찍는다** — 안 찍으면 「후보 줄 N개」가 전수로 읽힌다.
  - **표 밖의 산문은 안 본다.** 「`century-3c` 는 아직 이르다」가 문단에 있으면 못 잡는다.
    표로 적는 것이 이 파일의 관례라 표만 본다 — 산문까지 넓히면 인용·회고까지 걸린다.
  - **자동 측정 블록은 건너뛴다.** 빌더 산출물이라 사람이 고칠 자리가 아니다.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP = os.path.join(ROOT, "math", "ROADMAP.md")
NOTES = os.path.join(ROOT, "math", "notes")

AUTO_BEGIN = "<!-- 자동측정:시작 -->"
AUTO_END = "<!-- 자동측정:끝 -->"
SLUG = re.compile(r"`((?:person|century|concept|episode)-[a-z0-9-]+)`")


FENCE = re.compile(r"^```.*?^```", re.S | re.M)
STRUCK_HEAD = re.compile(r"^(#{2,6}) *~~.*?~~.*$", re.M)


def drop_details(sec):
    """<details> 를 **깊이를 세며** 지운다 — 중첩·`<details open>` 을 비탐욕 정규식은 못 판다."""
    out, depth, i = [], 0, 0
    tok = re.compile(r"<details\b[^>]*>|</details>", re.I)
    for m in tok.finditer(sec):
        if m.group(0).lower().startswith("</"):
            depth = max(0, depth - 1)
            if depth == 0:
                i = m.end()
        else:
            if depth == 0:
                out.append(sec[i:m.start()])
            depth += 1
    out.append(sec[i:])
    return "".join(out)


def drop_struck_sections(sec):
    """취소선 그은 제목(`#### ~~…~~`) 아래를, 같은 깊이 이상의 다음 제목까지 지운다."""
    lines = sec.split("\n")
    out, skip_at = [], None
    for line in lines:
        m = re.match(r"^(#{2,6}) ", line)
        if m:
            lvl = len(m.group(1))
            if skip_at is not None and lvl <= skip_at:
                skip_at = None
            if skip_at is None and STRUCK_HEAD.match(line):
                skip_at = lvl
                continue
        if skip_at is None:
            out.append(line)
    return "\n".join(out)


def section_11(text):
    """§11 본문만 잘라 내고, 자동 측정 블록과 <details> 아카이브는 비운다."""
    i = text.find("## 11.")
    if i < 0:
        return None
    sec = text[i:]
    while AUTO_BEGIN in sec and AUTO_END in sec:
        head, rest = sec.split(AUTO_BEGIN, 1)
        _auto, tail = rest.split(AUTO_END, 1)
        sec = head + tail
    sec = FENCE.sub("", sec)
    sec = drop_details(sec)
    return drop_struck_sections(sec)


def rows(sec):
    for n, line in enumerate(sec.split("\n"), 1):
        s = line.strip()
        if not s.startswith("|") or s.count("|") < 3:
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if set(cells[0]) <= set("-: "):      # 표 구분선
            continue
        yield n, cells


def main():
    if not os.path.exists(ROADMAP):
        print("ROADMAP 이 없다: %s" % ROADMAP)
        return 2
    text = open(ROADMAP, encoding="utf-8").read()
    sec = section_11(text)
    if sec is None:
        print("§11 을 찾지 못했다 — 제목이 바뀌었는가")
        return 2

    seen, unseen, stale = 0, 0, []
    for n, cells in rows(sec):
        slugs = SLUG.findall(cells[0])
        if not slugs:
            if len(cells) >= 3 and cells[-1].strip() in ("권고", "보류", "차선", "채우기", "판단 필요", "끼워넣기"):
                unseen += 1
            continue
        seen += 1
        last = cells[-1].strip()
        done = ("~~" in cells[0]) or (last.endswith("완료") and "미완료" not in last)
        for slug in slugs:
            exists = os.path.exists(os.path.join(NOTES, slug, "note.md"))
            if exists and not done:
                stale.append((slug, cells[-1]))

    print("§11 후보 줄 %d개를 쟀다 (아카이브·코드블록·자동측정 블록 제외)" % seen)
    if unseen:
        print("⚠ 첫 칸에 슬러그가 없어 **못 본** 후보 줄 %d개 — 한글 이름으로만 적힌 줄은 이 게이트 밖이다." % unseen)
    if stale:
        print("\n! 이미 쓴 노트가 아직 「쓸 것」으로 적혀 있다 — %d건" % len(stale))
        for slug, w in stale:
            print("   %-26s 무게=%s   → 그 줄을 완료로 바꿀 것" % (slug, w))
        print("\n지적 %d건. ⚠ 판단이 옳은가는 이 검사기가 보지 않는다 — 머리말 참조." % len(stale))
        return 1
    print("\nOK — §11 의 후보 줄이 서가와 어긋나지 않는다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
