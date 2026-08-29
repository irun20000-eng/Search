# -*- coding: utf-8 -*-
"""컷툰 — A4 한 면(1240×1754)에 만화 여섯 컷.

Shorts_Flow(비공개 리포·드라이브 사본 `19Glc5hs8h3UXhOahDmm6V4jo3PFMRzG1`)의
`templates/cuttoon-a4.html` 을 그대로 옮겨 온 것이다. 손으로 텍스트를 갈아 끼우던
템플릿을 **스펙 한 덩어리 → 렌더** 로 바꾼 것만 다르다. 판형·색·말풍선 꼬리 위치까지
원본과 같게 두었다 — 이미 그 톤으로 그려진 QED프렌즈 컷과 나란히 놓아야 하기 때문.

--- 왜 그림이 아니라 자리부터 만드나 ------------------------------------------
그림은 사용자가 구글 Flow(Nano Banana Pro)에서 만든다. 모델은 한글을 정확히 못 쓰므로
**말풍선·나레이션·효과음은 그림에 넣지 않고** 여기 HTML 이 얹는다. 그래서 순서가
    ① 여기서 컷 구성과 대사를 확정하고 자리표(placeholder)로 렌더
    ② 자리표에 적힌 '연출 지시'를 그대로 Flow 에 넣어 그림을 받고
    ③ 스펙의 img 에 파일 경로를 채워 다시 렌더
가 된다. ①에서 이미 읽을 수 있는 한 장이 나오는 것이 요점이다.

--- spec 스키마 ---------------------------------------------------------------
{
 "ep": "EP.001", "title": "제목", "logo": "Q.E.D.",
 "panels": [ {
     "n": 1,                       # 컷 번호(생략 시 순서)
     "wide": True,                 # 한 행 전체
     "cast": ["닥터파이", "루트"],  # 등장 인물 — 자리표에 그대로 찍힌다
     "shot": "연출 지시 한 줄",      # Flow 프롬프트의 씨앗
     "img": "assets/characters/....png",   # 있으면 자리표 대신 그림
     "bubbles": [ {"t": 대사, "at": "top l"|"top r"} ],
     "narr": "나레이션",  "fx": "효과음",
 } × 6 ],
 "credit_l": "...", "credit_r": "...",
}
"""
import html as _html
import os
import pathlib

W, H = 1240, 1754

CSS = r"""
:root{--mustard:#E8B93E;--navy:#1F3A5F;--mint:#9FD8C9;--cream:#FAF6EE;--gray:#8A8F98}
*{margin:0;padding:0;box-sizing:border-box;forced-color-adjust:none;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:A4 portrait;margin:0}
html,body{width:1240px}
body{height:1754px;background:var(--cream);
  font-family:"Pretendard","Noto Sans CJK KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  display:flex;flex-direction:column;padding:48px 56px 36px;word-break:keep-all}
.title-bar{display:flex;align-items:baseline;justify-content:space-between;
  border-bottom:6px solid var(--navy);padding-bottom:14px;margin-bottom:24px}
.title-bar h1{font-size:44px;color:var(--navy);letter-spacing:-1px}
.title-bar h1 .ep{color:var(--mustard);margin-right:12px}
.title-bar .logo{font-size:26px;font-weight:800;color:#fff;background:var(--navy);
  border-radius:999px;padding:8px 22px}
.grid{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:16px}
.panel{position:relative;background:#fff;border:4px solid var(--navy);
  border-radius:14px;overflow:hidden}
.panel.wide{grid-column:1 / -1}
.panel img{width:100%;height:100%;object-fit:cover;display:block}
.panel .ph{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:10px;padding:64px 28px 28px;text-align:center;
  background:repeating-linear-gradient(45deg,#eee,#eee 14px,#f7f7f7 14px,#f7f7f7 28px);
  color:var(--gray)}
.panel .ph .cast{font-size:26px;font-weight:800;color:var(--navy)}
.panel .ph .shot{font-size:18px;font-weight:500;line-height:1.5;max-width:86%}
.panel .ph .no{font-size:15px;font-weight:700;letter-spacing:.14em}
.num{position:absolute;top:10px;left:10px;z-index:3;width:40px;height:40px;
  border-radius:50%;background:var(--mustard);color:var(--navy);display:flex;
  align-items:center;justify-content:center;font-weight:800;font-size:22px;
  border:3px solid var(--navy)}
.bubble{position:absolute;z-index:2;max-width:62%;background:#fff;
  border:3px solid var(--navy);border-radius:18px;padding:10px 16px;
  font-size:22px;font-weight:600;line-height:1.35;color:#222;
  box-shadow:2px 3px 0 rgba(31,58,95,.25)}
.bubble::after{content:"";position:absolute;bottom:-14px;left:28px;
  border:8px solid transparent;border-top-color:var(--navy)}
.bubble.right::after{left:auto;right:28px}
.bubble.top{top:12px}
.bubble.top.l{left:60px}
.bubble.top.r{right:12px}
.narr{position:absolute;z-index:2;bottom:10px;left:10px;background:var(--navy);
  color:#fff;padding:8px 14px;border-radius:6px;font-size:19px;font-weight:500;
  max-width:70%}
.fx{position:absolute;z-index:2;right:14px;bottom:12px;font-size:30px;font-weight:900;
  color:var(--mustard);-webkit-text-stroke:2px var(--navy);transform:rotate(-6deg)}
.credit{margin-top:22px;display:flex;justify-content:space-between;
  font-size:18px;color:var(--gray)}
"""


