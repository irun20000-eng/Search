---
주제: Orca(오르카) — 병렬 AI 코딩 에이전트 IDE(ADE) 완전 가이드
날짜: 2026-07-17
깊이: deep
카드모드: auto
대상수준: 실무 가이드(DEEP)
태그: [AI도구, Orca, ADE, ClaudeCode, 코딩에이전트, 병렬개발, gitworktree, 생산성]
소스수: { 국내: 5, 해외: 8 }
위키링크: ["[[Orca 에이전트 IDE]]", "[[클로드 코드]]", "[[git worktree]]", "[[코딩 에이전트]]", "[[클로드 MCP 가이드]]"]
갤러리URL: "#r=orca-agent-ide"
---

# Orca(오르카) — 병렬 AI 코딩 에이전트 IDE 완전 가이드

> "AI 하나 쓰던 시대는 끝"이라는 말이 나온다. Orca는 Claude Code·Codex 같은 CLI 코딩 에이전트를 **여러 개 동시에**, 각자 격리된 **git worktree**에서 굴리고 데스크톱·모바일에서 지휘하는 오픈소스 **ADE(Agent Development Environment)**다. 이 글은 "Orca가 무엇이고 → 왜 지금 뜨는지 → 어떻게 동작하는지 → 무엇을 할 수 있는지 → 어떻게 깔고 쓰는지 → 요금·유사도구·한계"까지 한 편에 정리한 실무 가이드다. (조회일 2026-07-17, 버전 v1.4.143 기준.)

## TL;DR
- **Orca는 IDE가 아니라 ADE(Agent Development Environment)** 다. 코드를 직접 쓰는 편집기가 아니라, **여러 AI 코딩 에이전트를 병렬로 실행·비교·머지**하는 지휘 환경이다 [국내 joy014][2].
- 핵심 설계는 **격리된 git worktree**. 작업마다 별도 worktree·터미널·브라우저·컨텍스트를 줘서, 여러 에이전트가 **서로 충돌·오염 없이** 동시에 다른(혹은 같은) 문제를 푼다 [1][국내 min-inter].
- **40종 이상의 CLI 에이전트**(Claude Code·Codex·Cursor CLI·Copilot CLI·Grok·OpenCode·Pi·Devin·Goose·Cline 등)를 붙일 수 있고, **"어떤 CLI 에이전트든" 작동**한다. 붙일 때는 **내 구독/API 키를 그대로 사용**한다 [1][국내 bihyun07].
- **MIT 라이선스 오픈소스라 Orca 자체는 무료**. 다만 에이전트 사용료(Claude Code·ChatGPT/Codex 구독, API 토큰)는 **내 계정에 청구**된다 [1][국내 ideasman].
- **데스크톱(macOS·Windows·Linux) + 모바일 컴패니언(iOS·Android)**. 모바일로 에이전트 상태·사용량(rate limit) 실시간 확인, **계정 hot-swap**까지. 2026년 상반기 rate limit·요금 티어 조임의 통증을 정면으로 건드려 화제 [3][국내 qjc].
- 저장소 2026-03-17 생성, 조회일 기준 **GitHub 20.7k stars·1.5k forks**, 최신 v1.4.143(2026-07-16). 넉 달 만의 급성장 [1].

## 핵심 포인트
1. **작성에서 지휘로.** 코딩의 무게중심이 "내가 타이핑" → "에이전트 함대를 지휘"로 옮겨간다. ADE라는 이름이 그 변화를 먼저 붙인 것 [국내 iamwonny87].
2. **worktree 격리 = 병렬의 안전판.** 브랜치 저글링 없이 여러 에이전트가 동시에 작업 [1].
3. **BYO 구독.** Orca는 무료, 에이전트는 내 계정으로 [국내 bihyun07].
4. **모바일 지휘 + 계정 hot-swap.** rate limit 시대의 실질 통증 해결 [3].
5. **오픈소스지만 신생.** 유지가능성·권한·리소스는 따로 점검해야 [국내 bihyun07].

## 1. Orca란 무엇인가 — IDE에서 ADE로

전통적 **IDE(Integrated Development Environment)** 는 사람이 코드를 **직접 쓰는** 편집기다(VS Code, JetBrains 등). Orca는 그 자리를 **ADE(Agent Development Environment, 에이전트 개발 환경)** 로 다시 정의한다 — 사람이 코드를 치는 게 아니라, **여러 AI 에이전트에게 과제를 나눠주고 그 결과를 지휘·비교·병합**하는 환경이다 [국내 joy014][2].

