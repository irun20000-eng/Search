# Search — 주제 리서치 갤러리 (Claude Code 운영 계약)

Claude Code 세션이 **오케스트레이터**다. 백엔드·크론·서버 코드 없음 — 세션이 `PIPELINE.md`를 그대로 따라 보고서를 만들고 갤러리·옵시디언에 반영한다. 정적 자산(`index.html`)만 코드.

## 작업 시작 전 필수 (preflight)
1. **`PIPELINE.md`를 먼저 읽는다** — 보고서 작업의 정본 런북(트리거·수집·합성·검수·배포 전 절차). 이 CLAUDE.md는 요약·포인터일 뿐, 상세는 PIPELINE이 정본.
2. **`LESSONS.md`의 "방지 규칙 체크리스트"를 로드**한다 — 같은 실수 재발 차단(품질 복리). 검수 후 새 교훈을 거기에 append.
2-1. **세션을 이어받는 자리라면 `HANDOVER.md` 를 먼저 본다** — 지금 무엇이 열려 있나(서가 가로지르는 것·리포 바깥 일). 수학사는 그쪽이 아니라 `math/ROADMAP.md` §11 이 인계를 맡는다. **계약문서(이 파일·PIPELINE)는 잘 안 바뀌고, HANDOVER 는 살아 있는 목록이다.**
3. 스펙 정본: `E:\AI_Project\.omc\specs\deep-interview-topic-research-pipeline.md` (로컬).

## 트리거
```
주제: <조사할 주제>
깊이: quick | deep
카드모드: auto | manual | none   # 생략 시 manual(클라우드)/auto(로컬)
```
"시리즈" 지시 → 메인 1편 + 내가 선정·사전보고하는 파생 3편 = 4편 DEEP, 각 편 독립 게이트 통과.

### 영상 노트 · 가이드 (상세는 `VIDEO_PIPELINE.md`)
```
영상: <유튜브 URL>          # 다음 줄에 --- 를 두고 제미나이 분석 결과를 붙여넣는다
가이드: <주제>               # 난이도: 입문|중급|고급 (생략 시 입문)
영상 프롬프트                # 제미나이용 프롬프트 전문 출력
```
- **유튜브 자막 자동수집은 불가**(클라우드 IP 차단) → 영상 분석은 제미나이 수동. 이건 우회로가 아니라 정해진 설계다.
- **영상 메타데이터(제목·채널·길이·게시일)는 절대 모델에게 묻지 않는다.** `get_video_details`가 정본이다. 응답에 ID가 없으면 존재하지 않는 영상 → 폐기(무환각 검증기).
- 영상 노트·가이드의 옵시디언 폴더는 리서치와 **다르다**: `011-보고따라해` = `1eCkQ7HySXci0UOL_dZwM0yTnS1NioUlk`.
- `videos/notes/<ID>.md` 파일이 갤러리 렌더 원본이다. 볼트 사본은 `sync_obsidian.py` 가 만든다.
- **개념노트 정본도 리포다**(2026-08-22 이전에는 구글드라이브 `학습자료` 폴더였다).
  `concept/notes/*.md` 가 프론트매터를 그대로 갖고 `build_concept_manifest.py` 가 그것으로
  manifest 를 만든다. 그래서 클라우드·러너에서도 갤러리를 갱신할 수 있다. `ingest_concept.py` 는 폐지.

## 절대 규칙 (어기기 쉬움 — 항상 적용)
- **"작성만 하고 멈추지 말 것."** 보고서 요청 = 작성→커밋→푸시→PR→**main 머지**→갤러리 반영→**옵시디언 저장**까지가 완료 1건. 별도 언급 없어도 끝까지 수행.
- **무환각**: 모든 사실 주장에 인용 `[n]`. 출처 없는 단정 0건. 해외 인용엔 한글 설명. 국내(네이버 MCP)+해외(WebSearch) 균형 필수.
- **용어 주석 = 각주 `[^라벨]`**(상세는 PIPELINE §2). 어려운 용어는 본문 흐름 안 끊고 `[^라벨]` 참조 → 하단 정의. 갤러리가 위첨자+"용어 주석" 섹션으로 자동 렌더. **`[^라벨]`=용어설명 / `[n]`=출처** — 별개 체계, 섞지 말 것.
- **검수는 별도 패스 · self-approve 금지.** 작성한 컨텍스트에서 스스로 합격 처리하지 않는다(작성 ≠ 검수).
- **DEEP 분량 게이트는 측정으로 강제(판단 아님).** 커밋 직전 측정, 하한 미달이면 **머지 금지·본문 보강**:
  - ★정본 지표 = **글자수 `LC_ALL=C.UTF-8 wc -m`** (개념 이해편 **≥8,000자** / 확장편 **≥11,000자**). ⚠️ **로케일 없는 `wc -m`은 바이트를 센다**(한글 1자=3바이트) — 반드시 `LC_ALL=C.UTF-8`을 붙일 것. 줄수·섹션·시각화·worked·출처 하한은 PIPELINE "분량·구조 보장 테이블".
  - `wc -w`(단어수)는 **참고만** — 한국어+수식은 동일 분량 서사형보다 30~40% 낮게 찍혀 부당 탈락. gold standard = 이란-미국 보고서 25,104자.
  - **PR 본문에 측정값 표 첨부 의무.** 지표 보정은 가능하나 gold standard 비교 근거를 남길 것 — 게이트를 몰래 낮추지 말 것.
