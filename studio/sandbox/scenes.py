# -*- coding: utf-8 -*-
"""컷 배경을 코드로 그린다 — 생성형 이미지 없이 컷툰을 완성하는 길.

왜 이게 있나
------------
컷툰 가이드(`Shorts_Flow/guidelines/cuttoon-guide.md`)의 정본 공정은
**컷별 프롬프트 → 사용자가 구글 Flow 로 그림 생성 → 조립**이다. 그림 생성이
사람 손에 묶여 있어서, 그 한 칸이 비면 컷툰이 자리표로 멈춘다.

여기는 그 칸을 **코드로 채우는** 두 번째 길이다. 인물은 이미 QED프렌즈
컷아웃(`figures`)으로 들어가므로, 배경만 있으면 컷이 선다. 그리고 배경은
평면 벡터라 SVG 로 그리기에 알맞다.

덤이 하나 있다 — **글자가 정확하다.** 가이드가 "수식·기호는 이미지에 그리게
하지 말고 조립 단계에서 오버레이하라"고 정해 둔 이유가 생성 모델이 한글·숫자를
못 쓰기 때문인데, SVG 로 그리면 애초에 그 문제가 없다. 컷 3 의 칠판 숫자가
그 예다.

규약
----
- 함수 하나가 컷 하나를 그린다. 반환값은 `<svg>` 문자열.
- **viewBox 는 그 컷의 실제 픽셀 크기**로 잡는다(렌더가 찍어 주는 값:
  통컷 1128x430 / 보통컷 556x341 / 마지막 통컷 1128x359). 그래야 좌표를
  머리로 계산하지 않고 눈에 보이는 대로 놓을 수 있다.
- 색은 컷툰 CSS 와 같은 팔레트만 쓴다. 새 색을 들이지 않는다.
- **말풍선·나레이션 자리는 비워 둔다.** 말풍선은 불투명하지만, 그 밑에 그림이
  빽빽하면 컷이 답답해진다. 각 함수의 주석에 그 자리를 적어 둔다.
"""

# 컷툰 CSS 와 같은 값(:root). 여기서 새 색을 만들지 않는다.
NAVY = "#1F3A5F"
MUSTARD = "#E8B93E"
MINT = "#9FD8C9"
CREAM = "#FAF6EE"
GRAY = "#8A8F98"

WALL = "#F1EADC"      # 벽 — 크림보다 한 톤 눌러 컷 안에서 인물이 뜨게 한다
FLOOR = "#E4DAC6"     # 바닥 띠
WOOD = "#B0865A"      # 책상
WOOD_D = "#8A6844"    # 책상 그늘
PAPER = "#FCFAF4"     # 종이


def _svg(w, h, inner):
    """컷을 꽉 채우는 SVG. object-fit:cover 와 같게 slice 로 자른다."""
    return (
        f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" '
        f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{inner}</svg>'
    )


def _papers(x, y, n=4, w=54, step=3):
    """종이 더미 — 얇은 판을 겹쳐 쌓고 숫자 줄을 흉내 낸 잔선을 얹는다."""
    out = []
    for i in range(n):
        yy = y - i * step
        out.append(
            f'<rect x="{x}" y="{yy}" width="{w}" height="{step + 1}" rx="1" '
            f'fill="{PAPER}" stroke="{NAVY}" stroke-width="1.2" opacity=".95"/>'
        )
    return "".join(out)


def _numlines(x, y, w, rows=4, gap=7):
    """숫자표 흉내 — 글자를 쓰지 않고 잔선으로만 '빽빽함'을 만든다."""
    out = []
    for i in range(rows):
        yy = y + i * gap
        out.append(
            f'<rect x="{x}" y="{yy}" width="{w}" height="2" rx="1" '
            f'fill="{NAVY}" opacity=".38"/>'
        )
    return "".join(out)