만든 곳은 **Stably AI**(GitHub 조직 `stablyai`)이고, 저장소는 `github.com/stablyai/orca`다. 공식 소개 문구가 성격을 압축한다: *"the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop and mobile."*(병렬 에이전트 **함대(fleet)** 를 다루는 ADE. 어떤 코딩 에이전트든 **내 구독으로** 실행. 데스크톱·모바일 지원.) [1].

정리하면 Orca의 정체성은 세 축이다:
- **오케스트레이터**: 여러 코딩 에이전트를 한 화면에서 나란히(side-by-side) 돌린다.
- **격리 실행기**: 각 에이전트를 독립 git worktree에 묶어 충돌·컨텍스트 오염을 막는다.
- **지휘 인터페이스**: 데스크톱과 모바일에서 각 에이전트의 진행·사용량을 실시간 추적하고 결과를 병합한다.

> 이 갤러리를 만드는 Claude Code 세션도 "세션이 오케스트레이터"라는 점에서 결이 같다. 다만 우리 파이프라인은 **클라우드 단일 세션**이 순차로 도는 구조인 반면, Orca는 **로컬(또는 원격)에서 여러 CLI 에이전트를 worktree로 병렬 조율**한다. "한 명이 순서대로" vs "여러 명이 동시에"의 차이다.

## 2. 왜 지금 뜨나 — 단일 에이전트에서 '함대'로

2025년까지 AI 코딩은 대체로 **에이전트 하나**를 붙잡고 대화하는 방식이었다. Claude Code든 Codex든, 터미널 하나에 에이전트 하나. 그런데 2026년 들어 흐름이 바뀌었다 [국내 iamwonny87][국내 skwu1]:

- **에이전트가 충분히 유능해져** 사람이 여러 과제를 **동시에** 위임할 수 있게 됐다. "이건 A에게, 저건 B에게" 병렬 위임의 실익이 커졌다.
- 같은 문제를 **여러 에이전트에게 동시에** 풀게 하고 **결과를 비교해 이긴 것을 채택**하는 방식(경쟁 실행)이 품질을 끌어올린다.
- 그런데 한 저장소(repo)에서 에이전트 여럿을 돌리면 **파일 충돌·git 스태시 지옥·컨텍스트 오염**이 터진다. 이 병목을 **worktree 격리**로 푼 것이 Orca의 핵심 기여다 [1][국내 min-inter].

여기에 **타이밍**이 겹쳤다. 2026년 상반기 Anthropic·OpenAI가 **rate limit과 요금 티어를 조였고**, 개발자들이 "지금 내 사용량이 얼마 남았나", "한 계정이 막히면 어쩌나"로 스트레스를 받았다. Orca는 **실시간 rate limit 표시 + 계정 hot-swap(즉시 전환)** 으로 바로 이 지점을 건드렸다 [3][국내 qjc]. "묻지도 따지지도 말고 써라" 수준의 반응이 나온 배경이다.

한마디로 **"작성(writing)에서 지휘(directing)로"** — 코딩의 무게중심 이동을, IDE 대신 **ADE**라는 이름으로 먼저 포착한 도구다 [국내 iamwonny87].

## 3. 어떻게 동작하나 — git worktree 병렬 격리

Orca를 이해하는 열쇠는 **git worktree** 하나다.

### worktree가 뭔가
보통 git 저장소는 작업 폴더가 하나다. 브랜치를 바꾸면 **같은 폴더**의 내용이 통째로 갈린다. 그래서 A 기능을 짜다 B 기능으로 넘어가려면 커밋하거나 스태시해야 하고, **두 작업을 물리적으로 동시에** 열어둘 수 없다.

**worktree**는 같은 저장소에 대해 **여러 개의 독립 작업 폴더**를 만드는 git 기본 기능이다. 각 worktree는 자기 브랜치·자기 파일 상태를 가지므로, **서로 간섭 없이 병렬 작업**이 된다 [국내 min-inter][1].

