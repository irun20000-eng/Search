#!/usr/bin/env python3
"""
제미나이 VIDEO-NOTE v1 출력 → videos/notes/<id>.md + manifest.json 갱신

메타데이터(제목·채널·길이·게시일)는 제미나이가 아니라 YouTube API에서 온다.
  --meta 는 get_video_details 응답을 그대로 담은 JSON 파일.

사용:
  python3 tools/ingest_video.py --gemini out.txt --meta meta.json [--added 2026-08-08]

파싱 실패 시 추측하지 않고 무엇이 왜 안 읽혔는지 출력하고 종료한다.
"""
import re, json, sys, argparse
from pathlib import Path

ROOT  = Path(__file__).resolve().parent.parent
NOTES = ROOT / "videos" / "notes"
MAN   = ROOT / "videos" / "manifest.json"

CATS = {"knowledge", "design", "agent", "automation", "video", "build"}
CAT_ALIAS = {
    "지식관리": "knowledge", "리서치": "knowledge", "research": "knowledge", "knowledge management": "knowledge",
    "디자인": "design", "ui": "design", "uiux": "design", "ux": "design",
    "에이전트": "agent", "클로드코드": "agent", "claude": "agent", "claudecode": "agent", "mcp": "agent",
    "자동화": "automation", "업무자동화": "automation", "n8n": "automation", "zapier": "automation",
    "영상": "video", "영상제작": "video", "편집": "video",
    "웹": "build", "앱": "build", "제작": "build", "배포": "build", "개발": "build", "dev": "build",
}


def die(msg, hint=None):
    print(f"❌ 파싱 실패: {msg}")
    if hint:
        print(f"   {hint}")
    print("   → 추측해서 채우지 않았다. 위 지점을 고쳐 다시 붙여넣어 달라.")
    sys.exit(1)


def vid_from_url(u):
    m = (re.search(r'youtu\.be/([A-Za-z0-9_-]{11})', u)
         or re.search(r'[?&]v=([A-Za-z0-9_-]{11})', u)
         or re.search(r'/(?:embed|shorts|live)/([A-Za-z0-9_-]{11})', u)
         or re.search(r'\b([A-Za-z0-9_-]{11})\b', u))
    return m.group(1) if m else None


def ts_to_sec(t):
    t = t.strip().lstrip('@').strip()
    if re.fullmatch(r'\d+', t):
        return int(t)
    if re.fullmatch(r'(\d+:)?\d{1,2}:\d{1,2}', t):
        s = 0
        for p in t.split(':'):
            s = s * 60 + int(p)
        return s
    return None


def fmt_dur(s):
    h, m, x = s // 3600, s % 3600 // 60, s % 60
    return f"{h}:{m:02d}:{x:02d}" if h else f"{m:02d}:{x:02d}"