# ──────────────────────────────────────────────────────────────
# 컷 1 — 1600년경 천문 관측실, 새벽 (통컷 1128x430)
#   비워 둘 자리: 상단 왼쪽(말풍선 x60~640,y12~60) · 하단 왼쪽(나레이션)
#   인물: 코코가 오른쪽 끝(flex-end)
# ──────────────────────────────────────────────────────────────
def observatory_dawn():
    w, h = 1128, 430
    floor_y = 352
    s = [
        f'<rect width="{w}" height="{h}" fill="{WALL}"/>',
        # 바닥
        f'<rect y="{floor_y}" width="{w}" height="{h - floor_y}" fill="{FLOOR}"/>',
        f'<rect y="{floor_y}" width="{w}" height="3" fill="{NAVY}" opacity=".18"/>',
        # ── 아치창 (새벽) — 말풍선 아래로 내려 앉힌다
        '<defs>'
        '<linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2C4568"/>'
        '<stop offset=".55" stop-color="#6E7C93"/>'
        '<stop offset="1" stop-color="#E0B98C"/>'
        '</linearGradient></defs>',
        f'<path d="M252 268 V168 a76 76 0 0 1 152 0 V268 Z" fill="url(#dawn)" '
        f'stroke="{NAVY}" stroke-width="7"/>',
        # 창살
        f'<rect x="324" y="96" width="7" height="172" fill="{NAVY}" opacity=".85"/>',
        f'<rect x="252" y="212" width="152" height="6" fill="{NAVY}" opacity=".85"/>',
        # 새벽 별 둘
        '<circle cx="292" cy="140" r="3" fill="#FDF6E6" opacity=".9"/>',
        '<circle cx="368" cy="122" r="2.2" fill="#FDF6E6" opacity=".7"/>',
        # 창턱
        f'<rect x="240" y="266" width="176" height="9" rx="3" fill="{WOOD}" '
        f'stroke="{NAVY}" stroke-width="3"/>',
        # ── 책상
        f'<rect x="470" y="296" width="392" height="14" rx="4" fill="{WOOD}" '
        f'stroke="{NAVY}" stroke-width="4"/>',
        f'<rect x="470" y="310" width="392" height="8" fill="{WOOD_D}"/>',
        f'<rect x="492" y="318" width="14" height="{floor_y - 318}" fill="{WOOD_D}"/>',
        f'<rect x="826" y="318" width="14" height="{floor_y - 318}" fill="{WOOD_D}"/>',
        # 종이 더미 셋 — 여덟 자리 숫자가 빼곡하다는 것을 잔선으로만
        _papers(506, 292, n=7, w=86, step=4),
        _numlines(514, 252, 70, rows=3, gap=6),
        _papers(614, 294, n=5, w=74, step=4),
        _papers(706, 293, n=6, w=68, step=4),
        # ── 촛불 — 지친 새벽의 유일한 광원
        f'<rect x="806" y="252" width="16" height="44" rx="3" fill="{PAPER}" '
        f'stroke="{NAVY}" stroke-width="3"/>',
        f'<rect x="798" y="292" width="32" height="7" rx="3" fill="{MUSTARD}" '
        f'stroke="{NAVY}" stroke-width="3"/>',
        f'<ellipse cx="814" cy="242" rx="8" ry="13" fill="{MUSTARD}"/>',
        '<ellipse cx="814" cy="245" rx="3.4" ry="6" fill="#FFF3D0"/>',
        f'<circle cx="814" cy="243" r="34" fill="{MUSTARD}" opacity=".13"/>',
    ]
    return _svg(w, h, "".join(s))


# ──────────────────────────────────────────────────────────────
# 컷 2 — 단순한 크림 배경 (556x341)
#   스펙이 "배경은 단순한 크림색"이라 적어 두었다. 그 지시를 지키고,
#   인물이 허공에 뜨지 않을 만큼만 바닥과 굽도리를 넣는다.
# ──────────────────────────────────────────────────────────────
def plain_room():
    w, h = 556, 341
    floor_y = 268
    s = [
        f'<rect width="{w}" height="{h}" fill="{WALL}"/>',
        f'<rect y="{floor_y}" width="{w}" height="{h - floor_y}" fill="{FLOOR}"/>',
        f'<rect y="{floor_y}" width="{w}" height="3" fill="{NAVY}" opacity=".16"/>',
        # 스펙이 "배경은 단순한 크림색"이라 적어 두었다. 이야기 소품은 놓지 않는다 —
        # 종이 한 장을 놓아 봤더니 종이로 읽히지 않고 흰 막대로만 보였다.
        #
        # 다만 A4 에서는 이 정도로 충분했는데 카드 판형(1000×700)으로 커지자
        # 그냥 빈 벽이 됐다. 그래서 '이야기'가 아니라 '건축'만 더한다 —
        # 굽도리 선과 창빛 한 조각. 무엇도 설명하지 않지만 방으로는 읽힌다.
        f'<rect y="{floor_y - 26}" width="{w}" height="4" fill="{NAVY}" opacity=".08"/>',
        f'<path d="M96 {floor_y} L150 {h} L392 {h} L308 {floor_y} Z" '
        f'fill="{MUSTARD}" opacity=".10"/>',
    ]
    return _svg(w, h, "".join(s))


