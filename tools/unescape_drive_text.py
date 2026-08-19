#!/usr/bin/env python3
"""
Drive `read_file_content` 출력 → 스파크 원문(VIDEO-NOTE 블록) 복원기.

배경: 원문을 `download_file_content`(base64)로 받아 세션이 다시 타이핑하면
base64 한 글자가 바뀌어도 알아챌 수 없다. 2026-08-19 회차에서 5건 중 3건이
그렇게 깨졌다(`코드`→`코듘` c→Y, `짧게`→`쇧게` K→I, `안팎`→`안팍` O→N).

`read_file_content`는 대신 **평문 한글**을 준다. 같은 오류가 나면 곧바로
헛소리로 드러나므로 세션이 잡을 수 있다. 대가로 마크다운이 이스케이프되고
줄 끝에 공백 2칸이 붙고 중첩 불릿 들여쓰기가 뭉개진다 — 전부 되돌릴 수 있다.

관측된 이스케이프(2026-08-19, 파일 2건):
    \\===  \\>  \\*\\*  \\#\\#  \\-  \\`  1\\.
규칙은 "ASCII 구두점 앞의 백슬래시 제거" 하나로 전부 덮인다.

⚠️ 한계: 본문에 **진짜 백슬래시**가 있으면 (`C:\\path`, LaTeX 등) 원문과
구별되지 않는다. 스파크 영상노트에는 지금까지 사례가 없지만, 복원 결과에
백슬래시가 남아 있으면 경고한다(--strict 면 실패 처리).

사용: python3 tools/unescape_drive_text.py <입력> [-o 출력] [--strict]
"""
import argparse
import re
import sys
from pathlib import Path

# 마크다운 이스케이프 대상 — GFM이 쓰는 구두점 집합.
PUNCT = r"""!"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~"""
ESCAPED = re.compile(rf'\\([{PUNCT}])')


def unescape(text):
    """`\\X`(X=ASCII 구두점) → `X`, 줄 끝 공백 제거, 중첩 불릿 들여쓰기 정규화."""
    out = []
    for line in text.split('\n'):
        line = ESCAPED.sub(r'\1', line)
        line = line.rstrip()
        # read_file_content가 2칸 들여쓰기를 1칸으로 뭉갠다. 원문은 2칸.
        # '- ' 로 시작하는 불릿만 대상 — 본문 문장은 건드리지 않는다.
        m = re.match(r'^( +)(- )', line)
        if m and len(m.group(1)) == 1:
            line = '  ' + line[1:]
        out.append(line)
    # 문단 사이 빈 줄에 남은 공백도 제거된 상태로 합친다.
    return '\n'.join(out).strip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('-o', '--out')
    ap.add_argument('--strict', action='store_true',
                    help='복원 후 백슬래시가 남아 있으면 실패 처리')
    a = ap.parse_args()

    text = Path(a.src).read_text(encoding='utf-8')
    result = unescape(text)

    problems = []
    if not result.startswith('===VIDEO-NOTE v1==='):
        problems.append('시작 마커 없음 (===VIDEO-NOTE v1===)')
    if not result.rstrip().endswith('===END==='):
        problems.append('종료 마커 없음 (===END===)')
    left = result.count('\\')
    if left:
        problems.append(f'백슬래시 {left}개 잔존 — 원문에 실제 백슬래시가 있는지 확인할 것')

    chapters = len(re.findall(r'^## \d+\.', result, re.M))
    quotes = result.count('**핵심 인용**')
    tips = result.count('**내 팁**') + result.count('**내 질문**')
    print(f'복원: {len(result)}자 · 챕터 {chapters} · 인용 {quotes} · 팁/질문 {tips}')

    for p in problems:
        print(f'  ⚠️  {p}')

    if a.out:
        Path(a.out).write_text(result, encoding='utf-8')
        print(f'저장: {a.out}')

    fatal = [p for p in problems if '마커' in p] or (problems if a.strict else [])
    sys.exit(1 if fatal else 0)


if __name__ == '__main__':
    main()
