#!/usr/bin/env python3
"""리포 → 옵시디언 볼트. 없을 때만 쓴다.

■ 왜 하나로 묶었나 (2026-08-22)
서가마다 볼트로 가는 길이 제각각이었다.
  수학사   sync_math_obsidian.py 가 반복 동기화하며 **덮어썼다**
  리서치   세션이 글을 쓸 때 손으로 복사 → 잊으면 빠진다 (실제로 4편 누락)
  영상·가이드  마찬가지로 손으로 → 96편은 맞았지만 보장이 없었다
  개념노트  볼트가 정본이었다가 리포로 옮겼다
전부 "리포가 정본, 볼트는 사본" 으로 통일한다.

■ 덮지 않는다
볼트에 이미 있는 노트는 **건드리지 않는다**. 토요일마다 옵시디언에서 노트끼리
위키링크를 거는 작업이 있어, 덮으면 그게 매주 사라진다.
리포 노트는 발행 이후 수정된 적이 한 번도 없으므로(수학사 24편·리서치 64편 실측 0건)
"없을 때만 쓴다" 로 잃는 것이 없다. 정말 다시 밀어야 하면 --force.

예외 — 목차·지도 노트(_MOC_수학사, _INDEX_카드뉴스학습자료)는 편이 늘면 갱신돼야
하므로 매번 다시 만든다. 그 파일들에는 "직접 고치지 않는다" 가 적혀 있다.

사용:
    python tools/sync_obsidian.py --dry-run        무엇이 새로 갈지만 본다
    python tools/sync_obsidian.py                  새 노트만 볼트로
    python tools/sync_obsidian.py --only concept   한 서가만
    python tools/sync_obsidian.py --force          이미 있는 것도 덮는다 (주의)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = Path(r"G:\내 드라이브\00_Obsidian_Second Brain\Insight Miner\000-수집")

# ■ 이미 있는지는 파일 이름으로 판정하지 않는다
# 볼트 파일명은 사람이 손으로 붙여 온 것이라 manifest 제목과 다르다
#   볼트  20260622_벡터(Vector) — 왜 배우고 어디까지 가나 (이해편).md
#   제목  벡터(Vector) — 고등학교에서 배우는 이유와 그 개념의 확장 (이해편)
# 이름으로 대조하면 60편이 있는데도 "없다" 로 보고 153편을 새로 만든다(실제로 겪었다).
# 그래서 **파일 안의 식별자**로 판정한다 — 리서치는 갤러리URL(#r=슬러그),
# 영상은 youtu.be/<ID>, 가이드·개념노트는 갤러리 링크(#g= / #n=).

# 볼트에 이미 쌓인 이름 규칙을 실측해 그대로 따른다 (2026-08-22 기준).
#   001-주제리서치      20260622_벡터(Vector) — … .md          공백 유지
#   011-보고따라해      20240824_여러분은_왜_요약하나요_… .md    공백을 _ 로
#   003-카드뉴스학습자료 [2026-08-04] 심슨의 역설 — 이해편.md
#   002-수학사          02-개념/개념_미분법.md                   유형별 하위폴더
SAFE = re.compile(r'[\\/:*?"<>|]')


def safe(name: str) -> str:
    return SAFE.sub("", name).strip()


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def strip_fm(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n?", "", text, count=1, flags=re.S)


def read_fm(text: str):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    out = {}
    for line in m.group(1).splitlines():
        if ": " in line:
            k, v = line.split(": ", 1)
            out[k.strip()] = v.strip()
    return out, m.group(2)


def gallery_note(url: str, label: str) -> str:
    return "> [!info] %s\n> 갤러리에서 보기 — https://irun20000-eng.github.io/Search/%s\n" \
           "> 이 노트는 리포에서 왔습니다. 여기에 링크·메모를 더해도 동기화가 덮지 않습니다.\n\n" \
           % (label, url)


# ── 서가별 수집 ────────────────────────────────────────────────
def plan_reports():
    out = []
    for r in load("reports/manifest.json").get("reports", []):
        src = ROOT / r["path"]
        if not src.exists():
            continue
        d = (r.get("date") or "").replace("-", "")
        name = "%s_%s.md" % (d, safe(r["title"]))
        out.append((src, VAULT / "001-주제리서치" / name,
                    gallery_note("research/#r=" + r["slug"], "주제 리서치"),
                    "#r=" + r["slug"]))
    return out


def plan_videos():
    out = []
    for v in load("videos/manifest.json").get("videos", []):
        src = ROOT / "videos" / v["path"]
        if not src.exists():
            continue
        d = (v.get("added") or v.get("published") or "").replace("-", "")
        name = "%s_%s.md" % (d, safe(v["title"]).replace(" ", "_"))
        out.append((src, VAULT / "011-보고따라해" / name,
                    gallery_note("videos/#post-" + v["id"], "영상 노트"),
                    v["id"]))
    return out


def plan_guides():
    out = []
    for g in load("guides/manifest.json").get("guides", []):
        src = ROOT / "guides" / g["path"]
        if not src.exists():
            continue
        d = (g.get("date") or "").replace("-", "")
        name = "%s_%s.md" % (d, safe(g["title"]).replace(" ", "_"))
        out.append((src, VAULT / "011-보고따라해" / name,
                    gallery_note("guides/#g=" + g["slug"], "가이드"),
                    "#g=" + g["slug"]))
    return out


def plan_concept():
    out = []
    for n in load("concept/manifest.json").get("notes", []):
        src = ROOT / n["path"]
        if not src.exists():
            continue
        short = n["title"].split(" — ")[0]
        short = re.sub(r"\s*\([^)]*\)", "", short).strip()
        name = "[%s] %s — 이해편.md" % (n.get("date", ""), safe(short))
        out.append((src, VAULT / "003-카드뉴스학습자료" / name,
                    gallery_note("concept/#n=" + n["slug"], "개념노트"),
                    "#n=" + n["slug"]))
    return out


PLANS = {"reports": plan_reports, "videos": plan_videos,
         "guides": plan_guides, "concept": plan_concept}


def main():
    ap = argparse.ArgumentParser(description="리포 → 옵시디언 볼트 (없을 때만)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="이미 있는 노트도 덮는다")
    ap.add_argument("--only", choices=sorted(PLANS), help="한 서가만")
    ap.add_argument("--vault", help="볼트 경로 (기본: 위 VAULT)")
    a = ap.parse_args()

    global VAULT
    if a.vault:
        VAULT = Path(a.vault)
    if not VAULT.is_dir():
        sys.exit("볼트를 찾지 못했다: %s" % VAULT)

    names = [a.only] if a.only else sorted(PLANS)
    total_new = total_skip = 0

    for shelf in names:
        items = PLANS[shelf]()
        # 대상 폴더의 모든 노트를 한 번 읽어 "이 식별자가 이미 볼트에 있나" 를 만든다.
        seen = {}
        for src, dest, head, key in items:
            folder = dest.parent
            if folder in seen or not folder.is_dir():
                continue
            blob = []
            for f in folder.glob("*.md"):
                try:
                    blob.append(f.read_text(encoding="utf-8", errors="ignore"))
                except OSError:
                    pass
            seen[folder] = chr(10).join(blob)

        new, skip = [], 0
        for src, dest, head, key in items:
            already = key and key in seen.get(dest.parent, "")
            if (already or dest.exists()) and not a.force:
                skip += 1
                continue
            body = strip_fm(src.read_text(encoding="utf-8"))
            fm, _ = read_fm(src.read_text(encoding="utf-8"))
            # 프론트매터는 볼트에서도 쓸모가 있다(태그·날짜). 있으면 그대로 얹는다.
            text = src.read_text(encoding="utf-8")
            m = re.match(r"^(---\n.*?\n---\n)", text, re.S)
            fmb = m.group(1) + "\n" if m else ""
            # 첫 H1 뒤에 갤러리 안내를 넣는다
            h = re.match(r"(\s*#\s+[^\n]*\n)", body)
            body = (h.group(1) + "\n" + head + body[h.end():]) if h else (head + body)
            if not a.dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(fmb + body, encoding="utf-8")
            new.append(dest.name)

        # 개념노트는 그림도 함께 (볼트에서 바로 보이게)
        if shelf == "concept":
            for n in load("concept/manifest.json").get("notes", []):
                if not n.get("pic"):
                    continue
                p = ROOT / "concept" / "assets" / n["pic"]
                key = re.sub(r"\s*\([^)]*\)", "", n["title"].split(" — ")[0]).strip()
                d = VAULT / "003-카드뉴스학습자료" / ("개념한장_%s.png" % safe(key).replace(" ", ""))
                if p.exists() and (a.force or not d.exists()) and not a.dry_run:
                    shutil.copy2(p, d)

        total_new += len(new)
        total_skip += skip
        print("%-9s 새로 %2d · 이미 있음 %3d" % (shelf, len(new), skip))
        for n in new[:12]:
            print("    + %s" % n)
        if len(new) > 12:
            print("    … 외 %d편" % (len(new) - 12))

    print()
    if a.dry_run:
        print("[미리보기] %d편이 새로 갑니다. 이미 있는 %d편은 건드리지 않습니다."
              % (total_new, total_skip))
    elif a.force:
        print("[강제] %d편을 덮었습니다. 볼트에서 고친 내용이 있었다면 사라졌습니다."
              % total_new)
    else:
        print("[완료] 새로 %d편 · 그대로 둔 것 %d편." % (total_new, total_skip))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
