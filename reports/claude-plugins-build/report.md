---
주제: 나만의 클로드 플러그인·마켓플레이스 만들기 (시리즈 ②)
날짜: 2026-06-23
깊이: deep
카드모드: auto
대상수준: 실무 가이드(DEEP)
시리즈: "클로드 플러그인 마스터"
시리즈순서: 2/4
태그: [AI, 시리즈, 클로드플러그인, ClaudeCode, 마켓플레이스, 플러그인제작, 배포, 자동화]
소스수: { 국내: 5, 해외: 9 }
위키링크: ["[[클로드 플러그인 만들기]]", "[[클로드 플러그인]]", "[[Claude Code]]", "[[MCP(Model Context Protocol)]]", "[[클로드 확장 생태계]]", "[[클로드 플러그인 워크플로우]]"]
갤러리URL: "#r=claude-plugins-build"
---

# 나만의 클로드 플러그인·마켓플레이스 만들기

> 「클로드 플러그인 마스터」 시리즈 **②편(제작·배포)**. 작성·조회 기준일 **2026-06-23 (KST)**. 디렉터리·필드명 같은 사양은 빠르게 바뀌므로 **공식 문서(code.claude.com/docs/en/plugins, /plugin-marketplaces)** 로 최종 확인할 것. ①편 [[클로드 플러그인]] 을 먼저 읽으면 좋다.

## TL;DR
- 플러그인은 **특별한 디렉터리 구조 + 매니페스트(`plugin.json`)를 가진 깃 저장소**일 뿐이다. 어렵지 않다 [6][7].
- 구조의 핵심 규칙: **`.claude-plugin/` 안에는 `plugin.json` 만**, `commands/`·`agents/`·`skills/`·`hooks/`·`.mcp.json` 은 **플러그인 루트**에 둔다 [7][8].
- `plugin.json`에서 **유일한 필수 필드는 `name`**이며, 이 이름이 **네임스페이스**가 되어 모든 스킬·에이전트·명령 앞에 접두사로 붙는다 [7].
- 로컬 테스트는 **`--plugin-dir`** 로 띄우고, 수정은 **`/reload-plugins`** 로 재시작 없이 반영한다(플러그인·스킬·에이전트·훅·MCP·LSP를 다시 로드) [7].
- 배포는 **3단계**다: ①로컬(`--plugin-dir`) → ②git에 push해 `/plugin marketplace add`로 설치 → ③공식 마켓플레이스에 **URL 제출**(누구나 열려 있음, 검토 후 등재) [6][7]. "코드 모양은 그대로, **설치 출처만 바뀐다**" [국내 배포 3단계].

## 핵심 포인트
1. **플러그인 = 깃 저장소.** GitHub/GitLab 등에 올리면 곧 배포 채널이 된다 [6][7].
2. **두 개의 JSON이 전부의 뼈대**: 플러그인은 `plugin.json`, 마켓플레이스는 `marketplace.json` [7].
3. **`name`이 네임스페이스**: `my-plugin`이면 `/my-plugin:command`처럼 접두사가 붙어 충돌을 막는다 [7].
4. **마켓플레이스 = 카탈로그 저장소**: `marketplace.json`의 `plugins` 배열이 어떤 플러그인을 어디서 받을지 가리킨다 [7].
5. **조직 배포는 화이트리스트가 핵심**: 사내 보안팀이 검증된 플러그인만 등록하는 **중앙 마켓플레이스** 패턴이 권장된다 [국내 가상부서].

## 1. 만들기 전 — 무엇을, 언제 플러그인으로 묶나

플러그인을 만드는 동기는 단순하다. **반복 + 공유**다. 같은 슬래시 명령·서브에이전트·훅·MCP 조합을 매번 손으로 세팅하거나, 팀원에게 "이렇게 설정해"라고 설명하는 게 번거로울 때 플러그인으로 묶는다 [6].