def iso_to_sec(iso):
    m = re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    if not m:
        return None
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def parse_gemini(raw):
    txt = raw.replace('\r', '')
    # 코드펜스로 감싸져 있으면 벗긴다
    fence = re.search(r'```(?:\w+)?\n(.*?)```', txt, re.S)
    if fence and '===VIDEO-NOTE' in fence.group(1):
        txt = fence.group(1)
    # 마커 구간만 취한다 (===END=== 누락 허용)
    m = re.search(r'===\s*VIDEO-NOTE[^\n]*\n(.*?)(?:===\s*END\s*===|\Z)', txt, re.S | re.I)
    if not m:
        die("'===VIDEO-NOTE v1===' 시작 마커를 찾지 못했다.",
            "제미나이 답변에서 형식 블록 전체를 복사했는지 확인해 달라.")
    body = m.group(1)

    def head(key):
        mm = re.search(rf'^\s*{key}\s*[:：]\s*(.+)$', body, re.M | re.I)
        return mm.group(1).strip() if mm else None

    url = head('url') or head('영상') or head('link')
    if not url:
        die("헤더 'url:' 줄이 없다.")
    vid = vid_from_url(url)
    if not vid:
        die(f"URL에서 영상 ID(11자)를 못 뽑았다: {url!r}")

    cat_raw = (head('category') or head('cat') or head('분류') or '').strip().lower()
    cat = cat_raw if cat_raw in CATS else CAT_ALIAS.get(cat_raw.replace(' ', ''))
    if not cat:
        die(f"분류 '{cat_raw}' 를 6개 열거값으로 해석할 수 없다.",
            f"허용: {', '.join(sorted(CATS))}")

    tags_raw = head('tags') or head('태그') or ''
    tags = [t.strip().lstrip('#') for t in tags_raw.strip('[]').split(',') if t.strip()]
    if not tags:
        die("태그 줄이 비어 있다.")

    # 헤더 이후 = 노트 본문
    hdr_end = 0
    for mm in re.finditer(r'^\s*(?:url|category|cat|분류|tags|태그)\s*[:：].*$', body, re.M | re.I):
        hdr_end = max(hdr_end, mm.end())
    note = body[hdr_end:].strip('\n')

    one = re.search(r'^>\s*한 줄 요약\s*[:：]\s*(.*(?:\n(?!\s*$)(?!##).*)*)', note, re.M)
    if not one:
        die("'> 한 줄 요약:' 줄을 찾지 못했다.")

    chaps = re.findall(r'^##\s+\d+\..*$', note, re.M)
    if len(chaps) < 4:
        die(f"챕터가 {len(chaps)}개다 (최소 4개).",
            "챕터 제목은 '## 1. 제목 @0:00' 형식이어야 한다.")

    # @타임스탬프 → 마크다운 링크로 변환
    bad_ts = []

    def conv(mo):
        title, t = mo.group(1).rstrip(), mo.group(2)
        sec = ts_to_sec(t)
        if sec is None:
            bad_ts.append(t)
            return mo.group(0)
        return f"{title} · [{fmt_dur(sec)}](https://youtu.be/{vid}?t={sec})"

    note = re.sub(r'^(##\s+\d+\..*?)\s*[@＠]\s*([\d:]+)\s*$', conv, note, flags=re.M)
    if bad_ts:
        die(f"타임스탬프를 못 읽었다: {bad_ts}", "'@0:00' 또는 '@91' 형식이어야 한다.")

    # 이미 마크다운 링크 형태로 준 경우도 허용
    missing = [c for c in re.findall(r'^##\s+\d+\..*$', note, re.M) if '?t=' not in c]
    if missing:
        die(f"타임스탬프 없는 챕터 {len(missing)}개: {missing[0][:60]}…")

    return {"id": vid, "cat": cat, "tags": tags, "note": note,
            "one": re.sub(r'\s+', ' ', one.group(1)).strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gemini', required=True)
    ap.add_argument('--meta', required=True)
    ap.add_argument('--added')
    a = ap.parse_args()

    g = parse_gemini(Path(a.gemini).read_text(encoding='utf-8'))
    meta_all = json.loads(Path(a.meta).read_text(encoding='utf-8'))
    meta = meta_all.get(g["id"])
    if not meta:
        die(f"YouTube 메타데이터에 {g['id']} 가 없다.",
            "존재하지 않거나 비공개·삭제된 영상일 수 있다. (검증기 통과 실패)")

    dur = iso_to_sec(meta.get('duration'))
    if dur is None:
        die(f"영상 길이를 해석할 수 없다: {meta.get('duration')!r}")

    over = [int(x) for x in re.findall(r'\?t=(\d+)', g["note"]) if int(x) > dur]
    if over:
        die(f"타임스탬프 {max(over)}초가 영상 길이 {dur}초를 넘는다.",
            "제미나이가 시간을 지어냈을 가능성이 높다. 해당 챕터를 확인해 달라.")

    published = (meta.get('publishedAt') or '')[:10]
    added = a.added or published
    title = (meta.get('title') or '').strip()
    channel = (meta.get('channelTitle') or '').strip()

    fm = ["---", f"title: {title}", f"channel: {channel}",
          f"video_url: https://youtu.be/{g['id']}", f"duration: {fmt_dur(dur)}",
          f"published: {published}", f"captured: {added}",
          f"tags: [{', '.join(g['tags'])}]", f"category: {g['cat']}", "---", ""]
    NOTES.mkdir(parents=True, exist_ok=True)
    (NOTES / f"{g['id']}.md").write_text(
        "\n".join(fm) + f"# {title}\n\n" + g["note"].strip() + "\n", encoding='utf-8')

    man = json.loads(MAN.read_text(encoding='utf-8'))
    entry = {"id": g["id"], "title": title, "channel": channel, "published": published,
             "added": added, "duration": dur, "cat": g["cat"], "tags": g["tags"],
             "one": re.sub(r'\*\*|\*|`', '', g["one"]), "path": f"notes/{g['id']}.md"}
    man["videos"] = [v for v in man["videos"] if v["id"] != g["id"]]
    man["videos"].insert(0, entry)
    man["generated"] = max(v["added"] for v in man["videos"])
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding='utf-8')

    safe = re.sub(r'[\\/:*?"<>|]', '', title).replace(' ', '_')[:70]
    print(f"✅ 인제스트 완료  {g['id']}")
    print(f"   {title}")
    print(f"   {channel} · {fmt_dur(dur)} · {published} · {g['cat']} · 태그 {len(g['tags'])}개")
    print(f"   노트: videos/notes/{g['id']}.md · 갤러리 총 {len(man['videos'])}편")
    print(f"   옵시디언 파일명: {added.replace('-','')}_{safe}.md")


if __name__ == "__main__":
    main()
