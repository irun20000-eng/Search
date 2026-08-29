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
 "rows": [1.15, 1, .9],           # 행 높이 비율 — 판면에 리듬을 준다(생략 시 균등)
 "panels": [ {
     "n": 1,                       # 컷 번호(생략 시 순서)
     "wide": True,                 # 한 행 전체
     "tall": True,                 # 두 행 높이
     "cast": ["닥터파이", "루트"],  # 등장 인물 — 자리표에 그대로 찍힌다
     "shot": "연출 지시 한 줄",      # Flow 프롬프트의 씨앗
     "img": "assets/bg/....png",   # 컷 전체를 채우는 그림(cover)
     "figures": [                  # 배경 없는 컷아웃을 바닥에 세운다
         {"src": "assets/characters/dr-pi.png", "h": 74}   # h = 컷 높이 대비 %
     ],
     "stage": "center"|"flex-start"|"flex-end"|"space-between",
     "bubbles": [ {"t": 대사, "at": "top l"|"top r"|"bot l"|"bot r"} ],
     "narr": "나레이션",  "narr_at": "l"|"r",  "fx": "효과음",  "fx_at": "l"|"r",
 } × 6 ],
 "credit_l": "...", "credit_r": "...",
}

--- 왜 리듬이 필요한가 --------------------------------------------------------
첫 판은 여섯 컷이 전부 같은 높이였고 말풍선이 전부 왼쪽 위였다. 그러면 눈이 매 컷
같은 자리에 떨어져서 **만화가 아니라 표**로 읽힌다. rows·tall 로 컷 크기를 흔들고
말풍선 자리를 위아래로 나눠 시선이 지면을 훑게 한다.
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
.panel.tall{grid-row:span 2}
.panel>img.bg{width:100%;height:100%;object-fit:cover;display:block}
/* 컷아웃 무대 — 배경 없는 인물 PNG 를 컷 바닥에 세운다.
   전신 그림(cover)과 달리 컷아웃은 잘라 채우면 안 되므로 contain 으로 둔다. */
.stage{position:absolute;inset:0;display:flex;align-items:flex-end;
  padding:0 5% 5%;gap:3%}
/* 바닥 띠 — 컷아웃만 있는 컷은 인물이 흰 허공에 뜬다. 옅은 띠 하나로 설 자리를
   만들어 준다. Flow 배경 그림(img)이 들어오면 필요 없으므로 그때는 끈다. */
