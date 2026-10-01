#!/usr/bin/env python3
"""
서가 게이트를 **로컬에서** 그대로 돌린다 — 목록은 `.github/workflows/gates.yml` 에서 읽는다.

■ 왜 있나 (2026-10-01)
카드뉴스 루틴의 마지막 커밋은 렌더 봇의 것이다. 그 커밋은 `[skip ci]` 이거나(카드뉴스)
봇 푸시라 PR 게이트가 `action_required` 로 멈춘다(개념 한 장). 그래서 컷·manifest 가 다
붙은 **최종 head 에는 게이트가 저절로 돌지 않는다.** 루틴이 `workflow_dispatch` 로 돌리면
되겠다 싶었지만 루틴이 쓰는 GitHub 통합은 dispatch 에 **403**(Resource not accessible by
integration)을 받는다 — 실제로 시험해 확인했다.

그래서 루틴은 최종 head 를 pull 한 뒤 이것을 돌린다. 게이트 목록을 여기 손으로 적지 않고
gates.yml 에서 읽는 이유는 이 리포가 게이트 목록을 두 번 어긋나게 적은 적이 있어서다
(CLAUDE.md 「수를 세지 말고 이름을 맞댈 것」). gates.yml 에 스텝이 늘면 여기도 저절로 는다.

■ 도해(verify_figures)만 다르게 다룬다
한글 자폭을 깔린 폰트로 재므로 **러너가 정본**이다(gates.yml 머리말). 로컬 결과는 참고로만
찍고, 이 브랜치가 `math/` 를 바꾸지 않았으면 판정에서 뺀다 — 그때 정본은 main 의 결과다.
`math/` 를 바꿨는데 로컬에서 실패하면 실패로 센다(러너 기준으로 다시 볼 것).

■ 이것이 보장하지 않는 것
머지 뒤 main push 의 서가 게이트(러너)가 최종 확인이다. 루틴은 머지 SHA 의 그 run 이
success 인지까지 본다(routines/cardnews-weekly.md §5.5).

사용:
    python3 tools/run_gates_local.py              # 전부
    python3 tools/run_gates_local.py --base origin/main   # math/ 변경 판정의 기준(기본값)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GATES = ROOT / ".github" / "workflows" / "gates.yml"
RUNNER_ONLY = {"python tools/verify_figures.py"}   # 러너가 정본인 계측


def gate_steps():
    d = yaml.safe_load(GATES.read_text(encoding="utf-8"))
    out = []
    for st in d["jobs"]["gates"]["steps"]:
        cmd = (st.get("run") or "").strip()
        # 한 줄짜리 검사 스텝만 — 설치·요약 스텝은 여러 줄이라 걸러진다
        if "\n" in cmd or not cmd.startswith(("python tools/", "bash tools/")):
            continue
        out.append((st.get("name", cmd), cmd))
    return out


def math_changed(base):
    r = subprocess.run(["git", "diff", "--quiet", base, "--", "math/"], cwd=ROOT)
    return r.returncode != 0


def main():
    base = "origin/main"
    if "--base" in sys.argv:
        base = sys.argv[sys.argv.index("--base") + 1]

    steps = gate_steps()
    if not steps:
        print("gates.yml 에서 검사 스텝을 하나도 못 읽었다 — 형식이 바뀌었는지 볼 것")
        return 2
    touched_math = math_changed(base)

    print("서가 게이트 · 로컬 — gates.yml 에서 %d개 (기준 %s · math/ 변경 %s)"
          % (len(steps), base, "있음" if touched_math else "없음"))
    failed, advisory = [], []
    for name, cmd in steps:
        r = subprocess.run(cmd, shell=True, cwd=ROOT,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        ok = r.returncode == 0
        runner_only = cmd in RUNNER_ONLY
        if ok:
            mark = "OK"
        elif runner_only and not touched_math:
            mark = "참고"          # 로컬 폰트로 잰 값 — math/ 를 안 건드렸으니 판정 밖
            advisory.append(name)
        else:
            mark = "X"
            failed.append((name, r.stdout))
        print("  %-4s %s" % (mark, name))

    for name, log in failed:
        print("\n── %s ── 끝 15줄" % name)
        print("\n".join(log.rstrip().splitlines()[-15:]))
    if advisory:
        print("\n참고: %s — 러너가 정본이고 이 브랜치는 math/ 를 바꾸지 않았다."
              % ", ".join(advisory))
    print()
    if failed:
        print("[X] %d/%d 실패 — 머지 금지" % (len(failed), len(steps)))
        return 1
    print("[OK] %d개 통과%s" % (len(steps) - len(advisory),
                               " · 참고 %d" % len(advisory) if advisory else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
