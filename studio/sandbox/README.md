# studio/sandbox — 시각화 실험대

**발행되지 않는 자리다.** manifest 에도 갤러리에도 올라가지 않는다.
여기서 마음껏 부수고, 마음에 드는 것만 정식 슬러그로 옮긴다.

## 왜 만들었나

지금까지 시각화를 시험하려면 **발행된 개념 한 장 7편 중 하나를 건드려야** 했다.
실패가 비싸니 시험을 안 하게 되고, 그래서 양식이 하나로 굳었다.
이 자리는 **실패를 싸게 만드는 것**이 목적이다.

## 쓰는 법

```bash
python3 studio/sandbox/render.py sheet size-bias --plan all   # 한 스펙을 세 판형으로
python3 studio/sandbox/render.py sheet --all --plan B         # 전 스펙을 판형 B 로
python3 studio/sandbox/render.py cuttoon                      # 컷툰 A4 6컷
python3 studio/sandbox/render.py cuttoon --stubs              # 컷아웃 대신 임시 실루엣
python3 studio/sandbox/render.py same                         # A 판형 동일성 확인 ★
```

`sheet` 가 읽는 스펙은 `studio/concepts/*.py` (발행분과 같은 원본)이고,
`cuttoon` 이 읽는 스펙은 `studio/sandbox/specs/cuttoon-*.py` 다.

★ **`same` 이 제일 중요하다.** 판형을 넣으면서 이미 발행된 다섯 장의 A 판형이
한 바이트라도 달라지면 서가의 그림이 소리 없이 바뀐다. `same` 은 **판형 도입 직전
커밋**(`07dd26c`)의 모듈과 지금 모듈로 각각 HTML 을 뽑아 **바이트로 비교한다** —
주장이 아니라 증거다. 판형 CSS 를 건드렸으면 반드시 돌릴 것.

⚠️ 기준을 `HEAD` 로 두면 안 된다. 판형이 머지된 뒤에는 자기 자신과 비교하게 돼
**언제나 통과하는 가짜 초록**이 된다. 그래서 기준 커밋을 `render.py` 의 `BASELINE`
상수에 못박아 두었다.

산출물은 `out/` 에 떨어지고 **git 이 무시한다**(`.gitignore`).

## 환경 — 이 세션에서 바로 렌더된다

```
chromium      /opt/pw-browsers/chromium-1194/chrome-linux/chrome
playwright    pip install playwright  (브라우저는 이미 있으므로 install 하지 말 것)
폰트          apt-get install fonts-noto-cjk   ← 러너와 같은 Noto Sans CJK KR
```

⚠️ **폰트가 다르면 발행본과 다르게 보인다.** `concept-sheet-render.yml` 이 렌더를 러너로
옮긴 이유가 그것이다(처음 다섯 장이 윈도우 폴백 폰트로 그려졌던 사고).
**여기서는 구조·배치를 보고, 최종 판정은 러너에서 한다.**

## 무엇을 시험할 수 있나

| | 무엇 | 지금 상태 |
|---|---|---|
| 판형 | 개념 한 장의 A/B/C | `render.py sheet --plan`. A=기준(발행분) · B=센터 임팩트 · C=구조 강조 |
| 컷툰 | A4 6컷 만화 조립 | `render.py cuttoon`. `rows`(행 높이 비율)·`tall`(두 행)로 판면 리듬 |
| 캐릭터 | QED프렌즈 컷아웃 세우기 | `figures` — 파일이 없으면 자리표, `--stubs` 로 대역 |

### 렌더가 자동으로 재는 것

눈으로만 보면 매번 놓치는 것들이라 숫자로 만들었다. 실패시키지는 않는다 —
실험대에서 죽이면 시험을 못 하기 때문이다. 대신 무엇이 얼마나 어긋났는지 짚어 준다.

