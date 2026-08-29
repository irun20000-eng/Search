# -*- coding: utf-8 -*-
"""실험대 — 서가에 올리지 않는 렌더를 여기서 돌린다.

발행 경로(`studio/concept_sheet.py`, 러너 워크플로)는 건드리지 않는다. 여기서
망가지는 것은 `out/` 뿐이고 그 폴더는 git 이 무시한다. 실패를 싸게 만드는 것이
이 폴더의 존재 이유다.

    python3 studio/sandbox/render.py sheet size-bias --plan all
    python3 studio/sandbox/render.py sheet --all --plan B
    python3 studio/sandbox/render.py cuttoon cuttoon-logarithm
    python3 studio/sandbox/render.py same                 # A 판형 동일성 확인

`same` 이 하는 일 — 판형(plan) 을 넣기 전과 후에 A 의 HTML 이 한 바이트도
달라지지 않았는지 본다. 이미 발행된 일곱 장이 A 이므로 이게 깨지면 서가의 그림이
소리 없이 바뀐다. 렌더 없이 문자열만 비교하므로 브라우저가 없어도 돈다.

로컬에서 브라우저를 못 찾으면 `CONCEPT_CHROMIUM` 을 준다 (README 참고).
"""
import argparse
import importlib.util
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
STUDIO = HERE.parent
OUT = HERE / "out"
SPECS = HERE / "specs"

sys.path.insert(0, str(STUDIO / "engine"))
sys.path.insert(0, str(HERE))

DEFAULT_CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# 판형(plan) 이 들어가기 **직전** 커밋. `same` 의 기준은 여기여야 한다.
# HEAD 를 기준으로 삼으면 판형이 머지된 뒤에는 자기 자신과 비교하게 돼
# 언제나 통과하는 가짜 초록이 된다 — 검사가 아니라 위안이다.
BASELINE = "07dd26c"


def use_local_chromium():
    if not os.environ.get("CONCEPT_CHROMIUM") and pathlib.Path(DEFAULT_CHROMIUM).exists():
        os.environ["CONCEPT_CHROMIUM"] = DEFAULT_CHROMIUM


