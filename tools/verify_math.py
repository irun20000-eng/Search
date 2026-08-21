#!/usr/bin/env python3
"""
수학사 노트 품질 게이트 + 스키마 검증.

이 파일이 math/ 스키마의 실행 가능한 명세다. 문서로만 적힌 규칙은 지켜지지
않으므로, 지켜야 하는 것은 전부 여기서 막는다.

■ 게이트 수치의 출처 (LESSONS.md "근거 없는 숫자를 쓰지 말 것")

  · 개념 이해편 / 개념 확장편
      LESSONS.md 2026-08-16 게이트를 그대로 승계한다. 기존 코퍼스 실측값이므로
      근거가 있다. 임의로 낮추지 않는다.

  · 세기
      개념 이해편에 앵커링했다. 세기 개관은 성격상 개념 이해편과 같은
      '한 주제를 처음부터 훑는 글'이고, 출처만 ≥10으로 올렸다 —
      한 세기를 다루면 참조해야 할 사료 범위가 개념 하나보다 넓다.

  · 인물                                              [잠정]
      코퍼스 없음. 개념 이해편 8,000자의 75%인 6,000자를 잠정 하한으로 둔다.
      일대기는 개념 해설보다 얇아도 되지만 크게 얇으면 안 된다고 보았다.
      → 인물 노트 6편이 쌓이면 실측 분포로 재보정하고 근거를 여기에 남긴다.
        (목표 시점: 17세기 완료 직후)

  · 일화                                              [잠정]
      코퍼스 없음. 유일하게 상한을 둔다.
        하한 800  — 출처 3개를 인용하며 맥락과 진위 판정까지 담는 최소 분량
        상한 2500 — 담기 합본에서 한 꼭지가 차지해도 부담 없는 크기
      일화는 '짧아야 재사용된다'는 것이 설계 전제이므로 상한이 본질적이다.
      → 일화 8편이 쌓이면 재보정한다. (목표 시점: 17세기 완료 직후)

■ 측정 공식 — 자수는 '본문만' 센다 (frontmatter 제외)

  CLAUDE.md의 정본 지표는 파일 전체를 재는 `LC_ALL=C.UTF-8 wc -m` 이다.
  그 8,000자 기준은 frontmatter가 작은 기존 리포트에 맞춰 정해졌다.
  실측(2026-08-21, reports/*/report.md 62편):

      기존 리포트 frontmatter  중앙값 327자 (최소 228 · 최대 402)
      → 기존 게이트의 실질 본문 하한 = 8,000 − 327 = 7,673자

  수학사 노트는 발전단계·출처·이미지를 구조화해 담으므로 frontmatter가
  3,553자에 이른다. 여기에 '파일 전체 8,000자'를 그대로 적용하면 실질
  본문 하한이 4,447자로 떨어져 게이트가 3,226자(42%)만큼 헐거워진다.

  그래서 자수는 본문만 재고, 하한은 기존의 실질 하한을 그대로 옮긴다.
  기준을 낮춘 것이 아니라 같은 높이를 유지하려고 측정 지점을 옮긴 것이며,
  환산 근거를 여기에 남긴다. (LESSONS.md "게이트를 몰래 낮추지 말 것")

      개념 이해편  8,000 → 7,673      개념 확장편  11,000 → 10,673
      세기         이해편과 동일        인물  이해편의 75% = 5,750  [잠정]
      일화         800~2,500 (처음부터 본문 기준)  [잠정]

  섹션  = '^## ' 개수
  시각화 = 마크다운 표 + 이미지 + <figure>

사용:
  python tools/verify_math.py              # 전체
  python tools/verify_math.py <슬러그>...   # 일부
  python tools/verify_math.py --backlog    # 미해결 위키링크만 출력
"""
import sys
import re
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M          # noqa: E402

# 유형별 게이트. 자수는 본문 기준 (위 "측정 공식" 참조 — frontmatter 327자 환산 반영)
G = {
    "개념/이해편": dict(chars=7673,  chars_max=None, lines=140, sections=8,  visuals=3, sources=7),
    "개념/확장편": dict(chars=10673, chars_max=None, lines=165, sections=10, visuals=2, sources=12),
    "세기":       dict(chars=7673,  chars_max=None, lines=140, sections=8,  visuals=3, sources=10),
    "인물":       dict(chars=5750,  chars_max=None, lines=110, sections=7,  visuals=2, sources=7),
    "일화":       dict(chars=800,   chars_max=2500, lines=0,   sections=3,  visuals=1, sources=3),
}