### Orca의 구조
Orca는 이 worktree를 **에이전트 병렬화의 단위**로 삼는다 [1][국내 joy014]:
- **작업(task) 하나 = worktree 하나 = 에이전트 하나.** 각 작업은 자기만의 **격리된 git worktree + 전용 터미널 + 브라우저 탭 + 컨텍스트**를 갖는다.
- 여러 작업을 만들면 **에이전트들이 동시에** 각자 폴더에서 일한다. 서로의 파일을 안 건드리니 충돌이 없다.
- **같은 문제를 여러 worktree에 병렬로** 던져놓고, 나온 결과(diff)를 **나란히 비교해 이긴 것을 머지**할 수도 있다 — 브랜치 저글링 없이.

즉 Orca가 파는 것은 "여러 에이전트를 동시에 돌리되 **서로 안전하게 격리**하고, 결과를 **한 화면에서 비교·병합**하는 경험"이다. worktree라는 오래된 git 기능을, 에이전트 시대의 **병렬 작업대**로 재발명한 셈이다.

## 4. 주요 기능 총정리

공식 저장소·문서 기준 핵심 기능을 표로 정리한다 [1][국내 bokgoon].

| 기능 | 무엇을 | 왜 유용한가 |
|---|---|---|
| **병렬 워크트리(Parallel Worktrees)** | 작업마다 격리 worktree·터미널·브라우저·컨텍스트 | 여러 에이전트 동시 작업, 충돌·오염 없음, 결과 비교·머지 |
| **모바일 컴패니언(iOS·Android)** | 에이전트 상태·사용량 실시간 모니터, 계정 hot-swap | 자리 비워도 폰으로 지휘, rate limit 관리 |
| **Orca CLI** | `orca worktree create`·`snapshot`·`click`·`fill` 등 | 에이전트가 **Orca 자체를 조작** — 워크플로우 스크립팅 |
| **Design Mode** | 브라우저 UI 요소를 클릭해 HTML/CSS를 프롬프트에 주입 | "이 버튼 고쳐" 같은 시각 지시를 에이전트에 정확히 전달 |
| **SSH 원격 워크트리** | 원격 서버(강력한 박스)에서 에이전트 실행 | 로컬 자원 아끼고 무거운 빌드·테스트를 원격에서 |
| **GitHub·Linear 통합** | 이슈/작업 브라우징, PR 리뷰 네이티브 지원 | 작업 지시→PR까지 도구 이동 없이 |
| **터미널 분할(WebGL)** | 무한 분할 터미널, GPU 렌더링 | 여러 에이전트 로그를 한눈에, 빠른 렌더 |

특히 **Orca CLI**는 방향이 흥미롭다. 사람이 Orca를 쓰는 것을 넘어, **에이전트가 `orca worktree create` 같은 명령으로 Orca를 직접 몰 수 있다**(agent-to-IDE control). "에이전트를 지휘하는 도구를, 에이전트가 다시 조작"하는 재귀 구조다 [1].

## 5. 지원 에이전트 — 40종 이상, 내 구독으로

Orca는 특정 모델에 묶이지 않는다. **40개 이상의 CLI 코딩 에이전트**를 붙일 수 있고, 공식적으로 **"어떤 CLI 에이전트든 작동"**한다고 명시한다 [1][국내 bihyun07]. 대표적으로:

| 계열 | 에이전트(예) |
|---|---|
| Anthropic | **Claude Code** |
| OpenAI | **Codex**, Copilot CLI |
| 기타 상용 | Cursor CLI, **Grok**, Devin, Antigravity |
| 오픈소스 | **OpenCode**, Pi, Goose, Cline |

핵심 원칙은 **BYO(Bring Your Own) 구독**이다. Orca는 에이전트를 **대신 호스팅하지 않는다**. 내가 이미 쓰는 **Claude Code Max, ChatGPT/Codex 구독, 각종 API 키를 그대로 연결**해 Orca 안에서 나란히 돌린다. 그래서 비용 구조가 투명하다(§8) [1][국내 ideasman]. Claude Code를 붙이는 방법은 공식 문서의 `docs/agents/claude-code` 항목에 정리돼 있다 [4].

## 6. 설치·시작하기

### 설치
**macOS(Homebrew)**:
```bash
brew install --cask stablyai/orca/orca
```
**Arch Linux(AUR)**:
```bash
yay -S stably-orca-bin
```
**직접 다운로드**: 공식 사이트 `onorca.dev` 또는 GitHub Releases에서 macOS·Windows·Linux 바이너리를 받는다 [1].

