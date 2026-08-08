#!/usr/bin/env python3
"""
videos/notes/*.md → videos/manifest.json 재생성.
노트를 손으로 고쳤을 때 카드 메타를 다시 맞추는 용도.
기존 manifest의 순서(최신순 배치)는 최대한 유지한다.
"""
import re, json
from pathlib import Path

ROOT  = Path(__file__).resolve().parent.parent
NOTES = ROOT / "videos" / "notes"
MAN   = ROOT / "videos" / "manifest.json"


def sec(lbl):
    s = 0
    for p in str(lbl).split(':'):
        s = s * 60 + int(p)
    return s


def main():
    old = json.loads(MAN.read_text(encoding='utf-8')) if MAN.exists() else {"videos": [], "categories": []}
    order = {v["id"]: i for i, v in enumerate(old.get("videos", []))}

    out = []
    for f in NOTES.glob("*.md"):
        txt = f.read_text(encoding='utf-8')
        fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', txt, re.S).groups()
        m = {}
        for line in fm.split('\n'):
            if ': ' in line:
                k, v = line.split(': ', 1)
                m[k.strip()] = v.strip()
        one = re.search(r'^>\s*한 줄 요약:\s*(.*)$', body, re.M)
        out.append({
            "id": f.stem,
            "title": m.get("title", ""),
            "channel": m.get("channel", ""),
            "published": m.get("published", ""),
            "added": m.get("captured", m.get("published", "")),
            "duration": sec(m.get("duration", "0")),
            "cat": m.get("category", ""),
            "tags": [t.strip() for t in m.get("tags", "").strip("[]").split(",") if t.strip()],
            "one": re.sub(r'\*\*|\*|`', '', re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', one.group(1))).strip() if one else "",
            "path": f"notes/{f.stem}.md",
        })

    out.sort(key=lambda v: (order.get(v["id"], 10**6), v["id"]))
    man = {"generated": max((v["added"] for v in out), default=""),
           "categories": old.get("categories", []), "videos": out}
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding='utf-8')
    print(f"manifest 재생성: {len(out)}편")


if __name__ == "__main__":
    main()
