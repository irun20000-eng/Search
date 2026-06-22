---
주제: 클로드 MCP 완전 가이드 — 추천 서버부터 실전 워크플로우까지 (DEEP)
날짜: 2026-06-23
깊이: deep
카드모드: auto
대상수준: 실무 가이드(DEEP)
태그: [AI, MCP, ModelContextProtocol, ClaudeCode, ClaudeDesktop, 자동화, 생산성, 도구연동, 보안]
소스수: { 국내: 5, 해외: 9 }
위키링크: ["[[MCP(Model Context Protocol)]]", "[[Claude Code]]", "[[Claude Desktop]]", "[[AI 에이전트]]", "[[프롬프트 인젝션]]", "[[OAuth 2.1]]", "[[주제 리서치 파이프라인]]"]
갤러리URL: "#r=claude-mcp-guide"
---

# 클로드 MCP 완전 가이드 — 추천 서버부터 실전 워크플로우까지

> 작성·조회 기준일: **2026-06-23 (KST)**. 다운로드 수·스타 수·서버 개수 같은 유동 수치는 모두 이 시점 기준이며, 빠르게 변하므로 인용 시 날짜를 함께 확인할 것.

## TL;DR
- **MCP(Model Context Protocol)**는 Anthropic이 2024년 11월 공개한 **오픈 표준**으로, AI 모델과 외부 도구·데이터를 잇는 "AI용 USB-C 포트"다. 통합을 M×N에서 M+N으로 줄이는 게 핵심 가치다 [1][3][7].
- 2026년 현재 MCP는 사실상 업계 표준이 됐다. 공개 서버 **500종 이상**, 공식 SDK는 TypeScript·Python·C#·Java·Swift 등으로 제공된다 [1][3]. OpenAI·Google DeepMind를 포함한 주요 벤더가 채택했다 [3][7].
- 클로드에서 MCP를 쓰는 경로는 둘이다. **Claude Code**(터미널, `claude mcp add`)와 **Claude Desktop**(GUI, `claude_desktop_config.json` 또는 DXT/커넥터). 이 가이드는 **둘 다** 다룬다.
- 추천은 3층이다. **① 공식 reference 7종**(학습·기본기), **② 범용 베스트**(GitHub·Playwright·Context7·Notion·Slack 등), **③ 내 스택 맞춤**(이 리서치 갤러리를 실제로 굴리는 조합).
- 가장 중요한 건 **보안**이다. MCP는 프롬프트 인젝션·도구 중독(tool poisoning)·과도한 권한이라는 새 공격면을 연다. 최소권한·승인 게이트·신뢰 경계를 처음부터 설계해야 한다 [8][9][10].

## 핵심 포인트
1. **MCP = 표준 프로토콜**이지 특정 제품이 아니다. 한 번 만든 서버를 클로드·커서·여러 IDE가 공유한다 [1][7].
2. **구조는 host–client–server 3계층**, 통신은 **JSON-RPC 2.0**, 노출 단위는 **tools·resources·prompts** 세 가지다 [1][6].
3. **전송(transport)은 두 가지로 정리됐다**: 로컬은 **stdio**, 원격은 **Streamable HTTP**. 옛 HTTP+SSE 단독 방식은 2026년 들어 사실상 폐기 수순이고, 원격 인증은 **OAuth 2.1**이 기본이다 [6][11].
4. **추천 서버는 "필요에서 출발"한다.** 다 깔지 말고, 실제로 반복하는 작업(코드·문서·검색·배포)에 매핑되는 것만 단계적으로 붙인다 [5(국내)][12].
5. **권한은 줄수록 안전하다.** 읽기 전용으로 시작하고, 쓰기·삭제는 승인 게이트와 함께 점진적으로 연다 [8][10].

## 1. MCP란 무엇인가 — "AI용 USB-C"

