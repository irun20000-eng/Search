#!/usr/bin/env python3
"""모션그래픽 HTML → MP4 렌더러 (세로 쇼츠 1080×1920 기본).

장면은 HTML/CSS 애니메이션(@keyframes)과 선택적 JS 훅으로 쓴다. 이 스크립트는
브라우저(Chromium)에서 모든 애니메이션을 멈춘 뒤 프레임마다 시각 t 로 **되감아**
캡처한다 — 실시간 녹화가 아니라서 컴퓨터가 느려도 프레임이 빠지지 않는다.

  - CSS 애니메이션: document.getAnimations() 의 currentTime 을 t 로 맞춘다.
  - JS 로 그리는 것(숫자 카운터 등): 페이지가 window.__seek(t초) 를 정의하면 매 프레임 부른다.
  - 길이: 페이지의 window.__duration(초) 이 있으면 그 값을, 없으면 --duration 을 쓴다.

캡처한 PNG 를 ffmpeg(H.264, yuv420p) 표준입력으로 흘려 MP4 를 만든다.
ffmpeg 는 시스템에 없어도 `pip install imageio-ffmpeg` 의 정적 바이너리를 쓴다.

사용: python3 tools/motion/render_short.py scene.html out.mp4 [--fps 30] [--duration 60]
      [--size 1080x1920] [--still 3.5 still.png]  # 특정 시각 한 장만 PNG 로
"""
import argparse
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def ffmpeg_bin():
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg 가 없다 — `pip install imageio-ffmpeg` 로 정적 바이너리를 받을 것")


# 이 컨테이너에는 playwright 패키지가 기대하는 빌드와 다른 Chromium 이 /opt/pw-browsers 에
# 깔려 있어 기본 launch() 가 실패한다 — tools/verify_figures.py 의 find_chrome 과 같은 방식으로
# 가장 높은 버전을 찾아 쓰고, 못 찾으면 playwright 에 맡긴다.
CHROME_GLOBS = (
    "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
    "/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell",
)


def find_chrome():
    def version(path):
        m = re.search(r"-(\d+)/", path)
        return int(m.group(1)) if m else -1
    for pattern in CHROME_GLOBS:
        found = glob.glob(pattern)
        if found:
            return max(found, key=version)
    return None


# 이 환경의 Chromium 은 에이전트 프록시를 거치지 않아 구글 폰트를 받지 못하고, 조용히
# 대체 글꼴로 그린다(한글 모양이 바뀌어도 오류가 나지 않는다). 그래서 폰트 요청만
# 가로채 curl(프록시·CA 설정을 따른다)로 받아 넘기고, 받은 파일은 캐시해 둔다.
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")
FONT_CACHE = Path(os.environ.get("MOTION_FONT_CACHE", Path.home() / ".cache" / "motion-fonts"))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"


def fetch_cached(url):
    FONT_CACHE.mkdir(parents=True, exist_ok=True)
    f = FONT_CACHE / hashlib.sha1(url.encode()).hexdigest()
    if not f.exists():
        r = subprocess.run(["curl", "-sSfL", "-A", UA, "-o", str(f), url], capture_output=True)
        if r.returncode:
            raise RuntimeError(f"폰트를 받지 못했다: {url}\n{r.stderr.decode(errors='replace')}")
    return f.read_bytes()


def route_fonts(route):
    url = route.request.url
    body = fetch_cached(url)
    ctype = "text/css; charset=utf-8" if "googleapis" in url else "font/woff2"
    route.fulfill(status=200, body=body, headers={"content-type": ctype, "access-control-allow-origin": "*"})


SEEK_JS = """(t) => {
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
  if (window.__seek) window.__seek(t);
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--duration", type=float, default=None)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--still", type=float, default=None, help="이 시각 한 장만 PNG 로 저장(out 은 .png)")
    a = ap.parse_args()
    w, h = map(int, a.size.split("x"))

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        exe = find_chrome()
        br = p.chromium.launch(**({"executable_path": exe} if exe else {}))
        pg = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        for host in FONT_HOSTS:
            pg.route(f"https://{host}/**", route_fonts)
        pg.goto(Path(a.html).resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready.then(() => true)")
        # 글꼴이 실제로 올라왔는지 확인한다 — 대체 글꼴로 그려지면 오류 없이 모양만 바뀐다.
        fams = pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)")
        print("  불러온 글꼴:", sorted(set(fams)) or "없음(시스템 글꼴로 그린다)", file=sys.stderr)
        dur = a.duration or pg.evaluate("window.__duration || null")
        if not dur and a.still is None:
            sys.exit("길이를 모른다 — 페이지에 window.__duration 을 두거나 --duration 을 줄 것")

        if a.still is not None:
            pg.evaluate(SEEK_JS, a.still)
            pg.screenshot(path=a.out)
            print("→", a.out)
            br.close()
            return

        n = int(round(dur * a.fps))
        cmd = [ffmpeg_bin(), "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps),
               "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf),
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(n):
            pg.evaluate(SEEK_JS, i / a.fps)
            ff.stdin.write(pg.screenshot(type="png"))
            if i % (a.fps * 5) == 0:
                print(f"  {i}/{n} 프레임", file=sys.stderr)
        ff.stdin.close()
        rc = ff.wait()
        br.close()
        if rc:
            sys.exit(f"ffmpeg 실패({rc})")
        print(f"→ {a.out} ({n} 프레임, {dur}초, {a.fps}fps)")


if __name__ == "__main__":
    main()
