#!/usr/bin/env python3
"""수학사 도해 현황 — 몇 장이 있고 어느 유형이 비어 있나.

왜 있나.
    이 수를 **인계 문서에 손으로 적었더니 세 회차 연속으로 낡았다.** 「14장 · 12편 ·
    세기 5/6」이 하루 만에 틀렸고, 그 전에도 「여유 34자」가 실제 24자를 42% 부풀렸다.
    `math/ROADMAP.md` §11 이 「숫자를 손으로 적으면 어디에 적든 낡는다」를 네 번 확인했다고
    적어 뒀다. 그래서 이 수는 문장에서 빼고 여기로 옮긴다 — LESSONS 2026-09-09
    「손으로 적은 숫자는 빌더가 안 따라온다」의 처방이 「측정 명령을 대신 적는다」였다.

무엇을 세나.
    노트가 도해를 가졌다는 표지는 **frontmatter 의 `이미지:` 필드**다(본문 임베드가 아니라).
    갤러리 카드·볼트 동기화·manifest 가 전부 그 필드를 보므로 그것이 정본이다.
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
    used = collections.Counter()
    for note in sorted((ROOT / 'math/notes').glob('*/note.md')):
        kind = note.parent.name.split('-')[0]
        tot[kind] += 1
        body = note.read_text(encoding='utf-8')
        # ⚠ `이미지:` 가 있다고 도해가 아니다 — MATH_PIPELINE M3 은 같은 필드에
        #   `assets/portraits/` PD 초상도 넣게 돼 있다. 초상이 들어오는 날 이 도구가
        #   도해 없는 노트를 「보유」로 세게 된다. 그래서 경로까지 본다.
        if re.search(r'^이미지:', body, re.M) and 'assets/figures/' in body:
            has[kind] += 1
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
    print('도해 SVG %d장 · 도해를 가진 노트 %d편 / 전체 %d편'
          % (len(svgs), sum(has.values()), sum(tot.values())))
    print()
    print('  %-6s %7s   %s' % ('유형', '보유/전체', '남은 무도해'))
    for key, label in TYPES:
        print('  %-6s %4d/%-4d   %d편' % (label, has[key], tot[key], tot[key] - has[key]))

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
