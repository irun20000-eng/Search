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
from pathlib import Path

ALLOWED_OTHER = set('\n\t')


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
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
