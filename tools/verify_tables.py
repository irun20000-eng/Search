#!/usr/bin/env python3
"""서가 전체의 마크다운 표가 실제로 그려지는지 잰다.

규칙과 근거는 `tools/mdtables.py` 머리말이 정본이다. 서가마다 렌더러가 달라
규칙이 둘이므로(marked = "gfm" / 손으로 쓴 파서 = "plain") 여기서 대상별로 건다.

사용:
  python3 tools/verify_tables.py            # 전체
  python3 tools/verify_tables.py reports    # 한 서가만
  결함이 있으면 exit 1.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdtables as MT          # noqa: E402

# (서가 이름, 글롭, 규칙) — 규칙은 그 갤러리 index.html 을 실측해 정했다
TARGETS = [
    ("reports", "reports/*/report.md",   "gfm"),     # research/index.html  marked@12.0.2
    ("concept", "concept/notes/*.md",    "gfm"),     # concept/index.html   marked@12.0.2
    ("math",    "math/notes/*/note.md",  "gfm"),     # math/index.html      marked@12.0.2
    ("videos",  "videos/notes/*.md",     "plain"),   # videos/index.html    자체 파서
    ("guides",  "guides/*/guide.md",     "plain"),   # guides/index.html    자체 파서
    ("docs",    "*.md",                  "gfm"),     # 루트 계약문서(GitHub 도 GFM)
    ("docs",    "math/*.md",             "gfm"),
]


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    root = Path(__file__).resolve().parent.parent
    total_files = total_bad = 0

    for name, glob, rule in TARGETS:
        if only and name != only:
            continue
        for p in sorted(root.glob(glob)):
            total_files += 1
            bad = MT.defects(p.read_text(encoding="utf-8"), rule)
            if not bad:
                continue
            total_bad += len(bad)
            rel = p.relative_to(root)
            for ln, want, got, row in bad:
                print("[FAIL] %s:%d  (%s · %s 규칙)" % (rel, ln, name, rule))
                print("       머리행 %d칸인데 이 행은 %d칸 — %s" % (want, got, row[:70]))
                print("       → %s" % MT.advice(rule))

    print("\n훑은 파일 %d개 · 깨진 표 행 %d건" % (total_files, total_bad))
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