LLM은 강력하지만 기본적으로 **고립**돼 있다. 내 파일, 내 깃 저장소, 사내 위키, 캘린더를 모른다. 예전에는 모델 하나를 도구 하나에 붙이려면 전용 연동 코드를 매번 짰다. 모델이 M개, 붙일 도구가 N개면 최악의 경우 **M×N개**의 커넥터가 필요했다. 이게 "통합 지옥"이다.

MCP는 이 문제를 **공통 규격**으로 푼다. 도구 쪽은 "MCP 서버"를 한 번만 만들고, 모델(호스트) 쪽은 "MCP 클라이언트"를 한 번만 구현하면, 둘은 같은 언어로 대화한다. 그래서 통합 비용이 **M+N**으로 떨어진다 [1][3][7]. 흔히 쓰는 비유가 **"AI 애플리케이션을 위한 USB-C 포트"** — 어떤 기기든 같은 단자로 꽂는다는 뜻이다 [3][7].

- **누가·언제**: Anthropic이 **2024년 11월** 오픈소스로 공개했다 [1][3].
- **왜 빨리 퍼졌나**: 표준이 개방형이라 특정 벤더에 묶이지 않는다. 2025~2026년 사이 OpenAI, Google DeepMind 등 경쟁사까지 자사 제품에 MCP를 채택하면서 사실상 **산업 표준**이 됐다 [3][7].
- **2026년 규모**: 공개 MCP 서버 **500개 이상**, 공식 SDK 다수(TypeScript·Python·C#·Java·Swift), 광범위한 호스트(클로드, 여러 IDE, 에이전트 프레임워크) 지원 [1][3].

핵심은 이거다. **MCP를 배우면 한 번 익힌 걸 클로드에서도, 커서에서도, 내가 만든 에이전트에서도 똑같이 쓴다.** 도구가 늘어도 학습 곡선이 다시 시작되지 않는다.

## 2. 아키텍처 — host / client / server

MCP는 세 역할로 나뉜다 [1][6].

```
┌─────────────────────────────────────────────────────────┐
│  HOST  (Claude Desktop / Claude Code / IDE / 내 에이전트) │
│   - 사용자와 대화하는 AI 애플리케이션                      │
│   - 내부에 여러 CLIENT를 둔다                              │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐          │
│   │ CLIENT 1  │   │ CLIENT 2  │   │ CLIENT 3  │          │
│   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘          │
└─────────┼───────────────┼───────────────┼────────────────┘
          │ JSON-RPC 2.0  │               │
   stdio  │        Streamable HTTP        │  (OAuth 2.1)
          ▼               ▼               ▼
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │ SERVER:    │  │ SERVER:    │  │ SERVER:    │
   │ Filesystem │  │ GitHub     │  │ Notion     │
   │ (로컬)     │  │ (원격 API) │  │ (원격 API) │
   └────────────┘  └────────────┘  └────────────┘
        tools / resources / prompts 노출
```

- **Host**: 사용자가 직접 쓰는 AI 앱. Claude Desktop, Claude Code, IDE 확장, 또는 내가 만든 에이전트. 호스트는 내부에 **여러 클라이언트**를 띄운다.
- **Client**: 호스트 안에서 **서버 하나당 하나씩** 1:1로 붙는 커넥터. 연결·세션·메시지 라우팅을 담당한다.
- **Server**: 실제 능력을 노출하는 쪽. 파일 읽기, 깃 조작, API 호출 등을 표준 형식으로 내보낸다.

**통신 규격은 JSON-RPC 2.0**이다. 모든 요청/응답이 정해진 JSON 형식을 따르므로, 서버를 어떤 언어로 짜든 호스트는 동일하게 이해한다 [1][6].

서버가 노출하는 단위는 셋이다 [1][6]:

| 프리미티브 | 누가 주도하나 | 무엇인가 | 예시 |
|---|---|---|---|
| **Tools** | 모델(AI) | 모델이 호출하는 "행동/함수" | `create_pull_request`, `search_web`, `read_file` |
| **Resources** | 앱/사용자 | 모델 맥락에 넣을 "읽기 데이터" | 파일 내용, DB 레코드, 위키 문서 |
| **Prompts** | 사용자 | 재사용 가능한 "프롬프트 템플릿" | "이 PR 리뷰해줘" 슬래시 명령 |

### 전송(Transport)과 인증

- **stdio**: 서버를 내 컴퓨터에서 **하위 프로세스**로 실행하고 표준입출력으로 통신. 로컬 도구(Filesystem, Git 등)에 적합. 빠르고 네트워크 노출이 없다 [6].
- **Streamable HTTP**: 원격 서버에 HTTP로 접속. 2026년 원격 연결의 **표준 전송**이다. 과거 별도의 HTTP+SSE 방식은 이걸로 통합·대체됐다 [6][11].
- **OAuth 2.1**: 원격 서버 인증의 기본. 토큰 기반으로 권한을 위임하므로 비밀번호를 직접 넘기지 않는다 [6][11].

## 3. 추천 MCP ① — 공식 reference 7종 (기본기·학습용)

`modelcontextprotocol/servers` 저장소가 유지하는 **공식 reference 서버**는 "프로덕션 제품"이 아니라 **MCP 기능을 보여주는 교육용 예제**다. 그래서 MCP를 처음 배울 때 먼저 깔아보기 딱 좋다 [1].

| 서버 | 무엇을 하나 | 언제 쓰나 |
|---|---|---|
| **Filesystem** | 설정 가능한 접근 제어 하의 안전한 파일 읽기/쓰기 | 로컬 폴더를 클로드에게 맥락으로 줄 때 |
| **Fetch** | 웹 콘텐츠를 가져와 LLM이 쓰기 좋게 변환 | URL 내용을 요약·분석할 때 |
| **Git** | 깃 저장소 읽기·검색·조작 | 로컬 리포 히스토리/diff를 다룰 때 |
| **Memory** | 지식 그래프 기반 영속 메모리 | 세션을 넘어 사실을 기억시키고 싶을 때 |
| **Sequential Thinking** | 단계적·반성적 사고 시퀀스 | 복잡한 문제를 쪼개 추론시킬 때 |
| **Time** | 시간·시간대 변환 | "지금 KST 몇 시?" 같은 시간 연산 |
| **Everything** | prompts·resources·tools를 전부 시연하는 테스트 서버 | 클라이언트 구현/디버깅 레퍼런스 |

> 주의: 초기엔 reference 목록이 더 길었지만, 2026년 들어 다수는 각 벤더가 자체 유지하는 공식 서버로 이관됐고, **이 7종이 steering group이 직접 유지하는 핵심**이다 [1]. "공식이라 production-ready"라는 건 오해 — 어디까지나 데모·학습 목적이다 [1].

## 4. 추천 MCP ② — 범용 베스트 (실무에서 가장 자주 쓰는 것)

다 깔 필요 없다. **반복하는 작업에 매핑되는 것만** 고른다. 카테고리별로 2026년 실무에서 자주 채택되는 서버들이다 [4][5(국내)][12].

| 카테고리 | 서버(예) | 핵심 용도 |
|---|---|---|
| 코드 호스팅 | **GitHub** | PR·이슈·코드 검색·리뷰·머지를 대화로 |
| 브라우저 자동화 | **Playwright** | 실제 브라우저로 웹 조작·E2E 테스트·스크래핑 |
| 최신 문서 주입 | **Context7** | 라이브러리 최신 문서를 모델 맥락에 실시간 공급 |
| 문서/지식관리 | **Notion** | 페이지·DB 읽기/쓰기, 회의록·위키 연동 |
| 팀 커뮤니케이션 | **Slack** | 채널 읽기·메시지 전송·검색 |
| 로컬 제어 | **Desktop Commander** | 로컬 파일/터미널 제어 ("이것만 깔아도 반은 먹고 들어간다"고 평가받음) [5(국내)] |
| 웹 검색 | **Brave Search / Tavily 등** | 실시간 웹 검색 결과 주입 |
| 코드 시맨틱 분석 | **Serena** | 심볼 단위 코드 탐색으로 개발 워크플로우 강화 [국내 사례] |

국내 실무 가이드들도 비슷한 결론을 낸다. 한 가이드는 "**클로드 앱에 MCP 서버 5개만 깔면 완전히 다른 도구가 된다**"며 Desktop Commander를 1순위로 꼽았고 [5(국내)], 다른 글은 "MCP는 **실시간 연결이 필요할 때** 쓰는 것"이라며 목적부터 정하라고 조언한다 [국내]. 즉 **"멋져 보여서"가 아니라 "내가 매주 하는 일"** 기준으로 고르라는 것.

## 5. 추천 MCP ③ — 내 스택 맞춤 (이 갤러리를 실제로 굴리는 조합)

이 가이드가 올라가는 **'Search' 주제 리서치 갤러리**가 곧 살아있는 MCP 활용 사례다. 이 세션에 실제로 연결된 MCP들과 그 용도를 매핑하면 다음과 같다.

| 연결된 MCP | 역할(이 파이프라인에서) |
|---|---|
| **PlayMCP / 네이버 검색** | 국내 1차 자료 수집(블로그·뉴스·백과·지식인), `get_current_korean_time`으로 조회일 확정 |
| **WebSearch (내장)** | 해외 자료·최신 사실 교차검증 |
| **GitHub** | 리포트 커밋 푸시 → PR 생성 → main 머지(갤러리 자동 반영) |
| **Google Drive** | 완성 리포트를 옵시디언 볼트(`YYYYMMDD_제목.md`)로 저장 |
| **Notion** | 지식 DB·회의록 연동(선택) |
| **Slack** | 작업 알림·결과 공유(선택) |
| **Figma / Gamma** | 학습 카드·시안·프레젠테이션 생성(선택) |
| **Vercel** | 배포·런타임 로그 확인(선택) |
| **Google Calendar / Gmail** | 일정·메일 자동화(선택) |

핵심 통찰: **MCP의 진짜 가치는 "단일 도구"가 아니라 "오케스트레이션"에서 나온다.** 네이버로 모으고, WebSearch로 교차검증하고, GitHub로 배포하고, Drive로 아카이브하는 **한 줄기 흐름**을 클로드가 직접 지휘한다.

## 6. 실전 워크플로우 (Worked) — 리서치→갤러리→옵시디언

이 갤러리의 리포트 한 편이 만들어지는 과정을 MCP 관점에서 풀면 이렇다. 이게 **여러 MCP를 엮은 실전 오케스트레이션**의 구체 사례다.

```
[1] 수집      네이버 MCP(search_blog/news/encyc) + WebSearch
                 └→ 국내·해외 출처 균형, get_current_korean_time으로 조회일 고정
[2] 작성      report.md 단일 정본 작성 (무환각·인용 1:1, DEEP 게이트 측정)
[3] 검증      wc -m / wc -l / grep -cE '^## ' 로 분량·구조 객관 카운트
[4] 배포      GitHub MCP: 브랜치 커밋 → push → create_pull_request → merge
                 └→ GitHub Pages 갤러리가 manifest.json 읽어 자동 최신화
[5] 아카이브  Google Drive MCP: create_file 로 옵시디언 볼트에 'YYYYMMDD_제목.md' 저장
[6] 확인      라이브 URL + Drive viewUrl 로 결과 검증
```

여기서 배울 점:
- **MCP는 "AI가 직접 손을 쓰게" 한다.** 사람이 깃을 치고 파일을 옮기는 대신, 클로드가 GitHub MCP로 PR을 만들고 Drive MCP로 노트를 저장한다.
- **단일 정본 + 다중 출력**: `report.md` 하나를 작성하면 갤러리(웹)와 옵시디언(노트)으로 동시에 퍼진다. MCP가 그 분배를 담당한다.
- **검증도 도구로**: 분량 게이트를 사람 눈대중이 아니라 `wc`/`grep`으로 측정한다(MCP가 아닌 셸이지만, 같은 "도구로 자동화" 철학).

## 7. 설치·설정 (a) — Claude Code (터미널)

Claude Code에서는 명령 한 줄로 서버를 붙인다. 시간에 민감한 명령이므로 **공식 문서(code.claude.com/docs) 기준**으로 확인하고 쓸 것 [2(국내 설치기 교차)][12].

**원격(HTTP) 서버 추가:**
```bash
claude mcp add --transport http <이름> <URL>
# 예: claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

**로컬(stdio) 서버 추가** — 국내 설치기에서 실제로 쓰인 형태 [국내 Serena 사례]:
```bash
claude mcp add -s user --transport stdio serena \
  uvx --from git+https://github.com/oraios/serena serena-mcp-server
```

**관리 명령:**
```bash
claude mcp list          # 연결된 서버·상태 확인
claude mcp auth <서버>    # OAuth 인증(원격 서버)
/mcp                     # 대화 중 슬래시 명령으로 서버/도구 상태 보기
```

**스코프(scope)** — 설정이 어디까지 적용되나:

| 스코프 | 저장 위치 | 적용 범위 |
|---|---|---|
| `local` | 프로젝트 로컬(개인) | 나만, 이 프로젝트 |
| `project` | `.mcp.json`(리포에 커밋) | 팀 전체가 공유 |
| `user` | 사용자 전역 | 내 모든 프로젝트 |

팀과 공유하려면 `.mcp.json`을 리포에 커밋하는 `project` 스코프가 편하다. 단, **비밀키를 그 파일에 넣지 말 것**(환경변수 참조로).

## 8. 설치·설정 (b) — Claude Desktop (GUI)

Claude Desktop은 설정 파일 또는 GUI 커넥터로 붙인다 [5(국내)][6].

**설정 파일 직접 편집** — `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/work"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }
    }
  }
}
```
저장 후 앱을 재시작하면 입력창 근처 아이콘에서 **연결된 서버와 사용 가능한 도구 목록**을 확인할 수 있다 [5(국내)].

**더 쉬운 길 — DXT 확장 / 커넥터**: JSON을 직접 만지기 부담스러우면, 원클릭 설치형 **DXT 확장**이나 GUI **커넥터**로 붙일 수 있다. 비개발자·데스크톱 중심 사용자에게 권장된다 [6][국내].

> Code vs Desktop, 어느 쪽? **개발·자동화·CI 연동**이면 Claude Code(스코프·`.mcp.json`·CLI가 강점), **문서 작업·일상 도구 연결**이면 Claude Desktop(GUI·DXT가 강점). 둘은 배타적이지 않고, 같은 MCP 서버를 양쪽에서 쓸 수 있다.

## 9. 보안·권한·비용 — 가장 중요한 절

MCP는 편의만큼 **새 공격면**을 연다. 2026년 보안 연구들이 반복해 경고하는 지점이다 [8][9][10].

- **프롬프트 인젝션(간접)**: 모델이 읽는 외부 데이터(웹페이지·이슈 본문·문서)에 "이 토큰을 유출해라" 같은 악성 지시가 숨어 있을 수 있다. 모델이 그걸 명령으로 오인하면 도구를 악용한다 [8][9].
- **도구 중독(tool poisoning)**: 서버가 노출하는 **도구 설명(metadata)** 자체에 악성 지시를 심는 수법. 사용자에겐 평범해 보이지만 모델에겐 숨은 명령이 된다 [9][10].
- **러그풀(rug pull)**: 처음엔 정상이던 서버가 나중에 도구 정의를 바꿔 악성으로 돌변 [9].
- **과도한 권한**: 한 번 토큰을 받으면 필요 이상으로 넓게 접근. 유출 시 피해가 커진다 [8][10].
- **벤치마크 경고**: 도구 호출 에이전트를 겨냥한 공격 연구에서 일부 모델은 매우 높은 공격 성공률을 보였다(예: MCPTox류 평가에서 일부 소형 모델이 70%대) — 즉 **모델 자체가 방어선이 되긴 어렵다** [9].

**방어 원칙(처음부터 설계):**
1. **최소권한**: 읽기 전용으로 시작, 쓰기·삭제는 꼭 필요한 서버에만.
2. **승인 게이트(human-in-the-loop)**: 외부로 나가거나 되돌리기 어려운 행동(머지·전송·삭제)은 사람 확인.
3. **신뢰 경계**: 출처가 불확실한 서버는 깔지 않는다. 공식/검증된 배포처를 쓰고, 도구 설명도 의심한다.
4. **점진적 권한 동의**: 2026년 스펙 흐름은 한 번에 다 주지 않고 **필요할 때 증분 동의**하는 방향이다 [10][11].
5. **모니터링**: 어떤 도구가 무엇을 호출했는지 로깅·감사.
6. **서버 측 강제**: 클라이언트만 믿지 말고 서버에서도 권한을 강제.

**비용**: MCP 자체는 무료 오픈 표준이다. 비용은 **(a) 토큰** — 도구 설명·결과가 모두 컨텍스트를 먹으므로 서버를 많이 붙일수록 입력 토큰이 늘고, (b) **원격 서버의 자체 요금**(유료 API를 감싼 서버)에서 발생한다. 그래서도 **꼭 쓰는 것만** 붙이는 게 비용 면에서도 유리하다.

## 10. 베스트 프랙티스 & 흔한 함정 (체크리스트)

**DO**
- [ ] **필요에서 출발**: 매주 반복하는 작업을 먼저 적고, 거기 매핑되는 서버만 깐다.
- [ ] **읽기 전용으로 시작**, 검증되면 쓰기 권한을 연다.
- [ ] **공식/검증 배포처** 사용, 출처 불명 서버 회피.
- [ ] **비밀키는 환경변수/시크릿 매니저**로, 설정 파일·리포에 평문 금지.
- [ ] **팀 공유는 `.mcp.json`(project 스코프)**, 개인 실험은 local.
- [ ] **되돌리기 어려운 행동엔 승인 게이트**를 둔다.
- [ ] 유동 수치(버전·명령)는 **공식 문서로 재확인**하고 날짜를 적는다.

**DON'T**
- [ ] 멋져 보인다고 서버를 무더기로 깔지 말 것(토큰·공격면·혼란 증가).
- [ ] reference 서버를 "production-ready"로 착각하지 말 것(데모·학습용) [1].
- [ ] 외부에서 읽어온 텍스트의 지시를 무비판적으로 실행하지 말 것(프롬프트 인젝션) [8][9].
- [ ] 도구 설명(metadata)을 무조건 신뢰하지 말 것(도구 중독) [9][10].
- [ ] 모델이 알아서 막아줄 거라 믿지 말 것 — **권한 설계가 진짜 방어선** [9].

## 한눈 요약
- MCP = **AI용 USB-C**, 통합을 M×N→M+N으로. 2024-11 공개, 2026 사실상 표준(서버 500+) [1][3][7].
- 구조: **host–client–server**, **JSON-RPC 2.0**, **tools·resources·prompts**, 전송은 **stdio/Streamable HTTP**, 인증 **OAuth 2.1** [1][6][11].
- 추천 3층: **공식 7종(학습) → 범용 베스트(GitHub·Playwright·Context7·Notion·Slack·Desktop Commander) → 내 스택 맞춤(이 갤러리 파이프라인)**.
- 설치: **Claude Code**(`claude mcp add`, 스코프/`.mcp.json`) + **Claude Desktop**(`claude_desktop_config.json`/DXT).
- 보안이 핵심: **최소권한·승인 게이트·신뢰 경계·점진 동의·모니터링** [8][9][10][11].

## 출처

**국내**
1. (국내) 아키젠트, "클로드 MCP 서버 실전 가이드 — 설치부터 워크플로우까지", 네이버 블로그, 2026-03-22 — 데스크톱 MCP 설치·도구 목록 확인 UI 설명. https://blog.naver.com/onjeon_life/224216709059
2. (국내) 비비의 AI 실험실, "클로드 앱에 MCP 서버 5개만 깔면 완전히 다른 도구가 돼요", 네이버 블로그, 2026-03-23 — Desktop Commander 1순위 추천. https://blog.naver.com/vivihealth/224226087415
3. (국내) NADOO_AI, "클로드 코드 초보자가 바로 설치하면 좋은 도구와 MCP 정리", 네이버 블로그, 2026-05-25 — "MCP는 실시간 연결이 필요할 때" 목적 우선론. https://blog.naver.com/nadoo-ai/224295935063
4. (국내) 길벗출판사, "클로드 코드 세레나(Serena) MCP 개요와 설치", 네이버 블로그, 2025-09-10 — `claude mcp add -s user --transport stdio` 실제 명령 사례. https://blog.naver.com/gilbutzigy/224002693009
5. (국내) 영어뉴스와 미드영어, "클로드 MCP 커넥터 뜻·활용법", 네이버 블로그, 2026-06-21 — 노션·옵시디언·구글드라이브·깃허브·버셀 등 연동 범위 개관. https://blog.naver.com/babydreamer5/224322531482

**해외**
6. (해외) modelcontextprotocol/servers, GitHub 공식 저장소 — reference 7종(Everything·Fetch·Filesystem·Git·Memory·Sequential Thinking·Time), "데모/학습용" 명시, 공개 서버 500+. https://github.com/modelcontextprotocol/servers
7. (해외) Model Context Protocol Blog, "The 2026 MCP Roadmap" — 2026 로드맵·전송·인증 방향. https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
8. (해외) Model Context Protocol Blog, "The 2026-07-28 Specification Release Candidate" — 스펙 갱신(권한·전송) 흐름. https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
9. (해외) "What Is MCP? Model Context Protocol Explained for 2026", decodethefuture.org — USB-C 비유·아키텍처·벤더 채택. https://decodethefuture.org/en/what-is-mcp-model-context-protocol/
10. (해외) "Model Context Protocol (MCP): The Complete 2026 Guide", SurePrompts — host/client/server·프리미티브·전송 정리. https://sureprompts.com/blog/model-context-protocol-mcp-complete-guide-2026
11. (해외) "The Complete Guide to Model Context Protocol (MCP) in 2026: Building the USB-C for AI", Essa Mamdani — M×N→M+N 통합·실무 적용. https://www.essamamdani.com/blog/complete-guide-model-context-protocol-mcp-2026
12. (해외) "MCP Cheat Sheet (2026)", Webfuse — 명령·전송·구성 퀵레퍼런스. https://www.webfuse.com/mcp-cheat-sheet
13. (해외) Model Context Protocol — Wikipedia — 2024-11 공개, JSON-RPC 2.0, 경쟁사 채택, OAuth 2.1·Streamable HTTP. https://en.wikipedia.org/wiki/Model_Context_Protocol
14. (해외) "What Is MCP (Model Context Protocol)? Complete Guide for 2026", HauerPower — 프롬프트 인젝션·도구 중독·최소권한 등 보안 베스트프랙티스. https://www.hauerpower.com/en/insights-posts/what-is-mcp-model-context-protocol

## 후속 질문·연결
- MCP 서버를 **직접 만들기**(Python/TypeScript SDK)로 한 편 더 깊게 갈까? → [[MCP 서버 개발]]
- **보안 단독 심화**: 프롬프트 인젝션·도구 중독 방어 실전 → [[프롬프트 인젝션]]
- 이 갤러리 파이프라인의 자동화 설계 → [[주제 리서치 파이프라인]]
- 관련: [[Claude Code]] · [[Claude Desktop]] · [[AI 에이전트]] · [[OAuth 2.1]]
