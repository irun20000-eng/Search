---
주제: Google Flow 실습편 — 실전 예제·실행 순서·따라하기 가이드 (DEEP)
날짜: 2026-07-09
깊이: deep
카드모드: auto
대상수준: 실무 실습 가이드(DEEP)
태그: [AI영상, GoogleFlow, Veo, 실습가이드, 프롬프트, Scenebuilder, 크리에이터, 따라하기]
소스수: { 국내: 5, 해외: 10 }
위키링크: ["[[Google Flow]]", "[[Veo]]", "[[프롬프트 엔지니어링]]", "[[AI 영상 생성]]", "[[콘텐츠 크리에이터]]", "[[Scenebuilder]]"]
갤러리URL: "#r=google-flow-practice"
---

# Google Flow 실습편 — 실전 예제·실행 순서·따라하기 가이드

> 작성·조회 기준일 **2026-07-09 (KST)**. UI 명칭·버튼은 업데이트로 바뀔 수 있으니 공식 도움말(support.google.com/flow)과 함께 볼 것. 선행: [[Google Flow]] 개요편(`#r=google-flow`) — 개념·요금·유사도구를 먼저 봤다면, 이번엔 **손으로 직접 만드는 실습편**이다. 프롬프트는 전부 **복사해 바로 써먹도록** 담았다.

## TL;DR
- Flow의 실전 뼈대는 **네 가지 생성 모드**다: **텍스트→영상 · 프레임→영상 · 재료(Ingredients)→영상 · 샷 익스플로러**. 그리고 완성 후 **Scenebuilder**에서 이어붙인다 [해외 Help][국내 ryujongpan].
- 좋은 결과의 90%는 **프롬프트 공식**에서 나온다: **주제(Subject) + 동작(Action) + 스타일 + 카메라 + 구도 + 렌즈/초점 + 분위기 + 오디오** — 단, **핵심 3~4개만** 골라 또렷하게 [해외 DeepMind][해외 Cloud].
- 길이를 늘리는 건 **Extend**(끝 프레임을 분석해 동작을 이어감), 배경/상황을 바꾸는 건 **Jump To**(캐릭터 외형은 유지하며 새 장면으로) [해외 digiweb][해외 Help].
- 카메라 무빙은 **텍스트로 쓰거나 UI 카메라 컨트롤(dolly in·pan 등)로 지정**하며 둘은 함께 쌓인다. **카메라 지시는 별도 문장**으로 쓰는 게 잘 먹힌다 [해외 Help][해외 Cloud].
- 실전 팁: **한글보다 영어 프롬프트가 더 잘 통한다**, 대사는 **따옴표**, 효과음은 `SFX:`, 배경음은 `Ambient noise:`로 명시 [국내 bpgun][해외 SurePrompts].

## 핵심 포인트
1. **"완성 영상 한 방"이 아니라 "짧은 컷을 만들고 → 이어붙이고 → 다듬는다".** 이 리듬이 실습의 전부 [국내 ryujongpan].
2. **프롬프트는 공식대로 + 핵심 3~4개만.** 요소를 많이 넣을수록 오히려 흐려진다 [해외 Cloud].
3. **캐릭터/소품은 먼저 Ingredient로 고정**하고 씬을 만든다(일관성) [개요편].
4. **카메라 무빙은 별도 문장**, 대사·효과음·배경음은 **라벨로 명시** [해외 Cloud][해외 SurePrompts].
5. **크레딧을 아끼려면**: 저해상도로 구도 확정 → 확정 컷만 4K 재생성 [개요편].

## 0. 시작 전 준비 (5분)

1. **구독 확인**: Flow는 Google AI Plus/Pro/Ultra 구독이 있어야 열린다(개요편 요금표 참고).
2. **접속**: 컴퓨터로 **flow.google.com** → 새 프로젝트(New project). PC가 전체 기능(Scenebuilder·4K)에 유리 [해외 Help].
3. **언어 세팅(중요)**: 프롬프트는 **영어로** 쓰는 걸 권장. 국내 실사용 후기도 "한글보다 영어 프롬프트가 더 잘 먹힌다"고 공통 지적 [국내 bpgun]. (한글로 구상 → 영어로 번역해 입력하는 습관.)
4. **크레딧 감각**: 4K·립싱크·긴 씬은 크레딧을 많이 쓴다. **처음엔 짧게·저해상도로** 실험.

