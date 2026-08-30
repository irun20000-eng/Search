# -*- coding: utf-8 -*-
"""카드뉴스 판 컷툰 — 1080×1350, 장당 두 컷.

같은 스펙에서 두 가지 물건이 나온다.
    cuttoon.py  A4 세로 한 면에 여섯 컷      — 인쇄·PDF·학습지
    cards.py    카드뉴스 여러 장, 장당 두 컷  — 인스타·블로그 스와이프

**원본은 하나다.** `specs/cuttoon-*.py` 를 두 판형이 함께 읽는다. 대사를 고치면
두 산출물이 같이 바뀐다 — 카드뉴스용 대사를 따로 두면 그 순간 갈라지고, 어느 쪽이
맞는지 아무도 모르게 된다(카드뉴스 갤러리가 2026-08-17 에 그렇게 갈렸다).

--- 왜 판형이 따로 필요한가 ---------------------------------------------------
A4 는 여섯 컷을 **한눈에** 보여 준다. 판면 리듬(통컷·2×2)이 읽는 속도를 만든다.
카드뉴스는 반대다 — 한 번에 두 컷만 보이고 **손가락으로 넘긴다.** 그래서
  · 컷이 커진다(1000×555). 작은 화면에서 대사가 읽혀야 한다.
  · 장마다 '지금 어디쯤인가'가 필요하다(섹션 이름 + 01/03 + 점).
  · 마지막에 다음 장으로 미는 신호가 필요하다(넘겨보기 →).

--- 스펙에서 더 쓰는 것 -------------------------------------------------------
    "pages": ["도입", "발견", "완성"]   # 장별 섹션 이름(두 컷 묶음마다 하나)
없으면 번호만 나온다. 나머지 키(panels·bubbles·narr·fx·scene·figures)는 A4 와 같다.
"""
import os
import pathlib

import scenes
from cuttoon import esc

W, H = 1080, 1350
PER_PAGE = 2

