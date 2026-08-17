#!/usr/bin/env python3
"""
제미나이 VIDEO-NOTE v1 출력 → videos/notes/<id>.md + manifest.json 갱신

메타데이터(제목·채널·길이·게시일)는 제미나이가 아니라 YouTube API에서 온다.
  --meta 는 get_video_details 응답을 그대로 담은 JSON 파일.

사용:
  python3 tools/ingest_video.py --gemini out.txt --meta meta.json [--added 2026-08-08]

파싱 실패 시 추측하지 않고 무엇이 왜 안 읽혔는지 출력하고 종료한다.
"""
import re, json, sys, argparse, datetime as _dt
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
    # 경계를 명시한다. 경계가 없으면 12자 이상 토큰에서 조용히 앞 11자만 잘라 쓴다.
    B = r'(?![A-Za-z0-9_-])'
    m = (re.search(r'youtu\.be/([A-Za-z0-9_-]{11})' + B, u)
         or re.search(r'[?&]v=([A-Za-z0-9_-]{11})' + B, u)
         or re.search(r'/(?:embed|shorts|live)/([A-Za-z0-9_-]{11})' + B, u))
    if m:
        return m.group(1)
    # 정규 URL 형태가 아니면 '아무 11자 토큰'을 ID로 삼지 않는다.
    # 우연히 실재하는 다른 영상 ID였다면 엉뚱한 영상의 메타데이터로 노트가 저장된다.
    bare = re.fullmatch(r'\s*([A-Za-z0-9_-]{11})\s*', u)
    return bare.group(1) if bare else None


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
        if not mm:
            return None
        # 모델이 값을 백틱·굵게로 감싸 내는 경우가 흔하다 (표에 `automation` 으로 제시했으므로)
        return mm.group(1).strip().strip('`*_ ').strip()

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
    # 기록일(갤러리 등록일)의 기본값은 '오늘'이다.
    # published 로 폴백하면 영상 게시일이 등록일로 둔갑한다 — 실제로 7건이 그렇게 들어갔다.
    added = a.added or _dt.date.today().isoformat()
    title = (meta.get('title') or '').strip()
    channel = (meta.get('channelTitle') or '').strip()

    fm = ["---", f"title: {title}", f"channel: {channel}",
          f"video_url: https://youtu.be/{g['id']}", f"duration: {fmt_dur(dur)}",
          f"published: {published}", f"captured: {added}",
          f"tags: [{', '.join(g['tags'])}]", f"category: {g['cat']}", "---", ""]
    NOTES.mkdir(parents=True, exist_ok=True)
    # 롤백 대비 스냅샷 — 반드시 쓰기 '이전'에. 쓰고 나서 뜨면 손상본을 보관하게 된다.
    _np = NOTES / f"{g['id']}.md"
    note_before = _np.read_text(encoding='utf-8') if _np.exists() else None
    (NOTES / f"{g['id']}.md").write_text(
        "\n".join(fm) + f"# {title}\n\n" + g["note"].strip() + "\n", encoding='utf-8')

    man = json.loads(MAN.read_text(encoding='utf-8'))
    man_before = json.loads(MAN.read_text(encoding='utf-8'))   # 게이트 미달 시 롤백용
    entry = {"id": g["id"], "title": title, "channel": channel, "published": published,
             "added": added, "duration": dur, "cat": g["cat"], "tags": g["tags"],
             "one": re.sub(r'\*\*|\*|`', '', g["one"]), "path": f"notes/{g['id']}.md"}
    man["videos"] = [v for v in man["videos"] if v["id"] != g["id"]]
    man["videos"].insert(0, entry)
    man["generated"] = max((v.get("added", "") for v in man["videos"]), default="")
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding='utf-8')

    # 품질 게이트를 파이프라인 안에서 강제한다.
    # 사람의 기억에 맡기면 미달 노트가 그대로 갤러리에 올라간다.
    sys.path.insert(0, str(Path(__file__).resolve().parent))

    # 인코딩 손상 검사 — Drive→디스크 경로에서 한글이 다른 문자로 치환되는 사고가 있었다.
    # 치환 결과도 유효한 UTF-8이고 챕터·인용 개수도 그대로라 품질 게이트가 못 잡는다.
    # 실제로 U+AE30(기) → U+EE30(사설영역)이 갤러리까지 발행된 적이 있다.
    from check_encoding import check as enc_check
    enc_hits = enc_check(NOTES / f"{g['id']}.md")
    if enc_hits:
        MAN.write_text(json.dumps(man_before, ensure_ascii=False, indent=1) + "\n", encoding='utf-8')
        if note_before is None:
            _np.unlink(missing_ok=True)
        else:
            _np.write_text(note_before, encoding='utf-8')   # 기존 노트 원상복구
        print(f"❌ 인코딩 손상 의심 — 갤러리에 넣지 않고 되돌렸다 ({g['id']})")
        for pos, cp, why, ctx in enc_hits[:6]:
            print(f"     · {cp} {why} @{pos}")
            print(f"       {ctx}")
        print("   → 본문이 옮겨지는 과정에서 깨진 것이다. 원본을 다시 받아 재시도할 것.")
        sys.exit(1)

    from verify_video import check as gate_check
    gfails, GM = gate_check(NOTES / f"{g['id']}.md")
    if gfails:
        # manifest 롤백 — 게이트를 통과하지 못한 노트는 갤러리에 넣지 않는다
        MAN.write_text(json.dumps(man_before, ensure_ascii=False, indent=1) + "\n", encoding='utf-8')
        if note_before is None:
            _np.unlink(missing_ok=True)
        else:
            _np.write_text(note_before, encoding='utf-8')   # 기존 노트 원상복구
        print(f"❌ 품질 게이트 미달 — 갤러리에 넣지 않고 되돌렸다 ({g['id']})")
        for f in gfails:
            print(f"     · {f}")
        print("   → 제미나이 출력을 보강해 다시 붙여넣어 달라.")
        sys.exit(1)

    safe = re.sub(r'[\\/:*?"<>|]', '', title).replace(' ', '_')[:70]
    print(f"✅ 인제스트 완료  {g['id']}")
    print(f"   {title}")
    print(f"   {channel} · {fmt_dur(dur)} · {published} · {g['cat']} · 태그 {len(g['tags'])}개")
    print(f"   게이트 통과 — 챕터 {GM['chapters']} · 인용 {GM['quotes']} · TL;DR {GM['tldr']} · 본문 {GM['body']}자")
    print(f"   노트: videos/notes/{g['id']}.md · 갤러리 총 {len(man['videos'])}편")
    print(f"   옵시디언 파일명: {added.replace('-','')}_{safe}.md")


if __name__ == "__main__":
    main()
