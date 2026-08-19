# VIDEO_PIPELINE — 영상 노트·가이드 런북

`PIPELINE.md`(리서치 보고서)의 자매편. 이 문서는 **영상 노트**와 **따라하기 가이드** 두 갈래를 다룬다.
세션이 오케스트레이터라는 원칙은 동일하다 — 백엔드·크론 없음, 정적 자산 + 세션 실행.

---

## 0. 환경 전제 (실측 기준, 2026-08-08)

| 기능 | 상태 | 대응 |
|---|---|---|
| `YouTubeData-get_video_details` | ✅ 작동 (배치, 1 unit) | 메타데이터 **정본 출처** |
| 섬네일 `i.ytimg.com/vi/<ID>/hqdefault.jpg` | ✅ API 불필요 | 결정적 URL |
| `WebSearch(allowed_domains:["youtube.com"])` | ✅ 작동 | 영상 탐색 **주경로** |
| `YouTubeData-search_videos` | ⚠️ 공용 키·일일 쿼터 소진 잦음 | 보조 경로 |
| `get_transcripts` / `list_available_captions` | ❌ 클라우드 IP 차단 | **자막 자동수집 불가 → 제미나이 수동 분석** |
| `WebFetch` | ⚠️ egress 차단 빈번 | WebSearch 요약 다중 교차검증 |
| Google Drive MCP | ✅ | 옵시디언 저장 |

### 무환각 검증기 (핵심 장치)

`get_video_details`는 **존재하지 않는 ID를 응답에서 조용히 누락**한다.
따라서 판정 규칙은 결정적이다.

```
응답에 ID 있음 → 실재하는 공개 영상 → 채택
응답에 ID 없음 → 없거나 비공개·삭제       → 폐기
```

검색으로 얻은 후보는 **예외 없이 이 검증기를 통과해야** 갤러리·가이드에 들어간다.
이 덕분에 죽은 링크·환각 영상이 구조적으로 0건이 된다.

같은 이유로 **제미나이에게 제목·채널·길이·게시일을 묻지 않는다.** API가 채우므로
모델이 사실 메타데이터를 지어낼 경로 자체가 없다.

---

## 1. 영상 노트 — 트리거

```
영상: https://youtu.be/XXXXXXXXXXX
---
<제미나이 분석 결과 붙여넣기>
```

`영상 프롬프트` 라고만 입력하면 `prompts/gemini-video-analysis.md` 전문을 출력한다.

### 절차

1. **파싱** — `tools/ingest_video.py`. 코드펜스·`===END===` 누락·`@91`/`@1:31` 혼용·
   태그 `#` 접두사·분류 별칭을 모두 수용한다.
   **파싱 실패 시 추측해 채우지 않는다.** 어느 줄이 왜 안 읽혔는지 짚어 재요청한다.
2. **메타데이터 확정** — `get_video_details(video_ids=[ID])` → 제목·채널·게시일·길이.
   응답에 ID가 없으면 중단(존재하지 않는 영상).
3. **시간 창작 검사** — 타임스탬프가 영상 길이를 넘으면 즉시 실패.
4. **노트 기록** — `videos/notes/<ID>.md` + `videos/manifest.json` 선두 삽입.
5. **품질 게이트** — `python3 tools/verify_video.py videos/notes/<ID>.md`
6. **검수(별도 패스)** — 아래 §4.
7. **배포** — 커밋 → 푸시 → PR(측정표 첨부) → main 머지 → 갤러리 확인
8. **옵시디언 저장** — 아래 §5.

---

## 2. 가이드 — 트리거

```
가이드: <주제>
난이도: 입문 | 중급 | 고급     # 생략 시 입문
```

### 절차

1. **조사** — WebSearch + 네이버 MCP. `WebFetch` 403·차단을 전제로 **요약 다중 교차검증**.
   단일 스니펫 단정 금지(LESSONS 방지규칙 2).
2. **집필** — `guides/<슬러그>/guide.md`. 필수 섹션:
   `이 가이드로 만들 것` / `사전 준비물` / `N단계`(각 단계에 **화면에서 확인할 것** +
   **막히면**) / `흔히 막히는 지점` / `다음으로 할 것` / `관련 영상` / `출처`
3. **영상 탐색** — `WebSearch(allowed_domains:["youtube.com"])` 주경로.
4. **영상 검증** — 후보 ID 전량 `get_video_details` **배치 1회**. 누락 ID는 폐기.
5. **캐시** — 검증된 제목·채널·길이·게시일을 `guides/manifest.json`의 `videos[]`에 기록.
   페이지 로드 시 API 호출이 없도록 한다.
6. **품질 게이트** — `python3 tools/verify_guide.py guides/<슬러그>/guide.md`
7. 이후 §4 검수 → 배포 → 옵시디언 저장.

**검증 한계를 반드시 본문에 밝힌다.** 원문 페이지를 직접 못 읽었으면 그 사실과,
버튼 이름·UI가 버전에 따라 달라질 수 있다는 점을 가이드 안에 적는다.

---

## 3. 품질 게이트 (측정이지 판단이 아니다)

### 영상 노트 — 기존 73편 코퍼스 실측 기반

| 항목 | 실측 min | p10 | 중앙값 | max | **채택 하한** |
|---|---|---|---|---|---|
| 챕터 수 | 4 | 5 | 5 | 11 | **≥ 4** |
| 핵심 인용 | 4 | 5 | 5 | 11 | **= 챕터 수** |
| 내 팁/질문 | 4 | 5 | 5 | 11 | **= 챕터 수** |
| TL;DR 줄 | 5 | 5 | 5 | 5 | **정확히 5** |
| 한줄요약 글자 | 121 | 234 | 313 | 615 | **≥ 120** |
| 본문 글자(공백 제외) | 2,091 | 2,565 | 3,065 | 4,819 | **≥ 2,050** |
| 태그 수 | 7 | 8 | 10 | 14 | **7~14** |