COMMON_REQUIRED = ["유형", "제목", "슬러그", "볼트파일명", "세기", "요약", "출처"]
TYPE_REQUIRED = {
    "개념": ["트랙", "발전단계", "기여인물"],
    "인물": ["생몰"],
    "일화": ["사실성", "사실성근거"],
    "세기": ["연대", "시대이슈"],
}


def gate_key(fm):
    if fm.get("유형") == "개념":
        return "개념/%s" % fm.get("트랙", "이해편")
    return fm.get("유형")


def check_note(slug, path):
    """(errors, warnings, stats) 반환."""
    err, warn = [], []
    try:
        fm, body = M.read_note(path)
    except ValueError as e:
        return ["%s" % e], [], {}

    def E(msg):
        err.append(msg)

    def W(msg):
        warn.append(msg)

    # ── 공통 필수 필드 ──
    for k in COMMON_REQUIRED:
        if not fm.get(k):
            E("필수 필드 누락: %s" % k)

    typ = fm.get("유형")
    if typ not in M.TYPES:
        E("유형이 %s 중 하나가 아님: %r" % (sorted(M.TYPES), typ))
        return err, warn, {}

    for k in TYPE_REQUIRED.get(typ, []):
        if not fm.get(k):
            E("%s 필수 필드 누락: %s" % (typ, k))

    if fm.get("슬러그") != slug:
        E("슬러그(%r)가 폴더명(%r)과 다름" % (fm.get("슬러그"), slug))

    cents = fm.get("세기")
    if not isinstance(cents, list) or not all(isinstance(c, int) for c in cents):
        E("세기는 정수 배열이어야 함: %r" % (cents,))

    if typ == "개념" and fm.get("트랙") not in M.TRACKS:
        E("트랙은 이해편|확장편: %r" % fm.get("트랙"))

    if typ == "일화":
        if fm.get("사실성") not in M.FACTUALITY:
            E("사실성은 %s 중 하나: %r" % (sorted(M.FACTUALITY), fm.get("사실성")))
        if len(str(fm.get("사실성근거") or "")) < 20:
            E("사실성근거가 너무 짧다 (판정 이유를 1~2문장으로)")

    if typ == "인물":
        lp = fm.get("생몰") or {}
        if not isinstance(lp, dict) or "출생" not in lp or "사망" not in lp:
            E("생몰은 {출생:, 사망:, 출생지:} 매핑이어야 함")
        elif isinstance(lp.get("출생"), int) and isinstance(lp.get("사망"), int):
            if lp["사망"] <= lp["출생"]:
                E("생몰 연도가 뒤집혀 있음: %s–%s" % (lp["출생"], lp["사망"]))

    # ── 출처 ──
    srcs = fm.get("출처") or []
    nums = []
    for i, s in enumerate(srcs, 1):
        if not isinstance(s, dict):
            E("출처[%d]가 매핑이 아님" % i)
            continue
        for k in ("번호", "제목", "URL", "유형"):
            if not s.get(k):
                E("출처[%d] 필드 누락: %s" % (i, k))
        if s.get("유형") not in ("1차", "2차"):
            E("출처[%d] 유형은 1차|2차: %r" % (i, s.get("유형")))
        if isinstance(s.get("번호"), int):
            nums.append(s["번호"])
    dup = [n for n, c in Counter(nums).items() if c > 1]
    if dup:
        E("출처 번호 중복: %s" % sorted(dup))

    numset = set(nums)
    used = M.extract_citations(body)
    dangling = sorted(used - numset)
    if dangling:
        E("본문 인용이 출처에 없음: %s" % dangling)
    unused = sorted(numset - used)
    if unused:
        W("출처에 있으나 본문에서 인용되지 않음: %s" % unused)

    # ── 발전단계 (개념) ──
    for i, st in enumerate(fm.get("발전단계") or [], 1):
        if not isinstance(st, dict):
            E("발전단계[%d]가 매핑이 아님" % i)
            continue
        for k in ("세기", "인물", "변화"):
            if not st.get(k):
                E("발전단계[%d] 필드 누락: %s" % (i, k))
        if st.get("출처") is not None and st["출처"] not in numset:
            E("발전단계[%d]의 출처 %r 가 출처 목록에 없음" % (i, st["출처"]))

    # ── 이미지 라이선스 ──
    for i, im in enumerate(fm.get("이미지") or [], 1):
        if not isinstance(im, dict):
            E("이미지[%d]가 매핑이 아님" % i)
            continue
        for k in ("파일", "출처", "라이선스", "설명"):
            if not im.get(k):
                E("이미지[%d] 필드 누락: %s  (라이선스 미상은 게시 불가)" % (i, k))
        f = im.get("파일")
        if f and not (M.MATH / f).exists() and not str(f).startswith("http"):
            E("이미지[%d] 파일이 없음: math/%s" % (i, f))

    # ── 분량 게이트 ──
    g = G.get(gate_key(fm))
    stats = {}
    if g:
        stats = dict(
            chars=M.count_chars(body),
            lines=M.count_lines(body),
            sections=M.count_sections(body),
            visuals=M.count_visuals(body),
            sources=len(srcs),
        )
        labels = dict(chars="자수", lines="줄", sections="섹션", visuals="시각화", sources="출처")
        for k, label in labels.items():
            need = g.get(k, 0)
            if need and stats[k] < need:
                E("%s 미달: %s < %s" % (label, stats[k], need))
        if g.get("chars_max") and stats["chars"] > g["chars_max"]:
            E("자수 초과: %s > %s  (일화는 짧아야 재사용된다)" % (stats["chars"], g["chars_max"]))

    return err, warn, stats


