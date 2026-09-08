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

왜 임시 트리에 안 돌리나 — **커밋 안 된 워킹트리를 못 보기 때문이다.**
    `git worktree`·`git clone` 이 주는 것은 HEAD 다. 그런데 이 게이트가 재야 하는 것은
    **커밋 직전에 손에 든 트리**다 — 방금 고친 노트와 아직 안 돌린 빌더의 관계.
    임시 트리로는 그 자리를 아예 못 본다. (부수적으로 `.git` 없는 복사본에서는
    `build_math_manifest.py` 의 `generated` 가 `git log -1` 을 못 불러 빈 문자열이 되어
    없는 차이까지 생긴다 — 다만 `.git` 을 함께 복사하면 그건 사라지므로 결정적 이유는 아니다.)
    그래서 **제자리에서 돌리고 되돌려 놓는다**(`--write` 면 새것을 남긴다).

무엇을 보나.
    `python3 tools/build_link_index.py` 는 끝에 `build_backlog.build()` 를 **이어서 부른다**
    (그 파일이 「따로 돌리게 두면 반드시 잊는다」고 적어 둔 결정이다). 그래서 `backlog.json`
    도 이 명령의 산출물이고 여기서 함께 잰다 — 빼 두면 검사기가 그 파일을 **말없이 덮어쓰고**
    낡음도 영영 안 잡힌다(첫 판이 그랬다).
    ⚠ **빌더가 늘면 `BUILDERS` 와 `OUTPUTS` 를 함께 늘려야 한다** — 목록에 없는 산출물은 못 본다.
    ⚠ **되돌리기도 `OUTPUTS` 안에서만 참이다.** 빌더가 목록 밖 파일에 한 일은 그대로 남는다
      (지금 빌더 3종은 목록 밖을 안 건드리는 것을 확인했다).
    ⚠ `build_link_index.py` 는 `build_backlog` 의 예외를 **삼키고 rc 0 을 돌려준다.** 그러면
      `backlog.json` 이 갱신되지 않아 「안 바뀌었다 = 고정점」으로 읽힌다 — 그래서 그 실패 문구를
      stdout 에서 찾아 FAIL 로 올린다(`BACKLOG_FAIL`).

시계가 섞인 자리 **둘**만 비교에서 뺀다 — 나머지는 절대 빼지 않는다.
    ① `math/manifest.json` 의 `generated` — `git log -1 --format=%cs` 가 준 **HEAD 의 커밋 날짜**다.
       `%cs` 는 커밋의 타임존으로 찍히므로 같은 날 작업도 로컬(+0900)과 클라우드(+0000)에서 갈린다.
       이 값을 읽는 화면은 없다(`grep -n '"generated"' math/index.html` → 0건).
    ② `backlog.json` 의 `generated` — `build_backlog.py` 가 `datetime.date.today()` 로 찍는 **벽시계**다.
       빼지 않으면 **소스를 한 글자도 안 고쳐도 날짜가 바뀌는 순간부터 매일 첫 실행이 FAIL 한다.**
       매일 거짓 FAIL 하는 게이트는 곧 무시되므로 그 자체가 결함이다. 값의 뜻은 `backlog.html` 이
       화면에 쓰므로(「<날짜> 기준」) **빌더 쪽은 건드리지 않고 검사기에서만 뺀다.**

    ⚠ **다른 산출물의 `generated` 는 절대 빼지 않는다.** `link-index.json` 의 것은
    `reports/manifest.json` 에서 온 **소스 값**이라(`build_link_index.py` 가 복사한다), 빼면 진짜 낡음을 숨긴다.
    (LESSONS 2026-08-31 「빌더를 두 번 돌려 같지 않으면 그 자리에 시계가 섞여 있다」—
     여기가 그 시계이고, 이 두 자리만 의도된 것이다. **산출물을 늘릴 때 그 빌더가 시계를 찍는지
     반드시 읽어 볼 것** — `backlog.json` 을 목록에 넣으면서 `build_backlog.py` 를 안 읽어 이 함정에 빠졌다.)

쓰기.
    python3 tools/verify_builders.py           # 확인만 (워킹트리를 되돌린다)
    python3 tools/verify_builders.py --write   # 낡았으면 새로 만든 것을 남긴다
    ※ 읽기 전용 검사가 아니다 — 빌더를 **실제로 돌린다**. 되돌리기는 그 뒤의 일이다.
    ※ `--write` 는 낡은 파일을 **통째로** 남기므로 그 파일의 시계 줄도 새 값이 된다
      (확인 모드에서만 시계를 되돌린다). 빌더가 방금 찍은 값이니 그대로 커밋하면 된다.
