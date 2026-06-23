# Search — 주제 리서치 갤러리 (Claude Code 운영 계약)

Claude Code 세션이 **오케스트레이터**다. 백엔드·크론·서버 코드 없음 — 세션이 `PIPELINE.md`를 그대로 따라 보고서를 만들고 갤러리·옵시디언에 반영한다. 정적 자산(`index.html`)만 코드.

## 작업 시작 전 필수 (preflight)
1. **`PIPELINE.md`를 먼저 읽는다** — 보고서 작업의 정본 런북(트리거·수집·합성·검수·배포 전 절차). 이 CLAUDE.md는 요약·포인터일 뿐, 상세는 PIPELINE이 정본.
2. **`LESSONS.md`의 "방지 규칙 체크리스트"를 로드**한다 — 같은 실수 재발 차단(품질 복리). 검수 후 새 교훈을 거기에 append.
3. 스펙 정본: `E:\AI_Project\.omc\specs\deep-interview-topic-research-pipeline.md` (로컬).

## 트리거
```
주제: <조사할 주제>
깊이: quick | deep
카드모드: auto | manual | none   # 생략 시 manual(클라우드)/auto(로컬)
```
"시리즈" 지시 → 메인 1편 + 내가 선정·사전보고하는 파생 3편 = 4편 DEEP, 각 편 독립 게이트 통과.

## 절대 규칙 (어기기 쉬움 — 항상 적용)
- **"작성만 하고 멈추지 말 것."** 보고서 요청 = 작성→커밋→푸시→PR→**main 머지**→갤러리 반영→**옵시디언 저장**까지가 완료 1건. 별도 언급 없어도 끝까지 수행.
- **무환각**: 모든 사실 주장에 인용 `[n]`. 출처 없는 단정 0건. 해외 인용엔 한글 설명. 국내(네이버 MCP)+해외(WebSearch) 균형 필수.
- **검수는 별도 패스 · self-approve 금지.** 작성한 컨텍스트에서 스스로 합격 처리하지 않는다(작성 ≠ 검수).
- **DEEP 분량 게이트는 측정으로 강제(판단 아님).** 커밋 직전 측정, 하한 미달이면 **머지 금지·본문 보강**:
  - ★정본 지표 = **글자수 `wc -m`** (개념 이해편 ≥15,000 / 확장편 ≥20,000). 줄수·섹션·시각화·worked·출처 하한은 PIPELINE "분량·구조 보장 테이블".
  - `wc -w`(단어수)는 **참고만** — 한국어+수식은 동일 분량 서사형보다 30~40% 낮게 찍혀 부당 탈락. gold standard = 이란-미국 보고서 25,104자.
  - **PR 본문에 측정값 표 첨부 의무.** 지표 보정은 가능하나 gold standard 비교 근거를 남길 것 — 게이트를 몰래 낮추지 말 것.
- **개념 설명형은 투트랙**(이해편 `<concept>` + 확장편 `<concept>-advanced`), 둘 다 DEEP, 역할 분담으로 중복 금지, 문체 평어.
- **비주얼 톤 = 라이트/웜화이트(#FFF8F0)+Nunito+코랄.** 다크 기본 가정 금지. 큰 시각 변경 전 Figma 시안 확인. 학습카드 임베드는 작게(기본 1장 4분할 요약).

## 환경 차이 (중요)
- **클라우드/모바일은 WebFetch 403을 전제** — WebSearch 요약 + 네이버 MCP 스니펫 다중 교차검증으로 사실 확정(단일 스니펫 단정 금지).
- 학습카드 `auto`(HTML/SVG→Playwright PNG 렌더)는 **로컬 전용** → 클라우드는 `manual`.
- 옵시디언 저장: 로컬 = `G:\내 드라이브\00_Obsidian_Second Brain\Insight Miner\000-수집\001-주제리서치\`에 직접 쓰기 / 클라우드 = Google Drive MCP(`001-주제리서치` 폴더, `disableConversionToGoogleType=true` 필수). 파일명 = `<YYYYMMDD>_<제목>`.
- 세션 시작 시 네이버 MCP·Drive MCP 가용 점검(PIPELINE §0).

## 명령
```bash
# 로컬 갤러리 미리보기
cd Search && python -m http.server 8080   # http://localhost:8080

# 커밋 전 분량 게이트 측정 (개념 설명서)
wc -m reports/<slug>/report.md            # ★정본 글자수
wc -l reports/<slug>/report.md            # 줄수
grep -cE '^## ' reports/<slug>/report.md  # 섹션수
grep -cE '^- \[' reports/<slug>/report.md # 출처수
```

## 구조
- `index.html` — 정적 갤러리(카드 → 전문, 태그/주제/날짜 필터).
- `reports/<slug>/report.md` — 보고서 전문(frontmatter+본문). **단일 진실의 원천**(볼트 전문 = 갤러리 렌더, 분리 금지). ※ README의 `<slug>.md` 표기와 달리 실제 파일명은 `report.md`.
- `reports/manifest.json` — 카드 메타 목록(`{slug,title,date,depth,tags,tldr,sources,cover?,path}`). 보고서 추가 시 갱신.
- `reports/<slug>/comics/` — 학습카드 PNG(auto 모드 산출).
- `LESSONS.md` — 검수 학습 원장(방지규칙 누적). 라이브 갤러리: https://irun20000-eng.github.io/Search/