# ──────────────────────────────────────────────────────────────
# 컷 3 — 칠판: 위는 곱해 가고 아래는 더해 간다 (556x341)
#   비워 둘 자리: 상단 오른쪽(말풍선 2줄, y12~95) · 하단 오른쪽(효과어 "짝!")
#   인물: 닥터파이가 왼쪽 끝(flex-start) → 칠판은 가운데~오른쪽
#   ★ 여기가 코드 배경의 값이 가장 큰 컷이다. 생성 모델은 이 숫자를 못 쓴다.
# ──────────────────────────────────────────────────────────────
def blackboard_pairing():
    w, h = 556, 341
    floor_y = 276
    # 오른쪽 가장자리에 붙지 않게 폭을 줄였다(첫 판에서 테두리에 닿았다).
    bx, by, bw, bh = 190, 104, 316, 150
    num = ('font-family="Pretendard,Noto Sans CJK KR,sans-serif" '
           'font-weight="800" font-size="27" fill="#FDFBF4"')
    top = [2, 4, 8, 16]
    bot = [1, 2, 3, 4]
    xs = [bx + 50, bx + 124, bx + 198, bx + 272]
    s = [
        f'<rect width="{w}" height="{h}" fill="{WALL}"/>',
        f'<rect y="{floor_y}" width="{w}" height="{h - floor_y}" fill="{FLOOR}"/>',
        f'<rect y="{floor_y}" width="{w}" height="3" fill="{NAVY}" opacity=".16"/>',
        # 칠판 — 나무틀 + 짙은 판
        f'<rect x="{bx - 9}" y="{by - 9}" width="{bw + 18}" height="{bh + 18}" rx="7" '
        f'fill="{WOOD}" stroke="{NAVY}" stroke-width="4"/>',
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3" fill="#2A3F39"/>',
    ]
    # 윗줄 — 곱해 간다
    for x, v in zip(xs, top):
        s.append(f'<text x="{x}" y="{by + 52}" text-anchor="middle" {num}>{v}</text>')
    # 아랫줄 — 더해 간다
    for x, v in zip(xs, bot):
        s.append(f'<text x="{x}" y="{by + 126}" text-anchor="middle" {num}>{v}</text>')
    # 두 줄을 잇는 세로 화살표
    for x in xs:
        s.append(f'<path d="M{x} {by + 66} V{by + 96}" stroke="{MUSTARD}" '
                 f'stroke-width="3.4" marker-end="url(#ar)"/>')
    # ×2 / +1 라벨
    lab = ('font-family="Pretendard,Noto Sans CJK KR,sans-serif" '
           f'font-weight="700" font-size="15" fill="{MUSTARD}"')
    for i in range(3):
        mx = (xs[i] + xs[i + 1]) / 2
        s.append(f'<text x="{mx}" y="{by + 30}" text-anchor="middle" {lab}>×2</text>')
        s.append(f'<text x="{mx}" y="{by + 146}" text-anchor="middle" {lab}>+1</text>')
    s.insert(0,
             '<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" '
             'markerWidth="5" markerHeight="5" orient="auto">'
             f'<path d="M0 0 L10 5 L0 10 z" fill="{MUSTARD}"/></marker></defs>')
    # 분필 받침
    s.append(f'<rect x="{bx - 9}" y="{by + bh + 9}" width="{bw + 18}" height="8" rx="3" '
             f'fill="{WOOD_D}" stroke="{NAVY}" stroke-width="3"/>')
    s.append(f'<rect x="{bx + 22}" y="{by + bh + 11}" width="22" height="4" rx="2" fill="#FDFBF4"/>')
    return _svg(w, h, "".join(s))