## 1. 화면·모드 이해 — 무엇을 언제 쓰나

Flow의 생성 입력은 크게 넷이다 [해외 Help][국내 genity].

| 모드 | 입력 | 언제 |
|---|---|---|
| **Text to Video** | 텍스트 프롬프트만 | 아이디어를 바로 영상으로 |
| **Frames to Video** | 시작(+끝) 프레임 이미지 | 특정 그림에서 시작/끝나게, 카메라 무빙 |
| **Ingredients to Video** | 저장한 재료(캐릭터·소품) | **일관된 캐릭터**로 여러 컷 |
| **Shot Explorer** | 이미지 기반 다양한 샷 탐색 | 컨셉·앵글 후보를 여러 개 [국내 genity] |

그리고 생성된 클립들은 **Scenebuilder**(인-플로우 스토리보드)에서 **순서 변경·삭제·길이 조절·이어붙이기**를 한다 [국내 ryujongpan][해외 Help].

## 2. 프롬프트 공식 — 이것만 외우면 절반은 성공

Veo가 잘 알아듣는 프롬프트 구조는 다음과 같다 [해외 DeepMind][해외 Cloud].

```
[프롬프트 공식]
Subject(주제) + Action(동작) + Style(스타일)
+ Camera(카메라 위치·움직임) + Composition(구도)
+ Focus/Lens(초점·렌즈) + Ambiance(분위기·조명·색)
+ Audio(대사/효과음/배경음)

핵심 규칙:
① 반드시 넣을 3요소 = Subject · Context(장소) · Action
② 나머지는 3~4개만 골라 또렷하게(과적재 금지)
③ 카메라 무빙은 별도 문장으로
④ 대사는 "따옴표", 효과음은 SFX:, 배경음은 Ambient noise:
⑤ 추상어(멋진·감성적인) 금지 → 시각적 묘사로
```

**나쁜 예 → 좋은 예**
```
❌ "멋지고 감성적인 도시 영상"
✅ "Close-up, shallow depth of field, a young woman's face looking
   out a bus window at passing city lights, rain on the glass at night,
   melancholic mood, cool blue tones, cinematic.
   The camera slowly dollies in.
   Ambient noise: soft rain and distant traffic."
```
(핵심 3~4요소 + 카메라 별도 문장 + 오디오 라벨 — 이 형태가 표준이다 [해외 Cloud][해외 SurePrompts].)

**요소별 한 줄 감각**을 잡아두면 프롬프트를 즉석에서 조립할 수 있다. **Subject**는 "누가/무엇이"(a young woman, a red sports car), **Action**은 "무엇을 한다"(runs, slowly turns), **Style**은 "어떤 결"(cinematic, anime, documentary), **Camera**는 "어떻게 잡나"(wide shot, low angle, dolly-in), **Composition**은 "화면 배치"(centered, rule of thirds), **Focus/Lens**는 "초점/렌즈"(shallow depth of field, 85mm), **Ambiance**는 "빛·색·분위기"(golden hour, cool blue tones, foggy), **Audio**는 "소리"(대사·SFX·배경음)다. 이 여덟 서랍에서 **장면에 꼭 필요한 3~4개만** 꺼내 쓰는 게 요령이다 — 여덟 개를 다 채우면 서로 충돌해 오히려 결과가 흐려진다 [해외 DeepMind][해외 Cloud]. 처음엔 Subject·Action·Ambiance 세 개로 시작해, 결과를 보며 카메라·오디오를 한 개씩 더하는 방식을 추천한다.

## 3. 실습 A — 첫 8초 클립 만들기 (텍스트→영상)