판단 기준:
- **한 번 쓰고 말 것** → 그냥 슬래시 명령/스킬 하나로 충분(묶을 필요 없음).
- **여러 구성요소가 함께 움직임**(명령+에이전트+훅) → 플러그인으로 묶어 **한 번에 설치·활성화**.
- **팀·조직이 동일 환경을 재현해야 함** → 플러그인 + (사내) 마켓플레이스.

국내 워크숍 후기의 비유가 깔끔하다. **"스킬은 작업 레시피, 플러그인은 스킬(구성요소) 묶음, 마켓플레이스는 저장소"** [국내 워크숍]. 이 위계를 머리에 넣고 시작하자.

또 하나 자주 빠지는 함정은 **"처음부터 완벽한 대형 플러그인"을 만들려는 것**이다. 권장 순서는 반대다. 먼저 슬래시 명령 하나를 `.claude/commands/`에 두고 손에 익힌 뒤, 반복되는 짝(명령+에이전트, 또는 명령+훅)이 보일 때 비로소 플러그인으로 승격한다. 국내 스킬 제작 글이 "직접 복사(개인용)"와 "`/plugin` 설치(공유용)" 두 경로를 함께 안내하는 이유도 같다 — **개인 실험은 가볍게, 공유 시점에 포장한다** [국내 스킬 3단계]. 즉 플러그인화는 *목표*가 아니라 *공유가 필요해진 순간의 결과*다.

## 2. 디렉터리 구조 — 어디에 무엇을 두나

가장 많이 틀리는 지점이 **무엇을 `.claude-plugin/` 안에 넣느냐**다. 규칙은 명확하다: **`.claude-plugin/` 폴더에는 `plugin.json`만**, 나머지 기능 폴더는 **플러그인 루트**에 둔다 [7][8].

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # ★ 매니페스트 — 여기엔 이것만
├── commands/                # 슬래시 명령(.md)
│   └── hello.md
├── agents/                  # 서브에이전트(.md)
│   └── reviewer.md
├── skills/                  # 스킬(작업 레시피)
│   └── my-skill/SKILL.md
├── hooks/                   # 훅 스크립트/설정
│   └── hooks.json
├── .mcp.json                # MCP 서버 정의(선택)
└── README.md
```

> 흔한 실수: `commands/`나 `agents/`를 `.claude-plugin/` 안에 넣는 것. **루트에 둬야 인식된다** [7][8].

## 3. plugin.json 매니페스트 — 이름이 곧 네임스페이스

`plugin.json`은 플러그인의 신분증이다. **필수는 `name` 하나**, 나머지는 권장이다 [7].

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "내 워크플로우를 묶은 플러그인",
  "author": { "name": "홍길동", "email": "me@example.com" },
  "keywords": ["productivity", "review", "automation"]
}
```

- **`name`**: 유일한 필수 필드. **네임스페이스로 작동**하여 이 플러그인의 모든 스킬·에이전트·명령이 `name:` 접두사를 갖는다(예: `/my-plugin:hello`). 충돌 방지의 핵심 [7].
- **`version`·`description`·`author`·`keywords`**: 마켓플레이스 노출·검색·신뢰에 쓰인다. 채워두는 게 좋다.

## 4. 구성요소 만들기 ① 슬래시 명령

`commands/` 안의 마크다운 한 장이 곧 슬래시 명령이 된다. 파일명이 명령 이름이 된다(`commands/hello.md` → `/my-plugin:hello`).

```markdown
---
description: 인사하고 오늘 할 일을 정리한다
---
오늘 날짜를 확인하고, 사용자의 할 일 목록을 3개로 요약해 제시해줘.
```

활용예시: 자주 쓰는 "커밋 메시지 생성", "PR 설명 작성", "릴리스 노트 초안" 같은 프롬프트를 명령으로 박제한다.

## 5. 구성요소 만들기 ② 서브에이전트