CSS = r"""
:root{--mustard:#E8B93E;--navy:#1F3A5F;--mint:#9FD8C9;--cream:#FAF6EE;--gray:#8A8F98}
*{margin:0;padding:0;box-sizing:border-box;forced-color-adjust:none;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{width:1080px}
body{height:1350px;background:var(--cream);
  font-family:"Pretendard","Noto Sans CJK KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  display:flex;flex-direction:column;padding:40px;word-break:keep-all}

/* 머리 — 섹션 이름과 지금 자리. 카드뉴스는 한 번에 두 컷만 보이므로
   '무엇을 읽는 중인가'를 장마다 다시 말해 줘야 한다. */
.head{display:flex;align-items:baseline;justify-content:space-between;
  padding-bottom:14px;border-bottom:5px solid var(--navy);margin-bottom:20px}
.head .kicker{font-size:34px;font-weight:800;color:var(--navy);letter-spacing:-1px}
.head .kicker .ep{color:var(--mustard);margin-right:10px;font-size:26px}
.head .pg{font-size:22px;font-weight:800;color:var(--gray);letter-spacing:.16em}

.cuts{flex:1;display:flex;flex-direction:column;gap:22px}
.cut{position:relative;flex:1;background:#fff;border:4px solid var(--navy);
  border-radius:20px;overflow:hidden}
/* 통컷은 낮게 앉힌다 — 장면이 A4 통컷 비율(1128×430 · 1128×359)로 그려져 있어
   정사각에 가까운 칸에 넣으면 양옆이 잘려 나가고 소품이 인물 뒤로 숨는다.
   칸을 눕히면 원래 구도가 거의 그대로 들어오고, 남은 높이는 옆 컷이 가져간다
   (그 컷은 대개 인물 하나뿐이라 넓을수록 낫다). */
.cut.wide{flex:.62}
.cut>.scene{position:absolute;inset:0;z-index:0}
.cut>.scene svg{width:100%;height:100%;display:block}
.cut>img.bg{width:100%;height:100%;object-fit:cover;display:block}
.ground{position:absolute;left:0;right:0;bottom:0;height:22%;z-index:0;
  background:linear-gradient(#F3EFE6 0%, #EAE4D6 100%)}
.stage{position:absolute;inset:0;display:flex;align-items:flex-end;
  padding:0 6% 5%;gap:4%}
.stage img{height:64%;width:auto;object-fit:contain;display:block;
  filter:drop-shadow(0 6px 0 rgba(31,58,95,.10))}

.num{position:absolute;top:16px;left:16px;z-index:3;width:52px;height:52px;
  border-radius:50%;background:var(--mustard);color:var(--navy);display:flex;
  align-items:center;justify-content:center;font-weight:800;font-size:28px;
  border:4px solid var(--navy)}

/* 말풍선 — A4 보다 크게. 손바닥만 한 화면에서 이것부터 읽힌다. */
.bubble{position:absolute;z-index:2;max-width:74%;background:#fff;
  border:4px solid var(--navy);border-radius:22px;padding:14px 22px;
  font-size:30px;font-weight:700;line-height:1.35;color:#222;
  box-shadow:3px 4px 0 rgba(31,58,95,.25)}
.bubble::after{content:"";position:absolute;bottom:-18px;left:34px;
  border:10px solid transparent;border-top-color:var(--navy)}
.bubble.right::after{left:auto;right:34px}
.bubble.top{top:18px}
.bubble.top.l{left:82px}      /* 번호와 겹치지 않게 */
.bubble.top.r{right:18px}
.bubble.bot{bottom:18px}
.bubble.bot.l{left:18px}
.bubble.bot.r{right:18px}
.bubble.bot::after{bottom:auto;top:-18px;
  border-top-color:transparent;border-bottom-color:var(--navy)}

/* 해설 띠 — 대사가 건너뛴 것을 메운다. 학습만화의 나레이션이다. */
.narr{position:absolute;z-index:2;left:0;right:0;bottom:0;background:var(--navy);
  color:#fff;padding:14px 24px;font-size:24px;font-weight:500;line-height:1.4}
.fx{position:absolute;z-index:2;right:24px;bottom:96px;font-size:42px;font-weight:900;
  color:var(--mustard);-webkit-text-stroke:3px var(--navy);transform:rotate(-6deg)}
.fx.l{right:auto;left:24px;transform:rotate(5deg)}
.ph{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:12px;padding:80px 40px 40px;text-align:center;
  background:repeating-linear-gradient(45deg,#eee,#eee 16px,#f7f7f7 16px,#f7f7f7 32px);
  color:var(--gray)}
.ph .cast{font-size:32px;font-weight:800;color:var(--navy)}
.ph .shot{font-size:22px;font-weight:500;line-height:1.5;max-width:84%}

/* 발 — 어디까지 왔는지와 다음으로 미는 신호 */
.foot{margin-top:18px;display:flex;align-items:center;justify-content:space-between}
.dots{display:flex;gap:10px}
.dot{width:12px;height:12px;border-radius:50%;background:#D8D0C2}
.dot.on{width:34px;border-radius:999px;background:var(--navy)}
.swipe{font-size:22px;font-weight:700;color:var(--gray)}
.credit{font-size:19px;color:var(--gray)}
"""


def cut_html(p, i, base):
    """컷 하나. A4 판과 같은 자리(scene·figures·img)를 읽되 카드 판형으로 조판한다."""
    n = p.get("n", i + 1)
    cls = "cut" + (" wide" if p.get("wide") else "")
    missing = []
    body = ""
    if p.get("img"):
        f = pathlib.Path(base, p["img"])
        if f.exists():
            body = '<img class="bg" src="%s" alt="">' % f.resolve().as_uri()
        else:
            missing.append(p["img"])
    if not body and p.get("scene"):
        svg = scenes.get(p["scene"])
        if svg:
            body = '<div class="scene">%s</div>' % svg
        else:
            missing.append("scene:" + p["scene"])

    figs = []
    for g in p.get("figures") or []:
        f = pathlib.Path(base, g["src"])
        if f.exists():
            # A4 의 h(컷 높이 대비 %)를 그대로 쓰면 카드 컷이 더 커서 인물이 과하게
            # 커진다. 카드 컷 높이에 맞춰 한 단 낮춘다.
            figs.append('<img src="%s" style="height:%s%%" alt="">'
                        % (f.resolve().as_uri(), round(g.get("h", 70) * 0.9)))
        else:
            missing.append(g["src"])
    if figs:
        has_bg = bool(p.get("img") or p.get("scene"))
        if p.get("ground", not has_bg):
            body += '<div class="ground"></div>'
        body += ('<div class="stage" style="justify-content:%s">%s</div>'
                 % (p.get("stage", "center"), "".join(figs)))
    if not body:
        cast = " · ".join(p.get("cast") or []) or "—"
        body = ('<div class="ph"><div class="cast">%s</div>'
                '<div class="shot">%s</div></div>'
                % (esc(cast), esc(p.get("shot", ""))))

    bub = "".join(
        '<div class="bubble {at}{r}">{t}</div>'.format(
            at=b.get("at", "top l"),
            r=" right" if b.get("at", "top l").strip().endswith("r") else "",
            t=esc(b["t"]))
        for b in p.get("bubbles", []))
    # 해설 띠는 카드 판에서 컷 아래를 가로지른다 — A4 의 작은 상자와 달리
    # 스와이프로 읽을 때는 이것이 본문 노릇을 한다.
    narr = '<div class="narr">%s</div>' % esc(p["narr"]) if p.get("narr") else ""
    fx = ('<div class="fx %s">%s</div>' % (p.get("fx_at", ""), esc(p["fx"]))
          if p.get("fx") else "")
    return (f'<div class="{cls}"><div class="num">{n}</div>'
            f'{body}{bub}{narr}{fx}</div>'), missing


