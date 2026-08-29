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
python3 studio/sandbox/render.py same                         # A 판형 동일성 확인 ★
```

`sheet` 가 읽는 스펙은 `studio/concepts/*.py` (발행분과 같은 원본)이고,
`cuttoon` 이 읽는 스펙은 `studio/sandbox/specs/cuttoon-*.py` 다.

★ **`same` 이 제일 중요하다.** 판형을 넣으면서 이미 발행된 다섯 장의 A 판형이
한 바이트라도 달라지면 서가의 그림이 소리 없이 바뀐다. `same` 은 옛 모듈(git HEAD)과
지금 모듈로 각각 HTML 을 뽑아 **바이트로 비교한다** — 주장이 아니라 증거다.
판형 CSS 를 건드렸으면 반드시 돌릴 것.

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
| 컷툰 | A4 6컷 만화 조립 | `render.py cuttoon` |
| 캐릭터 | QED프렌즈 컷아웃 끼우기 | **플레이스홀더** — 아래 참조 |

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

```python
{"n": 3, "cast": ["닥터파이"], "img": "assets/characters/dr-pi.png",
 "bubbles": [{"t": "위는 곱해 가고 아래는 더해 가지.", "at": "top r"}]}
```

경로는 `studio/sandbox` 기준 상대경로다. `img` 가 없으면 `cast`·`shot` 이 적힌
자리표가 그려진다.