`agents/`의 마크다운으로 **특정 역할에 특화된 보조 에이전트**를 정의한다. 국내에도 "서브에이전트 배포하기 — `/plugin install`부터 마켓플레이스까지" 같은 실전 정리가 있다 [국내 배포 3단계].

```markdown
---
name: reviewer
description: 변경분을 컨벤션·버그 관점으로 리뷰하는 전용 에이전트
---
너는 코드 리뷰어다. CLAUDE.md 규약 위반, 잠재 버그, 누락된 테스트를
항목별로 지적하고 수정안을 제시한다.
```

활용예시: "버그 탐지 전용", "보안 점검 전용", "문서화 전용"처럼 관심사를 나눠 두면 메인 흐름이 깔끔해진다.

## 6. 구성요소 만들기 ③ 훅(hook)

훅은 **특정 시점에 자동 실행**되는 동작이다. `hooks/`에 설정/스크립트를 둔다.

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "command": "npm run lint --silent" }
    ]
  }
}
```

활용예시: 파일을 수정할 때마다 린트, 커밋 전 테스트, 응답 종료 후 Slack 알림 등 **"사람이 잊는 절차"를 강제**한다. (정확한 이벤트명·스키마는 공식 문서로 확인 [6].)

## 7. 구성요소 만들기 ④ MCP 서버(.mcp.json)

플러그인에 외부 연결을 끼우려면 루트에 `.mcp.json`을 둔다. ①편(MCP)에서 본 서버 정의를 그대로 번들한다 [14(①)].

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

활용예시: "이 플러그인을 깔면 Context7(최신 문서)·GitHub 연결이 함께 켜진다"처럼 **연결까지 한 묶음**으로 배포한다.

## 8. 로컬 테스트 — `--plugin-dir` 와 `/reload-plugins`

배포 전에 내 머신에서 돌려본다. 만들면서 가장 자주 쓰는 두 가지다 [7]:

```bash
# 로컬 디렉터리를 플러그인으로 띄워 테스트
claude --plugin-dir ./my-plugin

# 수정 후 재시작 없이 반영 (플러그인·스킬·에이전트·훅·MCP·LSP 재로드)
/reload-plugins
```

- `--plugin-dir`: git에 올리기 전 **로컬 경로**로 바로 검증.
- `/reload-plugins`: 명령·에이전트·훅을 고칠 때마다 **즉시 반영**되어 반복이 빠르다 [7].

국내 스킬 제작 글도 "`.claude/skills/`에 직접 복사하거나 `/plugin`으로 마켓플레이스에서 설치"하는 두 경로를 안내한다 [국내 스킬 3단계].

## 9. 마켓플레이스 만들기 — marketplace.json

남에게 나눠주려면 **마켓플레이스(카탈로그 저장소)** 를 만든다. 저장소 루트의 `.claude-plugin/marketplace.json`이 등록부다 [7].

```json
{
  "name": "my-marketplace",
  "owner": { "name": "홍길동", "email": "me@example.com" },
  "description": "내가 만든 플러그인 모음",
  "plugins": [
    { "name": "my-plugin", "source": "./my-plugin" },
    { "name": "team-review", "source": "github:myorg/team-review" }
  ]
}
```

- `plugins` 배열의 각 항목은 **최소 `name` + `source`**가 필요하다. `source`는 같은 repo 내 경로일 수도, **다른 저장소**(`github:owner/repo`)일 수도 있다 [7].
- 즉 **여러 저장소의 플러그인을 한 마켓플레이스로 묶어** 배포할 수 있다.

## 10. 배포 3단계 — 출처만 바뀐다

국내 정리가 명쾌하다: **"각 단계에서 코드의 모양은 바뀌지 않고 설치 출처만 바뀐다"** [국내 배포 3단계]. 단계는 이렇다 [6][7]:

```
[1] 로컬       claude --plugin-dir ./my-plugin        (내 머신에서 검증)
                 │  git init / commit / push
                 ▼