> **★ 글자수는 반드시 '공백 제외'로 잰다.** 공백 포함으로 재면 min이 2,675로 달라져
> 게이트가 어긋난다. 최초 산정 때 실제로 이 혼동이 있었다.

추가 기계 검사: 분류 ∈ 6개 열거값 · 타임스탬프 단조 증가 · 마지막 타임스탬프 < 영상 길이 ·
프론트매터 필수 필드 · manifest ↔ notes 1:1.

### 가이드 — 잠정 기준

구조 게이트(엄격): 단계 ≥ 5 · 단계마다 `화면에서 확인할 것` + `막히면` · 막히는 지점 ≥ 3 ·
검증 통과 영상 ≥ 3 · 출처 ≥ 5 · 필수 섹션 전부 · 난이도 ∈ 열거값 ·
**관련 영상이 manifest에 검증 캐시로 존재**할 것.

분량 게이트(잠정): 본문 ≥ 3,000자(공백 제외).
가이드는 코퍼스가 없어 실측 대상이 없다. 영상 노트 중앙값 3,065자를 앵커로 삼은 잠정값이며,
**가이드 3건이 쌓이면 실측 분포로 재보정하고 근거를 `tools/verify_guide.py` 주석에 남긴다.**

> 게이트를 몰래 낮추지 말 것. 조정할 일이 있으면 **근거와 함께 공개**한다.

---

## 4. 검수 — 별도 패스, self-approve 금지

`CLAUDE.md` 규칙을 구조로 강제한다.

```
작성 → verify_*.py 기계 측정 (판단 아님)
     → 별도 리뷰어 서브에이전트: 작성 컨텍스트를 갖지 않고 산출물만 받아 검수
        · 인용문이 실제 발화인지 (창작 여부)
        · 팁이 영상 밖 지식으로 지어낸 것은 아닌지
        · 출처 없는 단정이 있는지
        · 태그·분류가 내용과 맞는지
     → 불합격 시 지적사항 + 원문 → 개정 → 재측정
     → 최대 3회. 3회 후에도 미달이면 머지 중단하고 측정표와 미달 항목을 그대로 제시
```

리뷰어가 **작성 컨텍스트를 갖지 않는 별개 에이전트**라는 점이 self-approve 금지의 실체다.

---

## 5. 옵시디언 저장

영상 노트·가이드는 리서치 보고서와 **폴더가 다르다.**

| 종류 | Drive 폴더 | ID |
|---|---|---|
| 리서치 보고서 | `000-수집/001-주제리서치` | `1nScRmPu8XhHElDEf2yjnmSHThGkacYVf` |
| **영상 노트·가이드** | `000-수집/011-보고따라해` | `1eCkQ7HySXci0UOL_dZwM0yTnS1NioUlk` |

```
create_file(
  title = "<YYYYMMDD>_<제목>.md",
  parentId = "1eCkQ7HySXci0UOL_dZwM0yTnS1NioUlk",
  contentMimeType = "text/markdown",
  disableConversionToGoogleType = true      # ★ 없으면 구글 문서로 변환된다
)
```

**단일 진실의 원천** — `videos/notes/<ID>.md` 파일이 곧 볼트 노트다. 두 벌로 나눠 관리하지 않는다.
갤러리는 이 파일을 렌더링할 뿐이다.

---

## 6. 명령 모음

```bash
# 갤러리 미리보기
cd Search && python3 -m http.server 8080     # /videos/ , /guides/

# 품질 게이트
python3 tools/verify_video.py videos/notes/<ID>.md
python3 tools/verify_guide.py guides/<슬러그>/guide.md
python3 tools/verify_video.py                 # 전편 일괄

# 이관 동일성 (구조 변경 시)
python3 tools/render_parity.py

# manifest 재생성 (노트를 손으로 고친 경우)
python3 tools/build_manifest.py
```

---

## 7. 구조

```
videos/
  index.html          데이터 주도 셸 (~21KB, 외부 의존성 0)
  manifest.json       카드 메타 + 카테고리 정의
  notes/<영상ID>.md   노트 = 볼트 원본 = 갤러리 렌더 소스
  _legacy/            이관 전 1MB 모놀리스 스냅샷
guides/
  index.html          영상 갤러리와 동일 CSS·렌더러
  manifest.json       가이드 메타 + 검증된 영상 캐시
  <슬러그>/guide.md
prompts/
  gemini-video-analysis.md
routines/
  spark-video-curator.md  스파크 폴더 → 갤러리 발행 예약 루틴 지침
tools/
  extract_videos.py   1회성 이관
  build_manifest.py   notes/ → manifest 재생성
  ingest_video.py     제미나이 출력 → 노트 + manifest
  verify_video.py     영상 노트 게이트
  verify_guide.py     가이드 게이트
  render_parity.py    이관 동일성 대조
  unescape_drive_text.py  Drive read_file_content 출력 → 스파크 원문 복원
  check_encoding.py   인코딩 손상 검출(사설영역 차단 + 코퍼스 대조 자문)
```

`videos/index.html`과 `guides/index.html`은 **외부 CDN에 의존하지 않는다.**
마크다운 렌더러를 자체 구현해 두었으므로 CDN 차단·오프라인에서도 노트가 열린다.
(원본 모놀리스가 갖고 있던 성질을 유지한 것이다.)
