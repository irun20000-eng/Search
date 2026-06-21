# Search — 주제 리서치 갤러리

주제 하나를 입력하면 국내(네이버 MCP)+해외(WebSearch) 출처를 모아 **무환각·인용 기반**의 단일 `.md` 보고서를 만들고, 이를 옵시디언 볼트와 이 GitHub Pages 갤러리에 동일하게 렌더링한다. Claude Code 세션이 오케스트레이터이며 별도 백엔드/크론은 없다.

- **실행 절차(모바일/클라우드 포함)**: [PIPELINE.md](PIPELINE.md) — 세션이 그대로 따라 도는 런북
- 스펙 정본: `E:\AI_Project\.omc\specs\deep-interview-topic-research-pipeline.md`
- 단일 `.md` = 진실의 원천 (볼트 전문 = 갤러리 렌더, 분리하지 않음)

## 구조
```
index.html              # 정적 갤러리 (카드 → 전문, 태그/주제/날짜 필터)
reports/
  manifest.json         # 카드 메타데이터 목록 (보고서 추가 시 갱신)
  <slug>/
    <slug>.md           # 보고서 전문 (frontmatter + 본문)
    comics/             # 학습만화 컷 이미지 (auto: HTML/SVG→PNG)
LESSONS.md              # 검수 학습 원장 (방지규칙 누적, 복리 품질)
```

## 보고서 .md 구조
frontmatter(주제·날짜·깊이·만화모드·태그·소스수·위키링크·갤러리URL) →
`## TL;DR` → `## 핵심 포인트` → `## 학습만화` → `## 본문` → `## 출처` → `## 후속 질문·연결`

## 멀티 에이전트 (독립 패스 + 공유 아티팩트)
작성 → 만화(auto/manual/hybrid) → 검수(별도 컨텍스트, self-approve 금지). 공유: fact-ledger / style sheet / LESSONS.md.

## 만화 모드
- `auto`: HTML/SVG 패널을 Playwright로 PNG 렌더 (완전자동·$0)
- `manual`: 컷별 프롬프트만 출력 → 무료 웹툴로 고화질 생성 후 동일 경로 투입
- `hybrid`: auto 초안 + 원하는 보고서만 고화질 교체 (경로 고정)

## 로컬 미리보기
```
cd Search && python -m http.server 8080   # http://localhost:8080
```