def load_spec(path, name="SPEC"):
    p = pathlib.Path(path)
    s = importlib.util.spec_from_file_location("spec_" + p.stem.replace("-", "_"), p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    if not hasattr(m, name):
        raise SystemExit("%s 에 %s 가 없다" % (p.name, name))
    return getattr(m, name)


# --- 개념 한 장 ------------------------------------------------------------
def cmd_sheet(a):
    import build_concept_sheet as sheet
    src = STUDIO / "concepts"
    slugs = sorted(p.stem for p in src.glob("*.py") if not p.stem.startswith("_"))
    targets = slugs if a.all else ([a.slug] if a.slug else [])
    if not targets:
        raise SystemExit("슬러그를 주거나 --all. 있는 것: %s" % ", ".join(slugs))
    plans = list(sheet.PLAN_CSS) if a.plan == "all" else [a.plan]
    use_local_chromium()
    fail = 0
    for slug in targets:
        spec = load_spec(src / (slug + ".py"))
        for pl in plans:
            out = OUT / ("sheet_%s_%s.png" % (slug, pl))
            print("\n=== %s · 판형 %s ===" % (slug, pl))
            try:
                sheet.build(spec, out, plan=pl)
            except SystemExit as e:      # 넘침·두부는 실험대에서 죽이지 않는다
                fail += 1
                print("  [실패] %s" % e)
    return 1 if fail else 0


# --- 컷툰 ------------------------------------------------------------------
# 진짜 컷아웃이 없어도 **그림이 들어가는 경로가 도는지**는 확인할 수 있어야 한다.
# 아래는 캐릭터가 아니라 그냥 사람 크기의 투명 PNG 다. 배관 점검용이고,
# 진짜 컷아웃이 오면 같은 파일명으로 덮으면 된다.
STUB_COLORS = {"dr-pi": "#1F3A5F", "root": "#9FD8C9", "zero": "#E8B93E",
               "coco": "#C0704A", "mu": "#7A6AA8"}


STUB_MARK = "assets/characters/.stubs"


def _sha1(path):
    import hashlib
    return hashlib.sha1(pathlib.Path(path).read_bytes()).hexdigest()


def make_stubs(force=False):
    d = HERE / "assets" / "characters"
    d.mkdir(parents=True, exist_ok=True)
    need = {k: v for k, v in STUB_COLORS.items()
            if force or not (d / (k + ".png")).exists()}
    if not need:
        return []
    use_local_chromium()
    from playwright.sync_api import sync_playwright
    exe = os.environ.get("CONCEPT_CHROMIUM")
    with sync_playwright() as pw:
        b = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
        for name, c in need.items():
            pg = b.new_page(viewport={"width": 300, "height": 560})
            pg.set_content(
                '<body style="margin:0;background:transparent"><svg width="300" '
                'height="560"><g fill="%s"><circle cx="150" cy="110" r="86"/>'
                '<rect x="72" y="205" width="156" height="250" rx="46"/>'
                '<rect x="106" y="440" width="34" height="110" rx="16"/>'
                '<rect x="160" y="440" width="34" height="110" rx="16"/>'
                '</g></svg></body>' % c)
            pg.screenshot(path=str(d / (name + ".png")), omit_background=True)
            pg.close()
        b.close()
    # 대역이 깔려 있다는 표식을 남긴다. 이게 없으면 다음 사람이 실루엣을
    # 진짜 캐릭터로 착각한 채 만화를 뽑는다 — 렌더는 아무 말도 하지 않는다.
    # 이름만 적으면 진짜 컷아웃으로 덮은 뒤에도 계속 경고해서(거짓 경보) 검사를
    # 못 믿게 된다. 그래서 **그때 그 파일의 해시**를 함께 적고, 파일이 바뀌면
    # 저절로 조용해지게 한다.
    mark = HERE / STUB_MARK
    rec = {}
    if mark.exists():
        for line in mark.read_text(encoding="utf-8").split("\n"):
            bits = line.split()
            if len(bits) == 2:
                rec[bits[0]] = bits[1]
    for name in need:
        rec[name] = _sha1(d / (name + ".png"))
    mark.write_text("".join("%s %s\n" % kv for kv in sorted(rec.items())),
                    encoding="utf-8")
    print("[대역] 임시 실루엣 %d개 생성 — %s" % (len(need), d))
    print("       캐릭터가 아니다. 진짜 컷아웃이 오면 같은 이름으로 덮을 것.")
    return sorted(need)


def warn_stubs():
    """대역이 섞인 채로 렌더되고 있으면 매번 말한다."""
    mark = HERE / STUB_MARK
    if not mark.exists():
        return
    live = []
    for line in mark.read_text(encoding="utf-8").split("\n"):
        bits = line.split()
        if len(bits) != 2:
            continue
        f = HERE / "assets" / "characters" / (bits[0] + ".png")
        if f.exists() and _sha1(f) == bits[1]:   # 덮였으면 해시가 달라 조용해진다
            live.append(bits[0])
    if live:
        print("[대역] ⚠ 지금 쓰이는 %d개는 진짜 캐릭터가 아니라 실루엣이다: %s"
              % (len(live), ", ".join(live)))
        print("       발행용으로 쓰지 말 것. 진짜 컷아웃으로 덮으면 이 경고는 사라진다.")


def cmd_cuttoon(a):
    import cuttoon
    names = ([a.spec] if a.spec else
             [p.stem for p in sorted(SPECS.glob("cuttoon-*.py"))])
    if not names:
        raise SystemExit("specs/cuttoon-*.py 가 없다")
    if a.stubs:
        make_stubs()
    warn_stubs()
    use_local_chromium()
    for n in names:
        spec = load_spec(SPECS / (n + ".py"))
        cuttoon.build(spec, OUT / (n + ".png"), base=HERE, scale=a.scale)
    return 0


# --- A 판형 동일성 ---------------------------------------------------------
# 이미 발행된 다섯 장이 A 판형이다. 판형 기능을 넣으면서 A 의 HTML 이 한 글자라도
# 달라지면 서가의 그림이 소리 없이 바뀐다. "PLAN_CSS['A'] 가 빈 문자열이다" 는
# 주장이 아니라 **증거**로 확인한다 — 옛 모듈(git HEAD)과 지금 모듈로 각각 HTML 을
# 뽑아 바이트로 비교한다.
#
# 스크린샷은 필요 없다. build() 는 HTML 을 먼저 파일로 쓰고 그 다음 playwright 를
# 부르므로, playwright 를 가짜로 갈아 끼워 그 지점에서 멈추면 HTML 만 얻는다.
SENTINEL = "___html_written___"


def _fake_playwright():
    import types
    mod = types.ModuleType("playwright")
    api = types.ModuleType("playwright.sync_api")

    def sync_playwright():
        raise RuntimeError(SENTINEL)

    api.sync_playwright = sync_playwright
    mod.sync_api = api
    return mod, api


def _html_of(module_path, spec, out_png, plan=None):
    """module_path 의 build() 가 쓰는 HTML 문자열을 얻는다."""
    import importlib.util
    import types
    saved = {k: sys.modules.get(k) for k in ("playwright", "playwright.sync_api")}
    mod, api = _fake_playwright()
    sys.modules["playwright"], sys.modules["playwright.sync_api"] = mod, api
    try:
        sp = importlib.util.spec_from_file_location("bcs_" + pathlib.Path(out_png).stem,
                                                    module_path)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        kw = {} if plan is None else {"plan": plan}
        try:
            m.build(spec, out_png, **kw)
        except RuntimeError as e:
            if SENTINEL not in str(e):
                raise
        return pathlib.Path(out_png).with_suffix(".html").read_text(encoding="utf-8")
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v


def cmd_same(a):
    import subprocess
    import build_concept_sheet as sheet
    if sheet.PLAN_CSS.get("A") != "":
        print("[X] A 판형에 CSS 가 붙었다. A 는 빈 문자열이어야 한다.")
        return 1

    repo = STUDIO.parent
    rel = "studio/engine/build_concept_sheet.py"
    ref = a.ref
    old = subprocess.run(["git", "-C", str(repo), "show", "%s:%s" % (ref, rel)],
                         capture_output=True, text=True)
    if old.returncode:
        print("[?] %s 에서 옛 모듈을 못 읽었다 — 비교를 건너뛴다.\n    %s"
              % (ref, old.stderr.strip()))
        return 0
    tmp = OUT / "_old_build_concept_sheet.py"
    tmp.write_text(old.stdout, encoding="utf-8")

    src = STUDIO / "concepts"
    slugs = sorted(p.stem for p in src.glob("*.py") if not p.stem.startswith("_"))
    bad = 0
    for slug in slugs:
        spec = load_spec(src / (slug + ".py"))
        a_html = _html_of(tmp, spec, OUT / ("_same_old_%s.png" % slug))
        b_html = _html_of(STUDIO / "engine" / "build_concept_sheet.py", spec,
                          OUT / ("_same_new_%s.png" % slug), plan="A")
        same = a_html == b_html
        bad += 0 if same else 1
        print("  %-20s %s  (%d자)" % (slug, "동일" if same else "[X] 달라졌다",
                                      len(b_html)))
    if bad:
        print("[X] %d개 스펙에서 A 판형 HTML 이 달라졌다." % bad)
        return 1
    print("[OK] %s 대비 A 판형 HTML 이 %d개 스펙 전부에서 바이트까지 같다." % (ref, len(slugs)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="실험대 렌더")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sheet", help="개념 한 장 (판형 A/B/C)")
    s.add_argument("slug", nargs="?")
    s.add_argument("--all", action="store_true")
    s.add_argument("--plan", default="A")
    s.set_defaults(fn=cmd_sheet)

    c = sub.add_parser("cuttoon", help="A4 여섯 컷 만화")
    c.add_argument("spec", nargs="?")
    c.add_argument("--scale", type=int, default=1)
    c.add_argument("--stubs", action="store_true",
                   help="컷아웃이 없을 때 임시 실루엣을 만들어 배관을 확인한다")
    c.set_defaults(fn=cmd_cuttoon)

    m = sub.add_parser("same", help="A 판형 동일성 확인")
    m.add_argument("--ref", default=BASELINE,
                   help="비교 기준 커밋 (기본: 판형 도입 직전 %s)" % BASELINE)
    m.set_defaults(fn=cmd_same)

    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