[2] git 배포   /plugin marketplace add owner/repo      (내 repo를 마켓으로)
               /plugin install my-plugin@my-marketplace (남도 설치 가능)
                 │  공식 디렉터리에 URL 제출
                 ▼
[3] 공식 등재  검토 후 claude-plugins-official 등 디렉터리에 노출
               (누구나 제출 가능, GitHub 기반)
```

- 가장 빠른 인덱싱 경로는 **플러그인 repo를 GitHub에 push하고 URL을 제출**하는 것 [6].
- 공식 마켓플레이스는 **누구나 열려 있고**, 제출→검토→등재 절차를 거친다 [6].

## 11. 사내·조직 배포 — 화이트리스트가 핵심

기업 환경에서는 "아무 플러그인이나 설치"가 곧 보안 사고다(①편의 임의 코드 실행 경고). 권장 패턴은 **중앙 통제형 마켓플레이스**다 [국내 가상부서][7]:

```
[전사 중앙 보안 마켓플레이스]   ← 보안팀이 검증·등록만
        │  화이트리스트 필터링
        ▼
[개별 임직원 로컬 클로드 런타임]  ← 사내 마켓에서만 설치
```

- 사내 보안팀이 **검증된 플러그인만 등록**하고, 임직원은 그 사내 마켓에서만 받는다 [국내 가상부서].
- 클로드 코드의 **관리 설정(managed settings)으로 허용 마켓플레이스를 제한**해 강제한다(①편 [7]).
- 이렇게 하면 "가상 부서"처럼 여러 서브에이전트·스킬을 표준 배포하면서도 공급망 위험을 통제한다 [국내 가상부서].

조직 배포에서 실무적으로 챙길 세 가지를 덧붙인다. 첫째, **버전 고정**이다. 마켓플레이스 항목이 외부 repo를 `source`로 가리킬 때 그 repo가 바뀌면 사내 환경도 따라 바뀐다 — 태그·커밋 핀으로 의도치 않은 변경을 막는다. 둘째, **비밀 분리**다. `.mcp.json`에 토큰을 평문으로 넣지 말고 환경변수 참조로 두어, 플러그인 repo가 곧 비밀 유출 경로가 되지 않게 한다(①편 보안 원칙과 동일). 셋째, **검토 기록**이다. 사내 마켓에 등록할 때 누가·언제·어떤 구성요소(특히 훅·MCP)를 검증했는지 남기면, 사고 시 추적과 롤백이 빨라진다. 결국 조직용 플러그인은 "기능"보다 **"신뢰의 파이프라인"** 을 설계하는 일에 가깝다 [국내 가상부서][7].

## 12. 처음부터 끝까지 — "5분 플러그인" 워크스루 (Worked)

말로만 보면 추상적이니, **커밋 메시지 자동화 + 리뷰 에이전트**를 묶은 작은 플러그인 `myflow`를 처음부터 만들어 배포까지 가보자. 실제 절차를 그대로 따른다 [6][7].

**1) 뼈대 만들기**
```bash
mkdir -p myflow/.claude-plugin myflow/commands myflow/agents
cd myflow
```

**2) 매니페스트 작성** — `myflow/.claude-plugin/plugin.json`
```json
{
  "name": "myflow",
  "version": "0.1.0",
  "description": "커밋 메시지 생성 + 리뷰 에이전트 묶음",
  "author": { "name": "나", "email": "me@example.com" },
  "keywords": ["git", "review", "productivity"]
}
```
이 순간부터 모든 구성요소는 `myflow:` 접두사를 갖는다(네임스페이스) [7].

**3) 슬래시 명령 추가** — `myflow/commands/commit.md`
```markdown
---
description: 변경분을 분석해 컨벤셔널 커밋 메시지를 만든다
---
스테이징된 변경을 분석하고, type(scope): summary 형식의
한국어 커밋 메시지 후보 3개를 제시해줘.
```
→ 설치 후 `/myflow:commit`으로 호출된다.

**4) 서브에이전트 추가** — `myflow/agents/reviewer.md`
```markdown
---
name: reviewer
description: 커밋 전 변경분을 빠르게 점검하는 리뷰어
---
변경 파일을 훑어 버그 가능성·누락 테스트·컨벤션 위반을 항목화하고
수정안을 붙여라. 확실치 않으면 추측하지 말고 질문해라.
```

**5) 로컬 테스트**
```bash
claude --plugin-dir ./myflow      # 이 디렉터리를 플러그인으로 로드
# 명령을 고치면
/reload-plugins                   # 재시작 없이 즉시 반영
```
`/myflow:commit`이 동작하고 `reviewer` 에이전트가 보이면 성공이다 [7].

**6) git에 올려 남도 쓰게** — 마켓플레이스 카탈로그 추가(`./.claude-plugin/marketplace.json`)
```json
{
  "name": "my-marketplace",
  "owner": { "name": "나", "email": "me@example.com" },
  "plugins": [ { "name": "myflow", "source": "./myflow" } ]
}
```
```bash
git init && git add -A && git commit -m "add myflow plugin"
git push   # GitHub의 owner/repo 로
```
이제 누구든 `/plugin marketplace add owner/repo` → `/plugin install myflow@my-marketplace`로 설치한다 [7]. 여기서 본 것처럼 **코드는 그대로고 설치 출처(로컬→git→공식)만 단계적으로 바뀐다** [국내 배포 3단계].

**7) (선택) 공식 디렉터리 제출** — repo URL을 제출하면 검토 후 등재되어 검색에 노출된다 [6].

> 포인트: 한 플러그인에 **명령(commit) + 에이전트(reviewer)** 가 함께 들어가, 설치 한 번으로 둘 다 켜진다. 여기에 `hooks/`로 "커밋 후 자동 리뷰", `.mcp.json`으로 "GitHub 연결"을 더하면 4요소가 모두 든 본격 플러그인이 된다.

## 13. 함정·체크리스트

**DO**
- `.claude-plugin/`엔 `plugin.json`만, 기능 폴더는 루트에 [7][8].
- `name`을 신중히(네임스페이스가 됨). 충돌 없는 고유 이름 [7].
- `--plugin-dir`로 충분히 로컬 검증 후 push [7].
- `marketplace.json`의 `source`로 외부 repo도 묶어 배포 [7].
- 조직 배포는 화이트리스트 중앙 마켓 + 관리 설정 [국내 가상부서][7].

**DON'T**
- 기능 폴더를 `.claude-plugin/` 안에 넣지 말 것(인식 안 됨) [7][8].
- `name` 없이/중복으로 두지 말 것(필수·네임스페이스) [7].
- 검증 안 된 외부 플러그인을 사내 마켓에 그대로 등록 금지 [국내 가상부서].
- 훅·MCP가 무슨 코드를 실행하는지 모른 채 배포·설치 금지(①편 보안).

## 한눈 요약
- 플러그인 = **구조를 갖춘 git repo + `plugin.json`**. `.claude-plugin/`엔 매니페스트만, 나머지는 루트 [7][8].
- `name`이 **유일 필수 + 네임스페이스** [7].
- 구성요소: `commands/`·`agents/`·`hooks/`·`.mcp.json`. 테스트는 `--plugin-dir`·`/reload-plugins` [7].
- 마켓플레이스 = `marketplace.json`(`plugins[].name+source`). 배포 3단계(로컬→git→공식 제출), **출처만 변함** [6][7].
- 조직은 **화이트리스트 중앙 마켓 + 관리 설정**으로 공급망 통제 [국내 가상부서][7].

## 출처

**국내**
1. (국내) 아프니까 개발자다, "서브에이전트 배포하기 — /plugin install부터 마켓플레이스까지", 티스토리, 2026-06-19 — 배포 3단계("출처만 바뀐다"). https://storycompiler.tistory.com/567
2. (국내) 웃픈조의 리뷰 공작소, "클로드 코드 앱 워크숍 후기 — 터미널 없이 웹서비스 배포까지", 네이버 블로그, 2026-03-15 — "스킬=레시피, 플러그인=묶음, 마켓플레이스=저장소". https://blog.naver.com/cjg00kr/224217323651
3. (국내) 1234567890, "클로드 AI 반복 프롬프트, 스킬 만들기 3단계", 네이버 블로그, 2026-06-08 — `.claude/skills/` 복사 vs `/plugin` 설치, 자동/수동 호출. https://blog.naver.com/reaa1213/224309469677
4. (국내) 트레이드클루, "클로드 코워크와 지식작업 플러그인으로 가상 부서 만들기", 네이버 블로그, 2026-06-16 — 사내 중앙 보안 마켓플레이스·화이트리스트. https://blog.naver.com/tradeclue/224317536312
5. (국내) 구반장의 잡다한 지식, "앤트로픽 클로드 마켓플레이스 공개", 네이버 블로그, 2026-03-12 — 개발자가 마켓플레이스로 서비스 배포. https://blog.naver.com/ribis9/224213557896

**해외**
6. (해외) Anthropic, "Create plugins" 공식 문서 — 플러그인=구조+매니페스트 git repo, 제출·인덱싱. https://code.claude.com/docs/en/plugins
7. (해외) Anthropic, "Create and distribute a plugin marketplace" 공식 문서 — `.claude-plugin/` 규칙, `plugin.json`/`marketplace.json` 필드, `--plugin-dir`·`/reload-plugins`. https://code.claude.com/docs/en/plugin-marketplaces
8. (해외) anthropics/claude-code, `plugins/README.md` — 디렉터리 배치(루트 vs .claude-plugin). https://github.com/anthropics/claude-code/blob/main/plugins/README.md
9. (해외) Anthropic, "Customize Claude Code with plugins"(뉴스) — 플러그인 구성요소·배포 개요. https://www.anthropic.com/news/claude-code-plugins
10. (해외) DataCamp, "How to Build Claude Code Plugins: A Step-by-Step Guide". https://www.datacamp.com/tutorial/how-to-build-claude-code-plugins
11. (해외) alexop.dev, "How to Build a Claude Code Plugin: Skills, Agents & Commands". https://alexop.dev/posts/building-my-first-claude-code-plugin/
12. (해외) hidekazu-konishi.com, "Claude Code Plugins Complete Guide — Bundling Skills, Hooks, Agents, MCP for Team Distribution". https://hidekazu-konishi.com/entry/claude_code_plugins_complete_guide.html
13. (해외) DEV Community(nagell), "Build Your Own Claude Code Marketplace: Scaffold, Structure, Auto-Updates". https://dev.to/nagell/build-your-own-claude-code-marketplace-scaffold-structure-and-auto-updates-4n3f
14. (해외) systemprompt.io, "Publishing a Plugin to the Claude Marketplace". https://systemprompt.io/guides/publish-plugin-claude-marketplace

## 🔗 시리즈 내비게이션 — 「클로드 플러그인 마스터」
- ◀ 이전: **①편** [[클로드 플러그인]] 완전 가이드(개관·분야별 추천)
- ▶ **현재: ②편** 나만의 플러그인·마켓플레이스 만들기
- ▶ 다음: **③편** [[클로드 확장 생태계]] — 플러그인 vs MCP vs 스킬 vs 서브에이전트 vs 훅
- ④편 [[클로드 플러그인 워크플로우]] — 분야별 실전 레시피
- 선행: [[MCP(Model Context Protocol)]] 완전 가이드(`#r=claude-mcp-guide`)
