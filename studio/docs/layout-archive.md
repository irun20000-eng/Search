# 레이아웃 아카이브 (Stage 2)

슬라이드를 **기능**으로 보고, 기능마다 배치 **변형**을 보유한다.
같은 브랜드·같은 글이라도 변형을 바꾸면 구성이 달라진다 → 템플릿 반복 제거.

## 기능 × 변형

| 기능 | 슬라이드 | 변형 | 설명 |
|---|---|---|---|
| `cover` | 1 | `left` · `center` · `fullbleed` | 좌하단 정렬 / 중앙 / 풀블리드 대형 타이포 |
| `text` | 2·3·4·8 | `left` · `center` | 좌정렬 / 중앙정렬 |
| `contrast` | 5 | `cols` · `stack` · `vs` | 2단 세로분할 / 상하 분할(칩) / VS 박스(↔) |
| `steps` | 6 | `vertical` · `cards` · `timeline` | 세로 스텝 / 카드 / 가로 타임라인 |
| `rows` | 7 | `divider` · `numbered` | 구분선 행 / 번호형 |
| `check` | 9 | `box` · `numbered` · `toggle` | 체크박스 / 번호 배지 / 토글 알약 |
| `cta` | 10 | `box` · `center` | 박스형 / 중앙 강조형 |

## 레이아웃 플랜 (구성 프리셋)

변형을 일관되게 묶은 세트. 플랜만 바꾸면 덱 전체 인상이 바뀐다.

| 플랜 | 결 | cover | contrast | steps | rows | check | cta |
|---|---|---|---|---|---|---|---|
| **A 정렬형** | 클래식·안정 | left | cols | vertical | divider | box | box |
| **B 센터 임팩트** | 강하고 단순 | center | stack | cards | numbered | numbered | center |
| **C 구조 강조** | 도식·정보형 | fullbleed | vs | timeline | numbered | toggle | box |

## 사용

```python
from carousel_engine import CONTENT, THEME_BY_ID
from layout_archive import PLANS, auto_plan, render_v2

# 1) 명시적 플랜
render_v2(CONTENT, THEME_BY_ID["editorial_ink"], PLANS["C"], range(1,11), "out", "에디_C")

# 2) 자동 회전 (생성마다 다른 구성)
render_v2(CONTENT, THEME_BY_ID["bold_social"], auto_plan(seed=3), range(1,11), "out", "볼드_auto")

# 3) 커스텀 (변형 직접 조합)
my = {"cover":"center","text":"left","contrast":"vs","steps":"cards",
      "rows":"divider","check":"toggle","cta":"box"}
render_v2(CONTENT, THEME_BY_ID["magazine_noir"], my, range(1,11), "out", "매거진_커스텀")
```

## 변형 추가하는 법
1. `layout_archive.py`의 해당 렌더러(`_steps`, `_contrast` 등)에 `elif v=="새변형":` 분기 추가
2. 필요한 CSS를 `EXTRA_CSS`에 추가
3. `LAYOUT_VARIANTS`의 기능 목록에 변형 id 등록
4. (선택) 새 플랜을 `PLANS`에 추가

## 조합 수
브랜드 6 × 플랜 3 = **18 기본형**.
`auto_plan`까지 쓰면 cover3·text2·contrast3·steps3·rows2·check3·cta2 = **648 구성** × 6 브랜드.
→ 사실상 반복되지 않는다.