# ──────────────────────────────────────────────────────────────
# 컷 4 — 네이피어 『기술』: 설명 57쪽, 표가 90쪽 (556x341)
#   비워 둘 자리: 상단 왼쪽(말풍선) · 하단 왼쪽(나레이션)
#   인물: 닥터파이·제로가 양끝(space-between) → 책은 가운데
#   왼쪽 면은 글, 오른쪽 면은 숫자표. 그 두께 차이가 이 컷의 요점이다.
# ──────────────────────────────────────────────────────────────
def napier_book():
    w, h = 556, 341
    floor_y = 272
    cx, top = 278, 150
    s = [
        f'<rect width="{w}" height="{h}" fill="{WALL}"/>',
        f'<rect y="{floor_y}" width="{w}" height="{h - floor_y}" fill="{FLOOR}"/>',
        f'<rect y="{floor_y}" width="{w}" height="3" fill="{NAVY}" opacity=".16"/>',
        # 받침대
        f'<rect x="{cx - 108}" y="{top + 96}" width="216" height="11" rx="4" '
        f'fill="{WOOD}" stroke="{NAVY}" stroke-width="3.4"/>',
        # 펼친 책 — 두 면
        f'<path d="M{cx} {top + 92} L{cx - 104} {top + 78} V{top} L{cx} {top + 14} Z" '
        f'fill="{PAPER}" stroke="{NAVY}" stroke-width="4"/>',
        f'<path d="M{cx} {top + 92} L{cx + 104} {top + 78} V{top} L{cx} {top + 14} Z" '
        f'fill="{PAPER}" stroke="{NAVY}" stroke-width="4"/>',
        f'<path d="M{cx} {top + 14} V{top + 92}" stroke="{NAVY}" stroke-width="4"/>',
    ]
    # 왼쪽 면 — 글(설명 57쪽): 성긴 줄
    for i in range(6):
        y = top + 26 + i * 10
        s.append(f'<rect x="{cx - 92}" y="{y}" width="74" height="2.6" rx="1" '
                 f'fill="{NAVY}" opacity=".34"/>')
    # 오른쪽 면 — 숫자표(표가 90쪽): 촘촘한 격자
    for r in range(9):
        y = top + 24 + r * 7.4
        for c in range(4):
            s.append(f'<rect x="{cx + 18 + c * 20}" y="{y}" width="15" height="3.2" rx="1" '
                     f'fill="{NAVY}" opacity=".44"/>')
    # 첫 판에는 밀랍 봉인(노란 원)을 놓았는데, 받침대 옆에 떠서 뜻 없이 보였다.
    # 소품 하나가 컷을 설명하지 못하면 없는 편이 낫다.
    return _svg(w, h, "".join(s))


# ──────────────────────────────────────────────────────────────
# 컷 5 — 밑을 10으로 (556x341)
#   비워 둘 자리: 상단 오른쪽(말풍선) · 하단 왼쪽(나레이션)
#   인물: 뮤가 가운데 → 큰 10 은 왼쪽 위, 나레이션 위로
# ──────────────────────────────────────────────────────────────
def base_ten():
    w, h = 556, 341
    floor_y = 272
    s = [
        f'<rect width="{w}" height="{h}" fill="{WALL}"/>',
        f'<rect y="{floor_y}" width="{w}" height="{h - floor_y}" fill="{FLOOR}"/>',
        f'<rect y="{floor_y}" width="{w}" height="3" fill="{NAVY}" opacity=".16"/>',
        # 큰 10 — 원 안에 앉혀 배경이 아니라 '제안'으로 읽히게. 왼쪽 자리는
        # 뮤(가운데)와 말풍선(오른쪽 위) 어디와도 부딪히지 않는다.
        f'<circle cx="92" cy="146" r="60" fill="{MINT}" opacity=".55"/>',
        f'<circle cx="92" cy="146" r="60" fill="none" stroke="{NAVY}" stroke-width="5"/>',
        '<text x="92" y="171" text-anchor="middle" '
        'font-family="Pretendard,Noto Sans CJK KR,sans-serif" font-weight="800" '
        f'font-size="74" fill="{NAVY}">10</text>',
    ]
    # 오른쪽 — 스스로 떠맡은 '방대한 계산'. 표를 쌓아 두께로만 말한다.
    # (첫 판에는 손가락 열 개를 세로 막대로 그렸는데, 가운데 선 뮤의 몸통을
    #  그대로 관통했다. 인물이 서는 자리에는 소품을 놓지 않는다.)
    for k in range(3):
        bx, by = 424 + k * 6, 128 + k * 34
        s.append(f'<rect x="{bx}" y="{by}" width="104" height="30" rx="3" '
                 f'fill="{PAPER}" stroke="{NAVY}" stroke-width="3"/>')
        for r in range(3):
            s.append(f'<rect x="{bx + 9}" y="{by + 7 + r * 7}" width="86" height="2.4" '
                     f'rx="1" fill="{NAVY}" opacity=".40"/>')
    return _svg(w, h, "".join(s))


