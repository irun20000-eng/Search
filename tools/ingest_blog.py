#!/usr/bin/env python3
"""Blog 리포(irun20000-eng/Blog) published/ → 이룬 서재 blog/ 갤러리.

원천은 Blog 리포의 published/<연도>/<slug>/ 이며 편당 다음을 갖는다:
  obsidian.md  프론트매터(제목·날짜·필라·태그·발행 URL 등) — 메타데이터 정본
  post.html    <article class="post"> 안에 본문. 앞머리 <section class="thumb">는
               자체 브랜드 썸네일이라 이룬 서재에서는 걷어낸다.
  images/      본문이 <img> 로 참조하는 파일

산출:
  blog/notes/<slug>.md      본문 HTML(마크다운 파일 안에 그대로 둔다 — marked 가 통과시킨다)
  blog/assets/<slug>/       이미지 사본, 본문의 src 를 여기로 다시 씀
  blog/manifest.json        카드 메타

사용: python tools/ingest_blog.py <Blog 리포 경로>
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_NOTES = ROOT / "blog" / "notes"
OUT_ASSETS = ROOT / "blog" / "assets"
MANIFEST = ROOT / "blog" / "manifest.json"

PILLAR_KO = {"math": "수학 개념", "ai": "AI 활용", "admissions": "입시·진학"}

# 운영 지표(views/likes)는 시간에 따라 변하는 값이라 카드에 넣지 않는다 —
# 재인제스트마다 diff 가 생겨 빌드가 결정적이지 않게 된다.
# published_url·naver_url 은 원천 20편 모두 값이 비어 있어 필드 자체를 두지 않는다.

def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not km:
            continue
        k, v = km.group(1), km.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        else:
            v = v.strip('"\'')
        out[k] = v
    return out


def extract_body(html: str) -> str | None:
    art = re.search(r'<article class="post">(.*?)</article>', html, re.S)
    if not art:
        return None
    body = art.group(1)
    # 자체 브랜드 썸네일 제거 — 이룬 서재는 자기 카드 디자인을 쓴다
    body = re.sub(r'<section class="thumb".*?</section>', "", body, flags=re.S)
    return body.strip()


def main() -> int:
    if len(sys.argv) < 2:
        print("사용: python tools/ingest_blog.py <Blog 리포 경로>", file=sys.stderr)
        return 1
    src = Path(sys.argv[1]).resolve()
    dirs = sorted(p for p in (src / "published").glob("*/*") if p.is_dir())
    if not dirs:
        print("[ERR] published/<연도>/<slug>/ 를 찾지 못했다: %s" % src, file=sys.stderr)
        return 1

    OUT_NOTES.mkdir(parents=True, exist_ok=True)
    OUT_ASSETS.mkdir(parents=True, exist_ok=True)

    items, skipped = [], []
    for d in dirs:
        slug = d.name
        fm_path, html_path = d / "obsidian.md", d / "post.html"
        if not (fm_path.exists() and html_path.exists()):
            skipped.append((slug, "obsidian.md 또는 post.html 없음"))
            continue
        fm = parse_frontmatter(fm_path.read_text(encoding="utf-8"))
        body = extract_body(html_path.read_text(encoding="utf-8"))
        if body is None:
            skipped.append((slug, "<article class=\"post\"> 없음"))
            continue

        # 이미지 반입 + src 재작성
        img_dir = d / "images"
        if img_dir.is_dir():
            dst = OUT_ASSETS / slug
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(img_dir, dst)
            body = re.sub(r'(<img[^>]+src=")(?:\./)?images/', r"\1assets/%s/" % slug, body)

        (OUT_NOTES / (slug + ".md")).write_text(body + "\n", encoding="utf-8")

        pillar = fm.get("pillar", "")
        # 슬러그는 폴더명 하나로 통일한다. 프론트매터의 slug 는 20편 중 7편이
        # 폴더명과 달라서(예: 폴더 08-hs2-explog-trig / 프론트매터 2026-08-hs2-explog-trig)
        # 그쪽을 카드에 쓰면 notes/<slug>.md 를 못 찾아 글이 안 열린다.
        items.append({
            "slug": slug,
            "title": fm.get("title", slug),
            "date": fm.get("date", ""),
            "pillar": pillar,
            "pillar_ko": PILLAR_KO.get(pillar, pillar),
            "series": fm.get("series", ""),
            "tags": fm.get("keywords") or fm.get("tags") or [],
            "chars": len(re.sub(r"<[^>]+>", "", body)),
            "path": "blog/notes/%s.md" % slug,
        })

    items.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    pillars = []
    for p in ("math", "ai", "admissions"):
        n = sum(1 for i in items if i["pillar"] == p)
        if n:
            pillars.append({"key": p, "label": PILLAR_KO[p]})

    MANIFEST.write_text(
        json.dumps({"count": len(items), "pillars": pillars, "posts": items},
                   ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    print("[OK] blog/ %d편 · 이미지 %d슬러그" % (len(items), len(list(OUT_ASSETS.glob('*')))))
    for s, why in skipped:
        print("  건너뜀 %s — %s" % (s, why), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