### 첫 실행 — 온보딩
git 기본 개념(브랜치·커밋)만 알면 사용 자체는 어렵지 않다. **worktree 개념은 몰라도 온보딩 과정에서 UI가 안내**하므로, 실제로 worktree를 만들고 에이전트를 붙이는 흐름을 따라가며 익히게 된다 [국내 bokgoon][국내 aisparkup]:
1. Orca를 열고 **작업할 git 저장소를 연결**한다.
2. **에이전트를 등록**한다(이미 로그인된 Claude Code·Codex 등의 구독/키를 연결).
3. **새 작업(task)을 만든다** → Orca가 자동으로 **격리 worktree**를 만들고 전용 터미널·브라우저를 붙인다.
4. 그 작업에 **에이전트를 배정**하고 과제를 준다. 필요하면 작업을 여러 개 만들어 **병렬로** 돌린다.
5. 각 작업의 **diff를 비교**하고, 원하는 결과를 **머지**한다. (원격이면 SSH worktree, 이동 중이면 모바일 앱으로 상태 확인.)

## 7. 실전 워크플로우 (Worked)

### Worked 1 — 같은 문제를 3개 에이전트에 경쟁 실행
"로그인 폼의 버그를 고쳐라"라는 과제를 하나 정하고 [1][국내 joy014]:
1. Orca에서 **작업 3개**를 만든다 → 각각 격리 worktree 생성.
2. 작업①에 **Claude Code**, 작업②에 **Codex**, 작업③에 **Grok**을 배정하고 **같은 프롬프트**를 준다.
3. 세 에이전트가 **동시에** 각자 worktree에서 수정한다(서로 안 건드림).
4. 완료되면 **세 diff를 나란히 비교** — 가장 깔끔한 수정을 고른다.
5. 이긴 결과를 **머지**, 나머지 worktree는 버린다.

한 명에게 순차로 시키고 마음에 안 들면 되돌리는 대신, **세 후보를 병렬로 뽑아 최선을 채택**한다. 품질·속도 둘 다 이득이다.

### Worked 2 — 여러 기능을 병렬 분업
큰 기능 하나가 아니라 **독립적 작업 여러 개**(예: 결제 모듈, 알림 배너, 리팩터링)를 각각 다른 worktree·에이전트에 맡긴다. 사람은 **모바일 앱으로 진행 상황과 각 계정의 rate limit을 보며**, 막히는 작업만 개입한다. 자리를 비워도 폰으로 "함대"를 지휘하는 그림이다 [3][국내 iamwonny87].

### Worked 3 — Design Mode로 시각 지시
프런트엔드 수정 시, **Design Mode**로 브라우저에서 문제의 UI 요소를 **클릭**하면 해당 HTML/CSS가 에이전트 프롬프트에 자동 주입된다. "이 카드 그림자 좀"처럼 말로 설명하기 애매한 지시를, **요소를 콕 집어** 정확히 전달한다 [1].

## 8. 요금·비용 구조

Orca의 비용 모델은 두 층으로 분리된다 [1][국내 ideasman][국내 bihyun07]:

| 층 | 대상 | 비용 |
|---|---|---|
| **Orca 본체** | ADE 소프트웨어(데스크톱·모바일·CLI) | **무료(MIT 오픈소스)** |
| **에이전트 사용료** | Claude Code·Codex 등 구독/API | **내 계정에 청구**(Orca 무관) |

즉 **Orca를 깐다고 추가 비용이 붙지 않는다.** 지출은 전적으로 **내가 붙인 에이전트의 구독·토큰** 몫이다. 오히려 Orca의 **실시간 rate limit 표시·계정 hot-swap**이 이 비용을 **관리**하는 데 도움을 준다 — 한 계정 한도가 차면 다른 계정으로 즉시 전환해 작업을 끊지 않는다 [3][국내 qjc].

주의: **여러 에이전트를 병렬로 돌리면 토큰 소모가 곱으로 늘어난다.** 3개를 동시에 굴리면 대략 3배가 나갈 수 있으니, "무료 도구"라는 말이 "무료 사용"은 아니라는 점을 분명히 해야 한다.

## 9. 유사 도구 비교

Orca는 "병렬 에이전트 터미널/오케스트레이터" 범주의 대표 주자지만 단독은 아니다. 2026년 이 범주에는 **cmux, Conductor** 등 여러 도구가 경쟁한다 [국내 skwu1].