# ──────────────────────────────────────────────────────────────
# 컷 6 — 같은 책상, 아침 (통컷 1128x359)
#   비워 둘 자리: 하단 왼쪽(말풍선 bot l) · 하단 오른쪽(효과어 ✓)
#   인물: 셋이 좌·중·우(space-between) → 배경은 창과 빛으로 넓게
#   컷 1 과 같은 방을 아침으로 되받는다. 종이 더미가 로그표 한 권이 됐다.
# ──────────────────────────────────────────────────────────────
def observatory_morning():
    w, h = 1128, 359
    floor_y = 292
    s = [
        '<defs>'
        '<linearGradient id="morn" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#BEE0EE"/>'
        '<stop offset="1" stop-color="#FBEBCB"/>'
        '</linearGradient></defs>',
        f'<rect width="{w}" height="{h}" fill="#F6F0E4"/>',
        f'<rect y="{floor_y}" width="{w}" height="{h - floor_y}" fill="{FLOOR}"/>',
        f'<rect y="{floor_y}" width="{w}" height="3" fill="{NAVY}" opacity=".16"/>',
    ]
    # 아치창 둘 — 아침 빛.
    # 첫 판에는 왼쪽 창을 x=128 에 두었는데 왼쪽 끝에 선 코코가 통째로 가렸다.
    # 세 인물이 좌·중·우로 서므로 창은 **인물 사이 빈 자리**로 옮긴다.
    # 창(y 126~220)과 책상(y 238~292)은 세로로 안 겹치므로 같은 x 에 겹쳐 앉힌다 —
    # 컷 1 처럼 '책상 위의 창'이 되어 같은 방이라는 것이 읽힌다.
    for x in (300, 800):
        s += [
            f'<path d="M{x} 214 V126 a62 62 0 0 1 124 0 V214 Z" fill="url(#morn)" '
            f'stroke="{NAVY}" stroke-width="6"/>',
            f'<rect x="{x + 59}" y="64" width="6" height="150" fill="{NAVY}" opacity=".8"/>',
            f'<rect x="{x}" y="168" width="124" height="5" fill="{NAVY}" opacity=".8"/>',
            f'<rect x="{x - 10}" y="212" width="144" height="8" rx="3" fill="{WOOD}" '
            f'stroke="{NAVY}" stroke-width="3"/>',
        ]
    # 빛 기둥 — 창에서 바닥으로
    for x in (300, 800):
        s.append(f'<path d="M{x + 22} 218 L{x - 24} {floor_y} L{x + 158} {floor_y} '
                 f'L{x + 134} 218 Z" fill="{MUSTARD}" opacity=".12"/>')
    # 낮은 책상 하나와 그 위의 로그표 한 권 — 더미가 아니라 '한 권'.
    # 첫 판에는 책상을 한가운데(452~668)에 두었는데 가운데 선 루트가 책을 가려
    # 노란 조각만 보였다. 세 인물이 좌·중·우로 서므로 그 사이로 옮긴다.
    s += [
        f'<rect x="296" y="238" width="188" height="12" rx="4" fill="{WOOD}" '
        f'stroke="{NAVY}" stroke-width="4"/>',
        f'<rect x="312" y="250" width="12" height="{floor_y - 250}" fill="{WOOD_D}"/>',
        f'<rect x="456" y="250" width="12" height="{floor_y - 250}" fill="{WOOD_D}"/>',
        # 책 한 권 (닫힌 채로 — 표가 한 권으로 정리됐다는 뜻)
        f'<rect x="336" y="200" width="86" height="38" rx="4" fill="{NAVY}"/>',
        f'<rect x="346" y="207" width="68" height="24" rx="2" fill="{PAPER}"/>',
        f'<rect x="336" y="200" width="13" height="38" rx="4" fill="{MUSTARD}" '
        f'stroke="{NAVY}" stroke-width="2.6"/>',
    ]
    return _svg(w, h, "".join(s))


SCENES = {
    "observatory-dawn": observatory_dawn,
    "plain-room": plain_room,
    "blackboard-pairing": blackboard_pairing,
    "napier-book": napier_book,
    "base-ten": base_ten,
    "observatory-morning": observatory_morning,
}


def get(name):
    """스펙이 부른 이름으로 장면을 그린다. 없는 이름이면 None — 부르는 쪽이
    자리표로 되돌린다(조용히 빈 배경으로 넘어가지 않게)."""
    fn = SCENES.get(name)
    return fn() if fn else None
