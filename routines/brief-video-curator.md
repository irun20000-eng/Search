# 루틴 지침 — Aside 기초자료(brief) → 갤러리 영상 노트 (Search 전용)

> 사용법: claude.ai/code → Routines 「영상갤러리 추가」 지침란에 아래 한 줄을 넣는다.
> `Search 리포의 routines/brief-video-curator.md 지침을 그대로 수행해줘. 새 자료 없으면 "처리할 새 자료 없음"만 보고.`
> 대상 리포 `irun20000-eng/Search`, 평일 10:00 KST.
>
> **2026-10-15 교체.** 구글 스파크가 10월 초 산출을 멈춰(→ `LESSONS.md` 2026-10-13) 입력원을
> 바꿨다. 이제 **사용자 PC 의 Aside 가 평일 08:30 에** 재생목록 `보자따라하자` 를 읽고, 유튜브
> 메타데이터와 **한국어 자막 전문**을 이 리포의 `yt-inbox` 브랜치에 `briefs/<video_id>.md` 로
> 올린다(규격: 그 브랜치의 `README.md`, schema `yt-brief/v1`). 이 루틴은 그 brief 를 읽고
> **영상 노트를 직접 쓴다** — 스파크가 하던 「분석」이 이제 이 세션의 몫이다.
> 옛 지침 `spark-video-curator.md` 는 역사 기록으로만 남긴다.
>
> 이 문서와 `VIDEO_PIPELINE.md` 가 어긋나면 **런북이 정본**이다(단, 입력원과 전사 절차는 이 문서).

당신은 `irun20000-eng/Search` 리포가 체크아웃된 클라우드 에이전트입니다. 생성은 **Claude 본체(구독)**
— 유료 API 호출 금지. Drive 접근은 Google Drive MCP(옵시디언 저장에만 쓴다).

## 무엇이 달라졌나 (스파크 시절 대비)

| | 스파크 시절 | 지금 |
|---|---|---|
| 입력 | Drive 의 구글 문서(스파크 분석본) | 리포 `yt-inbox` 브랜치의 UTF-8 평문 brief |
| 분석·작성 | 스파크(제미나이) | **이 세션(Claude)** — 자막을 읽고 VIDEO-NOTE 를 쓴다 |
| 전사 손상 대책 | 2회 읽기 대조 · 복원기 · 코퍼스 음절 검사 · 3건 상한 | **불필요** — 평문 git 파일이라 손상 경로가 없다 |
| 인용 검증 | 「노트 = 스파크 원본」까지만 보증 | **「인용 = 실제 자막」까지 기계 대조**(`tools/check_quotes.py`) |

## 처리 절차 (회차당 최대 5건 — 폐기·스킵은 상한 미차감)

1. **목록**
   ```bash
   git fetch origin yt-inbox
   git ls-tree --name-only origin/yt-inbox briefs/ | grep -E '/[A-Za-z0-9_-]{11}\.md$'
   ```
2. **중복 검사**: `videos/notes/<video_id>.md` 가 이미 있으면 skip(주 dedup). `videos/_skipped.json` 에
   같은 ID 가 있으면 그 사유를 보고에 함께 싣고 재시도한다(같은 실패를 조용히 반복하지 않기 위함).
3. **새 자료가 없으면 — 끝내기 전에 상류를 한 번 본다** (2026-10-13 도입, 대상만 바뀜)
   - `get_playlist_items(playlist_id: "PLNRs-HbobHU3n14u_AWBUTKe4wU8gOuYh", max_results: 20)`
   - 각 `videoId` 에 대해 노트도 brief 도 없는 것이 **수집 적체**다(= Aside 수집이 멈춤 — PC 꺼짐 등).
   - 단, `git ls-tree --name-only origin/yt-inbox routed/` 에 `<videoId>.md` 가 있으면 적체가 아니다 — Aside 가 다른 파이프라인으로 보낸 영상이다
     (2026-10-16 사용자 결정: **3분 미만 영상은 갤러리 게이트를 정직하게 넘을 수 없어 일반 노트로** 보낸다. 예: `h4ko-Np28w0`, 1:37).
   - 적체 0 → '처리할 새 자료 없음'만 보고하고 종료. 적체 ≥1 → 발행 0건이어도 12번 알림
     (`Aside 수집 적체 N편(최고령 MM-DD) · 최신 brief MM-DD · 발행 0건`).
   - ⚠️ 적체를 직접 처리하지 말 것 — 클라우드는 자막을 못 받는다. **검출·알림까지가 끝.**
   - 플레이리스트 조회 실패 시 판정을 생략하고 그 사실을 보고에 남긴다.
