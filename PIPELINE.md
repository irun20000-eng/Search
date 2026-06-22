# PIPELINE.md — 주제 리서치 파이프라인 런북

이 문서는 **Claude Code 세션이 그대로 따라 실행하는 절차서**다. 모바일/클라우드에서 이 `Search` 레포로 세션을 열고 아래 한 줄로 트리거하면, 이 런북대로 보고서 작성 → 갤러리 갱신 → 옵시디언 저장까지 수행한다.

## 트리거 형식
```
주제: <조사할 주제>
깊이: quick | deep
카드모드: auto | manual | none   # 생략 시 manual(클라우드) / auto(로컬)
```
예) `주제: RAG 평가 방법, 깊이: deep, 카드모드: manual`

## 기본 동작 (사용자 상시 지시, 2026-06-21)
**보고서 요청이 오면 별도 언급이 없어도** 다음을 끝까지 자동 수행한다:
1. 작업 브랜치에서 보고서 작성·커밋·푸시 → **PR 생성 → main에 머지** → GitHub Pages 자동 빌드로 **갤러리 최신화**.
2. **옵시디언 노트 저장**(클라우드: Google Drive MCP, §5)까지 완료.
즉, "작성만 하고 멈추지 말 것" — PR 머지·갤러리 반영·옵시디언 저장이 1건의 완료 정의다.

## 개념 설명서 = 투트랙(이해편 + 확장편) (사용자 확정 2026-06-21, 최종)
**개념 설명·학습이 핵심인 주제**는 목적이 다른 **두 문서**로 낸다(수준이 아니라 *목적*이 축). 둘 다 **DEEP**(QUICK 아님)으로 쓰되 역할을 칼같이 나눠 **중복을 금지**한다. slug: 이해편=`<concept>`(대표), 확장편=`<concept>-advanced`. frontmatter `대상수준: 이해편(입문·딥)` / `확장편(학부·대학원 통합)`. 한 개념=카드 2장. 옵시디언도 각각 `YYYYMMDD_제목`. **문체는 둘 다 평어("~이다")** — 이해편은 쉬운 어휘·짧은 문장·비유를 평어로. 플래그십은 투트랙 기본, 가벼운 개념은 단일 이해편 허용. (시사·산업 동향형은 이 포맷 아님 — 기존 DEEP 타임라인/분석 기준.)

### ⚖️ 분량·구조 보장 테이블 (DEEP 가드레일)
**기준점(gold standard) = 이란-미국 보고서: 25,104자(`wc -m`) / 186줄 / 15섹션.**
> 📏 **측정 지표 주의(2026-06-22 보정)**: 1차 지표는 **글자수 `wc -m`**다. 한국어는 조사가 어절에 붙고 수학 문서는 수식·표 줄이 많아, `wc -w`(단어수)가 같은 분량의 서사형보다 **30~40% 낮게** 찍힌다(예: 이미 DEEP으로 인정된 hermes-deep는 742단어이나 본 벡터 확장편 1064단어보다 짧음). 그래서 단어수만으로 깊이를 판정하면 수학 DEEP을 부당하게 탈락시킨다 → **글자수·줄수를 정본 게이트**로, 단어수는 보조 참고로 둔다.

| 항목 | 이해편 `<concept>` | 확장편 `<concept>-advanced` |
|---|---|---|
| 대상 독자 | 고등학생 입문(본인 학습 노트) | 학부생~대학원생(이해편 전제) |
| **본문 글자수(`wc -m`)** ★정본 | **≥ 15,000** (기준의 ~60%) | **≥ 20,000** (기준의 ~80%) |
| 본문 줄수(`wc -l`) | **≥ 140** | **≥ 165** |
| 본문 섹션(`##`) 수 | **≥ 8** | **≥ 10** |
| 시각화(ASCII 그림/표/코드블록) | **≥ 3** | **≥ 2** + 발전지도 표 |
| Worked 예제(입력→과정→출력 손계산) | **≥ 1** | **≥ 2**(유도1+응용1) |
| 동기 서사("왜 배우나") | **필수**(1절 통째) | 권장(짧게) |
| FAQ/흔한 오해 | **필수 ≥ 3** | 함정 체크리스트 필수 |
| "다음 읽을 것"(책·영상·짝문서) | **필수** | "후속 질문" 필수 |
| 출처 | **≥ 7**(국내4+해외3) | **≥ 12**(국내5+해외7) |
| (참고) 단어수 `wc -w` | 보조 지표(하한 강제 아님) | 보조 지표 |

### 🟢 이해편 필수 골격
`## TL;DR`(3~5줄) → `## 핵심 포인트`(5) → `## 본문`[1절 **왜 필요했나**(동기 서사) / 2~4절 직관·비유·그림으로 정의(시각화 3+ 흩뿌림) / 5절 **Worked Example**(손계산 끝까지) / 6절 **흔한 오해·FAQ ≥3** / 7절 한눈 요약] → `## 더 깊이 — 확장편으로`(다리) → `## 다음 읽을 것`(책·강의·영상+짝문서) → `## 출처`.

