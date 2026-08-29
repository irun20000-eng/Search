#!/usr/bin/env python3
"""
math/ROADMAP.md 의 현황 블록을 실측으로 다시 쓴다.

■ 왜 필요한가 (2026-08-29)

  ROADMAP 의 「갚아야 할 부채」 표가 2026-08-25 기준으로 적혀 있었는데
  나흘 만에 낡았다. "17~18세기 인물 = 다음 대상" 이라 적힌 자리의 두 인물은
  08-26 에 이미 썼고, "`concept-real-analysis` 예약 2회" 는 실측하면 4회였다.

  같은 사고를 허브에서도 겪었다 — 편수는 코드가 세서 늘 맞는데 그 옆의
  소개 문구만 조용히 낡았다(#144). **자동으로 맞는 숫자 옆에 손으로 적은
  문장을 두면 숫자가 문장의 노후를 가려 준다.**

  그래서 셀 수 있는 것은 전부 여기서 세고, ROADMAP 에는 마커 사이로 끼워 넣는다.
  판단(무엇을 먼저 쓸 것인가·왜)은 사람이 적는 자리로 남긴다 — 그건 측정이 아니다.

사용:
  python3 tools/build_math_status.py            # ROADMAP 갱신
  python3 tools/build_math_status.py --print    # 화면에만 출력
"""
import sys
import collections
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M          # noqa: E402
import verify_math as V      # noqa: E402

ROADMAP = M.ROOT / "math" / "ROADMAP.md"
BEGIN = "<!-- 자동측정:시작 -->"
END = "<!-- 자동측정:끝 -->"

# frontmatter 가 슬러그를 가리키는 필드. 여기 적혀 있는데 문서가 없으면 예약이다.
REF_FIELDS = ["선행개념", "후속개념", "기여개념", "기여인물", "관련일화", "관련개념"]


def measure():
    fms = {}
    for slug, path in M.iter_notes():
        try:
            fm, _ = M.read_note(path)
        except ValueError:
            continue
        fms[slug] = fm

    kinds = collections.Counter(fm.get("유형") for fm in fms.values())

    centuries = collections.Counter()
    for fm in fms.values():
        for c in (fm.get("세기") or []):
            centuries[c] += 1
        for st in (fm.get("발전단계") or []):
            if st.get("세기"):
                centuries[st["세기"]] += 1

    # 예약: frontmatter 가 가리키는 슬러그인데 문서가 없는 것 (ROADMAP §0 유형①·③)
    reserved = collections.Counter()
    reserved_by = collections.defaultdict(set)
    for slug, fm in fms.items():
        for f in REF_FIELDS:
            for t in [str(x).strip() for x in (fm.get(f) or []) if str(x).strip()]:
                if t not in fms:
                    reserved[t] += 1
                    reserved_by[t].add(slug)

    _, wiki_pending, wiki_where = V.collect_wikilinks()
    stage_pending, stage_where = V.collect_stage_people()
    holes = V.collect_symmetry()

    fails = []
    for slug, path in M.iter_notes():
        err, _warn, _st = V.check_note(slug, path)
        if err:
            fails.append(slug)

    return dict(fms=fms, kinds=kinds, centuries=centuries,
                reserved=reserved, reserved_by=reserved_by,
                wiki=wiki_pending, wiki_where=wiki_where,
                stage=stage_pending, stage_where=stage_where,
                holes=holes, fails=fails)


