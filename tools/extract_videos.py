#!/usr/bin/env python3
"""
1회성 이관: videos/index.html(모놀리스) → videos/notes/<id>.md + videos/manifest.json

기존 73편을 손실 없이 데이터 주도 구조로 옮긴다.
노트 형식은 사용자의 옵시디언 볼트(011-보고따라해) 형식을 정본으로 따른다.
"""
import re, json, html, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "videos" / "index.html"
OUT  = ROOT / "videos" / "notes"

CATEGORIES = [
    {"key": "knowledge",  "label": "지식관리·리서치"},
    {"key": "design",     "label": "디자인"},
    {"key": "agent",      "label": "클로드코드·에이전트"},
    {"key": "automation", "label": "업무 자동화"},
    {"key": "video",      "label": "영상 제작"},
    {"key": "build",      "label": "웹·앱 제작·배포"},
]


def unesc(s):
    return html.unescape(s)


def inline_md(frag):
    """인라인 HTML → 마크다운. strong/em/a/code만 등장한다."""
    s = frag
    s = re.sub(r'<a\s[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.S)
    s = re.sub(r'</?strong>', '**', s)
    s = re.sub(r'</?b>', '**', s)
    s = re.sub(r'</?em>', '*', s)
    s = re.sub(r'</?i>', '*', s)
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)          # 잔여 태그 제거
    s = unesc(s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def hhmmss_to_sec(t):
    parts = [int(x) for x in t.split(':')]
    sec = 0
    for p in parts:
        sec = sec * 60 + p
    return sec


def main():
    h = SRC.read_text(encoding='utf-8')

    cards = re.findall(r'<a class="gcard".*?</a>', h, re.S)
    posts = re.findall(r'<details class="post" id="post-([^"]+)">(.*?)</details>', h, re.S)
    assert len(cards) == len(posts), f"카드 {len(cards)} != 상세 {len(posts)}"

    by_id = {}
    for c in cards:
        vid = re.search(r'href="#post-([^"]+)"', c).group(1)
        by_id[vid] = c

    OUT.mkdir(parents=True, exist_ok=True)
    videos = []

    for vid, body in posts:
        card = by_id[vid]

        cat     = re.search(r'data-cat="([^"]*)"', card).group(1)
        tags    = [t for t in unesc(re.search(r'data-tags="([^"]*)"', card).group(1)).split('|') if t]
        channel = unesc(re.search(r'data-channel="([^"]*)"', card).group(1))
        added   = re.search(r'data-date="([^"]*)"', card).group(1)
        dur_s   = int(re.search(r'data-dur="([^"]*)"', card).group(1))

        # 카드 본문
        title   = inline_md(re.search(r'<div class="ttl">(.*?)</div>', card, re.S).group(1))
        one_pl  = inline_md(re.search(r'<div class="one">(.*?)</div>', card, re.S).group(1))
        mt      = re.findall(r'<span>(.*?)</span>', re.search(r'<div class="mt">(.*?)</div>', card, re.S).group(1), re.S)
        published = unesc(mt[1]).strip()
        dur_lbl   = unesc(mt[2]).replace('⏱', '').strip()

        # 상세: 한 줄 요약 (볼드 포함, 노트 본문용)
        bq = re.search(r'<blockquote>(.*?)</blockquote>', body, re.S)
        one_md = inline_md(bq.group(1)) if bq else one_pl
        one_md = re.sub(r'^\*\*\s*한 줄 요약\s*:?\s*\*\*\s*:?\s*', '', one_md)
        one_md = re.sub(r'^한 줄 요약\s*:\s*', '', one_md)

        # 본문 조립
        lines = []
        lines.append(f"# {title}\n")
        lines.append(f"> 한 줄 요약: {one_md}\n")

        # 챕터 / TL;DR 를 등장 순서대로
        for m in re.finditer(r'<h2 class="chap">(.*?)</h2>(.*?)(?=<h2 class="chap">|<a class="top"|$)', body, re.S):
            head_raw, chunk = m.group(1), m.group(2)
            head = inline_md(head_raw)

            if head.startswith('TL;DR'):
                lines.append(f"## {head}\n")
                for a, b in re.findall(r'<p>(.*?)</p>|<li>(.*?)</li>', chunk, re.S):
                    txt = inline_md(a or b)
                    if txt:
                        lines.append(txt)
                lines.append("")
                continue

            lines.append(f"## {head}")
            items = [a or b for a, b in re.findall(r'<p>(.*?)</p>|<li>(.*?)</li>', chunk, re.S)]
            in_summary = False
            for it in items:
                txt = inline_md(it)
                if not txt:
                    continue
                if txt.startswith('**3줄 요약**'):
                    lines.append(f"- {txt}")
                    in_summary = True
                elif re.match(r'\*\*(핵심 인용|내 팁|내 질문)\*\*', txt):
                    in_summary = False
                    lines.append(f"- {txt}")
                elif in_summary:
                    lines.append(f"  - {txt}")     # 3줄 요약 하위로 중첩
                else:
                    lines.append(f"- {txt}")
            lines.append("")

        fm = [
            "---",
            f"title: {title}",
            f"channel: {channel}",
            f"video_url: https://youtu.be/{vid}",
            f"duration: {dur_lbl}",
            f"published: {published}",
            f"captured: {added}",
            f"tags: [{', '.join(tags)}]",
            f"category: {cat}",
            "---",
            "",
        ]
        (OUT / f"{vid}.md").write_text("\n".join(fm) + "\n".join(lines).rstrip() + "\n", encoding='utf-8')

        videos.append({
            "id": vid, "title": title, "channel": channel,
            "published": published, "added": added, "duration": dur_s,
            "cat": cat, "tags": tags, "one": one_pl,
            "path": f"notes/{vid}.md",
        })

    # 갤러리 원본 순서(=최신순 배치) 유지
    manifest = {
        "generated": max(v["added"] for v in videos),
        "categories": CATEGORIES,
        "videos": videos,
    }
    (ROOT / "videos" / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding='utf-8')

    print(f"추출 완료: 노트 {len(videos)}개 + manifest.json")
    from collections import Counter
    for k, n in Counter(v["cat"] for v in videos).most_common():
        print(f"  {k:11} {n}")


if __name__ == "__main__":
    main()