"""
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 실행 순서가 결과를 바꾼다 — manifest 를 link-index 가 읽고, 그 둘을 status 가 읽는다.
BUILDERS = (
    'tools/build_math_manifest.py',
    'tools/build_link_index.py',      # 끝에서 build_backlog 를 이어 부른다
    'tools/build_math_status.py',
)
OUTPUTS = (
    'math/manifest.json',
    'link-index.json',
    'backlog.json',
    'math/ROADMAP.md',
)

# 시계가 섞인 자리 — 두 곳뿐이고 이유가 서로 다르다(머리말 참조).
#   math/manifest.json → git log -1 (커밋 타임존)   backlog.json → date.today() (벽시계)
_GEN = re.compile(rb'^(\s*"generated":\s*)"[^"]*"', re.M)
CLOCK = {'math/manifest.json': _GEN, 'backlog.json': _GEN}

# build_link_index.py 가 backlog 실패를 삼키므로 이 문구를 직접 본다.
BACKLOG_FAIL = '! 백로그 갱신 실패'

USAGE = ('쓰기: python3 tools/verify_builders.py [--write]\n'
         '      --write 를 주면 낡았을 때 새로 만든 것을 남긴다(기본은 되돌린다).')


def normalize(path: str, data: bytes) -> bytes:
    pat = CLOCK.get(path)
    return pat.sub(rb'\1"<clock>"', data) if pat else data


def snapshot():
    return {p: (ROOT / p).read_bytes() for p in OUTPUTS if (ROOT / p).is_file()}


def restore(snap, only=None):
    """되돌린다. 쓰다 죽어도 반쪽 파일이 남지 않게 임시파일 → os.replace 로."""
    for p, data in snap.items():
        if only is not None and p not in only:
            continue
        f = ROOT / p
        if f.is_file() and f.read_bytes() == data:
            continue
        tmp = f.with_suffix(f.suffix + '.vbtmp')
        tmp.write_bytes(data)
        os.replace(tmp, f)


def diffs(old: bytes, new: bytes, limit: int = 3) -> str:
    """달라진 줄 몇 개 — 첫 줄만 보이면 정작 중요한 차이를 가린다.
    (첫 판이 그랬다: `generated` 한 줄이 앞에 있어 자수 2547 을 못 보여 줬다.
     그래서 **판정에서 뺀 자리는 여기서도 빼고** 넘긴다.)"""
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
    args = argv[1:]
    if {'-h', '--help'} & set(args):
        print(__doc__.strip())
        return 0
    write = '--write' in args
    unknown = [a for a in args if a != '--write']
    if unknown:
        print(f'모르는 인자: {" ".join(unknown)}\n{USAGE}')
        return 2

    before = snapshot()
    missing = [p for p in OUTPUTS if p not in before]
    if missing:
        print('FAIL — 산출물이 없다: ' + ', '.join(missing))
        return 1

    try:
        for b in BUILDERS:
            r = subprocess.run([sys.executable, b], cwd=str(ROOT),
                               capture_output=True, text=True)
            if r.returncode != 0:
                restore(before)
                print(f'FAIL — 빌더가 죽었다: {b} (exit {r.returncode})')
                print((r.stderr or r.stdout).strip()[:1500])
                return 1
            # rc 0 이어도 삼켜진 실패가 있다 — 그러면 산출물이 안 바뀌어 「고정점」으로 읽힌다.
            if BACKLOG_FAIL in (r.stdout or ''):
                restore(before)
                print(f'FAIL — 빌더는 살았는데 백로그 갱신이 실패했다: {b}')
                print('  ' + next(l for l in r.stdout.splitlines() if BACKLOG_FAIL in l).strip()[:300])
                print('  (rc 0 으로 삼켜지므로 여기서 직접 본다 — 이대로 두면 backlog.json 낡음이 안 잡힌다.)')
                return 1
    except KeyboardInterrupt:                 # 트리를 그대로 두고 나가지 않는다
        restore(before)
        print('\n중단됨 — 워킹트리는 되돌렸다.')
        return 130
    except BaseException:
        restore(before)
        raise

    after = snapshot()
    gone = [p for p in OUTPUTS if p not in after]
    if gone:
        restore(before)
        print('FAIL — 빌더가 산출물을 지웠다: ' + ', '.join(gone))
        return 1

    stale, clock = [], []
    for p in OUTPUTS:
        if before[p] == after[p]:
            continue
        (stale if normalize(p, before[p]) != normalize(p, after[p]) else clock).append(p)

    restore(before, only=clock)               # 시계는 어느 모드에서도 되돌린다

    if not stale:
        print(f'OK — 산출물 {len(OUTPUTS)}개가 지금 소스의 고정점이다.')
        return 0

    if not write:
        restore(before, only=stale)
    print(f'FAIL — 산출물 {len(stale)}개가 소스보다 낡았다. 빌더를 돌리고 함께 커밋할 것.')
    for p in stale:
        print(f'  ── {p}')
        print('     ' + diffs(normalize(p, before[p]),
                              normalize(p, after[p])).replace('\n', '\n     '))
    print('\n  고치기: ' + ' && '.join(f'python3 {b}' for b in BUILDERS))
    print('  (지금 워킹트리는 ' + ('새로 만든 것으로 바꿔 뒀다 — 그대로 커밋하면 된다.'
                                if write else '건드리지 않았다. --write 를 주면 새것을 남긴다.') + ')')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
