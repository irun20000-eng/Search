---
주제: 헤르메스 에이전트(Hermes Agent)란 무엇인가 — 초보자용 설치·활용
날짜: 2026-06-21
깊이: quick
카드모드: none
태그: [AI에이전트, 오픈소스, NousResearch, 자가발전, 로컬AI]
소스수: { 국내: 3, 해외: 3 }
위키링크: ["[[AI 에이전트]]", "[[오픈소스 LLM]]", "[[로컬 AI]]"]
갤러리URL: "#r=hermes-agent-quick"
---

# 헤르메스 에이전트(Hermes Agent) — 퀵 다이제스트

## TL;DR
- **헤르메스 에이전트**는 Nous Research가 만든 **오픈소스(MIT) 자율 AI 에이전트**로, 내 컴퓨터/서버에 직접 설치해 쓴다 [1][2].
- 보통 챗봇과 달리 **영속 메모리 + 자가발전(스킬 학습) 루프**가 핵심 — 쓸수록 나를 더 잘 알고 더 유능해진다 [2][3].
- 설치는 **한 줄 명령**이면 끝(의존성 자동 설치). 터미널에서 쓰거나 텔레그램·슬랙·디스코드 등으로도 대화 [1][3].
- 특정 모델에 묶이지 않아 **여러 LLM(수백 종)** 을 갈아끼울 수 있다 [1][3].
- 2026년 들어 경쟁 에이전트 **오픈클로(OpenClaw)** 를 사용량·개발자 관심도에서 추월하며 화제 [4].

## 핵심 포인트
1. **무엇**: "쓸수록 함께 성장하는 에이전트(The Agent That Grows With You)" — 경험에서 스킬을 만들고, 과거 대화를 검색해 맥락을 끌어온다 [1][3].
2. **왜 다른가**: 일회성 질의응답이 아니라 **세션이 끝나도 상태(메모리·스킬)가 남는** 지속형 실행체다 [국내: 5].
3. **어디서 도나**: Linux · macOS · WSL2 · Android(Termux), 그리고 최근 **네이티브 윈도우** 까지 [2][6].
4. **활용 예**: 경쟁사 조사 자동화, CI/CD 모니터링, 반복 업무·프로젝트 추적 등 [국내: elancer].

## 본문

### 1. 한 줄 정의
헤르메스 에이전트는 "사용자가 맡긴 일을 여러 도구와 연결해 직접 처리하도록 설계된 오픈소스 AI 에이전트"다 [국내: elancer]. Nous Research는 "중앙 집중형 AI의 한계를 극복"하고 "사용자의 로컬 환경에서 독립적으로 작동하는 주권적(sovereign) AI"를 목표로 이를 개발했다 [국내: Daddy Makers].

### 2. 설치 (초보자용, 한 줄)
운영체제별 권장 설치 [2]:

```bash
# Linux / macOS / WSL2 / Android(Termux)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Windows (네이티브 PowerShell)
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

- 사전 준비물은 사실상 **Git** 하나뿐이고, 나머지(Python·Node.js·ripgrep·ffmpeg)는 설치 프로그램이 자동으로 깔아 준다 [2].
- 설치 후 셸을 새로고침하고 `hermes` 를 실행하면 시작된다 [2]:

```bash
source ~/.bashrc   # 또는 ~/.zshrc
hermes             # 터미널 UI 시작
hermes model       # 사용할 LLM 설정
hermes setup --portal   # Nous 포털 빠른 설정(모델+기본 도구 한 번에)
```

> 참고: 과거엔 윈도우에서 WSL2 사용이 권장됐으나 [국내: tilnote], 이후 **네이티브 윈도우 지원이 추가**되었다 [2][6].

### 3. 처음 쓸 때 팁 (초보자 주의)
- "작업 범위와 결과물을 구체적으로 지시"하라 [국내: elancer].
- **모델 비용·사용량 한도**를 먼저 확인하라 — 에이전트는 토큰을 많이 쓸 수 있다 [국내: elancer].
- 처음엔 "테스트 폴더에서만 작업하게" 두고, 저장된 스킬을 주기적으로 점검하라 [국내: elancer].

## 출처(인용 링크)
- [1] Hermes Agent 공식 사이트 — https://hermes-agent.nousresearch.com/ (해외)
- [2] Hermes Agent 공식 문서 · 설치 — https://hermes-agent.nousresearch.com/docs/getting-started/installation (해외)
- [3] GitHub · NousResearch/hermes-agent — https://github.com/nousresearch/hermes-agent (해외)
- [4] AI타임스 「헤르메스, 신규 기여자 수에서 오픈클로 역전」 — https://www.aitimes.com/news/articleView.html?idxno=211931 (국내)
- [5] tilnote 「Hermes Agent란 설치 사용법 핵심 기능 정리」 — https://tilnote.io/pages/69dc5925df448d30aa398a63 (국내)
- [6] 이데일리 「엔비디아, 디퓨전젬마 가속화…헤르메스 에이전트 기본 윈도우 지원 추가」 — https://n.news.naver.com/mnews/article/018/0006303971 (국내)
- elancer 「Hermes Agent 사용법, 설치부터 활용 노하우까지」 — https://www.elancer.co.kr/blog/detail/1086 (국내)
- Daddy Makers 「헤르메스 에이전트 개발배경, 설치 및 사용방법」 — http://daddynkidsmakers.blogspot.com/2026/05/blog-post.html (국내)

## 후속 질문·연결
- 더 깊게: [[헤르메스 에이전트(Hermes Agent) — 심층 리서치]] (DEEP 버전)
- 헤르메스 에이전트와 [[Hermes 3]] **모델**은 어떻게 다른가? (에이전트=하네스, Hermes 3=LLM)
- [[오픈클로(OpenClaw)]] 와 비교하면 통제성·자율성 트레이드오프는?
- 관련: [[AI 에이전트]] · [[오픈소스 LLM]] · [[로컬 AI]]