def esc(t):
    return _html.escape(str(t), quote=False)


def panel_html(p, i, base):
    n = p.get("n", i + 1)
    cls = "panel wide" if p.get("wide") else "panel"

    if p.get("img"):
        src = pathlib.Path(base, p["img"]).resolve()
        body = f'<img src="{src.as_uri()}" alt="">'
    else:
        cast = " · ".join(p.get("cast") or []) or "—"
        body = (f'<div class="ph"><div class="no">PANEL {n}</div>'
                f'<div class="cast">{esc(cast)}</div>'
                f'<div class="shot">{esc(p.get("shot", ""))}</div></div>')

    bub = "".join(
        '<div class="bubble {at}{r}">{t}</div>'.format(
            at=b.get("at", "top l"),
            r=" right" if b.get("at", "").endswith("r") else "",
            t=esc(b["t"]))
        for b in p.get("bubbles", []))
    narr = f'<div class="narr">{esc(p["narr"])}</div>' if p.get("narr") else ""
    fx = f'<div class="fx">{esc(p["fx"])}</div>' if p.get("fx") else ""
    return (f'<div class="{cls}"><div class="num">{n}</div>'
            f'{body}{bub}{narr}{fx}</div>')


def check(spec):
    """렌더 전에 걸러 낼 수 있는 것만 본다."""
    ps = spec.get("panels") or []
    if not ps:
        raise SystemExit("[컷툰] panels 가 비었다")
    # 2단 격자라 wide 가 아닌 컷이 홀수면 마지막 줄에 빈칸이 남는다.
    narrow = sum(0 if p.get("wide") else 1 for p in ps)
    if narrow % 2:
        print("[컷툰] 주의 — 좁은 컷이 %d개(홀수)라 마지막 줄 한 칸이 빈다." % narrow)
    for i, p in enumerate(ps, 1):
        if not p.get("img") and not p.get("shot"):
            print("[컷툰] 주의 — %d번 컷에 연출 지시(shot)가 없다." % i)
    return True


def build(spec, out_png, base=None, scale=1):
    base = base or pathlib.Path(__file__).resolve().parent
    check(spec)
    panels = "".join(panel_html(p, i, base) for i, p in enumerate(spec["panels"]))
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
 <div class="title-bar">
  <h1><span class="ep">{esc(spec.get('ep',''))}</span>{esc(spec.get('title',''))}</h1>
  <div class="logo">{esc(spec.get('logo','Q.E.D.'))}</div>
 </div>
 <div class="grid">{panels}</div>
 <div class="credit"><span>{esc(spec.get('credit_l',''))}</span>
  <span>{esc(spec.get('credit_r',''))}</span></div>
</body></html>"""

    p = pathlib.Path(out_png).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    h = p.with_suffix(".html")
    h.write_text(doc, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        exe = os.environ.get("CONCEPT_CHROMIUM")
        b = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
        pg.goto(h.as_uri()); pg.wait_for_timeout(400)
        # 개념 한 장과 같은 두부 검사 — 한글 폰트가 없으면 네모로 그려진다.
        r = pg.evaluate("""()=>{const c=document.createElement('canvas').getContext('2d');
          c.font="100px 'Noto Sans CJK KR','Malgun Gothic',sans-serif";
          return {ko:Math.round(c.measureText('가나다라마바사').width),
                  tofu:Math.round(c.measureText('').width)}}""")
        if r["ko"] == r["tofu"]:
            b.close()
            raise SystemExit("[컷툰] 한글 폰트가 없다 — fonts-noto-cjk 를 설치할 것.")
        over = pg.evaluate("()=>document.body.scrollHeight - %d" % H)
        # 말풍선은 높이가 고정이 아니라 글이 길면 늘어난다 — 잘리는 게 아니라
        # **컷 밖으로 밀려나는** 것이 문제다. 컷은 overflow:hidden 이라 밀려난 만큼
        # 그냥 사라진다. 그래서 자식 상자가 컷 테두리를 넘는지를 잰다.
        # (말풍선 꼬리 ::after 는 일부러 14px 내려 그린 것이라 세지 않는다.)
        clip = pg.evaluate("""()=>{
          const out=[];
          document.querySelectorAll('.panel').forEach((p,i)=>{
            const pr=p.getBoundingClientRect();
            p.querySelectorAll('.bubble,.narr,.fx').forEach(e=>{
              const r=e.getBoundingClientRect();
              const d=Math.round(Math.max(r.bottom-pr.bottom, r.right-pr.right,
                                          pr.top-r.top, pr.left-r.left));
              if(d>0) out.push((i+1)+'번 컷 .'+e.className.split(' ')[0]+' +'+d);
            });
          });
          return out;}""")
        pg.screenshot(path=str(p))
        b.close()
    if over > 0 or clip:
        print("[컷툰] 넘침 — 지면 +%dpx, 잘린 블록 %s" % (over, clip))
    print("[컷툰] %d컷 -> %s" % (len(spec["panels"]), p))
    return p
