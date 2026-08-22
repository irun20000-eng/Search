#!/usr/bin/env python3
"""카드뉴스 학습자료(이해편) → 이룬 서재 concept/ 개념노트 서가.

원천은 볼트에서 내보낸 학습자료 폴더다. 편당 두 파일을 쌍으로 갖는다.
  <YYYYMMDD>_<제목> — 이해편.md   본문 (reports/ 와 사실상 같은 frontmatter)
  개념한장_<개념>.png              한 장 요약 그림

산출:
  concept/notes/<slug>.md    본문 (frontmatter 제거, 본문만)
  concept/assets/<slug>.png  개념한장
  concept/manifest.json      카드 메타

위키링크는 벗기지 않는다. 이룬 서재는 link-index.json 이 서가 경계를 넘게 해 주므로
[[최적 정지]] 가 다른 글로 실제 이동한다 — 볼트와 웹의 동작이 같아진다.

사용: python tools/ingest_concept.py <학습자료 폴더>
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_NOTES = ROOT / "concept" / "notes"
OUT_ASSETS = ROOT / "concept" / "assets"
MANIFEST = ROOT / "concept" / "manifest.json"


def parse_frontmatter(text: str):
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
            v = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        else:
            v = v.strip('"\'')
        out[k] = v
    return out, m.group(2)


def slugify(title: str) -> str:
    """제목 → 파일명 안전한 슬러그. 영문 병기가 있으면 그쪽을 쓴다."""
    en = re.search(r"\(([A-Za-z][A-Za-z' \-]+)\)", title)
    base = en.group(1) if en else title
    base = unicodedata.normalize("NFKC", base).strip().lower()
    base = base.replace("'", "").replace("’", "")   # simpson's → simpsons
    base = re.sub(r"[^a-z0-9가-힣]+", "-", base).strip("-")
    return base or "note"


def main() -> int:
    if len(sys.argv) < 2:
        print("사용: python tools/ingest_concept.py <학습자료 폴더>", file=sys.stderr)
        return 1
    src = Path(sys.argv[1]).resolve()
    mds = sorted(p for p in src.glob("*.md") if not p.name.startswith("_"))
    if not mds:
        print("[ERR] 이해편 .md 를 찾지 못했다: %s" % src, file=sys.stderr)
        return 1

    OUT_NOTES.mkdir(parents=True, exist_ok=True)
    OUT_ASSETS.mkdir(parents=True, exist_ok=True)

    pngs = {p.stem: p for p in src.glob("*.png")}
    items, skipped = [], []

    for md in mds:
        fm, body = parse_frontmatter(md.read_text(encoding="utf-8"))
        title = fm.get("주제") or md.stem
        slug = slugify(title)

        # 개념한장 짝 찾기 — '개념한장_<개념>' 에서 개념 부분이 제목에 들어 있는 것
        pic = None
        for stem, p in pngs.items():
            key = stem.replace("개념한장_", "")
            if key and key in title.replace(" ", ""):
                pic = p
                break
        if pic:
            shutil.copy2(pic, OUT_ASSETS / (slug + ".png"))

        (OUT_NOTES / (slug + ".md")).write_text(body.strip() + "\n", encoding="utf-8")

        items.append({
            "slug": slug,
            "title": title,
            "date": fm.get("날짜", ""),
            "depth": fm.get("깊이", ""),
            "level": fm.get("대상수준", ""),
            "tags": fm.get("태그") or [],
            "cardnews": fm.get("카드뉴스", ""),
            "chars": len(re.sub(r"\s+", "", body)),
            "pic": (slug + ".png") if pic else None,
            "path": "concept/notes/%s.md" % slug,
        })
        if not pic:
            skipped.append((slug, "개념한장 png 짝을 못 찾음"))

    items.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    MANIFEST.write_text(
        json.dumps({"count": len(items), "notes": items}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    print("[OK] concept/ %d편 · 개념한장 %d장"
          % (len(items), sum(1 for i in items if i["pic"])))
    for s, why in skipped:
        print("  주의 %s — %s" % (s, why), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