.ground{position:absolute;left:0;right:0;bottom:0;height:22%;z-index:0;
  background:linear-gradient(#F3EFE6 0%, #EAE4D6 100%)}
.stage img{height:70%;width:auto;object-fit:contain;display:block;
  filter:drop-shadow(0 5px 0 rgba(31,58,95,.10))}
.panel .ph{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:10px;padding:64px 28px 28px;text-align:center;
  background:repeating-linear-gradient(45deg,#eee,#eee 14px,#f7f7f7 14px,#f7f7f7 28px);
  color:var(--gray)}
.panel .ph .cast{font-size:26px;font-weight:800;color:var(--navy)}
.panel .ph .shot{font-size:18px;font-weight:500;line-height:1.5;max-width:86%}
.panel .ph .no{font-size:15px;font-weight:700;letter-spacing:.14em}
.panel .ph .miss{margin-top:6px;font-size:16px;font-weight:700;color:#C0392B}
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
.bubble.top.l{left:60px}      /* 컷 번호(.num)와 겹치지 않게 */
.bubble.top.r{right:12px}
/* 아래쪽 말풍선 — 꼬리가 위를 향한다. 위아래를 섞어야 시선이 컷마다 움직인다. */
.bubble.bot{bottom:12px}
.bubble.bot.l{left:12px}
.bubble.bot.r{right:12px}
.bubble.bot::after{bottom:auto;top:-14px;
  border-top-color:transparent;border-bottom-color:var(--navy)}
.narr{position:absolute;z-index:2;bottom:10px;left:10px;background:var(--navy);
  color:#fff;padding:8px 14px;border-radius:6px;font-size:19px;font-weight:500;
  max-width:70%}
.narr.r{left:auto;right:10px}
.fx{position:absolute;z-index:2;right:14px;bottom:12px;font-size:30px;font-weight:900;
  color:var(--mustard);-webkit-text-stroke:2px var(--navy);transform:rotate(-6deg)}
.fx.l{right:auto;left:14px;transform:rotate(5deg)}
.credit{margin-top:22px;display:flex;justify-content:space-between;
  font-size:18px;color:var(--gray)}
"""


def esc(t):
    return _html.escape(str(t), quote=False)


def panel_html(p, i, base):
    n = p.get("n", i + 1)
    cls = "panel" + (" wide" if p.get("wide") else "") + (" tall" if p.get("tall") else "")

    # 그림 자리 — 셋 중 하나. 파일이 없으면 조용히 깨지는 대신 자리표로 되돌린다.
    #   img     컷 전체를 채우는 그림(cover)
    #   figures 배경 없는 컷아웃을 바닥에 세운다(contain)
    #   없으면  cast·shot 이 적힌 자리표
    missing = []
    body = ""
    if p.get("img"):
        f = pathlib.Path(base, p["img"])
        if f.exists():
            body = '<img class="bg" src="%s" alt="">' % f.resolve().as_uri()
        else:
            missing.append(p["img"])
    figs = []
    for g in p.get("figures") or []:
        f = pathlib.Path(base, g["src"])
        if f.exists():
            figs.append('<img src="%s" style="height:%s%%" alt="">'
                        % (f.resolve().as_uri(), g.get("h", 70)))
        else:
            missing.append(g["src"])
    if figs:
        if p.get("ground", True):
            body += '<div class="ground"></div>'
        body += ('<div class="stage" style="justify-content:%s">%s</div>'
                 % (p.get("stage", "center"), "".join(figs)))
    if not body:
        cast = " · ".join(p.get("cast") or []) or "—"
        note = ""
        if missing:
            note = ('<div class="miss">그림 없음 — %s</div>'
                    % esc(" · ".join(pathlib.Path(m).name for m in missing)))
        body = (f'<div class="ph"><div class="no">PANEL {n}</div>'
                f'<div class="cast">{esc(cast)}</div>'
                f'<div class="shot">{esc(p.get("shot", ""))}</div>{note}</div>')

    bub = "".join(
        '<div class="bubble {at}{r}">{t}</div>'.format(
            at=b.get("at", "top l"),
            r=" right" if b.get("at", "top l").strip().endswith("r") else "",
            t=esc(b["t"]))
        for b in p.get("bubbles", []))
    narr = ('<div class="narr %s">%s</div>' % (p.get("narr_at", ""), esc(p["narr"]))
            if p.get("narr") else "")
    fx = ('<div class="fx %s">%s</div>' % (p.get("fx_at", ""), esc(p["fx"]))
          if p.get("fx") else "")
    return (f'<div class="{cls}"><div class="num">{n}</div>'
            f'{body}{bub}{narr}{fx}</div>'), missing


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
    made = [panel_html(pp, i, base) for i, pp in enumerate(spec["panels"])]
    panels = "".join(h for h, _ in made)
    missing = sorted({m for _, ms in made for m in ms})
    rows = spec.get("rows")
    rowcss = ("<style>.grid{grid-template-rows:%s;grid-auto-rows:unset}</style>"
              % " ".join("%sfr" % r for r in rows)) if rows else ""
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>{CSS}</style>{rowcss}</head><body>
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
        overlap = pg.evaluate(OVERLAP_JS)
        face = pg.evaluate(FACE_JS)
        sizes = pg.evaluate(SIZES_JS)
        pg.screenshot(path=str(p))
        b.close()
    if over > 0 or clip:
        print("[컷툰] 넘침 — 지면 +%dpx, 컷 밖으로 밀린 것 %s" % (over, clip))
    report_panels(sizes, overlap, face, missing)
    print("[컷툰] %d컷 -> %s" % (len(spec["panels"]), p))
    return p


# --- 겹침과 리듬 ------------------------------------------------------------
# 디자인 검토(2026-08-29)에서 나온 두 가지를 숫자로 만든 것이다.
#   ① 겹침 — "아무것도 겹치지 않는다"는 눈으로만 보면 매번 놓친다. 말풍선·나레이션·
#      효과음은 전부 absolute 라 서로 모르고 앉는다. 픽셀로 재서 보고한다.
#   ② 리듬 — 여섯 컷이 전부 같은 높이면 만화가 아니라 표로 읽힌다. 컷 높이가
#      몇 종류인지 세서, 한 종류뿐이면 짚어 준다.
OVERLAP_JS = """()=>{
  const out=[];
  document.querySelectorAll('.panel').forEach((p,i)=>{
    const es=[...p.querySelectorAll('.bubble,.narr,.fx')];
    for(let a=0;a<es.length;a++)for(let b=a+1;b<es.length;b++){
      const r=es[a].getBoundingClientRect(), q=es[b].getBoundingClientRect();
      const w=Math.min(r.right,q.right)-Math.max(r.left,q.left);
      const h=Math.min(r.bottom,q.bottom)-Math.max(r.top,q.top);
      if(w>0&&h>0) out.push((i+1)+'번 컷 '+es[a].className.split(' ')[0]
                            +' x '+es[b].className.split(' ')[0]
                            +' '+Math.round(w)+'x'+Math.round(h)+'px');
    }
  });
  return out;}"""

# 말풍선이 인물의 **머리**를 덮는지 본다. 몸통을 조금 가리는 것은 만화에서 흔한
# 연출이지만 얼굴을 가리면 컷이 죽는다. 컷아웃 상단 30% 를 머리로 본다.
FACE_JS = """()=>{
  const out=[];
  document.querySelectorAll('.panel').forEach((p,i)=>{
    p.querySelectorAll('.stage img').forEach(f=>{
      const r=f.getBoundingClientRect();
      const head={left:r.left,right:r.right,top:r.top,bottom:r.top+r.height*0.30};
      const area=(head.right-head.left)*(head.bottom-head.top);
      p.querySelectorAll('.bubble,.narr').forEach(e=>{
        const q=e.getBoundingClientRect();
        const w=Math.min(head.right,q.right)-Math.max(head.left,q.left);
        const h=Math.min(head.bottom,q.bottom)-Math.max(head.top,q.top);
        if(w>0&&h>0&&area>0){
          const pct=Math.round(w*h/area*100);
          if(pct>=12) out.push((i+1)+'번 컷 '+e.className.split(' ')[0]
                               +' 가 얼굴 '+pct+'% 를 덮는다');
        }
      });
    });
  });
  return out;}"""

SIZES_JS = """()=>{
  const g=document.querySelector('.grid');
  const rows=getComputedStyle(g).gridTemplateRows.split(' ').filter(Boolean).length;
  let used=0;
  const list=[...document.querySelectorAll('.panel')].map(e=>{
    used += (e.classList.contains('wide')?2:1) * (e.classList.contains('tall')?2:1);
    const r=e.getBoundingClientRect();
    return {w:Math.round(r.width), h:Math.round(r.height)};
  });
  return {panels:list, cells:rows*2, used:used};}"""


def report_panels(sizes, overlap, face, missing):
    panels = sizes["panels"]
    hs = sorted({s["h"] for s in panels})
    print("[컷툰] 컷 크기 %s" % " · ".join("%dx%d" % (s["w"], s["h"]) for s in panels))
    # 격자의 빈칸 — wide/tall 을 섞으면 마지막 줄에 구멍이 남는데, 렌더를 눈으로
    # 봐야만 보인다. 칸 수를 세면 숫자로 잡힌다.
    if sizes["used"] < sizes["cells"]:
        print("  [X] 격자에 빈칸 %d칸 (칸 %d · 쓴 것 %d) — 지면에 구멍이 남는다."
              % (sizes["cells"] - sizes["used"], sizes["cells"], sizes["used"]))
    if len(hs) == 1:
        print("  [!] 컷 높이가 %dpx 한 종류뿐이다 — 만화가 아니라 표로 읽힌다."
              % hs[0])
        print("      rows(행 높이 비율)나 tall(두 행 차지)로 리듬을 줄 것.")
    else:
        print("  [OK] 컷 높이 %d종 — 판면에 리듬이 있다." % len(hs))
    if overlap:
        print("  [X] 겹침 %d건: %s" % (len(overlap), " / ".join(overlap)))
    else:
        print("  [OK] 말풍선·나레이션·효과음 겹침 없음")
    if face:
        print("  [X] 얼굴 가림 %d건: %s" % (len(face), " / ".join(face)))
    elif any(s["h"] for s in panels):
        print("  [OK] 말풍선이 인물 얼굴을 덮지 않는다")
    if missing:
        print("  [!] 그림 파일 없음 %d개 — 자리표로 대체했다: %s"
              % (len(missing), ", ".join(missing)))
    return not (overlap or face)
