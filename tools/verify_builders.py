#!/usr/bin/env python3
"""산출물이 소스보다 낡았는지 잰다 — 빌더를 돌려 결과가 바뀌면 낡은 것이다.

왜 있나.
    2026-09-09 에 `episode-bernoulli-tomb` 이 일화 자수 상한에 걸려 게이트가 FAIL 했다.
    캡션을 줄여 통과시켰는데 **빌더를 다시 안 돌렸다.** 그래서 `math/manifest.json` 에
    실패 시점의 `"자수": 2547` 이 그대로 남았고, `math/index.html` 이 그 값을 카드에
    표시하므로 **라이브 갤러리에 틀린 수치가 나갔다.** `math/ROADMAP.md` 의 「자동 측정」
    블록은 **있지도 않은 게이트 실패**를 기록으로 남겼다(다음 세션이 없는 결함을 쫓는다).
    커밋 메시지에는 「빌더 통과」라고 적혀 있었다 — 돌리긴 돌렸다, 고치기 전에.

    그래서 규칙을 문서에 적었는데, 문서 규칙은 반드시 건너뛴다는 것이 이 리포의 교훈이다
    (LESSONS 2026-09-02 「재발 방지는 문서가 아니라 게이트에 적는다」). 그 규칙을 여기 옮긴다.

무엇을 재나 — 멱등성 하나다.
    지금 산출물이 **지금 소스의 고정점인가.** 소스를 고치고 빌더를 안 돌렸으면 재실행이
    값을 바꾸므로 잡힌다. 돌렸으면 이미 고정점이라 안 바뀐다.

    ⚠ `git diff` 로 재면 안 된다. HEAD 와 비교하므로 **정당한 변경까지** 걸린다.
    재야 할 것은 커밋과의 차이가 아니라 소스와의 고정점 관계다.

왜 임시 트리에 안 돌리나.
    `build_math_manifest.py` 가 `generated` 를 `git log -1` 로 채운다. `.git` 없는 복사본에서는
    빈 문자열이 되어 **없는 차이가 생긴다.** 그래서 제자리에서 돌리고 **되돌려 놓는다**
    (`--write` 를 주면 새로 만든 것을 남긴다). 중간에 죽어도 새 산출물이 남을 뿐이라 무해하다.

무엇을 안 보나.
    `backlog.json` 은 이 세 빌더의 산출물이 아니다(`build_backlog.py` 몫). 넣어 두면 늘
    OK 로 찍혀 검사 범위가 실제보다 넓어 보인다.
    **빌더가 늘면 `BUILDERS` 와 `OUTPUTS` 를 함께 늘려야 한다** — 목록에 없는 산출물은 못 본다.

    그리고 `manifest.json` 의 `generated` 는 **노트에서 오지 않는다** — `git log -1` 이 준
    HEAD 의 커밋 날짜다. 커밋이 날짜를 넘기면 그 한 줄만 어긋나고, 그것은 「소스를 고치고
    빌더를 안 돌렸다」가 아니라 「그 사이에 커밋이 있었다」는 뜻이다. 그래서 **비교에서
    빼고, 그것만 다르면 실패가 아니라 안내로 찍는다.** (LESSONS 2026-08-31 「빌더를 두 번
    돌려 같지 않으면 그 자리에 시계가 섞여 있다」— 여기가 그 시계이고, 의도된 것이다.)

쓰기.
    python3 tools/verify_builders.py           # 확인만 (워킹트리를 되돌린다)
    python3 tools/verify_builders.py --write   # 낡았으면 새로 만든 것을 남긴다
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 실행 순서가 결과를 바꾼다 — manifest 를 link-index 가 읽고, 그 둘을 status 가 읽는다.
BUILDERS = (
    'tools/build_math_manifest.py',
    'tools/build_link_index.py',
    'tools/build_math_status.py',
)
OUTPUTS = (
    'math/manifest.json',
    'link-index.json',
    'math/ROADMAP.md',
)


def snapshot():
    return {p: (ROOT / p).read_bytes() for p in OUTPUTS if (ROOT / p).exists()}


def restore(snap):
    for p, data in snap.items():
        if (ROOT / p).read_bytes() != data:
            (ROOT / p).write_bytes(data)


# `generated` 는 노트가 아니라 HEAD 의 커밋 날짜에서 온다 — 비교에서 뺀다(위 머리말).
GENERATED = re.compile(rb'^(\s*"generated":\s*)"[^"]*"', re.M)


def normalize(data: bytes) -> bytes:
    return GENERATED.sub(rb'\1"<git>"', data)


def diffs(old: bytes, new: bytes, limit: int = 3) -> str:
    """달라진 줄 몇 개 — 첫 줄만 보이면 정작 중요한 차이를 가린다.
    (실제로 그랬다: `generated` 한 줄이 앞에 있어 자수 2547 을 못 보여 줬다.)"""
    a = old.decode('utf-8', 'replace').splitlines()
    b = new.decode('utf-8', 'replace').splitlines()
    out, n = [], 0
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else '(없음)'
        y = b[i] if i < len(b) else '(없음)'
        if x == y:
            continue
        n += 1
        if len(out) < limit:
            out.append(f'{i + 1}행  낡음: {x.strip()[:76]}\n         새로: {y.strip()[:76]}')
    if not out:
        return '(줄 단위로는 같은데 바이트가 다르다 — 줄끝이나 마지막 개행을 볼 것)'
    if n > len(out):
        out.append(f'… 그 밖에 {n - len(out)}줄 더')
    return '\n'.join(out)


def main(argv):
    write = '--write' in argv[1:]
    unknown = [a for a in argv[1:] if a != '--write']
    if unknown:
        print(f'모르는 인자: {" ".join(unknown)}\n{__doc__.splitlines()[-2].strip()}')
        return 2

    before = snapshot()
    missing = [p for p in OUTPUTS if p not in before]
    if missing:
        print('FAIL — 산출물이 없다: ' + ', '.join(missing))
        return 1

    for b in BUILDERS:
        r = subprocess.run([sys.executable, b], cwd=str(ROOT),
                           capture_output=True, text=True)
        if r.returncode != 0:
            restore(before)
            print(f'FAIL — 빌더가 죽었다: {b} (exit {r.returncode})')
            print((r.stderr or r.stdout).strip()[:1500])
            return 1

    after = snapshot()
    stale = [p for p in OUTPUTS if normalize(before[p]) != normalize(after[p])]
    clock = [p for p in OUTPUTS if p not in stale and before[p] != after[p]]

    if not stale:
        print(f'OK — 산출물 {len(OUTPUTS)}개가 지금 소스의 고정점이다.')
        for p in clock:
            print(f'   · {p} 의 `generated` 만 HEAD 날짜와 다르다 — 다음 빌더 실행 때 따라온다.')
        if clock and write:
            return 0
        if clock:
            restore(before)
        return 0

    if not write:
        restore(before)
    print(f'FAIL — 산출물 {len(stale)}개가 소스보다 낡았다. 빌더를 돌리고 함께 커밋할 것.')
    for p in stale:
        print(f'  ── {p}')
        print('     ' + diffs(before[p], after[p]).replace('\n', '\n     '))
    print('\n  고치기: ' + ' && '.join(f'python3 {b}' for b in BUILDERS))
    print('  (지금 워킹트리는 ' + ('새로 만든 것으로 바꿔 뒀다 — 그대로 커밋하면 된다.'
                                if write else '건드리지 않았다. --write 를 주면 새로 만든 것을 남긴다.') + ')')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
