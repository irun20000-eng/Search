#!/usr/bin/env python3
"""카드뉴스 재렌더가 발행본과 같은가 — 픽셀로 대조한다.

기존 `cardnews.py parity` 는 해시만 찍었다. 해시는 PNG 인코더가 조금만 달라도 갈리므로
"다르다"는 것만 알려 주고 **무엇이 얼마나 다른지**는 말해 주지 않는다. 압축 차이와
글자가 다르게 그려진 것을 구분하지 못하면 판단을 못 한다.

여기서는 두 그림을 픽셀 단위로 빼서
  · 다른 픽셀 수와 비율
  · 다른 부분의 위치(bbox)
  · 채널 최대 차이
를 낸다. 그리고 판정을 셋으로 나눈다.

  같음      한 픽셀도 다르지 않다. 안심하고 바꿔도 된다.
  미세      0.1% 미만 · 최대 차이가 작다. 압축·안티에일리어싱 수준.
  다름      그 이상. **글자가 다르게 그려진 것이다. 바꾸면 안 된다.**

2026-08-22 에 이 검사로, 이 PC 에는 Noto Sans CJK KR 이 없어 맑은 고딕으로 그려진다는
사실을 확인했다(픽셀 6%가 달랐다). 렌더 환경을 러너로 고정한 이유가 이것이다.

사용:
    python tools/cardnews_parity.py <재렌더폴더> <원본폴더> [--prefix 평균착시] [--diff]
"""
from __future__ import annotations

import argparse
import pathlib
import sys

try:
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("Pillow 가 필요하다 — pip install pillow")

MICRO_RATIO = 0.001      # 이 비율 미만이면 '미세'
MICRO_DELTA = 24         # 그리고 채널 최대 차이가 이보다 작아야 '미세'


def compare(a_path: pathlib.Path, b_path: pathlib.Path):
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    if a.size != b.size:
        return {"verdict": "크기다름", "note": "%s vs %s" % (a.size, b.size)}
    d = ImageChops.difference(a, b)
    bbox = d.getbbox()
    if bbox is None:
        return {"verdict": "같음", "diff": 0, "ratio": 0.0, "maxd": 0, "bbox": None}
    # 밴드별 최대값으로 채널 최대 차이를, 히스토그램으로 다른 픽셀 수를 센다
    maxd = max(band.getextrema()[1] for band in d.split())
    total = a.size[0] * a.size[1]
    same = 0
    for band in (d.convert("L"),):
        same = band.histogram()[0]
    diff = total - same
    ratio = diff / total
    verdict = "미세" if (ratio < MICRO_RATIO and maxd <= MICRO_DELTA) else "다름"
    return {"verdict": verdict, "diff": diff, "ratio": ratio, "maxd": maxd, "bbox": bbox}


def main():
    ap = argparse.ArgumentParser(description="카드뉴스 재렌더 픽셀 대조")
    ap.add_argument("new", help="재렌더 결과 폴더")
    ap.add_argument("ref", help="발행본(원본) 폴더")
    ap.add_argument("--prefix", help="파일 접두어 (없으면 재렌더 폴더에서 추론)")
    ap.add_argument("--diff", action="store_true", help="다른 장의 차이 이미지를 저장")
    a = ap.parse_args()

    new, ref = pathlib.Path(a.new), pathlib.Path(a.ref)
    for p in (new, ref):
        if not p.is_dir():
            sys.exit("폴더가 없다: %s" % p)

    prefix = a.prefix
    if not prefix:
        cands = sorted(p.stem.rsplit("_", 1)[0] for p in new.glob("*_01.png"))
        if not cands:
            sys.exit("접두어를 추론하지 못했다. --prefix 로 줄 것.")
        prefix = cands[0]

    print("재렌더 %s" % new)
    print("발행본 %s" % ref)
    print("접두어 %s" % prefix)
    print()
    print("%-4s %-8s %-12s %-9s %-6s %s" % ("장", "판정", "다른 픽셀", "비율", "최대차", "위치"))

    verdicts = []
    for i in range(1, 11):
        name = "%s_%02d.png" % (prefix, i)
        b, r = new / name, ref / name
        if not b.exists() or not r.exists():
            print("%-4d 없음     재렌더 %s · 발행본 %s" % (i, b.exists(), r.exists()))
            verdicts.append("없음")
            continue
        c = compare(r, b)
        verdicts.append(c["verdict"])
        if c["verdict"] == "크기다름":
            print("%-4d %-8s %s" % (i, c["verdict"], c["note"]))
            continue
        print("%-4d %-8s %-12s %-9s %-6s %s" % (
            i, c["verdict"], "{:,}".format(c["diff"]), "%.3f%%" % (c["ratio"] * 100),
            c["maxd"], c["bbox"] or "-"))
        if a.diff and c["verdict"] == "다름":
            out = new / ("_diff_%02d.png" % i)
            ImageChops.difference(Image.open(r).convert("RGB"),
                                  Image.open(b).convert("RGB")).save(out)

    print()
    bad = sum(1 for v in verdicts if v == "다름")
    if bad:
        print("[X] %d장이 발행본과 다르게 그려졌다. 이 결과로 발행본을 갈아 끼우지 말 것." % bad)
        print("    글자 폭이 통째로 다르면 폰트 문제다 — `cardnews.py doctor` 로 먼저 확인할 것.")
        return 1
    if any(v == "미세" for v in verdicts):
        print("[!] 압축·안티에일리어싱 수준의 차이만 있다. 눈으로 한 번 보고 판단할 것.")
        return 0
    print("[OK] 전 장이 발행본과 픽셀 단위로 같다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
