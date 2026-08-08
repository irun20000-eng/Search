#!/usr/bin/env python3
"""
이관 동일성 대조: 원본 모놀리스(videos/_legacy/index-monolith.html) vs 추출된 notes/*.md
73편 전 항목이 일치해야 머지 가능. 불일치 1건이라도 있으면 exit 1.
"""
import re, json, html, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEG  = ROOT / "videos" / "_legacy" / "index-monolith.html"
NOTES= ROOT / "videos" / "notes"
MAN  = ROOT / "videos" / "manifest.json"


def norm(s):
    """비교용 정규화: 마크업 제거 + 공백 압축."""
    s = html.unescape(s)
    s = re.sub(r'<a\s[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', r'\2', s, flags=re.S)  # HTML 링크 → 텍스트
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)                                # MD 링크 → 텍스트
    s = re.sub(r'<[^>]+>', '', s)
    # 강조 표기는 내용이 아니므로 양쪽 모두에서 제거(별/백틱).
    # 원본에 깨진 마크업(*<em>x</em>**)이 1건 있어 대칭 제거해야 내용 비교가 성립한다.
    s = s.replace('*', '').replace('`', '')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def from_html():
    h = LEG.read_text(encoding='utf-8')
    out = {}
    for vid, body in re.findall(r'<details class="post" id="post-([^"]+)">(.*?)</details>', h, re.S):
        card = re.search(r'<a class="gcard"[^>]*href="#post-%s".*?</a>' % re.escape(vid), h, re.S).group(0)
        mt = re.findall(r'<span>(.*?)</span>', re.search(r'<div class="mt">(.*?)</div>', card, re.S).group(1), re.S)
        bq = re.search(r'<blockquote>(.*?)</blockquote>', body, re.S)
        chaps, bullets = [], []
        for m in re.finditer(r'<h2 class="chap">(.*?)</h2>(.*?)(?=<h2 class="chap">|<a class="top"|$)', body, re.S):
            head = norm(m.group(1))
            ts = re.search(r'\?t=(\d+)', m.group(1))
            chaps.append((head, int(ts.group(1)) if ts else None))
            # <p>와 <li>를 문서 순서대로 (모놀리스에 두 방언이 공존)
            for a, b in re.findall(r'<p>(.*?)</p>|<li>(.*?)</li>', m.group(2), re.S):
                t = norm(a or b)
                if t: bullets.append(t)
        out[vid] = {
            "title":   norm(re.search(r'<div class="ttl">(.*?)</div>', card, re.S).group(1)),
            "channel": norm(re.search(r'data-channel="([^"]*)"', card).group(1)),
            "dur":     norm(mt[2]).replace('⏱', '').strip(),
            "published": norm(mt[1]),
            "tags":    html.unescape(re.search(r'data-tags="([^"]*)"', card).group(1)).split('|'),
            "cat":     re.search(r'data-cat="([^"]*)"', card).group(1),
            "one":     re.sub(r'^한 줄 요약:\s*', '', norm(bq.group(1))) if bq else '',
            "chaps":   chaps,
            "bullets": bullets,
        }
    return out


def from_notes():
    out = {}
    for f in sorted(NOTES.glob("*.md")):
        vid = f.stem
        txt = f.read_text(encoding='utf-8')
        fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', txt, re.S).groups()
        meta = {}
        for line in fm.split('\n'):
            if ': ' in line:
                k, v = line.split(': ', 1)
                meta[k.strip()] = v.strip()
        chaps, bullets = [], []
        for line in body.split('\n'):
            ls = line.strip()
            if ls.startswith('## '):
                head = norm(ls[3:])
                ts = re.search(r'\?t=(\d+)', ls)
                chaps.append((head, int(ts.group(1)) if ts else None))
            elif ls.startswith('- ') or ls.startswith('* '):
                t = norm(ls[2:])
                if t: bullets.append(t)
            elif ls and not ls.startswith('#') and not ls.startswith('>'):
                # TL;DR 번호줄 + 문단(출처 고지 등) — 원본의 <p>에 대응
                t = norm(ls)
                if t: bullets.append(t)
        one = ''
        m = re.search(r'^> 한 줄 요약:\s*(.*)$', body, re.M)
        if m: one = norm(m.group(1))
        out[vid] = {
            "title": norm(meta.get('title', '')),
            "channel": norm(meta.get('channel', '')),
            "dur": meta.get('duration', ''),
            "published": meta.get('published', ''),
            "tags": [t.strip() for t in meta.get('tags', '').strip('[]').split(',') if t.strip()],
            "cat": meta.get('category', ''),
            "one": one,
            "chaps": chaps,
            "bullets": bullets,
        }
    return out


# 원본 데이터 자체의 오류를 권위 있는 출처로 교정한 항목.
# 파리티에서 제외하되 반드시 눈에 보이게 출력한다 (조용히 넘기지 않는다).
KNOWN_FIXES = {
    ("XzU81FfDXLs", "dur"): (
        "58:59+", "1:04:25",
        "원본 data-dur=58초·라벨 '58:59+' 모두 오류. "
        "YouTube API 권위값 PT1H4M25S(3865초)로 교정. '길이순' 정렬 오작동을 유발하던 버그."),
}


def main():
    A, B = from_html(), from_notes()
    fails = []
    if set(A) != set(B):
        fails.append(f"ID 집합 불일치: 원본에만 {set(A)-set(B)} / 노트에만 {set(B)-set(A)}")

    for vid in sorted(set(A) & set(B)):
        a, b = A[vid], B[vid]
        for k in ("title", "channel", "dur", "published", "cat", "tags", "one", "chaps", "bullets"):
            if a[k] != b[k]:
                if (vid, k) in KNOWN_FIXES:
                    continue
                fails.append(f"[{vid}] {k} 불일치")
                if k in ("chaps", "bullets"):
                    fails.append(f"    원본 {len(a[k])}개 / 노트 {len(b[k])}개")
                    for x, y in zip(a[k], b[k]):
                        if x != y:
                            fails.append(f"    원본: {str(x)[:110]}")
                            fails.append(f"    노트: {str(y)[:110]}")
                            break
                else:
                    fails.append(f"    원본: {str(a[k])[:110]}")
                    fails.append(f"    노트: {str(b[k])[:110]}")

    # manifest ↔ notes 1:1
    man = json.loads(MAN.read_text(encoding='utf-8'))
    mids = {v["id"] for v in man["videos"]}
    if mids != set(B):
        fails.append(f"manifest ↔ notes 불일치: {mids ^ set(B)}")

    n = len(set(A) & set(B))
    if fails:
        print(f"❌ 파리티 실패 — {len(fails)}건\n")
        print("\n".join(fails[:60]))
        sys.exit(1)
    if KNOWN_FIXES:
        print("ℹ️  의도적 교정 (파리티 예외):")
        for (vid, k), (was, now, why) in KNOWN_FIXES.items():
            print(f"   [{vid}] {k}: {was} → {now}")
            print(f"      사유: {why}")
        print()
    print(f"✅ 파리티 통과 — {n}편 전 항목 일치 (위 교정 {len(KNOWN_FIXES)}건 제외)")
    print(f"   (제목·채널·길이·게시일·분류·태그·한줄요약·챕터/타임스탬프·불릿 전수 대조)")
    tot_ch = sum(len(v['chaps']) for v in B.values())
    tot_bu = sum(len(v['bullets']) for v in B.values())
    print(f"   챕터 {tot_ch}개 · 불릿 {tot_bu}개 대조 완료")


if __name__ == "__main__":
    main()
