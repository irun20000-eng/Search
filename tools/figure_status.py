#!/usr/bin/env python3
"""수학사 도해 현황 — 몇 장이 있고 어느 유형이 비어 있나.

왜 있나.
    이 수를 **인계 문서에 손으로 적었더니 세 회차 연속으로 낡았다.** 「14장 · 12편 ·
    세기 5/6」이 하루 만에 틀렸고, 그 전에도 「여유 34자」가 실제 24자를 42% 부풀렸다.
    `math/ROADMAP.md` §11 이 「숫자를 손으로 적으면 어디에 적든 낡는다」를 네 번 확인했다고
    적어 뒀다. 그래서 이 수는 문장에서 빼고 여기로 옮긴다 — LESSONS 2026-09-09
    「손으로 적은 숫자는 빌더가 안 따라온다」의 처방이 「측정 명령을 대신 적는다」였다.

무엇을 세나 — **두 가지를 따로 센다.** 셀 수 있는 것을 한 가지로만 찍어 놓으면
다음 사람이 나머지를 손으로 세고 **셈법 없이 적는다.** 2026-09-18 에 실제로 그랬다 —
커밋 `b358f10` 본문이 「도해 없는 노트 49편에서 … 골랐다」라고만 적었는데, 그 49 는
②(본문 임베드까지) 값이었고 같은 시점의 ① 은 53 이었다. **두 기준의 차가 4편**이라
어느 쪽 기준인지를 안 밝히면 재현이 안 된다.

    ① **프론트매터 `이미지:` 기준** — 갤러리 카드·볼트 동기화·manifest 가 보는 정본이다.
    ② **본문 임베드까지 친 것** — 남의 그림을 짧은 alt 로 빌려 온 노트는 프론트매터에
       등재하지 않으므로 ① 로는 「무도해」로 찍히지만, **이미 그림이 붙어 있어 다음
       회차의 대상이 아니다.** 대상을 고를 때 보는 것은 이쪽이다.
    ⚠ ② 를 가리는 표지는 **경로**(`../../`)다. 문법은 하나가 아니다 — 마크다운
    `![alt](…)` 와 생 HTML `<img src="…">` 둘 다 쓰인다(리포 현재 48 대 4).
    정규식을 마크다운만으로 좁히면 `<img>` 로 빌려 온 노트가 조용히 「무도해」로 찍힌다.
    ⚠ 그래서 **SVG 장수와 노트 편수는 같지 않다** — 한 노트가 두 장을 갖기도 하고
    (`concept-probability-advanced`), 한 장이 두 노트에 물리기도 한다
    (`leibniz-characteristic-triangle`). 둘을 따로 센다.

게이트가 아니다 — 언제나 exit 0 이다. 부채는 실패가 아니라 다음 회차의 대상이다.
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TYPES = (('person', '인물'), ('concept', '개념'), ('century', '세기'), ('episode', '일화'))


def main():
    tot, has = collections.Counter(), collections.Counter()
    emb = collections.Counter()          # 프론트매터 ∪ 본문 임베드
    used = collections.Counter()
    for note in sorted((ROOT / 'math/notes').glob('*/note.md')):
        kind = note.parent.name.split('-')[0]
        tot[kind] += 1
        body = note.read_text(encoding='utf-8')
        # ⚠ `이미지:` 가 있다고 도해가 아니다 — MATH_PIPELINE M3 은 같은 필드에
        #   `assets/portraits/` PD 초상도 넣게 돼 있다. 초상이 들어오는 날 이 도구가
        #   도해 없는 노트를 「보유」로 세게 된다. 그래서 경로까지 본다.
        fm = bool(re.search(r'^이미지:', body, re.M)) and 'assets/figures/' in body
        # 본문 임베드는 노트 폴더 기준 경로다(MATH_PIPELINE M3) — 프론트매터의
        # `assets/figures/…` 와 갈리는 표지가 그 `../../` 다. **문법은 둘**이므로
        # 마크다운과 `<img>` 를 함께 문다(머리말 ⚠ — 마크다운만 물면 4편이 샌다).
        body_embed = bool(re.search(
            r'(?:!\[[^\]]*\]\(|<img[^>]*src=")\.\./\.\./assets/figures/', body))
        if fm:
            has[kind] += 1
        if fm or body_embed:
            emb[kind] += 1
        # ⚠ 한 노트가 같은 파일을 **두 번** 적는다 — frontmatter 의 `이미지.파일` 과
        #   본문 임베드. 낱개로 세면 거의 모든 SVG 가 「2곳에 물림」으로 찍힌다(첫 판이 그랬다).
        #   세려는 것은 **몇 편의 노트가 쓰는가**이므로 노트 단위로 집합을 만든다.
        for f in set(re.findall(r'assets/figures/([\w-]+\.svg)', body)):
            used[f] += 1

    # 유형 넷 밖의 접두사가 생기면 머리글 합계에는 들어가고 표에는 한 줄도 안 찍혀
    # **총계와 표가 조용히 어긋난다.** 여기서 끊는다(세는 단위가 틀리는 것이 이 도구의 실패 양식이다).
    unknown = sorted(set(tot) - {k for k, _ in TYPES})
    if unknown:
        print('⚠ TYPES 에 없는 슬러그 접두사: %s — 표와 총계가 어긋난다. TYPES 를 늘릴 것.'
              % ', '.join(unknown))

    svgs = sorted(p.name for p in (ROOT / 'math/assets/figures').glob('*.svg'))
    total = sum(tot.values())
    print('도해 SVG %d장 · 전체 노트 %d편' % (len(svgs), total))
    print('  ① 프론트매터 `이미지:` 기준  — 도해를 가진 노트 %d편 (남은 %d편)   ← manifest·갤러리·볼트가 보는 것'
          % (sum(has.values()), total - sum(has.values())))
    print('  ② 본문 임베드까지 치면      — %d편 (남은 %d편)   ← 다음 대상을 고를 때 보는 것'
          % (sum(emb.values()), total - sum(emb.values())))
    print()
    print('  %-6s %9s %7s   %9s %7s' % ('유형', '① 보유/전체', '① 남은', '② 보유/전체', '② 남은'))
    for key, label in TYPES:
        print('  %-6s %6d/%-4d %6d편   %6d/%-4d %6d편'
              % (label, has[key], tot[key], tot[key] - has[key],
                 emb[key], tot[key], tot[key] - emb[key]))

    orphan = [s for s in svgs if s not in used]
    if orphan:
        print('\n⚠ 어느 노트도 안 쓰는 SVG %d장: %s' % (len(orphan), ', '.join(orphan)))
    shared = [s for s, n in sorted(used.items()) if n > 1]
    if shared:
        print('\n두 곳 이상에 물린 SVG: %s' % ', '.join('%s(%d)' % (s, used[s]) for s in shared))

    print('\n다음 대상은 「도형어가 많은 노트」가 아니라 **그 절이 그림으로 논증하는 노트**로 고른다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
