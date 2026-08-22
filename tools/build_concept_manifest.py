#!/usr/bin/env python3
"""concept/notes/*.md → concept/manifest.json

■ 왜 ingest_concept.py 를 대체했나 (2026-08-22)
예전에는 구글드라이브의 '학습자료' 폴더가 정본이었고, 반입 스크립트가 프론트매터를
떼어 내며 서가로 옮겼다. 그래서 **리포에는 프론트매터가 남지 않았고**, manifest 를
만들려면 반드시 그 폴더가 붙은 로컬 PC 여야 했다. 클라우드 루틴이 이해편을 써도
갤러리에 못 올리는 이유가 이것이었다.

지금은 `concept/notes/*.md` 가 프론트매터를 그대로 갖는다. 정본이 리포이므로
클라우드·러너 어디서든 manifest 를 만들 수 있다. 옵시디언 볼트는 사본이며
`sync_obsidian.py` 가 **없을 때만** 내려보낸다(볼트에서 단 링크가 덮이지 않는다).

그림은 러너가 그린다(concept-sheet-render.yml). 여기서는 파일이 있는지만 본다.

사용: python tools/build_concept_manifest.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "concept" / "notes"
ASSETS = ROOT / "concept" / "assets"
OUT = ROOT / "concept" / "manifest.json"


def parse_fm(text: str):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    out = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([가-힣A-Za-z_]+):\s*(.*)$", line)
        if not km:
            continue
        k, v = km.group(1), km.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
        else:
            v = v.strip("\"'")
        out[k] = v
    return out, m.group(2)


def clean_vault_markup(body: str) -> str:
    """옵시디언 전용 마크업을 갤러리용으로 다듬는다.

    %% ... %% 는 옵시디언에서 주석이라 미리보기에 안 보이지만 갤러리에서는 글자로
    노출된다. 다만 LINKS 블록의 '내용' 은 버리지 않는다 — 이룬 서재는 link-index 로
    위키링크가 실제로 이동하므로 '관련 개념' 절로 승격시키는 편이 쓸모 있다.
    """
    m = re.search(r"%%\s*LINKS:START\s*%%(.*?)%%\s*LINKS:END\s*%%", body, re.S)
    if m:
        inner = m.group(1).strip()
        repl = (chr(10) + "## 관련 개념" + chr(10) * 2 + inner + chr(10)) if inner else ""
        body = body[:m.start()] + repl + body[m.end():]
    body = re.sub(r"%%.*?%%", "", body, flags=re.S)
    return re.sub(r"\n{3,}", chr(10) * 2, body)


def main() -> int:
    if not NOTES.is_dir():
        print("concept/notes/ 가 없다.", file=sys.stderr)
        return 1

    items, warn = [], []
    for p in sorted(NOTES.glob("*.md")):
        slug = p.stem
        fm, body = parse_fm(p.read_text(encoding="utf-8"))
        if not fm:
            warn.append((slug, "프론트매터 없음 — manifest 값이 비게 된다"))
        body = clean_vault_markup(body)
        pic = (slug + ".png") if (ASSETS / (slug + ".png")).exists() else None
        if not pic:
            warn.append((slug, "개념 한 장 그림이 없다 — concept-sheet-render 를 돌릴 것"))
        items.append({
            "slug": slug,
            "title": fm.get("주제", slug),
            "date": fm.get("날짜", ""),
            "depth": fm.get("깊이", ""),
            "level": fm.get("대상수준", ""),
            "tags": fm.get("태그") or [],
            "cardnews": fm.get("카드뉴스", ""),
            "chars": len(re.sub(r"\s+", "", body)),
            "pic": pic,
            "path": "concept/notes/%s.md" % slug,
        })

    items.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    M.dump_json(OUT, {"count": len(items), "notes": items})

    print("[OK] concept/ %d편 · 개념한장 %d장"
          % (len(items), sum(1 for i in items if i["pic"])))
    for slug, why in warn:
        print("  주의 %s — %s" % (slug, why), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
