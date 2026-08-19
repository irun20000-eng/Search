#!/usr/bin/env python3
"""
노트 본문의 인코딩 손상 검출기.

배경: Drive 원본을 base64로 받아 모델이 다시 타이핑해 디스크에 쓰는 경로에서
한글이 조용히 다른 문자로 치환된다. 치환 결과도 유효한 UTF-8이라 디코드 검사를
통과하고, 챕터·인용 개수도 그대로라 구조 게이트도 통과한다.
실제로 U+AE30(기) → U+EE30(사설영역)이 갤러리까지 발행된 적이 있다.

이 스크립트는 '한국어 노트에 있을 수 없는 문자'를 찾는다.
완전한 보증은 아니지만(정상 한글로 치환되면 못 잡는다) 관측된 손상 유형은 잡는다.

사용: python3 tools/check_encoding.py [파일...]
"""
import sys, unicodedata
from collections import Counter
from pathlib import Path

ALLOWED_OTHER = set('\n\t')

HANGUL = range(0xAC00, 0xD7A4)


def _file_syllables(path):
    return {ch for ch in Path(path).read_text(encoding='utf-8') if ord(ch) in HANGUL}


def corpus_counter(exclude=()):
    """발행된 노트별 음절 집합을 합산한 카운터.

    leave-one-out을 하려면 '몇 개 파일에서 쓰였나'가 필요하다. 집합 하나로 합치면
    검사 대상 자신이 코퍼스에 섞여 모든 음절이 정상으로 보인다.
    """
    ex = {str(Path(p).resolve()) for p in exclude}
    cnt = Counter()
    for p in sorted(Path("videos/notes").glob("*.md")):
        if str(p.resolve()) in ex:
            continue
        cnt.update(_file_syllables(p))
    return cnt


def corpus_syllables(exclude=()):
    """이미 발행된 노트 전체에서 쓰인 한글 음절 집합."""
    return set(corpus_counter(exclude))


def rare_syllables(path, corpus=None):
    """기존 코퍼스에 한 번도 안 쓰인 한글 음절을 찾는다.

    배경: 관측된 손상은 base64 한 글자가 바뀌는 형태였다(드→듘 c→Y, 짧→쇧 K→I,
    팎→팍 O→N, 년→륄 4→6). 결과가 '유효한 정상 한글'이라 suspicious()가 못 잡고,
    같은 오독이 결정적으로 재현되므로 2회 다운로드 대조로도 안 걸러진다.
    실제로 이 검사만이 4건을 잡아냈다(2026-08-19).

    오탐이 있다(뺄·뺀·닛처럼 드물 뿐 정상인 음절). 그래서 차단이 아니라 '검토 필요'다.
    판단은 사람/에이전트가 하되, 눈으로 놓치는 일은 없게 한다.
    """
    if corpus is None:
        corpus = corpus_syllables(exclude=[path])
    t = Path(path).read_text(encoding='utf-8')
    hits = []
    for i, ch in enumerate(t):
        if ord(ch) in HANGUL and ch not in corpus:
            ctx = t[max(0, i - 25):i].replace('\n', ' ')
            aft = t[i + 1:i + 20].replace('\n', ' ')
            hits.append((i, f"U+{ord(ch):04X}", ch, f"…{ctx}[{ch}]{aft}…"))
    return hits


def suspicious(ch):
    cp = ord(ch)
    if ch in ALLOWED_OTHER:
        return None
    if 0xE000 <= cp <= 0xF8FF:
        return "사설영역(PUA)"
    if 0xF0000 <= cp <= 0x10FFFD:
        return "보조 사설영역"
    if cp in (0x200B, 0x200C, 0x200D, 0xFEFF, 0x00AD):
        return "보이지 않는 문자"
    cat = unicodedata.category(ch)
    if cat in ('Cc', 'Cn', 'Cs'):
        return f"제어/미할당({cat})"
    # 낱자 자모(ㅣ ㅡ 등)는 검사하지 않는다.
    # 유튜브 제목·채널명에서 '|' 대신 쓰는 구분자라 오탐만 3건 나왔고 진탐은 0건이었다.
    # 실제 관측된 손상은 전부 사설영역/보이지 않는 문자 쪽이다.
    return None


def check(path):
    t = Path(path).read_text(encoding='utf-8')
    hits = []
    for i, ch in enumerate(t):
        why = suspicious(ch)
        if why:
            ctx = t[max(0, i - 30):i].replace('\n', ' ')
            aft = t[i + 1:i + 30].replace('\n', ' ')
            hits.append((i, f"U+{ord(ch):04X}", why, f"…{ctx}[{ch}]{aft}…"))
    return hits


def main():
    paths = sys.argv[1:] or sorted(Path("videos/notes").glob("*.md"))
    paths += sorted(Path("guides").glob("*/guide.md")) if not sys.argv[1:] else []
    bad = 0
    for p in paths:
        hits = check(p)
        if hits:
            bad += 1
            print(f"❌ {Path(p).name}")
            for pos, cp, why, ctx in hits[:8]:
                print(f"     · {cp} {why} @{pos}")
                print(f"       {ctx}")
    print(f"\n{len(paths)}개 검사 · 정상 {len(paths)-bad} · 의심 {bad}")

    # 코퍼스 대조 — 차단하지 않고 사람이 볼 수 있게 띄운다(오탐 있음).
    # 검사 대상 자신은 코퍼스에서 빼야 한다(leave-one-out). 안 그러면 자기 음절이
    # 자기를 정상이라고 보증해 검사가 통째로 무력해진다.
    base = corpus_counter()
    for p in paths:
        own = _file_syllables(p) if Path(p).parent.name == "notes" else set()
        corpus = {ch for ch, n in base.items() if n - (1 if ch in own else 0) > 0}
        rare = rare_syllables(p, corpus)
        if rare:
            print(f"\n⚠️  {Path(p).name} — 기존 코퍼스에 없는 음절 {len(rare)}개 (검토 필요)")
            for pos, cp, ch, ctx in rare[:8]:
                print(f"     · {ch} {cp} @{pos}")
                print(f"       {ctx}")

    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
