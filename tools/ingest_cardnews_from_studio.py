#!/usr/bin/env python3
"""studio 렌더 산출물 → cardnews/ 서가 반입.

ingest_cardnews.py 는 이미 만들어진 webp 묶음(Main 의 gallery_src)을 옮기는 도구다.
이 스크립트는 그 앞단 — studio/out/ 의 PNG 10장을 갤러리용 webp 로 줄여 넣고
cardnews/cardnews.yaml 의 편 항목과 맞춰 manifest 를 다시 만든다.

  studio/out/<폴더>/*.png  →  cardnews/assets/<폴더>/<prefix><NN>.webp

폴더·prefix·컷 목록은 cardnews.yaml 이 정본이다. 여기서 지어내지 않는다.
yaml 에 편 항목이 없으면 멈추고 보고한다 — 카피만 쓰고 편 항목을 빠뜨리는 실수가
가장 흔하기 때문이다.

사용: python tools/ingest_cardnews_from_studio.py <시리즈> <EPn>
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERR] pyyaml 필요: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "studio" / "out"
YAML = ROOT / "cardnews" / "cardnews.yaml"
ASSETS = ROOT / "cardnews" / "assets"

# 갤러리 표시 규격 — 원본 1080×1350 을 카드에 맞춰 줄인다
W, H, Q = 620, 775, 68


def webp(src: Path, dst: Path) -> bool:
    """cwebp 로 변환. 없으면 PIL 로 떨어진다."""
    try:
        subprocess.run(["cwebp", "-quiet", "-q", str(Q), "-resize", str(W), str(H),
                        str(src), "-o", str(dst)], check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    try:
        from PIL import Image
        im = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)
        im.save(dst, "WEBP", quality=Q)
        return True
    except Exception as e:                                   # noqa: BLE001
        print("[ERR] webp 변환 실패 %s — %s" % (src.name, e), file=sys.stderr)
        return False


def main() -> int:
    if len(sys.argv) < 3:
        print("사용: python tools/ingest_cardnews_from_studio.py <시리즈> <EPn>", file=sys.stderr)
        return 1
    series_ko, ep = sys.argv[1], sys.argv[2].upper()

    if not YAML.exists():
        print("[ERR] cardnews.yaml 이 없다: %s" % YAML, file=sys.stderr)
        return 1
    data = yaml.safe_load(YAML.read_text(encoding="utf-8")) or {}
    episodes = data.get("episodes", [])

    # EPn 의 숫자로 폴더를 찾는다 — 폴더명이 <시리즈>_<두자리>_<키워드> 규칙이다
    m = re.match(r"EP(\d+)$", ep)
    if not m:
        print("[ERR] 편 표기가 EPn 이 아니다: %s" % ep, file=sys.stderr)
        return 1
    num = int(m.group(1))
    prefix = "%s_%02d_" % (series_ko, num)
    cand = [e for e in episodes if str(e.get("folder", "")).startswith(prefix)]
    if not cand:
        print("[ERR] cardnews.yaml 에 %s%s 편 항목이 없다.\n"
              "      카피만 쓰고 편 항목을 빠뜨린 경우다 — yaml 에 먼저 추가할 것."
              % (prefix, "*"), file=sys.stderr)
        return 1
    e = cand[0]
    folder = e["folder"]
    want = e.get("images") or []
    if not want:
        print("[ERR] %s 의 images 목록이 비어 있다" % folder, file=sys.stderr)
        return 1

    srcdir = OUT / folder
    if not srcdir.is_dir():
        print("[ERR] 렌더 산출물이 없다: %s" % srcdir, file=sys.stderr)
        return 1

    # 10장을 번호 순으로 — 모아보기·영상은 제외한다
    pngs = sorted(p for p in srcdir.glob("*.png") if "모아보기" not in p.name)
    if len(pngs) != len(want):
        print("[ERR] 컷 수가 맞지 않는다: 렌더 %d장 vs yaml %d장"
              % (len(pngs), len(want)), file=sys.stderr)
        return 1

    dst = ASSETS / folder
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    ok = 0
    for src, name in zip(pngs, want):
        if webp(src, dst / name):
            ok += 1
    if ok != len(want):
        print("[ERR] 변환 실패 %d장" % (len(want) - ok), file=sys.stderr)
        return 1

    # manifest 재생성 — cardnews.yaml + 실제로 반입된 assets 를 읽는다
    rebuild_manifest(data)

    print("[OK] %s %s → cardnews/assets/%s (%d장)" % (series_ko, ep, folder, ok))
    return 0


def rebuild_manifest(data: dict) -> None:
    """assets 에 실제로 들어와 있는 편만 manifest 에 싣는다."""
    SERIES_ORDER = ["parent", "work", "number", "discovery"]
    series = {s["id"]: {"key": s["id"], "label": s["name"],
                        "desc": s.get("desc", ""),
                        "c1": (s.get("colors") or {}).get("c1", "#888888")}
              for s in data.get("series", [])}
    items = []
    for e in data.get("episodes", []):
        folder = e["folder"]
        if not (ASSETS / folder).is_dir():
            continue
        items.append({
            "folder": folder, "series": e.get("series", ""),
            "title": e.get("title", folder), "angle": e.get("angle", ""),
            "layout": e.get("layout", ""), "date": str(e.get("date", "")),
            "caption": e.get("caption", ""), "images": e.get("images") or [],
            "study": e.get("study") or None,
        })

    def sortkey(x):
        parts = x["folder"].split("_")
        n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return (SERIES_ORDER.index(x["series"]) if x["series"] in SERIES_ORDER else 99, -n)

    items.sort(key=sortkey)
    used = [series[k] for k in SERIES_ORDER
            if k in series and any(i["series"] == k for i in items)]
    (ROOT / "cardnews" / "manifest.json").write_text(
        json.dumps({"count": len(items), "series": used, "episodes": items},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