| 구분 | Orca | 단일 Claude Code / Codex | 다른 병렬 도구(cmux·Conductor 등) |
|---|---|---|---|
| 성격 | ADE, 다중 에이전트 오케스트레이션 | 단일 CLI 에이전트 | 병렬 터미널·칸반형 |
| 병렬 격리 | git worktree 네이티브 | 수동(직접 worktree 관리) | 도구마다 상이 |
| 모바일 | iOS·Android 컴패니언 | 없음(터미널) | 대체로 없음 |
| 에이전트 폭 | 40+ CLI, 벤더 중립 | 자사 에이전트 | 도구마다 상이 |
| 라이선스 | MIT 오픈소스 | 각 벤더 | 상이 |

정리하면 **"에이전트 하나로 충분"하면 굳이 Orca가 필요 없다.** Orca의 값어치는 **여러 에이전트를 동시에·비교하며·이동 중에도** 지휘해야 할 때 나온다. 반대로 병렬이 필요 없는 단순 작업엔 오히려 관리 오버헤드가 될 수 있다 [국내 skwu1][국내 bihyun07].

## 10. 보안·한계·주의점

신생 오픈소스인 만큼 냉정하게 짚을 지점이 있다 [국내 bihyun07][국내 ideasman]:

- **권한 범위 확인.** 여러 에이전트가 파일·터미널·git·(SSH면) 원격 서버까지 조작한다. 각 에이전트에 주는 권한과 자동 실행 범위를 반드시 점검해야 한다. 자동화가 편한 만큼 사고 반경도 넓다.
- **리소스 소모.** 에이전트를 병렬로 여러 개 돌리면 **CPU·메모리·토큰**이 곱으로 든다. 로컬 사양·요금 한도를 보고 병렬 수를 정할 것. 무거운 작업은 SSH 원격 worktree로 분산.
- **유지가능성(신생 리스크).** 저장소 생성 2026-03, 빠르게 크지만 아직 어린 프로젝트다. 로드맵·업데이트 지속성을 지켜보며 도입하는 게 안전하다 [국내 bihyun07].
- **git 이해가 전제.** worktree·브랜치·머지 개념이 약하면 병렬 결과를 병합할 때 혼란이 온다. UI가 안내하지만, **git 기본기는 있어야** 제 값을 한다 [국내 bokgoon].
- **품질은 여전히 에이전트 몫.** Orca는 지휘 환경일 뿐, 코드 품질·환각은 붙인 에이전트가 좌우한다. 병렬로 뽑아도 **사람의 리뷰·테스트**는 필수다.

## 11. 베스트 프랙티스 & 체크리스트

- [ ] **병렬은 '독립 작업' 또는 '경쟁 실행'에.** 서로 얽힌 작업을 무턱대고 쪼개지 말 것 — 머지 지옥이 온다.
- [ ] **경쟁 실행(같은 문제 N개)** 은 품질이 중요한 핵심 변경에, **분업 실행(다른 작업 N개)** 은 처리량이 필요할 때.
- [ ] **rate limit은 모바일로 상시 확인**, 한도 차면 계정 hot-swap. 병렬 수 = 지갑·사양과 상의.
- [ ] **권한 최소화.** 자동 실행·파일 쓰기·원격 접근 범위를 작업별로 좁힌다.
- [ ] **머지 전 반드시 diff 비교·테스트.** 이긴 후보도 사람이 검수.
- [ ] **무거운 빌드/테스트는 SSH 원격 worktree**로 로컬 보호.
- [ ] **git 기본기부터.** worktree·브랜치·머지 흐름을 알고 들어가면 학습 곡선이 확 준다.
- [ ] **버전 고정·백업.** 신생 도구이니 중요한 저장소는 별도 백업·브랜치 보호 규칙과 함께.

## 12. 한눈 요약
- **Orca = ADE**(에이전트 개발 환경). IDE가 코드를 쓰는 곳이라면, ADE는 **에이전트 함대를 지휘**하는 곳.
- **git worktree 격리**로 여러 에이전트를 **충돌 없이 병렬** 실행·비교·머지.
- **40+ CLI 에이전트**(Claude Code·Codex·Grok·OpenCode…)를 **내 구독으로** 연결.
- **데스크톱 + 모바일**, 계정 hot-swap·실시간 rate limit — 2026 상반기 제한 강화의 통증을 정조준.
- **Orca 무료(MIT), 에이전트 비용은 내 계정.** 병렬은 토큰이 곱으로 든다.
- 신생인 만큼 **권한·리소스·유지가능성·git 이해**를 함께 챙길 것.

