#!/usr/bin/env python3
"""
영상 노트 품질 게이트 — 측정이지 판단이 아니다.

하한은 기존 73편 코퍼스를 실측해 '관측된 최저값'으로 정했다.
따라서 이미 합격한 노트가 이 게이트에 걸리면 그것은 게이트 산정 오류다.

사용: python3 tools/verify_video.py videos/notes/*.md
"""
import re, sys, json
from pathlib import Path

CATS = {"knowledge", "design", "agent", "automation", "video", "build"}

# ── 게이트 (기존 73편 실측 최저값) ────────────────────────────
G = {
    "chapters_min":  4,      # 실측 min 4 / p10 5 / median 5
    "tldr_exact":    5,      # 실측 73편 전부 정확히 5 (예외 0건)
    "one_min":     120,      # 실측 min 121
    # ★ 반드시 '공백 제외' 글자수로 잴 것. 공백 포함으로 재면 min이 2,675로
    #   달라져 게이트가 어긋난다(초기 산정 시 실제로 이 혼동이 있었다).
    "body_min":   2050,      # 실측 min 2,091자(공백 제외) 기준
    "tags_min":      7,      # 실측 min 7
    "tags_max":     14,      # 실측 max 14
}


def parse(path):
    txt = Path(path).read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', txt, re.S)
    if not m:
        return None, None, "프론트매터 없음"
    fm, body = m.groups()
    meta = {}
    for line in fm.split('\n'):
        if ': ' in line:
            k, v = line.split(': ', 1)
            meta[k.strip()] = v.strip()
    return meta, body, None


def dur_sec(lbl):
    try:
        parts = [int(x) for x in str(lbl).split(':')]
        s = 0
        for p in parts: s = s * 60 + p
        return s
    except Exception:
        return None


def check(path):
    meta, body, err = parse(path)
    if err:
        return [err], {}

    fails = []
    chaps = re.findall(r'^##\s+(\d+\..*)$', body, re.M)
    tldr_h = re.findall(r'^##\s+TL;DR.*$', body, re.M)

    # TL;DR 줄수는 반드시 'TL;DR 섹션 안에서만' 센다.
    # 문서 전체에서 세면 다른 곳의 번호줄이 정족수를 채워 3줄짜리도 통과한다.
    tl = re.search(r'^##\s+TL;DR.*?$(.*?)(?=^##\s|\Z)', body, re.S | re.M)
    tldr_n = len(re.findall(r'^\d+\.\s', tl.group(1), re.M)) if tl else 0

    quotes = len(re.findall(r'\*\*핵심 인용\*\*', body))
    tips   = len(re.findall(r'\*\*(내 팁|내 질문)\*\*', body))

    # 챕터별 분포 — 총량만 보면 '인용 2개 + 0개'가 통과한다.
    blocks = re.split(r'^##\s+(?=\d+\.)', body, flags=re.M)[1:]
    per = []
    for i, blk in enumerate(blocks, 1):
        blk = re.split(r'^##\s', blk, flags=re.M)[0]
        per.append({
            "n": i,
            "q": len(re.findall(r'\*\*핵심 인용\*\*', blk)),
            "t": len(re.findall(r'\*\*(?:내 팁|내 질문)\*\*', blk)),
            "s": len(re.findall(r'\*\*3줄 요약\*\*', blk)),
        })
    # ingest 와 같은 다중행 캡처여야 한다. 첫 줄만 세면 줄바꿈된 요약이 오탈락한다.
    one_m  = re.search(r'^>\s*한 줄 요약:\s*(.*(?:\n(?!\s*$)(?!##)(?!>\s*$).*)*)', body, re.M)
    one    = re.sub(r'\s+', ' ', one_m.group(1)).strip() if one_m else ''
    tags   = [t.strip() for t in meta.get('tags', '').strip('[]').split(',') if t.strip()]
    body_n = len(re.sub(r'\s', '', body))
    # 타임스탬프는 챕터 헤딩 줄에서만 수집한다.
    # 본문 중간에 다른 영상 타임스탬프를 인용하면 단조증가 검사가 깨져 정상 노트가 탈락한다.
    ts     = [int(m) for line in re.findall(r'^##\s+\d+\..*$', body, re.M)
              for m in re.findall(r'\?t=(\d+)', line)]
    total  = dur_sec(meta.get('duration'))

    M = {"chapters": len(chaps), "tldr": tldr_n, "quotes": quotes, "tips": tips,
         "one": len(one), "body": body_n, "tags": len(tags), "ts": len(ts)}

    if len(chaps) < G["chapters_min"]:
        fails.append(f"챕터 {len(chaps)} < {G['chapters_min']}")
    if not tldr_h:
        fails.append("TL;DR 섹션 없음")
    elif tldr_n != G["tldr_exact"]:
        fails.append(f"TL;DR {tldr_n}줄 ≠ {G['tldr_exact']}줄")
    if quotes != len(chaps):
        fails.append(f"핵심 인용 {quotes} ≠ 챕터 {len(chaps)}")
    if tips != len(chaps):
        fails.append(f"내 팁/질문 {tips} ≠ 챕터 {len(chaps)}")
    for c in per:
        if c["q"] != 1:
            fails.append(f"{c['n']}번 챕터 핵심 인용 {c['q']}개 (챕터마다 정확히 1개)")
        if c["t"] != 1:
            fails.append(f"{c['n']}번 챕터 내 팁/질문 {c['t']}개 (챕터마다 정확히 1개)")
        if c["s"] != 1:
            fails.append(f"{c['n']}번 챕터 3줄 요약 라벨 {c['s']}개 (챕터마다 정확히 1개)")
    if len(one) < G["one_min"]:
        fails.append(f"한줄요약 {len(one)}자 < {G['one_min']}")
    if body_n < G["body_min"]:
        fails.append(f"본문 {body_n}자 < {G['body_min']}")
    if not (G["tags_min"] <= len(tags) <= G["tags_max"]):
        fails.append(f"태그 {len(tags)}개 (허용 {G['tags_min']}~{G['tags_max']})")
    if meta.get('category') not in CATS:
        fails.append(f"분류 '{meta.get('category')}' 가 열거값 아님")
    if ts != sorted(ts):
        fails.append("타임스탬프 단조 증가 아님")
    if total and ts and max(ts) > total:
        fails.append(f"타임스탬프 {max(ts)}초 > 영상 길이 {total}초 (시간 창작 의심)")
    if total is None:
        fails.append("duration 파싱 불가 — 타임스탬프 창작 검사가 무력화된다")
    for f in ("title", "channel", "video_url", "published", "duration", "category"):
        if not meta.get(f):
            fails.append(f"프론트매터 '{f}' 누락")

    return fails, M


def main():
    paths = sys.argv[1:] or sorted(Path("videos/notes").glob("*.md"))
    bad = 0
    for p in paths:
        fails, M = check(p)
        if fails:
            bad += 1
            print(f"❌ {Path(p).name}")
            for f in fails:
                print(f"     · {f}")
        elif len(paths) == 1:
            print(f"✅ {Path(p).name}")
            print(f"   챕터 {M['chapters']} · 인용 {M['quotes']} · 팁 {M['tips']} · "
                  f"TL;DR {M['tldr']} · 한줄요약 {M['one']}자 · 본문 {M['body']}자 · 태그 {M['tags']}")
    print(f"\n{len(paths)}편 검사 · 통과 {len(paths)-bad} · 실패 {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
