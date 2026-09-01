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

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
# 볼트에 이미 넣은 것을 적어 두는 장부.
# 금요일 볼트 동기화 루틴(클라우드)은 구글드라이브 MCP 로 볼트에 쓰는데, 볼트 197편을
# 매번 읽어 대조하기엔 무겁다. 이 장부를 보면 "무엇이 아직 안 갔는지" 를 바로 안다.
# 로컬 실행도 같은 장부를 갱신하므로 두 경로가 한 장부를 본다.
LEDGER = ROOT / ".obsidian-synced.json"
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


def render(src: Path, head: str) -> str:
    """볼트에 쓸 전문을 만든다. 쓰기 경로와 --check 가 같은 함수를 봐야
    둘이 갈라지지 않는다 — 갈라지면 검사기가 통과시키는 어긋남이 생긴다."""
    text = src.read_text(encoding="utf-8")
    body = strip_fm(text)
    m = re.match(r"^(---\n.*?\n---\n)", text, re.S)
    fmb = m.group(1) + "\n" if m else ""
    # 첫 H1 뒤에 갤러리 안내를 넣는다
    h = re.match(r"(\s*#\s+[^\n]*\n)", body)
    body = (h.group(1) + "\n" + head + body[h.end():]) if h else (head + body)
    return fmb + body


def has_key(text: str, key: str) -> bool:
    """식별자가 그 문서의 것인지 본다.

    ⚠ 단순 `in` 이면 안 된다. 슬러그가 다른 슬러그의 **접두사**이기 때문이다 —
    `#r=vector` 는 `#r=vector-advanced` 안에 들어 있다. 투트랙이 이 저장소의
    기본 포맷이라(이해편/확장편 쌍) 접두사 충돌이 예외가 아니라 다수다.
    실제 사고: 볼트에 확장편만 있으면 이해편이 "이미 있음" 으로 걸러져
    **영원히 안 써진다**(2026-09-01 --check 를 만들다 발견).
    그래서 슬러그가 이어지지 않는 자리에서 끝나는 것까지 확인한다."""
    return re.search(re.escape(key) + r"(?![0-9A-Za-z_-])", text) is not None


_CACHE: dict = {}          # 폴더 → {경로: 본문}. 쓰기 뒤에는 비운다.


def head_zone(text: str) -> str:
    """식별자의 **소유**가 적히는 구역 = 프론트매터 + 갤러리 안내 콜아웃.

    본문 언급은 소유가 아니다. 실제로 둘 다 일어난다 —
      · 가이드가 남의 영상 ID 를 본문에 캐시한다(`011-보고따라해` 를 영상노트와 공유).
      · 이해편이 확장편 갤러리 URL 을 「더 깊이」 링크로 갖는다.
    본문까지 뒤지면 그 파일이 주인으로 오인돼, 진짜 노트가 "이미 있음" 으로
    걸러지고 **영원히 안 써진다**(2026-09-01 발견).
    """
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    zone = m.group(0) if m else ""
    b = re.search(r"^> \[!info\](?:.*\n)(?:>.*\n)*", text, re.M)
    return zone + (b.group(0) if b else "")


def resolve(folder: Path, key: str):
    """볼트에서 이 노트를 찾는다 → 경로 또는 None.

    파일명으로 보면 안 된다 — 볼트 이름은 손으로 붙여 온 것이라 manifest 제목과
    다르다(이름으로 보면 60편을 못 찾고 중복 생성한다, CLAUDE.md). 그래서 내용 속
    식별자로 본다. 다만 **소유 구역만** 본다(`head_zone` 참조).

    본문까지 넓히는 폴백을 두었다가 걷어냈다 — 이해편 본문의 「더 깊이」 링크가
    확장편 URL 을 갖고 있어서 **확장편이 "이미 있음" 으로 걸러져 안 써졌다**
    (실측: 176편 중 170편만 기록). 넓은 그물이 안전망이 아니라 누락의 원인이었다.
    볼트 사본은 리포 노트의 복사본이라 프론트매터를 갖고 있으므로 소유 판정으로 충분하다.
    """
    if not key or not folder.is_dir():
        return None
    texts = _CACHE.get(folder)
    if texts is None:                      # 폴더당 한 번만 읽는다. 캐시가 없으면
        texts = {}                         # 항목마다 폴더를 다시 훑어 O(n²) 가 된다.
        for f in sorted(folder.glob("*.md")):
            try:
                texts[f] = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                pass
        _CACHE[folder] = texts
    for f, t in texts.items():
        if has_key(head_zone(t), key):
            return f
    return None


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
        # 식별자는 맨 ID 가 아니라 `youtu.be/<ID>` 다(CLAUDE.md 가 정한 형태).
        # 맨 ID 로 두면 가이드가 프론트매터에 `videos: [<ID>, …]` 로 인용한 것과
        # 구별되지 않아, 그 영상 노트가 가이드 파일을 제 사본으로 착각한다.
        out.append((src, VAULT / "011-보고따라해" / name,
                    gallery_note("videos/#post-" + v["id"], "영상 노트"),
                    "youtu.be/" + v["id"]))
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


