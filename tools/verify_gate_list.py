#!/usr/bin/env python3
"""CLAUDE.md 가 적어 둔 게이트 목록이 gates.yml 이 실제로 돌리는 것과 같은가.

■ 왜 있나 (2026-09-22)
이 줄은 **두 번 어긋났다.**
  · 2026-09-21 — 「일곱」이라 적힌 채 `reports_meta`(#248)·`roadmap`(#270) 둘이 빠져 있었다.
  · 2026-09-22 — 「아홉」으로 고친 자리에 `manifest_paths`(#294) 가 늘었다.
CLAUDE.md 가 스스로 **「수를 세지 말고 이름을 맞댈 것」** 이라고 적어 두고도 어긋났다 —
사람이 맞대야 하는 한 계속 어긋난다. 「재발 방지는 문서가 아니라 게이트에 적는다」
(LESSONS 2026-09-02)를 이 줄 자신에게 적용한다.

■ 무엇을 재나
gates.yml 의 `run:` 에 적힌 `tools/verify_*.py` 이름과, CLAUDE.md 의 gates.yml 줄에
백틱으로 적힌 이름을 **집합으로** 맞댄다. 순서·개수는 안 본다(개수는 이미 지웠다).

이 검사기 자신도 그 목록에 있어야 한다 — 그래야 제 등재를 제가 강제한다.

사용: python3 tools/verify_gate_list.py       어긋나면 exit 1.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    wf = (ROOT / ".github/workflows/gates.yml").read_text(encoding="utf-8")
    # `run: python tools/verify_x.py` — 주석 줄은 세지 않는다(머리말이 이름을 언급한다).
    runs = set()
    for line in wf.splitlines():
        if re.match(r"\s*run:", line) or re.match(r"\s*python ", line):
            runs |= {m for m in re.findall(r"tools/verify_(\w+)\.py", line)}

    doc = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    # ⚠ `workflows/gates.yml` 을 언급하는 줄은 하나가 아니다 — 「명령」절의 verify_figures
    #   주석도 CI 를 기준 환경으로 가리킨다. 목록을 든 줄은 「구조」절의 항목뿐이므로
    #   그 형태(`- \`.github/workflows/gates.yml\``)로 집는다.
    row = [ln for ln in doc.splitlines()
           if ln.lstrip().startswith("- `.github/workflows/gates.yml`")]
    if len(row) != 1:
        print("❌ CLAUDE.md 에서 gates.yml 항목 줄을 %d개 찾았다 (정확히 1개여야 한다)" % len(row))
        sys.exit(1)
    # 그 줄에서 백틱 토큰만 거둔다. 그 뒤 괄호의 이력 서술에도 이름이 나오므로
    # 「검증기를 …돌린다 — a·b·c.」 의 목록 구간만 본다.
    m = re.search(r"돌린다 — (.+?)\. \*\*수를 세지", row[0])
    if not m:
        print("❌ CLAUDE.md gates.yml 줄에서 목록 구간을 못 찾았다 "
              "(「돌린다 — …. **수를 세지」 형태를 기대한다)")
        sys.exit(1)
    listed = set(re.findall(r"`(\w+)`", m.group(1)))

    missing = runs - listed          # 돌리는데 안 적힌 것 — 2026-09-21·22 의 실패 양식
    extra   = listed - runs          # 적혔는데 안 도는 것 — 유령 게이트
    if missing or extra:
        print("❌ CLAUDE.md 의 게이트 목록이 gates.yml 과 어긋난다")
        for n in sorted(missing):
            print("     · gates.yml 이 돌리는데 CLAUDE.md 에 없다: %s" % n)
        for n in sorted(extra):
            print("     · CLAUDE.md 에 적혔는데 gates.yml 이 안 돌린다: %s" % n)
        sys.exit(1)

    print("✅ 게이트 목록 일치 — %s" % " · ".join(sorted(runs)))
    sys.exit(0)


if __name__ == "__main__":
    main()
