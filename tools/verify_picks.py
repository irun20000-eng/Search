#!/usr/bin/env python3
"""골라봄(picks) 게이트 — 측정이지 판단이 아니다. (2026-11-05, T-20261105-01 검수 B5)

■ 왜 있나
첫 노트(2026-11-05)는 인용 11개가 전부 자막에 「들어 있었는데도」 사고 셋이 공개됐다.
  · 인용은 맞지만 [분:초] 가 다른 구간을 가리켰다 (영상노트 LESSONS 43 구간 귀속의 재발)
  · 한정어가 빠졌다 ("90%" — 클로드 디자인 주간 사용량이라는 조건)
  · 사실과 반대인 문장 ("개인정보는 다루지 않음")
기계가 셋을 다 잡지는 못한다. 이 게이트는 **잡을 수 있는 것**을 잡고(구조·구간 귀속),
나머지(한정어·사실 방향)는 사람 검수(PICKS.md 보고의 인용 대조표)에 남긴다.

■ 두 단계
1) 구조 — 언제나 (CI 포함)
   · 프론트매터 테마·날짜·영상 · 파일명 == 날짜
   · 본문 유튜브 URL 집합 == 프론트매터 영상 목록
   · 영상마다 「확인함」「확인 못 함」 라벨이 있다 (UX 시안 1-B, 2026-11-05~)
     · 2026-11-05 이전 양식(✅/⬜)도 허용한다 — 이미 공개된 노트를 이 게이트가 막지 않는다
   · 「AI」 선별 고지가 본문에 있다
   · 원시 HTML 태그 금지 (<script, <iframe, on*=) — 외부 텍스트를 옮기는 노트다
2) 인용 구간 — 근거 자막이 있을 때만 (Aside 로컬, 커밋 전)
   --evidence <폴더> 에 <영상ID>_ts.txt (youtube.getTranscript includeTimestamp) 가 있으면
   · 따옴표 인용 "..." 바로 뒤의 [mm:ss] 가, 인용 앞부분(8자)이 처음 나오는 자막 구간의
     시작과 ±3초 안에 있어야 한다
   · 인용이 자막에 없으면 막음
   자막은 공개 레포에 올리지 않는다(저작권). 그래서 CI 에서는 2) 를 건너뛴다.

사용:
  python tools/verify_picks.py                          # picks/notes/*.md 구조만
  python tools/verify_picks.py --evidence <폴더> [노트] # 구간까지
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_concept_manifest import parse_fm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "picks" / "notes"
URL = re.compile(r"https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})")
QUOTE = re.compile(r'"([^"\n]{2,80})"[^\n\[]{0,40}?\[(\d{1,2}(?::\d{2}){1,2})\]')
TS = re.compile(r"^\[(\d{1,2}(?::\d{2}){1,2}) - ")
RAW = re.compile(r"<\s*(script|iframe|object|embed)|\son\w+\s*=", re.I)


def secs(t: str) -> int:
    n = 0
    for p in t.split(":"):
        n = n * 60 + int(p)
    return n


def sections(body: str):
    """## n. 영상 단위로 자른다 → (영상ID, 본문)"""
    parts = re.split(r"(?m)^## \d+\.", body)
    for chunk in parts[1:]:
        m = URL.search(chunk)
        yield (m.group(1) if m else None), chunk


def check(path: Path, evidence: Path | None):
    bad = []
    fm, body = parse_fm(path.read_text(encoding="utf-8"))
    vids = fm.get("영상") or []
    vids = [vids] if isinstance(vids, str) else vids
    for k in ("테마", "날짜"):
        if not fm.get(k):
            bad.append("프론트매터 %s 없음" % k)
    if fm.get("날짜") and fm["날짜"] != path.stem:
        bad.append("파일명(%s) ≠ 날짜(%s)" % (path.stem, fm["날짜"]))
    if set(URL.findall(body)) != set(vids):
        bad.append("본문 유튜브 URL ≠ 프론트매터 영상 목록")
    if "AI" not in body:
        bad.append("AI 선별 고지가 본문에 없다")
    if RAW.search(body):
        bad.append("원시 HTML(스크립트·이벤트 속성)이 있다")
    new_fmt = fm.get("날짜", "") > "2026-11-05"
    for vid, chunk in sections(body):
        if not vid:
            bad.append("영상 절에 유튜브 URL 이 없다")
            continue
        if new_fmt:
            if "확인함" not in chunk or "확인 못 함" not in chunk:
                bad.append("%s — 「확인함」「확인 못 함」 라벨 없음" % vid)
        elif not (("확인함" in chunk and "확인 못 함" in chunk) or ("✅" in chunk and "⬜" in chunk)):
            bad.append("%s — 검증 고지 없음" % vid)
        if evidence:
            ts = evidence / ("%s_ts.txt" % vid)
            if not ts.exists():
                bad.append("%s — 근거 자막 없음 (%s)" % (vid, ts.name))
                continue
            lines = ts.read_text(encoding="utf-8").splitlines()
            flat = " ".join(re.sub(r"^\[[^\]]*\]\s*", "", ln) for ln in lines)
            for q, t in QUOTE.findall(chunk):
                if q not in flat:
                    bad.append('%s — 인용이 자막에 없다: "%s"' % (vid, q))
                    continue
                head = q[:8]
                hit = next((ln for ln in lines if head in ln), None)
                if hit is None:  # 구간 경계에 걸친 인용 — 앞 4자로 다시
                    hit = next((ln for ln in lines if q[:4] in ln), None)
                m = TS.match(hit or "")
                if not m:
                    bad.append('%s — 구간을 못 찾음: "%s"' % (vid, q))
                elif abs(secs(m.group(1)) - secs(t)) > 3:
                    bad.append('%s — "%s" 의 [%s] 가 자막 구간 [%s] 와 다르다' % (vid, q, t, m.group(1)))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("notes", nargs="*")
    ap.add_argument("--evidence")
    a = ap.parse_args()
    ev = Path(a.evidence) if a.evidence else None
    files = [Path(p) for p in a.notes] or sorted(NOTES.glob("*.md"))
    n_bad = 0
    for f in files:
        b = check(f, ev)
        n_bad += len(b)
        print(("❌ " if b else "✅ ") + f.name + ("" if not b else ""))
        for x in b:
            print("   막음 " + x)
    print("[%s] picks %d편 · 막음 %d%s" % ("X" if n_bad else "OK", len(files), n_bad,
                                         "" if ev else " (인용 구간 검사는 --evidence 가 있을 때만)"))
    return 1 if n_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