4. **brief 확보**
   ```bash
   mkdir -p /tmp/brief /tmp/spark
   git show origin/yt-inbox:briefs/<video_id>.md > /tmp/brief/<video_id>.md
   ```
   - `schema: yt-brief/v1` 과 `## 자막` 절이 있는지 확인한다. 자막 줄이 30줄 미만이거나 영상 길이에
     비해 터무니없이 짧으면(예: 20분 영상에 2분치) **폐기**(5번) — 부족한 자막으로 지어 쓰지 않는다.
   - `route: search` 가 아니면 skip 하고 보고.
5. **폐기 시 기록**: `videos/_skipped.json` 에 append — `{"video_id","date","reason","detail"}`.
   brief 는 지우지 않는다(이 루틴은 yt-inbox 브랜치에 쓰지 않는다).
6. **메타데이터**: `get_video_details` 로 처리 대상 ID 를 **배치 1회** 조회 → `/tmp/spark/meta.json`
   (`{"<id>": {"title","channelTitle","publishedAt","duration"}}`). **응답에 없는 ID 는 폐기**(무환각 검증기).
   brief 머리말의 제목·채널 값과 다르면 API 값을 쓴다.
7. **작성 — VIDEO-NOTE v1 블록** (`prompts/gemini-video-analysis.md` 의 계약 그대로, 작성자만 이 세션)
   brief 의 **자막과 설명만** 근거로 쓴다. 계약의 절대 규칙·품질 기준·분류 6종·출력 형식을 전부 따르고,
   자막 기반이라 아래를 더 지킨다:
   - **핵심 인용 = 자막 문장 그대로.** 해당 구간 자막 줄을 이어 붙여 옮기고, 허용되는 손질은
     띄어쓰기·문장부호뿐이다. 자동자막 오인식(예: `재민아이`)도 **고치지 않고 보존**한다 —
     고치면 발화 창작이 된다. 문장 경계가 없으면 의미 단위로 1~3문장 분량을 잘라 온다.
   - **타임스탬프 = 자막 줄의 시각.** 챕터 시작은 그 주제가 처음 나오는 자막 줄의 `[mm:ss]` 를 쓴다.
     그 챕터의 핵심 인용은 **그 챕터 구간 안의 자막**에서 고른다.
   - **화면만 보고 알 수 있는 것은 쓰지 않는다.** 자막이 「여기 누르시고」라고만 하면 버튼 이름을
     추측하지 말고 「설정 화면에서 해당 메뉴를 연다」처럼 들린 범위로만 적는다.
   - **영상 설명란**은 맥락 파악용이다. 강의·구매·협찬 링크와 홍보 문구는 노트에 옮기지 않는다.
   - 자동자막에서 또렷하지 않은 **제품명·모델명·수치는 단정하지 않는다**(계약의 규칙 그대로).
     ⚠ 비우기 전에 **설명란을 먼저 `grep`** 한다 — 자막에 0건인 이름이 업로더가 직접 쓴 설명란에는
     또렷하게 적혀 있을 수 있다(2026-10-15 `ego lite`). 있으면 「설명란에는 ~로 적혀 있다」로 출처를
     밝혀 쓴다.
   - **요약·팁 안의 「」는 축자 인용으로 읽힌다** — 자막 그대로 옮기거나 괄호를 푼다. `check_quotes` 는
     `**핵심 인용**` 줄만 대조하므로 이 자리에 닿지 않는다(2026-10-15).
   - 결과를 `/tmp/spark/<video_id>.txt` 에 저장한다(`===VIDEO-NOTE v1===` ~ `===END===`, `url:` 은 brief 의 url).