### 🔵 확장편 필수 골격
`## TL;DR` / `## 핵심 포인트` → `## 1. 직관 압축`(이해편 1단락 요약, 중복금지) → `## 2. 정의·메커니즘` → `## 3. 왜 그런가(유도)`(유도/증명 스케치 worked) → `## 4. 대표 응용`(worked ≥2) → `## 5. 통합 의미`(역설·경계점) → `## 6. 🗺️ 개념 발전 지도`(**4방향 표 의무**: 가정을 풀면/무엇이 열리나/어디서 쓰나/더 알아야 할 것) → `## 7. 함정·체크리스트` → `## 출처` / `## 후속 질문·연결`.

### 🚦 분량·요소 객관 카운트 게이트 (커밋 전 필수 — 판단 아닌 측정)
이전 실패(419단어를 'deep'으로 오판)의 원인이 주관 판단 → **숫자로 강제**한다. 커밋 직전 측정:
```
wc -m reports/<slug>/report.md                          # ★정본: 글자수
wc -l reports/<slug>/report.md                          # 줄수
grep -cE '^## ' reports/<slug>/report.md                # 섹션수
grep -cE '^\|.*\||^```' reports/<slug>/report.md         # 시각화(표행+코드블록)
grep -cE '^- \[' reports/<slug>/report.md               # 출처수
wc -w reports/<slug>/report.md                          # (참고) 단어수
```
- 테이블의 **정본 지표(글자수·줄수)·섹션·시각화·worked·출처** 하한을 **하나라도 못 넘으면 머지 금지** → 본문 보강 후 재측정. (단어수는 참고만 — 글자수가 통과하면 단어수 미달은 무시.)
- **PR 본문에 측정값 표 첨부 의무**(예: `글자 22191/≥20000 ✅ · 줄 179/≥165 ✅ · 섹션 14/≥10 ✅ · 시각화 8/≥2 ✅ · 출처 16/≥12 ✅`).
- 자가 자문: "이건 이란-미국 보고서만큼 읽을 게 있나?" → 아니면 FAIL.
- **메타 규칙**: 지표가 내용과 안 맞아 보이면(예: 깊은데 단어수만 낮음) gold standard와 직접 비교해 **지표를 보정**하되, 그 근거(비교 수치)를 PIPELINE에 남긴다 — 게이트를 몰래 낮추지 말 것.

## 환경별 가용성 (중요)
| 단계 | 로컬 PC | 클라우드/모바일 |
|---|---|---|
| 수집: WebSearch/WebFetch | O | O |
| 수집: 네이버/유튜브 MCP | O | △ (커넥터 붙어야 함 — §0 점검) |
| 보고서 .md 합성 | O | O |
| 학습 카드 auto 렌더(Playwright) | O | ✗ → **manual 사용** |
| 갤러리 커밋·푸시(GitHub) | O | O |
| 옵시디언 저장 | 로컬 G: 직접 쓰기 | **Google Drive MCP** (§5, 검증됨 2026-06-21) |
| Slack 알림 | O(MCP) | O(MCP, 커넥터 붙으면) |

## 0. 사전 점검 (클라우드에서 1회)
- 네이버 MCP 가용 확인: `NaverSearch-get_current_korean_time` 호출 성공 여부. 실패 시 **국내 수집을 WebSearch(site:naver.com 등)로 대체**하고 그 사실을 보고서에 명시.
- Drive MCP 가용 확인: `Google_Drive search_files (title='001-주제리서치')` 로 폴더 존재 확인.

## 1. 수집 (C1/C2)
- 국내: 네이버 MCP `search_webkr / search_news / search_encyc / search_blog`(주제 한국어).
- 해외: `WebSearch`(영문 질의) → 핵심 소스 `WebFetch`로 정독.
- **국내+해외 균형 필수.** 중복 제거, 신뢰도 낮은 출처 배제.
- 산출: **fact-ledger**(주장 ↔ 출처 URL 표). 단일 자료 주장/충돌은 표시.

## 2. 합성 (C3) — frontmatter 스펙 엄수
```yaml
---
주제: <문자열>
날짜: <YYYY-MM-DD>          # 클라우드: get_current_korean_time 로 확인
깊이: quick | deep
카드모드: auto | manual | none
태그: [<주제태그>...]        # 첫 태그가 갤러리 카드 색을 정함
소스수: { 국내: N, 해외: M }
위키링크: ["[[연결노트]]", ...]
갤러리URL: "#r=<slug>"
---
```
본문 순서: `## TL;DR`(3~5줄) → `## 핵심 포인트` → `## 학습 카드` → `## 본문(섹션별)` → `## 출처(인용 링크)` → `## 후속 질문·연결([[위키링크]])`.
- **무환각**: 모든 사실 주장에 인용 [n]. 출처 없는 단정 0건. 해외 인용엔 한글 설명.
- **시작 전 [LESSONS.md](LESSONS.md)의 "방지 규칙 체크리스트"를 로드**하여 같은 실수 차단(복리 품질). DEEP는 개요+목록 금지 — why/how/비교/실전.

