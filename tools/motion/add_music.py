#!/usr/bin/env python3
"""무음 쇼츠 MP4 에 배경음악을 입힌다 (render_short.py 다음 단계).

음악은 저작권이 분명한 것만 쓴다 — 출처·라이선스·잘라 쓴 구간을 영상 옆 `music.json` 에
적고, 이 스크립트는 그 파일만 보고 같은 결과를 다시 만든다(재현 가능).

  music.json 예:
    {"title": "Home", "artist": "Tanner Helland",
     "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
     "source_page": "https://github.com/tannerhelland/free-music",
     "source_url": "https://raw.githubusercontent.com/tannerhelland/free-music/<commit>/mp3/Home.mp3",
     "start": 0, "lufs": -18, "fade_in": 1.0, "fade_out": 3.0,
     "changes": "앞 69초를 잘라 음량을 맞추고 끝을 페이드아웃"}

  - 음원은 source_url 에서 받아 ~/.cache/motion-music 에 둔다(커밋 고정 URL 을 쓸 것).
  - 영상 길이만큼 start 부터 잘라, loudnorm 으로 lufs 에 맞추고 앞뒤를 페이드한다.
  - 영상 스트림은 다시 인코딩하지 않는다(-c:v copy).

CC BY 는 「저작자 표기(원본에 있으면 저작권 표시 그대로) · 라이선스 링크 · 변경 여부」를 요구한다. 영상 끝 화면에
「음악: 작곡가 「곡명」 · CC BY 4.0」을, 보고서 「요약 영상」 칸에 셋을 모두 적는다.
남의 곡을 편곡·리믹스한 트랙은 원곡의 권리가 따로 있으니 쓰지 않는다.

사용: python3 tools/motion/add_music.py silent.mp4 music.json out.mp4 [--audio local.mp3]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_short import ffmpeg_bin  # noqa: E402

CACHE = Path.home() / ".cache" / "motion-music"


def fetch(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    dst = CACHE / (hashlib.sha1(url.encode()).hexdigest()[:16] + Path(url).suffix)
    if not dst.exists():
        tmp = dst.with_suffix(".part")
        subprocess.run(["curl", "-sSfL", "-o", str(tmp), url], check=True)
        tmp.rename(dst)
    return dst


def credit(meta):
    """파일 안에도 출처를 남긴다 — 영상만 따로 퍼져도 스스로 출처를 밝히도록."""
    who = meta.get("copyright") or meta["artist"]
    return (f"Music: \"{meta['title']}\" {who} — {meta['license']} {meta['license_url']} — "
            f"{meta['source_page']} — changes: {meta.get('changes', '')}")


def duration(ff, path):
    out = subprocess.run([ff, "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    if not m:
        sys.exit(f"길이를 읽지 못했다: {path}")
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("meta")
    ap.add_argument("out")
    ap.add_argument("--audio", help="source_url 대신 쓸 로컬 음원")
    a = ap.parse_args()

    meta = json.loads(Path(a.meta).read_text(encoding="utf-8"))
    for k in ("title", "artist", "license", "license_url", "source_page", "source_url"):
        if not meta.get(k):
            sys.exit(f"music.json 에 {k} 가 없다 — 출처·라이선스 없는 음악은 넣지 않는다")
    ff = ffmpeg_bin()
    audio = Path(a.audio) if a.audio else fetch(meta["source_url"])
    vdur = duration(ff, a.video)
    start = float(meta.get("start", 0))
    if duration(ff, audio) - start < vdur:
        sys.exit(f"음원이 영상({vdur:.1f}초)보다 짧다 — start 를 당기거나 다른 곡을 고를 것")
    fin, fout = float(meta.get("fade_in", 1.0)), float(meta.get("fade_out", 3.0))
    lufs = float(meta.get("lufs", -18))
    af = (f"atrim=0:{vdur:.3f},asetpts=PTS-STARTPTS,"
          f"loudnorm=I={lufs}:TP=-1.5:LRA=11,"
          f"afade=t=in:st=0:d={fin},afade=t=out:st={vdur - fout:.3f}:d={fout},"
          "aresample=48000")
    cmd = [ff, "-y", "-loglevel", "error", "-i", a.video, "-ss", f"{start}", "-i", str(audio),
           "-filter_complex", f"[1:a]{af}[a]", "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
           "-metadata", f"comment={credit(meta)}",
           "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    print(f"→ {a.out} ({vdur:.1f}초, 음악: {meta['artist']} 「{meta['title']}」 {meta['license']})")


if __name__ == "__main__":
    main()
