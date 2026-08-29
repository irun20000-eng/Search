# -*- coding: utf-8 -*-
"""컷툰 시험분 — 로그는 어떻게 태어났나.

내용은 서가의 `math/notes/concept-logarithm/note.md` 에서만 가져왔다. 만화라고
사실을 무르게 하지 않는다 — 연도·쪽수는 그 노트의 인용 [1][2][3] 이 받친다.
그림은 아직 없다. 각 컷의 shot 이 그대로 Flow 프롬프트의 씨앗이다.
"""

SPEC = {
    "ep": "EP.001",
    "title": "곱셈을 덧셈으로 바꾼 사람",
    "logo": "Q.E.D.",
    # 행 높이 비율 — 도입을 크게, 전개를 고르게, 마무리를 조금 낮게.
    # 여섯 컷이 전부 같은 높이면 만화가 아니라 표로 읽힌다.
    "rows": [1.2, .95, .95, 1],
    "panels": [
        {
            "wide": True,
            "cast": ["코코"],
            "shot": "1600년경 천문 관측실. 책상 위에 여덟 자리 숫자가 빼곡한 종이 더미, "
                    "촛불, 지친 표정. 창밖은 새벽.",
            "figures": [{"src": "assets/characters/coco.png", "h": 76}],
            "stage": "flex-end",
            "bubbles": [{"t": "여덟 자리 곱셈이 아직 스물세 개 남았어…", "at": "top l"}],
            "narr": "계산이 사람을 잡아먹던 시절이 있었다.",
        },
        {
            "cast": ["루트"],
            "shot": "루트가 종이 한 장을 들고 고개를 갸웃. 배경은 단순한 크림색.",
            # 말풍선이 왼쪽 위이므로 인물은 오른쪽에 세운다(얼굴 가림 검사가 잡았다).
            "figures": [{"src": "assets/characters/root.png", "h": 78}],
            "stage": "flex-end",
            "bubbles": [{"t": "곱셈을 덧셈으로 바꿀 수는 없나요?", "at": "top l"}],
        },
        {
            "cast": ["닥터파이"],
            "shot": "닥터파이가 칠판에 두 줄을 나란히 적는다. 위는 2·4·8·16, "
                    "아래는 1·2·3·4. 두 줄을 잇는 화살표.",
            "figures": [{"src": "assets/characters/dr-pi.png", "h": 80}],
            "stage": "flex-start",
            "bubbles": [{"t": "위는 곱해 가고 아래는 더해 가지. 이 둘을 짝지으면?",
                         "at": "top r"}],
            "fx": "짝!",
        },
        {
            "cast": ["닥터파이", "제로"],
            "shot": "1614년 에든버러. 작고 낡은 책 한 권을 펼쳐 보인다. "
                    "앞쪽은 글, 뒤쪽은 숫자표가 빽빽하다.",
            "figures": [{"src": "assets/characters/dr-pi.png", "h": 62},
                        {"src": "assets/characters/zero.png", "h": 56}],
            "stage": "space-between",
            "bubbles": [{"t": "네이피어의 『기술』. 설명 57쪽, 표가 90쪽이야.", "at": "top l"}],
            "narr": "로그는 함수가 아니라 표로 태어났다.",
        },
        {
            "cast": ["뮤"],
            "shot": "브리그스가 네이피어에게 손가락 열 개를 펴 보이는 장면. "
                    "둘 사이에 '10' 이 크게.",
            "figures": [{"src": "assets/characters/mu.png", "h": 74}],
            "bubbles": [{"t": "밑을 10으로 하면 어떨까요?", "at": "top r"}],
            "narr": "브리그스가 제안하고, 그 방대한 계산을 스스로 떠맡았다 — 1624년 『로그 산술』.",
            "narr_at": "l",
        },
        {
            "wide": True,
            "cast": ["코코", "루트", "닥터파이"],
            "shot": "같은 책상. 종이 더미가 얇아지고 로그표 한 권만 남았다. 창밖은 아침.",
            "figures": [{"src": "assets/characters/coco.png", "h": 70},
                        {"src": "assets/characters/root.png", "h": 66},
                        {"src": "assets/characters/dr-pi.png", "h": 72}],
            "stage": "space-between",
            # 마지막 컷은 말풍선을 아래로 내린다 — 여섯 컷 내내 왼쪽 위만 보면
            # 시선이 굳는다.
            "bubbles": [{"t": "곱셈 스물세 개가… 덧셈 스물세 개가 됐어!", "at": "bot l"}],
            "fx": "✓",
        },
    ],
    "credit_l": "Q.E.D. 프렌즈 — 이룬 서재 수학사",
    "credit_r": "출처: 개념 노트 「로그」 · 제작: Search/studio/sandbox",
}
