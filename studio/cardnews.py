#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""카드뉴스 스튜디오 CLI — 로컬(클로드 코드) 작업용 단일 진입점.

  python cardnews.py doctor                 환경 점검 (제일 먼저)
  python cardnews.py list                   시리즈·편 목록
  python cardnews.py render 부모노트 EP13    렌더 + 자동검사 + 모아보기
  python cardnews.py audit  부모노트 EP13    렌더 없이 검사만
  python cardnews.py video  부모노트 EP13    5초 MP4 (기본 정책상 사용 안 함)
  python cardnews.py parity 부모노트 EP12    폰트/렌더 동일성 해시 (이관 검증용)
  python cardnews.py gallery                단일 HTML 대시보드
  python cardnews.py web                    호스팅용 정적 폴더
"""
import argparse
import hashlib
import importlib
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent
for _d in ("engine", "contents", "gallery"):
    sys.path.insert(0, str(ROOT / _d))
sys.path.insert(0, str(ROOT))

SERIES = {
    "부모노트": "contents_부모노트",
    "일머리노트": "contents_일머리노트",
    "숫자노트": "contents_숫자노트",
    "발견노트": "contents_발견노트",
}


def _episodes(series):
    """콘텐츠 파일은 두 가지 관례가 섞여 있다.
      · 부모/일머리/발견 : EPn = {folder, prefix, layout, theme, title, content}
      · 숫자             : EPn = content 자체, EPISODES 가 래퍼 dict
    둘 다 EPISODES(래퍼 리스트)는 공통이므로 여기만 쓴다."""
    if series not in SERIES:
        sys.exit(f"알 수 없는 시리즈: {series} (가능: {', '.join(SERIES)})")
    m = importlib.import_module(SERIES[series])
    out = []
    for idx, ep in enumerate(m.EPISODES, 1):
        var = next((k for k, v in vars(m).items() if v is ep and k.startswith("EP")), None)
        out.append((var or f"#{idx}", ep))
    return out


def _load_ep(series, sel=None):
    eps = _episodes(series)
    if not sel:
        return eps[-1][1]
    s = sel.strip().lower()
    for var, ep in eps:
        keys = {var.lower(), str(ep.get("n", "")), ep.get("folder", "").lower(),
                ep.get("prefix", "").lower(), ep.get("title", "").lower()}
        if s in keys or s in ep.get("folder", "").lower():
            return ep
    sys.exit(f"{series} 에서 '{sel}' 를 못 찾았다. `list` 로 확인할 것.")


# ── doctor ────────────────────────────────────────────────────────────────
def cmd_doctor(_):
    ok = True
    print(f"파이썬          {sys.version.split()[0]}  ({sys.executable})")
    if sys.version_info < (3, 10):
        print("  ✗ 3.10 이상 필요"); ok = False

    for mod in ("playwright", "PIL"):
        try:
            importlib.import_module(mod)
            print(f"{mod:15s} 설치됨")
        except ImportError:
            print(f"{mod:15s} ✗ 없음 → pip install -r requirements.txt"); ok = False

    print(f"ffmpeg          {'있음' if shutil.which('ffmpeg') else '없음 (영상 안 만들면 무관)'}")

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={"width": 400, "height": 200})
            pg.set_content("<div id='t' style=\"font-family:'Noto Sans CJK KR';"
                           "font-size:100px;white-space:nowrap\">부모노트</div>")
            pg.wait_for_timeout(200)
            fonts = pg.evaluate("""() => ({
                sans:  document.fonts.check('16px "Noto Sans CJK KR"'),
                serif: document.fonts.check('16px "Noto Serif CJK KR"'),
                mono:  document.fonts.check('16px "Noto Sans Mono CJK KR"'),
                w: Math.round(document.getElementById('t').getBoundingClientRect().width)
            })""")
            b.close()
        print("크로미움        실행됨")
        for k, label in (("sans", "Noto Sans CJK KR"), ("serif", "Noto Serif CJK KR"),
                         ("mono", "Noto Sans Mono CJK KR")):
            mark = "있음" if fonts[k] else "✗ 없음"
            print(f"  {label:22s} {mark}")
            if not fonts[k]:
                ok = False
        print(f"  한글 4자 폭(100px) {fonts['w']}px  ← 기준 환경과 다르면 폰트가 다른 것")
    except Exception as e:
        print(f"크로미움        ✗ 실패: {e}\n                → playwright install chromium"); ok = False

    from paths import OUT_ROOT, DIST
    print(f"산출물 경로      {OUT_ROOT}")
    print(f"갤러리 빌드 경로  {DIST}")
    print("\n" + ("전부 정상. 작업 시작 가능." if ok else "★ 위 ✗ 항목을 먼저 해결할 것."))
    return 0 if ok else 1


# ── list ──────────────────────────────────────────────────────────────────
def cmd_list(_):
    import gallery_meta as G
    for s in SERIES:
        names = [f"{var}({ep['layout']}) {ep['title']}" for var, ep in _episodes(s)]
        nxt = G.NEXT_UP.get(s, {})
        print(f"\n[{s}]  마지막 발행 {G.LAST_PUBLISHED.get(s, '?')}")
        print("  콘텐츠 원본 보유:", ", ".join(names) if names else "없음")
        print(f"  다음 차례: {nxt.get('title', '미정')} · 레이아웃 {nxt.get('layout', '?')}"
              f" · 각도: {nxt.get('angle', '-')}")
    print("\n※ 원본이 없는 과거 편은 재렌더 불가(PNG 만 드라이브에 있음).")
    return 0


# ── render / audit ────────────────────────────────────────────────────────
def _report_audit(a):
    bad = {k: v["issues"] for k, v in a.items() if v["issues"]}
    for k, v in a.items():
        m = v["margins"]
        flag = "  ← " + ", ".join(v["issues"]) if v["issues"] else ""
        print(f"  {k:02d} 여백 L{m['left']:.0f} R{m['right']:.0f} "
              f"T{m['top']:.0f} B{m['bottom']:.0f}{flag}")
    print("검사:", "OK 10/10" if not bad else f"✗ {len(bad)}장 문제 {bad}")
    return not bad


def cmd_render(args):
    import build as B
    import carousel_engine as base
    import layout_archive as L
    ep = _load_ep(args.series, args.episode)
    print(f"렌더 {ep['title']} · {ep['theme']} × 레이아웃 {ep['layout']}")
    d = B.build(ep)
    a = B.audit(ep["content"], base.THEME_BY_ID[ep["theme"]], L.PLANS[ep["layout"]])
    passed = _report_audit(a)
    sheet, size = B.contact_sheet(d, ep["prefix"])
    print(f"출력 → {d}")
    print(f"모아보기 → {sheet} {size}")
    print("\n★ 모아보기를 눈으로 확인할 것. 자동검사는 지저분한 줄바꿈을 못 잡는다.")
    return 0 if passed else 1


def cmd_audit(args):
    import build as B
    import carousel_engine as base
    import layout_archive as L
    ep = _load_ep(args.series, args.episode)
    a = B.audit(ep["content"], base.THEME_BY_ID[ep["theme"]], L.PLANS[ep["layout"]])
    return 0 if _report_audit(a) else 1


def cmd_video(args):
    import makevideo
    from paths import OUT_ROOT
    ep = _load_ep(args.series, args.episode)
    d = OUT_ROOT / ep["folder"]
    print("영상은 2026-08-18 이후 기본 정책상 만들지 않는다. 요청이 있어서 생성한다.")
    print("→", makevideo.build(str(d), ep["prefix"]))
    return 0


def cmd_parity(args):
    """이관 검증 — 같은 편을 렌더해 슬라이드별 해시를 찍는다.
    기존 환경과 값이 다르면 폰트/크로미움 버전이 다른 것이다."""
    import build as B
    from paths import OUT_ROOT
    ep = _load_ep(args.series, args.episode)
    d = pathlib.Path(B.build(ep))
    for i in range(1, 11):
        p = d / f"{ep['prefix']}_{i:02d}.png"
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
        print(f"  {i:02d} {h}  {p.stat().st_size:>8,}B")
    print(f"\n비교 대상: 기존 환경에서 같은 명령을 돌린 결과.\n출력 위치 {OUT_ROOT}")
    return 0


def cmd_gallery(_):
    import build_gallery
    build_gallery.build()
    return 0


def cmd_web(_):
    import build_web
    build_web.build()
    return 0


def main():
    ap = argparse.ArgumentParser(description="카드뉴스 스튜디오 CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor").set_defaults(fn=cmd_doctor)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    for name, fn in (("render", cmd_render), ("audit", cmd_audit),
                     ("video", cmd_video), ("parity", cmd_parity)):
        p = sub.add_parser(name)
        p.add_argument("series", choices=list(SERIES))
        p.add_argument("episode", nargs="?", help="예: EP13 (생략 시 마지막 편)")
        p.set_defaults(fn=fn)
    sub.add_parser("gallery").set_defaults(fn=cmd_gallery)
    sub.add_parser("web").set_defaults(fn=cmd_web)
    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