8. **적재**:
   `python3 tools/ingest_video.py --gemini /tmp/spark/<video_id>.txt --meta /tmp/spark/meta.json --added <오늘 YYYY-MM-DD>`
   **`--added` 를 반드시 넘긴다.**
9. **품질 게이트**
   - `python3 tools/verify_video.py videos/notes/<video_id>.md` — 하한 미달이면 **자막으로 돌아가 보강**한다
     (영상에 없는 내용을 채워 넣어 통과시키지 않는다). 3회 안에 못 넘기면 폐기·보고.
   - `python3 tools/check_quotes.py videos/notes/<video_id>.md /tmp/brief/<video_id>.md`
     FAIL(포함률 < 0.75) 이 있으면 그 인용을 **자막에서 다시 옮겨 적는다**. WARN 은 눈으로 확인.
   - `python3 tools/check_encoding.py videos/notes/<video_id>.md` — 사설영역·제어문자 차단 검사는 유지.
     「코퍼스에 없는 음절」 자문은 이제 전사 손상 탐지용이 아니므로 참고만 한다.
10. **검수 (self-approve 금지)**: `VIDEO_PIPELINE.md` §4 — 작성 컨텍스트가 없는 **별도 리뷰어 서브에이전트**에게
    노트와 brief, 9번 `check_quotes` 결과를 함께 준다. 인용이 자막에 있는지는 `check_quotes` 가 이미 기계로 대조했으므로
    리뷰어는 전수 대조를 다시 하지 않고 **WARN 으로 찍힌 인용만** 확인한다(2026-10-29 중복 검증 정리).
    리뷰어 항목: 자막 밖 지식 혼입 · 화면 추측 · 근거 없는 단정 · 태그/분류 적합성 · 챕터 커버리지 ·
    **요약부의 한정어**(한 줄 요약·TL;DR 의 각 줄을 받치는 본문 줄과 맞대어
    「…때가 있다」·「…것 같다」·「…고 말한다」가 살아 있는가 — 압축하면서 가장 먼저 떨어지는 자리다.
    LESSONS 2026-10-15). 불합격 시 재작업, 최대 3회.
11. **배포**: 작업 브랜치 commit + push → PR → **rebase 머지** → deploy-pages 확인.
    `git push origin main` 금지. 커밋 직전 `git diff --stat` 확인.
12. **옵시디언 저장**: 노트 내용을 그대로
    `create_file(title="<YYYYMMDD>_<제목>.md", parentId="1eCkQ7HySXci0UOL_dZwM0yTnS1NioUlk",
    contentMimeType="text/markdown", disableConversionToGoogleType=true, textContent=<노트>)` →
    `get_file_metadata(id)` 로 `parentId`·`fileSize` 검증. **`base64Content` 금지.**
13. **보고 + 알림**: 아래 형식으로 정리하고 **PushNotification** 1줄. 발행 0건이고 이상도 없으면 알림 생략
    (3번에서 적체가 잡힌 경우만 예외).

## 보고 형식
- **발행 N건 · 스킵 M건 · 게이트 미달 K건 · 폐기 L건**
- 3번을 돈 회차: **상류: Aside 수집 적체 P건 · 최신 brief YYYY-MM-DD**
- 각 발행 건: 제목 · 갤러리 URL · Drive 링크 · PR 머지 해시 · 게이트 측정값 · **check_quotes 결과(PASS/WARN 수)**
- **🔶 판단 애매 — 확인 필요**: 자막만으로 확신이 안 선 대목(화면 의존 구간, 들리지 않는 고유명사 등).
  애매하면 발행하지 말고 여기 남긴다.

## 안전·상한
- dedup = `videos/notes/<id>.md`(주) + `_skipped.json`(보조). 재실행해도 중복 없음.
- 회차당 **발행 5건** 상한(초과분 이월). brief 는 계속 남아 있으므로 다음 회차가 이어서 처리한다.
- **막히면 지어내지 말고 폐기 후 보고.** 자막이 근거의 전부다.
- 도구 prefix(`Google-Drive`/`PlayMCP`/`github`)는 세션마다 바뀔 수 있다 — 같은 기능 도구로 대체.