| 재는 것 | 왜 |
|---|---|
| 컷 밖으로 밀림 | 컷은 `overflow:hidden` 이라 밀려난 말풍선은 **소리 없이 사라진다** |
| 격자 빈칸 | `wide`/`tall` 을 섞으면 마지막 줄에 구멍이 남는다 |
| 컷 높이 종수 | 여섯 컷이 전부 같은 높이면 만화가 아니라 **표로 읽힌다** |
| 말풍선·나레이션·효과음 겹침 | 전부 `absolute` 라 서로를 모르고 앉는다 |
| 얼굴 가림 | 몸통을 조금 가리는 건 연출이지만 **얼굴을 가리면 컷이 죽는다**(상단 30%, 12% 이상) |

### 그림은 어떻게 들어오나 — 세 단계

말풍선·나레이션·효과음은 **그림에 넣지 않는다.** 이미지 생성 모델이 한글을 정확히 못 쓰기
때문이다(카드뉴스가 HTML→스크린샷을 쓰는 이유와 같다). 그래서 순서가 이렇게 갈린다.

| | 하는 일 | 누가 |
|---|---|---|
| ① | 컷 구성·대사를 스펙으로 확정 → 자리표로 렌더 | 여기 |
| ② | 자리표에 찍힌 `shot`(연출 지시)을 구글 Flow(Nano Banana Pro)에 넣어 그림을 받는다 | 사용자 |
| ③ | 스펙의 `img` 에 파일 경로를 적고 다시 렌더 | 여기 |

**①에서 이미 읽을 수 있는 한 장이 나온다**는 게 요점이다. 그림이 없어도 컷 구성과
대사 흐름은 그대로 판단할 수 있고, 그림은 나중에 갈아 끼우면 된다.

캐릭터는 새로 만들 것이 없다. `Shorts_Flow` 드라이브 폴더
(`19Glc5hs8h3UXhOahDmm6V4jo3PFMRzG1`)에 **QED프렌즈 5인**(닥터파이·루트·제로·코코·뮤)의
설정집(`character-bible.md`)과 **배경 없는 컷아웃**(`characters/cutouts_*.png`)이 이미 있다.
그 파일들을 아래에 내려두고 스펙의 `img` 로 가리킨다.

```
studio/sandbox/assets/characters/dr-pi.png  root.png  zero.png  coco.png  mu.png
```

**이 폴더는 git 이 무시한다.** Search 는 공개 리포이고(갤러리가 여기서 Pages 로 나간다)
QED프렌즈는 비공개 Shorts_Flow 의 자산이라, 커밋하면 그대로 웹에 공개된다. 정본도
Shorts_Flow 쪽이다. 그러니 각자 자기 작업 폴더에 내려두고 쓴다.

그림을 넣는 자리는 둘로 나뉜다. **섞어 쓸 수 있다.**

```python
# ① 컷 전체를 채우는 그림 — Flow 가 그려 준 배경/연출컷
{"n": 1, "img": "assets/bg/ep001-cut1.png"}

# ② 배경 없는 컷아웃을 바닥에 세우기 — 인물만 갈아 끼울 때
{"n": 3, "cast": ["닥터파이"],
 "figures": [{"src": "assets/characters/dr-pi.png", "h": 80}],
 "stage": "flex-start",           # center(기본) · flex-start · flex-end · space-between
 "bubbles": [{"t": "위는 곱해 가고 아래는 더해 가지.", "at": "top r"}]}
```

경로는 `studio/sandbox` 기준 상대경로다. **파일이 없으면 조용히 깨지지 않고**
"그림 없음 — dr-pi.png" 라고 적힌 자리표로 되돌아간다.

컷아웃만 있는 컷은 인물이 흰 허공에 뜨므로 옅은 **바닥 띠**가 자동으로 깔린다
(`"ground": False` 로 끈다. `img` 배경이 들어오면 필요 없다).

진짜 컷아웃이 없어도 배관은 확인할 수 있다 — `--stubs` 가 사람 크기의 투명 PNG 를
만들어 준다. 캐릭터가 아니라 대역이고, 진짜가 오면 같은 이름으로 덮으면 된다.
