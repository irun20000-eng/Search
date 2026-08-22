# -*- coding: utf-8 -*-
"""렌더 + 자동 품질검사(audit) + 모아보기 이미지."""
import pathlib, sys, tempfile
from PIL import Image
import carousel_engine as base
import layout_archive as L

SAFE_X, SAFE_Y = 96, 104

# "/tmp/..." 는 윈도우에서 드라이브가 없는 경로가 되어 as_uri() 가 터진다.
# 이 리포는 윈도우에서도 돌아가야 하므로 표준 임시폴더를 쓴다.
TMP = pathlib.Path(tempfile.gettempdir())
W, H = 1080, 1350


def audit(C, theme, plan):
    """페이지를 띄워 슬라이드별 규격·넘침·안전여백을 검사한다."""
    from playwright.sync_api import sync_playwright
    html = L.build_html_v2(C, theme, plan)
    p = TMP / "_audit.html"; p.write_text(html, encoding="utf-8")
    js = """
    (i) => {
      const s = document.querySelector('#s'+i);
      const r = s.getBoundingClientRect();
      const pad = s.querySelector('.pad');
      const issues = [];
      if (Math.round(r.width) !== 1080 || Math.round(r.height) !== 1350)
        issues.push('규격 ' + Math.round(r.width) + 'x' + Math.round(r.height));
      if (pad.scrollHeight > pad.clientHeight + 1)
        issues.push('세로 넘침 ' + (pad.scrollHeight - pad.clientHeight) + 'px');
      let worst = {top: 9999, bottom: 9999, left: 9999, right: 9999};
      s.querySelectorAll('.pad *').forEach(el => {
        if (!el.textContent.trim() && !el.classList.contains('tick')) return;
        if (el.children.length && el.textContent.trim()) return;   // 잎 노드만
        const b = el.getBoundingClientRect();
        if (b.width === 0 || b.height === 0) return;
        worst.top = Math.min(worst.top, b.top - r.top);
        worst.left = Math.min(worst.left, b.left - r.left);
        worst.bottom = Math.min(worst.bottom, r.bottom - b.bottom);
        worst.right = Math.min(worst.right, r.right - b.right);
      });
      if (worst.left < 95) issues.push('좌여백 ' + Math.round(worst.left));
      if (worst.right < 95) issues.push('우여백 ' + Math.round(worst.right));
      if (worst.top < 103) issues.push('상여백 ' + Math.round(worst.top));
      if (worst.bottom < 103) issues.push('하여백 ' + Math.round(worst.bottom));
      return {issues: issues, margins: worst};
    }
    """
    out = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(p.as_uri()); pg.wait_for_timeout(400)
        for i in range(1, 11):
            out[i] = pg.evaluate(js, i)
        b.close()
    return out


def linecount(C, theme, plan, selector):
    """지정 셀렉터 요소들의 줄 수를 센다 (줄바꿈 지저분함 점검용)."""
    from playwright.sync_api import sync_playwright
    html = L.build_html_v2(C, theme, plan)
    p = TMP / "_lines.html"; p.write_text(html, encoding="utf-8")
    js = """
    (sel) => Array.from(document.querySelectorAll(sel)).map(el => {
      const cs = getComputedStyle(el);
      let lh = parseFloat(cs.lineHeight);
      if (isNaN(lh)) lh = parseFloat(cs.fontSize) * 1.2;
      return [el.textContent.trim().slice(0,24), Math.round(el.getBoundingClientRect().height / lh)];
    })
    """
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(p.as_uri()); pg.wait_for_timeout(300)
        res = pg.evaluate(js, selector)
        b.close()
    return res


def contact_sheet(outdir, prefix, cell_w=430, gap=10, margin=10):
    """10장을 5×2로 이어붙인 모아보기 이미지."""
    paths = [f"{outdir}/{prefix}_{i:02d}.png" for i in range(1, 11)]
    cell_h = round(cell_w * H / W)
    sheet_w = margin * 2 + cell_w * 5 + gap * 4
    sheet_h = margin * 2 + cell_h * 2 + gap
    sheet = Image.new("RGB", (sheet_w, sheet_h), (24, 26, 30))
    for idx, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS)
        x = margin + (idx % 5) * (cell_w + gap)
        y = margin + (idx // 5) * (cell_h + gap)
        sheet.paste(im, (x, y))
    out = f"{outdir}/{prefix}_모아보기.png"
    sheet.save(out)
    return out, sheet.size


def build(ep, outroot=None):
    if outroot is None:
        from paths import OUT_ROOT
        outroot = str(OUT_ROOT)
    theme = base.THEME_BY_ID[ep["theme"]]
    plan = L.PLANS[ep["layout"]]
    outdir = f"{outroot}/{ep['folder']}"
    L.render_v2(ep["content"], theme, plan, range(1, 11), outdir, ep["prefix"])
    return outdir


# 실행은 repo 루트의 cardnews.py CLI 를 쓴다 (python cardnews.py render 부모노트 EP12)