def collect_wikilinks(only=None):
    """(해결됨 Counter, 미해결 Counter, 출처노트맵)"""
    idx = M.load_link_index()
    resolved, pending = Counter(), Counter()
    where = {}
    for slug, path in M.iter_notes():
        if only and slug not in only:
            continue
        try:
            _, body = M.read_note(path)
        except ValueError:
            continue
        for target, _label in M.extract_wikilinks(body):
            if target in idx:
                resolved[target] += 1
            else:
                pending[target] += 1
                where.setdefault(target, set()).add(slug)
    return resolved, pending, where


def print_backlog(pending, where, limit=40):
    if not pending:
        print("미해결 위키링크 없음.")
        return
    total = sum(pending.values())
    print("\n── 콘텐츠 백로그 — 미해결 위키링크 %d종 %d회 ──" % (len(pending), total))
    print("   (아직 문서가 없는 대상. 참조가 많을수록 먼저 쓸 가치가 있다)")
    for t, c in pending.most_common(limit):
        src = ", ".join(sorted(where.get(t, ()))[:3])
        print("  %3d회  %-30s  ← %s" % (c, t[:30], src))
    if len(pending) > limit:
        print("  … 외 %d종" % (len(pending) - limit))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}

    notes = list(M.iter_notes())
    if args:
        notes = [(s, p) for s, p in notes if s in set(args)]

    if "--backlog" in flags:
        r, p, w = collect_wikilinks()
        print_backlog(p, w, limit=200)
        return 0

    if not notes:
        print("math/notes/ 에 노트가 없다.")
        return 0

    fail = 0
    for slug, path in notes:
        err, warn, st = check_note(slug, path)
        mark = "FAIL" if err else ("warn" if warn else " ok ")
        line = "[%s] %s" % (mark, slug)
        if st:
            line += "   %d자 · %d줄 · %d절 · 시각화 %d · 출처 %d" % (
                st["chars"], st["lines"], st["sections"], st["visuals"], st["sources"])
        print(line)
        for e in err:
            print("       ✗ %s" % e)
        for w in warn:
            print("       ! %s" % w)
        if err:
            fail += 1

    print("\n%d편 중 %d편 실패." % (len(notes), fail))

    resolved, pending, where = collect_wikilinks({s for s, _ in notes})
    print("위키링크: 해결 %d회 / 미해결 %d회" % (sum(resolved.values()), sum(pending.values())))
    print_backlog(pending, where)

    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
