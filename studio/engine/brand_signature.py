# -*- coding: utf-8 -*-
"""aftermath 낙관(서명) 블록 — 모든 PNG 산출물 한쪽 구석에 고정으로 넣는다.

브랜드 규칙(Aftermath Design System / SKILL.md):
  · 필자 신원 비공개 — 하단 서명은 **워드마크 + ∎ + @irun20000** 고정
  · "after" = #99A1B0, "math"+바 = green #1F7A4D (밝은 지면) / lime #D6FF3F (어두운 지면)
  · 워드마크 최소 가로 24px. 그보다 작아지면 로고마크(원형 심볼)를 쓸 것

원본 자산: Aftermath Design System(작업중)/assets/wordmark-primary-green.svg
글자가 아웃라인 path라 폰트 설치 없이도 100% 정확히 렌더된다.
"""
import pathlib, re

# 자산은 engine/assets/ 로 옮겨졌는데 참조가 형제 파일 그대로 남아 있었다.
# 낙관이 통째로 실패하면 그림에 서명이 안 들어가므로, 두 자리를 다 보고
# 없으면 무엇을 찾았는지 밝히며 멈춘다.
_CANDIDATES = [
    pathlib.Path(__file__).with_name("assets") / "wordmark-primary-green.svg",
    pathlib.Path(__file__).with_name("wordmark-primary-green.svg"),
]
_SRC = next((c for c in _CANDIDATES if c.exists()), _CANDIDATES[0])
_VIEWBOX = "56.4 65.9 471.61 74.25"      # 잉크 tight bbox
_RATIO = 471.61 / 74.25                   # 가로/세로 ≈ 6.35

GREEN, GRAY, LIME = "#1F7A4D", "#99A1B0", "#D6FF3F"


def _inner():
    if not _SRC.exists():
        raise SystemExit("[낙관] 워드마크 SVG 를 찾지 못했다. 찾아본 자리:\n  "
                         + "\n  ".join(str(c) for c in _CANDIDATES))
    s = _SRC.read_text(encoding="utf-8")
    return s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")]


def wordmark_svg(h=19, tone="light"):
    """워드마크 SVG 문자열. h = 높이(px). tone: light | dark"""
    body = _inner()
    if tone == "dark":
        body = body.replace(GREEN, LIME).replace(GRAY, "rgba(255,255,255,.62)")
    w = round(h * _RATIO, 1)
    return (f'<svg class="am-wm" width="{w}" height="{h}" viewBox="{_VIEWBOX}"'
            f' xmlns="http://www.w3.org/2000/svg">{body}</svg>')


CSS = """
.am-sig{display:inline-flex;align-items:center;gap:9px;line-height:1;white-space:nowrap}
.am-sig .am-wm{display:block}
.am-sig .am-qed{display:inline-block;width:6px;height:6px;border-radius:1px}
.am-sig .am-hd{font-family:'DejaVu Sans Mono',monospace;font-weight:700;
  letter-spacing:.01em;font-size:12px}
"""


def signature(h=19, tone="light", handle="@irun20000"):
    """낙관 한 덩어리 — 워드마크 + ∎ + 핸들."""
    if tone == "dark":
        sq, hc = LIME, "rgba(255,255,255,.55)"
    else:
        sq, hc = GREEN, "rgba(10,11,10,.45)"
    return (f'<span class="am-sig {tone}">{wordmark_svg(h, tone)}'
            f'<i class="am-qed" style="background:{sq}"></i>'
            f'<span class="am-hd" style="color:{hc};font-size:{round(h*0.63,1)}px">'
            f'{handle}</span></span>')