def build(spec, out_dir, base=None, scale=1, stem="cards"):
    base = base or pathlib.Path(__file__).resolve().parent
    panels = spec.get("panels") or []
    pages = [panels[i:i + PER_PAGE] for i in range(0, len(panels), PER_PAGE)]
    kickers = spec.get("pages") or []
    total = len(pages)
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright
    made, missing = [], set()
    with sync_playwright() as pw:
        exe = os.environ.get("CONCEPT_CHROMIUM")
        b = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
        for pi, cuts in enumerate(pages):
            html_cuts = ""
            for ci, c in enumerate(cuts):
                h, ms = cut_html(c, pi * PER_PAGE + ci, base)
                html_cuts += h
                missing |= set(ms)
            kicker = kickers[pi] if pi < len(kickers) else ""
            dots = "".join('<div class="dot%s"></div>' % (" on" if k == pi else "")
                           for k in range(total))
            doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
 <div class="head">
  <div class="kicker"><span class="ep">{esc(spec.get('ep',''))}</span>{esc(kicker)}</div>
  <div class="pg">{pi + 1:02d} / {total:02d}</div>
 </div>
 <div class="cuts">{html_cuts}</div>
 <div class="foot">
  <div class="dots">{dots}</div>
  <div class="swipe">{'넘겨보기 →' if pi + 1 < total else 'Q.E.D.'}</div>
 </div>
 <div class="foot"><div class="credit">{esc(spec.get('credit_l',''))}</div></div>
</body></html>"""
            out = out_dir / f"{stem}-{pi + 1:02d}.png"
            hp = out.with_suffix(".html")
            hp.write_text(doc, encoding="utf-8")
            pg.goto(hp.as_uri())
            pg.wait_for_timeout(350)
            if pi == 0:
                # 개념 한 장·A4 판과 같은 두부 검사. 폰트가 없으면 한글이 네모가 되고
                # 자동 검사는 그걸 못 잡는다.
                r = pg.evaluate("""()=>{const c=document.createElement('canvas').getContext('2d');
                  c.font="100px 'Noto Sans CJK KR','Malgun Gothic',sans-serif";
                  return {ko:Math.round(c.measureText('가나다라마바사').width),
                          tofu:Math.round(c.measureText('').width)}}""")
                if r["ko"] == r["tofu"]:
                    b.close()
                    raise SystemExit("[카드] 한글 폰트가 없다 — fonts-noto-cjk 를 설치할 것.")
            over = pg.evaluate("()=>document.body.scrollHeight - %d" % H)
            clip = pg.evaluate("""()=>{
              let out=[];
              document.querySelectorAll('.cut').forEach((c,i)=>{
                const cb=c.getBoundingClientRect();
                c.querySelectorAll('.bubble,.narr').forEach(e=>{
                  const b=e.getBoundingClientRect();
                  const d=Math.max(cb.top-b.top, b.bottom-cb.bottom,
                                   cb.left-b.left, b.right-cb.right);
                  if(d>1) out.push({cut:i+1, t:e.textContent.slice(0,14), px:Math.round(d)});
                });
              });
              return out;}""")
            pg.screenshot(path=str(out))
            made.append((out, over, clip))
        b.close()

    print("[카드] %d장 · %d×%d" % (len(made), W, H))
    for out, over, clip in made:
        flags = []
        if over > 1:
            flags.append("지면 넘침 %dpx" % over)
        for c in clip:
            flags.append("컷%d '%s' %dpx 밀림" % (c["cut"], c["t"], c["px"]))
        print("   %-22s %s" % (out.name, " · ".join(flags) if flags else "[OK]"))
    if missing:
        print("   그림 없음: %s" % ", ".join(sorted(missing)))
    return 0