def render(m):
    L = []
    A = L.append
    total = len(m["fms"])
    A("")
    A("> **이 블록은 `tools/build_math_status.py` 산출물이다. 손으로 고치지 말 것.**")
    A("> 아래 판단(무엇을 먼저 쓸 것인가·왜)은 사람이 적는 자리이고, 여기 숫자는 실측이다.")
    A("")
    A("### 규모")
    A("")
    A("| 유형 | 편수 |")
    A("|---|---|")
    for k in ["세기", "개념", "인물", "일화"]:
        A("| %s | %d |" % (k, m["kinds"].get(k, 0)))
    A("| **합계** | **%d** |" % total)
    A("")
    ok = total - len(m["fails"])
    A("`verify_math.py` — %d편 중 %d편 통과%s"
      % (total, ok, ("" if not m["fails"] else " · 실패: " + ", ".join(m["fails"]))))
    A("")
    A("### 세기 분포 (`세기` 필드 ∪ `발전단계[].세기`)")
    A("")
    cs = sorted(m["centuries"])
    A("| 세기 | " + " | ".join("%d" % c for c in cs) + " |")
    A("|---|" + "---|" * len(cs))
    A("| 편수 | " + " | ".join(str(m["centuries"][c]) for c in cs) + " |")
    A("")
    # 빈 세기를 하나씩 늘어놓으면 17줄이 된다(-2 ~ 15). 연속 구간으로 접는다 —
    # 읽는 사람이 알아야 하는 것은 '어디가 비었나'이지 목록이 아니다.
    gap = [c for c in range(min(cs), max(cs) + 1) if m["centuries"].get(c, 0) == 0]
    runs = []
    for c in gap:
        if runs and c == runs[-1][1] + 1:
            runs[-1][1] = c
        else:
            runs.append([c, c])
    if runs:
        def lab(c):
            return "기원전 %d" % -c if c < 0 else "%d" % c
        A("빈 세기: " + " · ".join(
            (lab(a) + "세기" if a == b else "%s~%s세기" % (lab(a), lab(b)))
            + ("" if a == b else " (%d개)" % (b - a + 1))
            for a, b in runs))
    A("")
    A("### 예약 — frontmatter 가 가리키는데 문서가 없다 (§0 유형①·③)")
    A("")
    if m["reserved"]:
        A("| 슬러그 | 예약 | 예약한 문서 |")
        A("|---|---|---|")
        for t, c in m["reserved"].most_common():
            A("| `%s` | %d회 | %s |" % (t, c, ", ".join(sorted(m["reserved_by"][t]))))
    else:
        A("없음.")
    A("")
    A("### 백로그 — 채널 둘")
    A("")
    A("| 채널 | 종 | 회 | 상위 |")
    A("|---|---|---|---|")
    def top(counter):
        return " · ".join("%s %d" % (t, c) for t, c in counter.most_common(5)) or "—"
    A("| 미해결 위키링크 | %d | %d | %s |"
      % (len(m["wiki"]), sum(m["wiki"].values()), top(m["wiki"])))
    A("| 호명(`발전단계[].인물`) | %d | %d | %s |"
      % (len(m["stage"]), sum(m["stage"].values()), top(m["stage"])))
    A("")
    A("### frontmatter 상호참조 — 단방향 %d건 (보고이며 게이트가 아니다)" % len(m["holes"]))
    A("")
    by = collections.Counter("`%s` → 역방향 `%s`" % (s, d) for _, s, _, d in m["holes"])
    if by:
        A("| 방향 | 건수 |")
        A("|---|---|")
        for k, c in by.most_common():
            A("| %s | %d |" % (k, c))
    else:
        A("구멍 없음.")
    A("")
    return "\n".join(L)


def main():
    m = measure()
    block = render(m)
    if "--print" in sys.argv:
        print(block)
        return 0
    if not ROADMAP.exists():
        print("ROADMAP 이 없다: %s" % ROADMAP)
        return 1
    text = ROADMAP.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print("마커를 찾지 못했다. ROADMAP 에 다음 두 줄을 넣고 다시 돌릴 것:")
        print("  %s\n  %s" % (BEGIN, END))
        return 1
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    out = head + BEGIN + "\n" + block + END + tail
    if out != text:
        ROADMAP.write_text(out, encoding="utf-8", newline="\n")
        print("ROADMAP 자동측정 블록 갱신 — %d편 · 예약 %d종 · 위키링크 백로그 %d종 · 호명 백로그 %d종"
              % (len(m["fms"]), len(m["reserved"]), len(m["wiki"]), len(m["stage"])))
    else:
        print("변경 없음 (이미 최신).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
