#!/usr/bin/env python3
"""매니페스트의 `path` 가 실제 파일을 가리키는지 잰다 — 서가마다 제 기준으로.

■ 왜 있나 (2026-09-22)
`guides/manifest.json` 새 항목에 path 를 `guides/aside-jev-start/guide.md` 로 적었다.
그런데 가이드 갤러리는 path 를 **`guides/index.html` 기준**으로 푼다. 그래서 실제 요청은
`guides/guides/aside-jev-start/guide.md` 가 되고 — **카드는 보이는데 펼치면 본문이 안 온다.**

어느 게이트도 못 잡았다. 각 서가 검사기는 파일을 **글롭**해서 읽고(`guides/*/guide.md`),
`sync_obsidian` 은 path 를 쓰지만 **없으면 조용히 건너뛴다**. 즉 「manifest 가 가리키는 곳에
파일이 있는가」를 재는 자리가 없었다. 발행된 뒤에도 초록이다.

■ 기준이 서가마다 다르다 — 여기가 이 검사의 핵심이다
소비자(갤러리·동기화)가 path 를 어디에 이어 붙이는지 실측해 정했다.

    guides   `guides/index.html:399` data-src="+esc(g.path)  → 기준 `guides/`
    videos   `videos/index.html:297` data-src="+esc(v.path)  → 기준 `videos/`
    concept  갤러리는 path 를 **안 쓴다**(`fetch("notes/"+slug+".md")`).
             `sync_obsidian.plan_concept` 만 쓰고 그쪽 기준은 **리포 루트**다.
             그래서 둘 다 본다 — path(루트 기준)와 갤러리가 만드는 `notes/<슬러그>.md`.

reports 는 `verify_reports_meta.py` 가 이미 path·양방향 고아를 덮으므로 여기서 제외한다.
하나를 두 곳에서 재면 둘이 갈라질 때 어느 쪽이 옳은지 알 수 없다(LESSONS 2026-09-02).

■ 양방향으로 본다
path 가 안 풀리면 「카드는 있는데 본문이 없다」, 디스크에만 있으면 「글은 썼는데 아무 데도
안 보인다」다. 둘 다 조용하므로 둘 다 센다.

사용: python3 tools/verify_manifest_paths.py      결함이 있으면 exit 1.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (서가, 매니페스트, 항목 키, path 기준, 디스크 글롭, 글롭→path 로 되돌리는 기준)
SHELVES = [
    ("guides",  "guides/manifest.json",  "guides", "guides",  "guides/*/guide.md",    "guides"),
    ("videos",  "videos/manifest.json",  "videos", "videos",  "videos/notes/*.md",    "videos"),
    ("concept", "concept/manifest.json", "notes",  ".",       "concept/notes/*.md",   "."),
]


def check(shelf, man_rel, key, base, glob, glob_base):
    man = ROOT / man_rel
    if not man.exists():
        return ["%s — 매니페스트가 없다: %s" % (shelf, man_rel)], 0
    items = json.loads(man.read_text(encoding="utf-8")).get(key, [])
    bad = []

    listed = set()
    for it in items:
        name = it.get("slug") or it.get("id") or "?"
        p = it.get("path")
        if not p:
            bad.append("%s/%s — path 필드가 없다" % (shelf, name))
            continue
        target = (ROOT / base / p).resolve()
        listed.add(target)
        if not target.exists():
            bad.append("%s/%s — path %r 가 %s 기준으로 안 풀린다 (찾은 곳: %s)"
                       % (shelf, name, p, base if base != "." else "리포 루트",
                          target.relative_to(ROOT) if ROOT in target.parents else target))

    # 갤러리가 path 대신 슬러그로 주소를 만드는 서가는 그쪽도 본다.
    if shelf == "concept":
        for it in items:
            s = it.get("slug")
            if s and not (ROOT / "concept" / "notes" / (s + ".md")).exists():
                bad.append("concept/%s — 갤러리가 여는 concept/notes/%s.md 가 없다" % (s, s))

    # 반대 방향 — 디스크에 있는데 매니페스트가 안 가리키는 것
    for f in sorted(ROOT.glob(glob)):
        if f.resolve() not in listed:
            bad.append("%s — %s 가 매니페스트 어느 항목의 path 도 아니다(갤러리에 안 나온다)"
                       % (shelf, f.relative_to(ROOT)))
    return bad, len(items)


def main():
    fails, total = [], 0
    for args in SHELVES:
        bad, n = check(*args)
        total += n
        if bad:
            fails += bad
            print("❌ %-8s %d항목" % (args[0], n))
            for b in bad:
                print("     · %s" % b)
        else:
            print("✅ %-8s %d항목 — path 가 전부 제 기준으로 풀리고 고아도 없다" % (args[0], n))

    print("\n%d항목 검사 · 결함 %d" % (total, len(fails)))
    print("ℹ️  reports 는 verify_reports_meta.py 가 같은 것을 이미 잰다(중복 회피).")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