- **개념 설명형은 투트랙**(이해편 `<concept>` + 확장편 `<concept>-advanced`), 둘 다 DEEP, 역할 분담으로 중복 금지, 문체 평어.
- **비주얼 톤 = 라이트/웜화이트(#FFF8F0)+Nunito+코랄.** 다크 기본 가정 금지. 큰 시각 변경 전 Figma 시안 확인. 학습카드 임베드는 작게(기본 1장 4분할 요약).
  - **예외 — `math/` 수학사 섹션(2026-08-21 사용자 승인).** 고문서·아카이브 톤: 세리프 본문, 미색 지면(#FAF6EC), 잉크빛 텍스트, 시에나 강조(#9C5A2C), 유형 4색만 절제 사용. 라이트가 기본이고 **다크는 2026-08-21 사용자 승인으로 추가**했다(양피지 → 황혼: 지면 #1B1713, 잉크 #EDE3D2, 강조 #C88A52). SVG 도해는 지면색을 파일 안에 갖고 있어 CSS 변수가 닿지 않으므로 다크에서 `filter:brightness(.84)` 로 눌러 앉힌다. 사용자가 "기존 Search 톤 유지" 선택지를 보고 이 톤을 고른 의도적 예외이니 되돌리지 말 것. 목업 승인 절차는 그대로 지켰다(`math/_design/mockup-v1.html`).
  - **예외 — `math/` 에서만 KaTeX 허용.** LaTeX 금지 규칙의 근본 원인은 *갤러리에 수식 렌더러가 없어 옵시디언과 웹이 달라 보이는 것*이었다. 옵시디언은 `$…$`를 원래 렌더하므로, `math/index.html`에 KaTeX를 넣으면 패리티가 오히려 회복된다. `reports/`·`videos/`·`guides/`는 기존대로 유니코드 평문을 쓴다.

## 환경 차이 (중요)
- **클라우드/모바일은 WebFetch 403을 전제** — WebSearch 요약 + 네이버 MCP 스니펫 다중 교차검증으로 사실 확정(단일 스니펫 단정 금지).
- 학습카드 `auto`(HTML/SVG→Playwright PNG 렌더)는 **로컬 전용** → 클라우드는 `manual`.
- **옵시디언 볼트는 사본이다. 정본은 항상 리포.** (2026-08-22 통일) 서가마다 제각각이던 것을
  `tools/sync_obsidian.py` 하나로 묶었다 — 리포 → 볼트, **없을 때만 쓰고 이미 있으면 건드리지 않는다**.
  토요일마다 볼트에서 노트끼리 위키링크를 거는 작업이 있어 덮으면 매주 사라진다.
  이미 있는지는 **파일 이름이 아니라 내용 속 식별자**(`#r=슬러그`·`youtu.be/<ID>`·`#n=`)로 본다 —
  볼트 파일명은 손으로 붙여 온 것이라 manifest 제목과 다르다(이름으로 보면 60편을 못 찾고 중복 생성한다).
  `python tools/sync_obsidian.py --dry-run` 으로 먼저 보고 돌릴 것.
  **`--check` 는 볼트가 리포와 어긋났는지 재기만 한다**(쓰지 않음, 어긋나면 exit 1) —
  「없을 때만 쓴다」의 대가인 *뒤처짐*(리포만 고침)과 *배너없음*(클라우드에서 직접 씀)을
  잡는다. 볼트 쪽 추가는 어긋남으로 세지 않는다. 수학사는 `sync_math_obsidian.py`
  (유형별 하위폴더·_MOC 때문에 따로)이며 같은 규칙을 쓴다.
  폴더: 리서치 `001-주제리서치` · 수학사 `002-수학사` · 개념노트 `003-카드뉴스학습자료` ·
  영상노트/가이드 `011-보고따라해`.
- 세션 시작 시 네이버 MCP·Drive MCP 가용 점검(PIPELINE §0).

## 명령
```bash
# 로컬 갤러리 미리보기
cd Search && python -m http.server 8080   # http://localhost:8080

# 영상 노트·가이드 게이트
python3 tools/verify_video.py videos/notes/<영상ID>.md
python3 tools/verify_guide.py guides/<슬러그>/guide.md
python3 tools/render_parity.py            # 영상 갤러리 구조 변경 시 동일성 대조

# 수학사(math/) — 정본 절차는 MATH_PIPELINE.md
python3 tools/verify_math.py                 # 스키마 + 유형별 분량 게이트
python3 tools/verify_math.py --backlog       # 백로그 2채널 (위키링크 + 발전단계 인물)
python3 tools/verify_math.py --symmetry      # frontmatter 상호참조 대칭 보고 (게이트 아님)
python3 tools/build_math_manifest.py         # math/manifest.json
python3 tools/build_link_index.py            # 루트 link-index.json (manifest 뒤에 실행)
python3 tools/build_math_status.py           # ROADMAP 「자동 측정」 블록 (link-index 뒤에 실행)
python3 tools/sync_math_obsidian.py --dry-run  # 볼트 002-수학사/ 동기화

# 커밋 전 분량 게이트 측정 (개념 설명서)
LC_ALL=C.UTF-8 wc -m reports/<slug>/report.md   # ★정본 글자수(로케일 필수! 없으면 바이트)
wc -l reports/<slug>/report.md            # 줄수
grep -cE '^## ' reports/<slug>/report.md  # 섹션수
grep -cE '^- \[' reports/<slug>/report.md # 출처수
```

## 구조
- `index.html` — 정적 갤러리(카드 → 전문, 태그/주제/날짜 필터).
- `reports/<slug>/report.md` — 보고서 전문(frontmatter+본문). **단일 진실의 원천**(볼트 전문 = 갤러리 렌더, 분리 금지). ※ README의 `<slug>.md` 표기와 달리 실제 파일명은 `report.md`.
- `reports/manifest.json` — 카드 메타 목록(`{slug,title,date,depth,tags,tldr,sources,cover?,path}`). 보고서 추가 시 갱신.
- `reports/<slug>/comics/` — 학습카드 PNG(auto 모드 산출).
- `videos/` — 영상 노트 갤러리. `manifest.json` + `notes/<영상ID>.md`. **1MB 단일 HTML이었던 것을 데이터 주도로 이관**(모바일에서 노트 1개 추가로 갱신 가능).
- `guides/` — 따라하기 가이드 갤러리. `manifest.json` + `<슬러그>/guide.md`. 관련 영상은 검증된 것만 캐시.
- `math/` — **수학사 아카이브**(2026-08-21 신설). `manifest.json` + `notes/<슬러그>/note.md` + `assets/`. 원자 4종(세기·개념·인물·일화)이 세기×개념×인물로 교차 참조되는 관계형 구조라 평면 갤러리와 데이터 모델이 다르다. 정본 런북은 **`MATH_PIPELINE.md`**.
- **테마 저장 키는 `stTheme` 하나다**(2026-08-21 통일). 예전엔 리서치·가이드 `stTheme`, 영상 `vgTheme`, 허브 `theme` 로 갈려
  페이지를 넘을 때마다 테마가 튀었다. 영상노트만 기존 사용자 설정을 잃지 않도록 `vgTheme` 를 읽기 폴백으로 남겨 뒀다.
  새 페이지를 만들 때 다른 키를 쓰지 말 것.
- `link-index.json`(루트) — 7개 갤러리 통합 링크 조회표. **항목마다 `검색어`**(각 갤러리 태그를 공백으로 이은 문자열)를 함께 실어 허브 검색이 제목만이 아니라 태그로도 걸리게 한다(2026-08-29). 리스트가 아니라 문자열인 이유는 이 파일을 모든 페이지가 받아 가기 때문 — 자세한 것은 `tools/build_link_index.py` 머리말. 본문 `[[위키링크]]`가 갤러리 경계를 넘게 한다. `tools/build_link_index.py` 산출물이며 **직접 편집 금지**. 자동 정규화로 안 잡히는 별칭만 `link-aliases.json`에 손으로 적는다.
- `prompts/gemini-video-analysis.md` — 제미나이 영상 분석 프롬프트(정본).
- `tools/` — 게이트 측정기·인제스트·이관 대조 스크립트.
- `routines/` — 예약 루틴 지침. `spark-video-curator.md` = 스파크 영상 분석본 → 갤러리 발행(정본 절차는 `VIDEO_PIPELINE.md`).
- `HANDOVER.md`(루트) — **인계 문서.** 열려 있는 것·닫힌 것·완료의 정의. 살아 있는 목록이라 자주 바뀐다(수학사 인계는 `math/ROADMAP.md` §11).
- `LESSONS.md` — 검수 학습 원장(방지규칙 누적). 라이브 갤러리: https://irun20000-eng.github.io/Search/