## 다음 읽을 것 / 시작하기
- 🌐 공식: [onorca.dev](https://www.onorca.dev/) · 저장소: [github.com/stablyai/orca](https://github.com/stablyai/orca) · 문서: onorca.dev/docs
- ⚙️ 설치: `brew install --cask stablyai/orca/orca` (macOS)
- 🔗 관련: [[클로드 코드]](붙일 대표 에이전트) · [[git worktree]](병렬의 토대) · [[클로드 MCP 가이드]](에이전트에 도구를 붙이는 표준)

## 출처

**국내**
1. (국내) 쏭로그(bihyun07), "Orca ADE란? AI 코딩 에이전트 40종 이상 연결하는 무료 도구", 네이버 블로그, 2026-07-13 — 40종·무료·별도 구독·주의점. https://blog.naver.com/bihyun07/224345644932
2. (국내) AI & Security Expert(ideasman), "[멀티 AI 에이전트 개발 환경] ORCA(오르카)", 네이버 블로그, 2026-07-14 — ADE 등장 배경·구독 비용 구조. https://blog.naver.com/ideasman/224346001190
3. (국내) JOYLAB.log(joy014), "Orca 분석: AI 코딩 에이전트를 병렬 운영하는 ADE", 네이버 블로그, 2026-07-15 — worktree·터미널·Diff·PR 흐름. https://blog.naver.com/joy014/224345445236
4. (국내) AI 꿈터(iamwonny87), "AI 하나 쓰던 시대는 끝 — 여러 에이전트를 나란히", 네이버 블로그, 2026-07-13 — '작성에서 지휘로'·ADE 명명. https://blog.naver.com/iamwonny87/224344893144
5. (국내) 개발 바닥(skwu1), "AI 에이전트 병렬 터미널 6종 비교, cmux·Orca·Conductor…", 네이버 블로그, 2026-07-15 — 유사도구 비교. https://blog.naver.com/skwu1/224347476297

**해외**
6. (해외) Stably AI, "Orca" GitHub 저장소(공식) — ADE 정의·40+ 에이전트·worktree·설치·기능·별 20.7k·v1.4.143. https://github.com/stablyai/orca
7. (해외) Orca, 공식 사이트 onorca.dev — "the most powerful ADE"·병렬·데스크톱/모바일. https://www.onorca.dev/
8. (해외) Orca Docs, "What is Orca?" / "Claude Code in Orca" — 개념·에이전트 연결. https://www.onorca.dev/docs
9. (해외) Andrew(andrew.ooo) / DEV, "Orca Review: The IDE Built for Parallel Coding Agents" — 리뷰·기능 검증. https://dev.to/andrew-ooo/orca-review-the-ide-built-for-parallel-coding-agents-15df
10. (해외) MOGE, "Orca: free, open-source ADE" 제품 페이지 — MIT·크로스플랫폼·모바일. https://moge.ai/product/orca
11. (해외) Quantum Jump Club, "Orca 완벽 정리: 병렬 AI 코딩 에이전트를 위한 무료 ADE" — rate limit·계정 hot-swap·성장세. https://qjc.app/en/blog/orca-parallel-agents
12. (해외) Daily AI World, "Orca: Run Parallel Coding Agents on Desktop and Mobile (2026)" — 병렬·모바일 개괄. https://dailyaiworld.com/blogs/orca-parallel-coding-agent-environment-2026
13. (해외) Wavise OpenLLM, "Orca ADE: Run Parallel AI Coding Agents with Your Own Subscription" — BYO 구독·기능. https://openllm.wavise.com/blog/orca-ade-parallel-agents

## 후속 질문·연결
- 붙일 대표 에이전트의 정체 → [[클로드 코드]]
- 병렬의 토대가 된 git 기능 → [[git worktree]]
- 에이전트에 도구를 붙이는 표준 → [[클로드 MCP 가이드]]
- 이 갤러리 파이프라인(단일 세션 오케스트레이션)과의 대비 → [[PIPELINE]]