## 3. 학습 카드 (C8) — 카드모드 분기
- **auto (로컬만)**: `reports/<slug>/comics/card.html` 작성(retail 스타일: 웜화이트 #FFF8F0·Nunito·코랄·4분할) → 로컬 http 서버 → Playwright `browser_take_screenshot(#card)` → `comics/card.png`. 본문에 `![...](comics/card.png)` 임베드.
- **manual (클라우드 기본)**: 카드 PNG를 못 만드는 환경 → 본문 `## 학습 카드`에 **4분할 텍스트 카드(표/불릿)** 로 대체하거나, 컷별 이미지 프롬프트만 출력해 사용자가 무료 웹툴로 생성 후 `comics/`에 투입.
- **none**: 섹션 생략(quick 다이제스트).

## 4. 검수 (C9) — 독립 패스, self-approve 금지
별도 에이전트(또는 명시적 별도 단계)로 무환각·인용1:1·국내해외 균형·카드↔본문 일치·DEEP 깊이 게이트. 결함·수정·방지규칙을 **[LESSONS.md](LESSONS.md)** 에 append.

## 5. 옵시디언 저장 (C5)
### 로컬 PC
`G:\내 드라이브\00_Obsidian_Second Brain\Insight Miner\000-수집\001-주제리서치\` 에 `<YYYYMMDD>_<보고서 제목>.md` + `comics/card.png` 직접 복사.

### 클라우드/모바일 — Google Drive MCP (검증됨)
1. 폴더 ID 확보: `search_files(title='001-주제리서치')` → 폴더 id (2026-06-21 기준 `1nScRmPu8XhHElDEf2yjnmSHThGkacYVf`, 부모 000-수집 `1KmzoExv5bZLDOCJQSwrCabVw29gYUrIj`). 없으면 `create_file(mimeType folder)`.
2. 노트 생성: `create_file(title='<YYYYMMDD>_<보고서 제목>.md', parentId=<폴더id>, textContent=<.md 전문>, contentMimeType='text/markdown', disableConversionToGoogleType=true)`.
   - **주의**: `disableConversionToGoogleType=true` 필수(안 하면 Google Doc로 변환됨).
   - 이미지 임베드가 `comics/card.png`면 동일 폴더 안 `comics` 하위폴더 id를 찾아(`search_files title='comics' and parentId='<폴더id>'`, 없으면 create) `create_file(base64Content=<png base64>, contentMimeType='image/png', parentId=<comics id>)`.
3. **파일명 = `<작성날짜 YYYYMMDD>_<보고서 제목>`** (날짜 접두사 필수, 사용자 지시 2026-06-21). 예: `20260621_이란–미국 분쟁의 역사 — 20세기부터의 갈등 타임라인 심층 분석`. 날짜는 frontmatter `날짜` 값(클라우드는 `get_current_korean_time`)을 `YYYYMMDD`로. 본문은 갤러리 .md와 동일(단일 진실의 원천), 위키링크는 제목 부분으로 해석.

## 6. 갤러리 갱신·배포 (C4/C7)
1. `reports/<slug>/report.md` (+ auto면 `comics/card.png`) 추가.
2. `reports/manifest.json` 에 항목 추가: `{slug,title,date,depth,tags,tldr,sources,cover?,path}`. DEEP+최신이면 `cover:"comics/card.png"`로 피처드 히어로.
3. 커밋 → 푸시 → **PR 생성 → main 머지(기본 동작)** → GitHub Pages 자동 빌드. (별도 요청 없어도 머지까지 진행)
4. 라이브 확인: https://irun20000-eng.github.io/Search/

## 7. (옵션) Slack 알림 (C7)
Slack MCP `slack_send_message` 로 `{제목, TL;DR, 갤러리 URL}` 발송.

## 8. 합격 기준 (배포 전 확인)
① TL;DR 한눈 파악 ② 무환각(인용1:1) ③ 통찰·[[링크]] ④ 국내+해외 균형 ⑤ 카드 충실성 ⑥ LESSONS 갱신. 미달 시 반복.

---
스펙 정본: `.omc/specs/deep-interview-topic-research-pipeline.md` (로컬). 디자인 시스템: 라이트/웜화이트(#FFF8F0)+Nunito+코랄, 카드 토픽 색상바+기하 도형 커버.
