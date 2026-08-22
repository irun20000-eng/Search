# -*- coding: utf-8 -*-
"""5초 MP4 생성 — 노출 0.68초 + 크로스페이드 0.20초, 30fps, 정확히 5.000초(150프레임).
드라이브 handoff/02_엔진/makevideo.py 와 같은 파라미터."""
import subprocess

EXPO, XF, FPS = 0.68, 0.20, 30


def build(outdir, prefix, n=10):
    imgs = [f"{outdir}/{prefix}_{i:02d}.png" for i in range(1, n + 1)]
    cmd = ["ffmpeg", "-y"]
    for p in imgs:
        cmd += ["-loop", "1", "-t", str(EXPO), "-i", p]
    step = EXPO - XF
    parts, prev = [], "0:v"
    for k in range(1, n):
        lab = f"v{k}"
        parts.append(f"[{prev}][{k}:v]xfade=transition=fade:duration={XF}:offset={k*step:.2f}[{lab}]")
        prev = lab
    fc = ";".join(parts) + f";[{prev}]fps={FPS},format=yuv420p[out]"
    out = f"{outdir}/{prefix}.mp4"
    cmd += ["-filter_complex", fc, "-map", "[out]", "-c:v", "libx264",
            "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out]
    subprocess.run(cmd, check=True, capture_output=True)
    return out


if __name__ == "__main__":
    import sys, json
    d = "/home/claude/work/out/발견노트_02_최적정지"
    p = build(d, "최적정지")
    info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                           "-show_entries", "stream=nb_frames,width,height,r_frame_rate",
                           "-show_entries", "format=duration", "-of", "json", p],
                          capture_output=True, text=True).stdout
    print(p); print(info)