가장 기본. **정확한 클릭 순서**로 따라해보자 [해외 Help][해외 Tom's].

```
1) 새 프로젝트 → 입력창을 'Text to Video'로 둔다.
2) 아래 프롬프트를 붙여넣는다:

   "A golden retriever runs across a sunny beach, kicking up sand,
    slow motion. Wide tracking shot following the dog.
    Warm afternoon light, shallow depth of field, cinematic.
    Ambient noise: ocean waves and seagulls."

3) (선택) 해상도·모델을 낮게 두어 크레딧 절약.
4) Generate 클릭 → 8초 클립 생성(오디오 포함).
5) 결과가 마음에 안 들면 프롬프트의 '한 요소만' 바꿔 재생성
   (예: 'slow motion' 빼기, 'sunset' 추가).
```

- **관찰 포인트**: 카메라 문장(Wide tracking shot…)을 넣고 뺐을 때 차이를 본다.
- **반복 전략**: 한 번에 여러 요소를 바꾸지 말 것. **한 변수씩** 바꿔야 무엇이 효과였는지 안다.

## 4. 실습 B — 캐릭터를 만들고 고정하기 (Ingredients)

여러 컷에서 **같은 인물**을 쓰려면 재료로 잠근다 [개요편][해외 Help].

```
1) Imagen(이미지 생성)으로 캐릭터 시안 만들기:
   "Portrait of a 30-year-old Korean man, short black hair,
    round glasses, navy hoodie, neutral studio background,
    soft lighting, photorealistic."
2) 마음에 드는 컷을 'Ingredient'로 저장(재료 보관함).
3) 입력 모드를 'Ingredients to Video'로 바꾸고 그 재료를 선택.
4) 씬 프롬프트 작성(재료가 주인공):
   "The man from the reference sits at a cafe, typing on a laptop,
    looking up and smiling. Medium shot. Warm window light.
    He says, 'Almost done with the project.'"
5) Generate → 같은 얼굴/의상으로 새 장면 생성.
```

- **팁**: 시안을 **여러 장** 만들어 가장 일관성 좋은 것을 재료로. 극단적 각도·표정은 흐트러질 수 있다 [개요편].

## 5. 실습 C — 클립 이어붙이기 (Extend · Jump To)

한 컷은 8~15초. 길게·이어지게 만들려면 두 도구를 쓴다 [해외 digiweb][해외 Help].

**Extend — 같은 장면을 더 길게**
```
1) Scenebuilder에서 늘리고 싶은 클립을 클릭.
2) 하단 'Extend' 클릭.
3) 이어질 동작을 서술:
   "He closes the laptop, stands up, and walks toward the door."
4) Generate → Flow가 끝 프레임을 분석해 자연스럽게 이어감.
```

**Jump To — 인물은 유지, 배경/상황만 전환**
```
1) 클립 선택 → 'Jump To'.
2) 새로운 상황 서술(외형은 자동 유지):
   "Now the same man is walking on a rainy city street at night,
    holding an umbrella. Cinematic, neon reflections."
3) Generate → Gemini가 이전 클립의 인물을 이해해 새 장면으로 연결.
```

- **차이**: Extend=**연속 동작**(같은 장면), Jump To=**장면 점프**(다른 배경/시간). 스토리 흐름에 맞게 골라 쓴다 [해외 Help].
- **편집**: Scenebuilder에서 **순서 변경·삭제·길이 조절**로 컷을 정리 [국내 ryujongpan].

## 6. 실습 D — 카메라 무빙·프레임 컨트롤 (Frames to Video)

특정 그림에서 시작하거나 **정교한 카메라 워크**가 필요할 때 [해외 Help][해외 Cloud].

```
1) 입력을 'Frames to Video'로.
2) 시작 프레임(과 원하면 끝 프레임) 이미지를 올린다.
3) 카메라 아이콘을 눌러 컨트롤 선택(dolly in / pan left /
   tilt up / orbit 등). 아이콘이 X로 바뀌면 취소.
4) 텍스트로도 카메라를 명시(둘은 함께 쌓임):
   "Start on the coffee cup, slow dolly-out revealing the whole cafe.
    The camera pulls back steadily."
5) Generate.
```

- **핵심 규칙**: **"The camera pulls back."처럼 카메라를 독립 문장**으로 쓰면 훨씬 잘 먹는다. 동작 설명 안에 파묻지 말 것 [해외 Cloud].
- **스택**: 프롬프트에 "low-angle"을 쓰고 UI에서도 "Low Angle"을 고르면 **일관된 신호**로 강화된다 [해외 Help].

## 7. 실습 E — 오디오·대사 넣기

Veo의 강점은 **오디오 동시 생성**. 프롬프트에 **라벨**로 지시한다 [해외 SurePrompts][해외 Cloud].

```
[대사] 따옴표로:
   A woman says, "We have to leave now."
[효과음] SFX 라벨:
   SFX: thunder cracks in the distance.
[배경음] Ambient 라벨:
   Ambient noise: the quiet hum of a starship bridge.
[음악] 분위기로:
   Soft piano melody, melancholic.
```

**통합 예(립싱크 광고 대사)**
```
"Medium close-up of the man from the reference, holding a coffee cup,
 warm cafe light. He looks at the camera and says,
 'This is how my morning begins.'
 Ambient noise: soft cafe chatter and espresso machine."
```

- **립싱크**: 대사를 따옴표로 주면 입 모양이 맞춰 생성된다(개요편의 네이티브 오디오).

## 8. 종합 실습 — 30초 미니 광고 완주 체크리스트

앞 실습을 이어 **완성작 하나**를 만든다. 순서대로 체크.

```
[ ] 1. 컨셉 한 줄: "카페에서 일하는 남자의 아침 루틴 → 제품 소개"
[ ] 2. 재료(Imagen): 남자 캐릭터 + 제품 컷 → 각각 Ingredient 저장
[ ] 3. 씬1 (Ingredients): 카페에 앉는 남자, 미디엄샷, 웜라이트 (8초)
[ ] 4. 씬2 (Frames+카메라): 제품 클로즈업, slow dolly-in (6초)
[ ] 5. 씬3 (대사): "This changes my mornings." 립싱크 (8초)
[ ] 6. 씬4 (텍스트): 로고+슬로건 화면, 잔잔한 피아노 (8초)
[ ] 7. Scenebuilder: 씬1→2→3→4 순서 배치, 길이 다듬기
[ ] 8. 자연어 편집(Gemini): "전체 톤 웜하게", "씬2 0.8배속"
[ ] 9. 저해상도로 전체 확인 → OK면 4K 재생성
[ ] 10. 9:16 세로 크롭 익스포트 → SNS 업로드
```

- **크레딧 절약 포인트**: 8·9단계 — **구도는 저해상도로 확정**하고 4K는 마지막에.
- **일관성 포인트**: 씬마다 **같은 Ingredient**를 걸어야 얼굴/제품이 유지된다.

이 종합 실습이 중요한 이유는, 실제 제작이 바로 이 **"조각을 따로 만들어 하나로 엮는"** 흐름이기 때문이다. 초보자가 흔히 저지르는 실수는 "30초짜리를 한 프롬프트로 뽑으려는 것"인데, Flow는 그렇게 설계돼 있지 않다. 8초 안팎의 **씬 단위로 쪼개 각각 최적화**한 뒤 Scenebuilder에서 순서·길이를 맞추는 게 정석이다 [국내 ryujongpan]. 그래서 위 10단계를 한 번 완주해보면, 이후 어떤 주제든 "컨셉 한 줄 → 재료 → 씬별 생성 → 편집 → 익스포트"라는 **같은 골격**을 재사용하게 된다. 처음엔 30분이 걸려도, 두세 번째부터는 10~15분이면 초안이 나온다.

## 9. 반복·수정 워크플로우 — "한 번에 완성"은 없다

AI 영상은 **반복(iteration)**이 정상이다. 효율적으로 도는 법 [국내 bpgun][해외 blog.google].

- **한 변수씩 바꾸기**: 프롬프트에서 조명만, 또는 카메라만 바꿔 재생성. 무엇이 효과인지 학습.
- **자연어 편집 우선**: 통째 재생성 전에 Gemini에게 "이 컷 더 밝게", "속도 늦춰" 먼저 시도(크레딧 절약).
- **좋은 씨앗 저장**: 잘 나온 컷/재료는 즉시 저장해 재사용.
- **레퍼런스 병행**: 원하는 톤의 참고 이미지를 Frames로 넣으면 방향이 잡힌다.
- **3~4요소 원칙 재확인**: 결과가 산만하면 프롬프트가 과적재된 경우가 많다 → 요소를 **줄인다** [해외 Cloud].

## 10. 트러블슈팅 — 자주 막히는 지점

| 증상 | 원인 | 해결 |
|---|---|---|
| 결과가 프롬프트와 딴판 | 요소 과다·추상어 | 핵심 3~4개로 줄이고 시각적 묘사 [해외 Cloud] |
| 한글이 잘 안 먹힘 | 언어 최적화 | **영어로 번역해 입력** [국내 bpgun] |
| 캐릭터 얼굴이 바뀜 | 재료 미사용·극단 각도 | Ingredient 걸기, 각도 완만하게 [개요편] |
| 카메라가 안 움직임 | 동작에 파묻힘 | **카메라 독립 문장**으로 [해외 Cloud] |
| 손·글자 깨짐 | 모델 한계 | 클로즈업/텍스트 오버레이는 후편집 |
| 크레딧 순삭 | 4K·긴 씬 남발 | 저해상도로 확정 후 4K [개요편] |
| 컷 연결이 어색 | 잘못된 도구 | 연속=Extend, 장면전환=Jump To [해외 Help] |

## 11. 3일 연습 커리큘럼 (하루 30분)

```
[1일차] 감 잡기
 - 실습 A: 텍스트→영상 8초 클립 3개(동물/풍경/인물)
 - 프롬프트에서 카메라 문장 넣고 뺀 차이 관찰

[2일차] 일관성·연결
 - 실습 B: 내 캐릭터 만들어 Ingredient 저장
 - 실습 C: 그 캐릭터로 2컷 만들고 Extend/Jump To 연결

[3일차] 완성작
 - 실습 D·E: 카메라 무빙 + 대사 넣기
 - 종합 실습: 30초 미니 광고 완주 → 익스포트
```

- 이 3일이면 "프롬프트 공식 → 재료 고정 → 이어붙이기 → 오디오 → 완성"의 **전 과정**을 한 바퀴 돈다.

## 12. 복붙 프롬프트 템플릿 모음

```
[제품 광고]
"Product close-up of a [제품], rotating slowly on a clean surface,
 studio lighting, minimal background, premium aesthetic.
 The camera slowly orbits the product.
 Soft ambient music."

[인물 인터뷰/토킹헤드]
"Medium close-up of [인물 from reference], warm office light,
 looking at the camera, professional aesthetic.
 They say, '[대사]'.
 Ambient noise: quiet room tone."

[풍경/드론]
"Aerial drone ascending over [장소] at sunrise, morning mist,
 distant peaks, cinematic, warm tones.
 The camera rises steadily.
 Ambient noise: gentle wind."

[감성 시네마틱]
"Close-up, shallow depth of field, [주제], [장소] at [시간],
 [분위기] mood, [색] tones, cinematic.
 The camera slowly dollies in.
 SFX: [효과음]."
```
(대괄호를 채우고 **핵심 3~4요소만** 남기면 된다.)

## 한눈 요약
- 네 모드(Text/Frames/Ingredients/Shot Explorer) + **Scenebuilder**로 이어붙이기 [해외 Help][국내 ryujongpan].
- 프롬프트 공식: **Subject+Action+Style+Camera+Composition+Lens+Ambiance+Audio**, 핵심 3~4개만 [해외 DeepMind][해외 Cloud].
- 길이=**Extend**, 장면전환=**Jump To**, 카메라=**독립 문장/UI 컨트롤 스택** [해외 Help].
- 오디오는 **"따옴표"·SFX:·Ambient noise:** 라벨로 [해외 SurePrompts].
- 실전 팁: **영어 프롬프트**, **한 변수씩** 반복, **저해상도→4K**로 크레딧 절약 [국내 bpgun][개요편].

## 출처

**국내**
1. (국내) 질문학 잡사(bpgun), "구글 플로우 사용법 — 대화만으로 수정하는 AI 영상 + 실전 팁·한계", 네이버 블로그, 2026-06-05 — "한글보다 영어 프롬프트가 잘 먹힘" 등 실전 팁. https://blog.naver.com/bpgun/224306739253
2. (국내) 앞선 디지로그(ryujongpan), "구글 Flow 스토리보드 스튜디오 완벽 가이드", 네이버 블로그, 2026-07-09 — 순서 변경·클립 삭제·길이 조절·이어붙이기. https://blog.naver.com/ryujongpan/224341251206
3. (국내) Genity AI Studio, "구글 플로우 샷 익스플로러(Shot Explorer) — 이미지 기반", 네이버 블로그, 2026-05-26 — Shot Explorer 활용. https://blog.naver.com/genity/224296565610
4. (국내) 알면좋을AI공학(allaboutaiedu), "제미나이 옴니 — 영상 이어붙이기·프롬프트·도구 활용", 네이버 블로그, 2026-05-27 — 이어붙이기·프롬프트 팁. https://blog.naver.com/allaboutaiedu/224297987893
5. (국내) '나답게' 성장하는 시간(okshadow), "무료 AI 이미지 생성 Flow 사용법 — 1분 고퀄리티", 네이버 블로그, 2026-03-22 — 접속·이미지·이어붙이기 기본. https://blog.naver.com/okshadow/224225454242

**해외**
6. (해외) Google DeepMind, "How to create effective prompts with Veo 3" — 프롬프트 구조·핵심 요소. https://deepmind.google/models/veo/prompt-guide/
7. (해외) Google Cloud Blog, "Ultimate prompting guide for Veo 3.1" — 카메라 독립 문장·요소 3~4개·오디오 라벨. https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
8. (해외) Google Flow Help, "Create videos in Google Flow" / "Edit videos & build scenes in Flow" — 모드·Scenebuilder·Extend·Frames 카메라 컨트롤. https://support.google.com/flow/answer/16935718
9. (해외) Google Blog, "5 tips for using Flow, Google's AI filmmaking tool" — 공식 팁. https://blog.google/technology/ai/flow-video-tips/
10. (해외) DigiWebInsight, "Flow Scenebuilder Extend Shots: Ultimate Guide" — Extend/Jump To 상세. https://digiwebinsight.com/flow-scenebuilder-extend-shots/
11. (해외) Tom's Guide, "How to use Google Flow — the new AI video generator meant for filmmakers" — 시작 워크스루. https://www.tomsguide.com/ai/google-gemini/how-to-use-google-flow-the-new-ai-video-generator-meant-for-filmmakers
12. (해외) SurePrompts, "Ultimate Veo 3 Prompt Guide: 100+ Examples" — 대사·SFX·Ambient 라벨·예시. https://sureprompts.com/blog/veo3-prompt-guide
13. (해외) Powtoon Blog, "Veo 3 Video Prompt Examples and Best Practices" — 샷 타입·조명 예시. https://www.powtoon.com/blog/veo-3-video-prompt-examples/
14. (해외) Medium(Furkan Gözükara), "VEO 3 FLOW Full Tutorial — How To Use VEO3 in FLOW" — 전체 튜토리얼. https://medium.com/@furkangozukara/veo-3-flow-full-tutorial-how-to-use-veo3-in-flow-guide-1e5cfd332489

## 후속 질문·연결
- 개념·요금·유사도구 → [[Google Flow]] 개요편(`#r=google-flow`)
- 프롬프트 더 깊게 → [[프롬프트 엔지니어링]]
- 다른 영상 도구 실습 → [[Runway]] · [[Kling]]
- 관련: [[Veo]] · [[Scenebuilder]] · [[콘텐츠 크리에이터]]
