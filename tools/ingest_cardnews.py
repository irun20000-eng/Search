#!/usr/bin/env python3
"""카드뉴스 원천 → 이룬 서재 cardnews/ 갤러리.

원천은 두 곳이다.
  <src>/data/galleries/cardnews.yaml        시리즈 토큰 + 편 메타(제목·앵글·레이아웃·캡션·컷 목록)
  <src>/gallery_src/cardnews/images/*.webp  620×775 컷 이미지

산출:
  cardnews/manifest.json     카드 메타 — 빌드 산출물, 직접 편집 금지
  cardnews/assets/<folder>/  편별 컷 이미지 사본

학습자료(개념노트)가 있는 편은 manifest 의 study 에 슬러그가 들어가고,
갤러리가 그 편 카드에 '이해편 읽기' 를 붙인다. 연결은 concept/manifest.json 이
가진 slug 와 맞춘다.

사용: python tools/ingest_cardnews.py <카드뉴스 원천 경로>
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERR] pyyaml 이 필요하다: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
OUT_ASSETS = ROOT / "cardnews" / "assets"
MANIFEST = ROOT / "cardnews" / "manifest.json"

# 시리즈 키가 yaml 에서는 영문(parent/work/number/discovery)이다.
SERIES_ORDER = ["parent", "work", "number", "discovery"]


def main() -> int:
    if len(sys.argv) < 2:
        print("사용: python tools/ingest_cardnews.py <카드뉴스 원천 경로>", file=sys.stderr)
        return 1
    src = Path(sys.argv[1]).resolve()
    # 메타 정본은 레포 안의 cardnews/cardnews.yaml 이다. 외부 원천에서는 이미지만 가져온다.
    # (이관 초기에는 Main 의 yaml 이 정본이었으나, 이제 이쪽이 정본이다.)
    yml = ROOT / "cardnews" / "cardnews.yaml"
    if not yml.exists():
        yml = src / "data" / "galleries" / "cardnews.yaml"
    imgdir = src / "gallery_src" / "cardnews" / "images"
    if not yml.exists():
        print("[ERR] cardnews.yaml 없음: %s" % yml, file=sys.stderr)
        return 1
    if not imgdir.is_dir():
        print("[ERR] 이미지 폴더 없음: %s" % imgdir, file=sys.stderr)
        return 1

    data = yaml.safe_load(yml.read_text(encoding="utf-8"))
    series_raw = data.get("series", [])
    episodes = data.get("episodes", [])

    series = {}
    for s in series_raw:
        series[s["id"]] = {"key": s["id"], "label": s["name"],
                           "desc": s.get("desc", ""),
                           "c1": (s.get("colors") or {}).get("c1", "#888888")}

    # 개념노트 슬러그 조회 — 있으면 편 카드에서 이해편으로 보낸다
    concept = {}
    cman = ROOT / "concept" / "manifest.json"
    if cman.exists():
        for n in json.loads(cman.read_text(encoding="utf-8")).get("notes", []):
            for k in (n.get("cardnews_folder"), n.get("slug")):
                if k:
                    concept[k] = n["slug"]

    OUT_ASSETS.mkdir(parents=True, exist_ok=True)
    items, missing = [], []

    for e in episodes:
        folder = e["folder"]
        imgs = e.get("images") or []
        gone = [i for i in imgs if not (imgdir / i).exists()]
        if gone:
            missing.append((folder, gone))
            continue

        dst = OUT_ASSETS / folder
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        for i in imgs:
            shutil.copy2(imgdir / i, dst / i)

        items.append({
            "folder": folder,
            "series": e.get("series", ""),
            "title": e.get("title", folder),
            "angle": e.get("angle", ""),
            "layout": e.get("layout", ""),
            "date": str(e.get("date", "")),
            "caption": e.get("caption", ""),
            "images": imgs,
            "study": e.get("study") or concept.get(folder) or None,
        })

    # 편 번호가 폴더명에 들어 있다(<시리즈>_<두자리>_<키워드>) → 시리즈·번호 순
    def sortkey(x):
        parts = x["folder"].split("_")
        num = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return (SERIES_ORDER.index(x["series"]) if x["series"] in SERIES_ORDER else 99, -num)

    items.sort(key=sortkey)

    used = [series[k] for k in SERIES_ORDER if k in series
            and any(i["series"] == k for i in items)]

    MANIFEST.write_text(
        json.dumps({"count": len(items), "series": used, "episodes": items},
                   ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    print("[OK] cardnews/ %d편 · 컷 %d장" % (len(items), sum(len(i["images"]) for i in items)))
    for f, g in missing:
        print("  건너뜀 %s — 이미지 %d장 없음" % (f, len(g)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