# ── 어긋남 대조 (--check) ───────────────────────────────────────
# 왜 있나: sync 는 "없을 때만 쓴다". 그래서 (a) 이미 볼트에 있는 노트의 본문을
# 리포에서 고치면 볼트가 따라오지 않고, (b) 클라우드에서 Drive MCP 로 직접 써 넣으면
# 이 스크립트가 얹는 갤러리 안내가 빠진다. 둘 다 조용해서 **기억에 의존**해 왔다.
# 셀 수 있는 것은 코드가 센다 — 여기서 잰다. 고치지는 않는다(비침습).
#
# ⚠ 볼트 사본은 사용자가 위키링크·메모를 덧붙이는 곳이라 단순 diff 는 전부 "다름" 으로
# 찍힌다. 그래서 **비대칭**으로 본다: 리포의 줄이 볼트에 전부 있으면 최신으로 친다.
# 볼트 쪽 추가는 정상(토요일 작업), 리포 쪽 줄이 없으면 볼트가 뒤처진 것이다.
def check_all(names) -> int:
    drift = 0
    for shelf in names:
        cnt = {"없음": 0, "같음": 0, "배너없음": 0, "뒤처짐": 0}
        notes = []
        for src, dest, head, key in PLANS[shelf]():
            found = resolve(dest.parent, key) or (dest if dest.exists() else None)
            if found is None:
                cnt["없음"] += 1
                continue
            actual = found.read_text(encoding="utf-8", errors="ignore")
            banner = head.strip().splitlines()[0]          # "> [!info] <라벨>"
            if banner not in actual:
                cnt["배너없음"] += 1
                notes.append(("배너없음", found.name, ""))
                continue
            # 리포 본문의 실질 줄이 볼트에 다 있는가
            missing = [ln for ln in (l.strip() for l in strip_fm(
                src.read_text(encoding="utf-8")).splitlines())
                if len(ln) >= 8 and ln not in actual]
            if missing:
                cnt["뒤처짐"] += 1
                notes.append(("뒤처짐", found.name,
                              "리포 줄 %d개가 볼트에 없음" % len(missing)))
            else:
                cnt["같음"] += 1
        bad = cnt["배너없음"] + cnt["뒤처짐"]
        drift += bad
        print("%-9s 없음 %3d · 같음 %3d · 배너없음 %2d · 뒤처짐 %2d"
              % (shelf, cnt["없음"], cnt["같음"], cnt["배너없음"], cnt["뒤처짐"]))
        for kind, name, why in notes[:10]:
            print("    ⚠ %-6s %s%s" % (kind, name, ("   (%s)" % why) if why else ""))
        if len(notes) > 10:
            print("    … 외 %d편" % (len(notes) - 10))
    if drift:
        print("\n어긋남 %d편. --force 로 밀지 말 것 — 볼트 전체를 덮어 위키링크 작업을 "
              "날린다. HANDOVER 「볼트 사본이 어긋난다」 의 고르는 법을 볼 것." % drift)
    else:
        print("\n어긋남 0.")
    return 1 if drift else 0


def main():
    ap = argparse.ArgumentParser(description="리포 → 옵시디언 볼트 (없을 때만)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="이미 있는 노트도 덮는다")
    ap.add_argument("--check", action="store_true",
                    help="볼트가 리포와 어긋났는지 재기만 한다(쓰지 않음). 어긋나면 exit 1")
    ap.add_argument("--only", choices=sorted(PLANS), help="한 서가만")
    ap.add_argument("--vault", help="볼트 경로 (기본: 위 VAULT)")
    a = ap.parse_args()

    global VAULT
    if a.vault:
        VAULT = Path(a.vault)
    if not VAULT.is_dir():
        sys.exit("볼트를 찾지 못했다: %s" % VAULT)

    names = [a.only] if a.only else sorted(PLANS)
    if a.check:
        sys.exit(check_all(names))
    total_new = total_skip = 0
    ledger = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {}

    for shelf in names:
        items = PLANS[shelf]()
        new, skip = [], 0
        for src, dest, head, key in items:
            hit = resolve(dest.parent, key)
            if (hit is not None or dest.exists()) and not a.force:
                # 건너뛰는 것도 장부에 남긴다 — 처음 돌릴 때 볼트에 있는 것이 한꺼번에 기록된다.
                # 손으로 만든 옛 파일은 식별자가 없어 dest.exists() 로만 걸리는데,
                # 그때도 기록해야 클라우드 루틴이 "이미 갔다" 를 안다.
                if key:
                    ledger.setdefault(shelf, {}).setdefault(key, dest.name)
                skip += 1
                continue
            if not a.dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(render(src, head), encoding="utf-8")
                _CACHE.pop(dest.parent, None)   # 방금 쓴 것이 다음 항목에 보이게
            new.append(dest.name)
            if key:
                ledger.setdefault(shelf, {})[key] = dest.name

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

    if not a.dry_run:
        import mathlib as M
        M.dump_json(LEDGER, ledger)
        print("장부 %s — %d편 기록"
              % (LEDGER.name, sum(len(v) for v in ledger.values())))

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
