#!/usr/bin/env python3
"""picks/notes/*.md → picks/manifest.json  (골라봄 서가)

골라봄은 AI(Aside)가 평일 하루 한 테마로 영상 3편 안팎을 골라 쓰는 서가다.
노트 한 편 = 하루 한 테마. 파일명은 날짜(YYYY-MM-DD.md)이고 그것이 슬러그다.
정본은 리포, 볼트는 사본(sync_obsidian.py 의 plan_picks).

막음(종료코드 1): 테마·날짜 없음 / 영상 ID 목록 비었거나 형식 틀림 /
「검증한 것 / 못 한 것」 고지 없음.

사용: python tools/build_picks_manifest.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M  # noqa: E402
from build_concept_manifest import parse_fm  # noqa: E402  같은 규칙으로 읽는다

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "picks" / "notes"
OUT = ROOT / "picks" / "manifest.json"
VID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def main() -> int:
    if not NOTES.is_dir():
        print("picks/notes/ 가 없다.", file=sys.stderr)
        return 1
    items, bad = [], []
    for p in sorted(NOTES.glob("*.md")):
        slug = p.stem
        fm, body = parse_fm(p.read_text(encoding="utf-8"))
        vids = fm.get("영상") or []
        if isinstance(vids, str):
            vids = [vids]
        for k in ("테마", "날짜"):
            if not fm.get(k):
                bad.append((slug, "프론트매터 %s 없음" % k))
        if not vids or any(not VID.match(v) for v in vids):
            bad.append((slug, "영상 ID 목록이 비었거나 형식이 틀림"))
        if "못 한 것" not in body:
            bad.append((slug, "'검증한 것 / 못 한 것' 고지가 없다"))
        items.append({
            "slug": slug,
            "title": fm.get("테마", slug),
            "sub": fm.get("부제", ""),
            "date": fm.get("날짜", ""),
            "axis": fm.get("축", ""),
            "field": fm.get("분야", ""),
            "videos": vids,
            "tags": fm.get("태그") or [],
            "chars": len(re.sub(r"\s+", "", body)),
            "path": "picks/notes/%s.md" % slug,
        })
    items.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    M.dump_json(OUT, {"count": len(items), "notes": items})
    print("[OK] picks/ %d편 · 영상 %d편" % (len(items), sum(len(i["videos"]) for i in items)))
    for slug, why in bad:
        print("  막음 %s — %s" % (slug, why), file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
