---
title: 클로드 코드 모드(mod) 활용하기 — 데스크톱 앱 Code 탭에서 설치부터 직접 만들기까지
date: 2026-10-15
level: 입문
minutes: 60
tags: [클로드코드, 모드, mods, 데스크톱앱, 플러그인, 훅, 타입스크립트, 상태줄, 패널, 슬래시명령]
prereq: [Claude 데스크톱 앱(Code 탭), Claude Code v2.1.286 이상]
videos: [yUuFvL1lK4k, dUKUgvyqAw0, yIvw5WtMTSU, KtquxqP2YnM, EiThSVZ8pME]
---

# 클로드 코드 모드(mod) 활용하기 — 데스크톱 앱 Code 탭에서 설치부터 직접 만들기까지

> 클로드 코드의 「모드(mod)」는 클로드 코드의 화면과 동작을 바꾸는 작은 코드다. 이 가이드는 **Claude 데스크톱 앱의 Code 탭**을 기준으로, 남이 만든 모드를 설치하고 끄는 법에서 시작해 **세 파일짜리 모드를 직접 읽고 고치는 데**까지 간다. 코드 예제는 모두 실제로 검사기를 통과한 것이다. 약 60분.

## 이 가이드로 만들 것

모드는 **자바스크립트·타입스크립트 이벤트 핸들러로 된 플러그인**이다. 도구 호출, 제출된 프롬프트, 화면의 한 부분이 그려지는 순간 같은 사건이 일어날 때 클로드 코드가 그 함수를 부른다[1][2]. 설정 훅과 상태줄은 클로드 코드 바깥에서 스크립트를 돌리지만, 모드는 클로드 코드 안에서 돌기 때문에 화면에 패널·띠를 그리고 클로드 코드가 그리는 부분을 바꿀 수 있다[1][13].

```
모드 한 개 = 폴더 한 개
  .claude-plugin/plugin.json   ← 이름표(매니페스트)
  hooks/hooks.json             ← "내 코드는 여기" 한 줄
  hooks/register.ts            ← 실제 코드: 사건마다 부를 함수들
```

끝내면 다음 세 모드를 읽고 고칠 수 있다.

| 모드 | 하는 일 | 쓰는 기능 |
|---|---|---|
| `guard-status` | `.env` 파일 편집을 막고, 실패한 셸 명령을 상태줄에 띄운다 | 도구 호출 훅 · 상태줄 |
| `turn-band` | 입력창 위에 「지난 턴 몇 초 · 도구 몇 회」를 띄우고, 데스크톱에서는 막대그래프까지 그린다 | 화면 그리기 훅 · 데스크톱 전용 Svg |
| `tool-calls` | `/tool-calls` 명령으로 이 세션의 도구 호출 목록 패널을 연다 | 슬래시 명령 · 패널 |

다루지 않는 것: 모드를 깃허브로 배포하는 법, 조직 관리자용 정책 설정, 모델이 직접 부르는 도구 등록. 「다음으로 할 것」에 남겼다.

## 사전 준비물

| 항목 | 설명 |
|---|---|
| Claude 데스크톱 앱 | Code 탭에서 **로컬 세션**을 연다. 데스크톱 앱은 클로드 코드 사본을 따로 갖고 있고, 모드는 그 사본 v2.1.286부터 돈다[1][9]. 버전은 로컬 세션에서 `/status` 를 쳐 Claude Code 행으로 본다[1] |
| 터미널(선택) | 2단계에서 마켓플레이스를 추가하고, 8단계에서 검사기를 돌릴 때 쓴다. 터미널 클로드 코드는 v2.1.287부터 모드가 기본으로 켜진다[1][10][13]. 버전은 셸에서 `claude --version` 으로 본다[1] |
| 코드 편집기(선택) | 4단계부터 파일을 열어 볼 때 |

**설정 훅과 헷갈리지 말 것.** 클로드 코드에는 원래 `settings.json` 에 적는 「훅」이 있었다. 모드의 핸들러도 공식 문서에서 훅이라 부르기 때문에, 문서는 예전 것을 **설정 훅(settings hook)** 으로 구분한다. 설정 훅은 설정 파일에 적는 셸 명령·HTTP 요청·프롬프트이고, 모드의 훅은 클로드 코드 안에서 실행되는 함수다[1][13].

> **모드는 샌드박스 없이 돈다.** 모드는 클로드 코드와 같은 권한으로 컴퓨터에 접근하고 격리되지 않는다. 그래서 공식 안내는 믿을 수 있는 작성자와 마켓플레이스의 모드만 설치하라고 한다[1][5]. 클로드 코드의 샌드박스는 클로드가 실행한 Bash 명령만 격리하므로, 샌드박스를 켜도 모드가 띄운 프로세스는 그 바깥에서 돈다[1][12].

## 1단계 — 내 데스크톱 앱이 모드를 돌릴 수 있는지 확인하기

**할 일**
1. 데스크톱 앱을 최신으로 업데이트한다.
2. Code 탭에서 **로컬 세션**(또는 SSH 세션)을 연다.
3. 세션 종류를 확인한다. 아래 표에서 「돈다」가 아닌 곳이면 모드가 나타나지 않는다.

| 데스크톱 앱 세션 | 모드 | 근거 |
|---|---|---|
| Code 탭 로컬 세션 | 돈다 | [1] |
| Code 탭 WSL 세션 | 안 돈다 — WSL 세션에서는 플러그인을 쓸 수 없다 | [1] |
| 클라우드 세션 | 내 기기에 설치한 플러그인이 실리지 않는다 | [4][11] |

**화면에서 확인할 것**
Code 탭의 프롬프트 입력창 옆 **+** 버튼을 누르면 **Plugins** 메뉴가 보인다. 로컬·SSH 세션에서 설치된 플러그인과 스킬을 보는 곳이다[4].

**막히면**
메뉴는 있는데 모드가 아무것도 안 그려지면 세션이 WSL인지부터 본다[1]. 또, 클로드 코드는 작업 폴더를 신뢰한다는 확인을 받기 전에는 모드를 싣지 않는다[6][16]. 처음 연 폴더라면 신뢰 확인부터 마친다 — 문서는 그 폴더에서 터미널로 `claude` 를 실행해 답하라고 안내한다[16].

## 2단계 — 남이 만든 모드 설치하고 끄기

**할 일**
1. Code 탭에서 **+ → Plugins → Add plugin** 을 눌러 플러그인 브라우저를 연다[4].
2. 브라우저에는 **이미 추가한 마켓플레이스**의 플러그인만 보인다[4][11]. 원하는 모드가 없으면 **+ → Plugins → Add marketplace** 에 `소유자/저장소` 를 넣어 마켓플레이스부터 추가한다[7].
3. 터미널이 편하면 한 줄로 설치할 수도 있다[7].

```bash
claude plugin install <모드이름> --marketplace <소유자>/<저장소>
```

셸에서 `--marketplace` 를 붙인 이 한 줄 설치는 v2.1.292 이상에서 된다[4].

4. 설치한 모드를 **끄는 방법**은 세 가지다[1].

| 범위 | 방법 |
|---|---|
| 모드 하나 | 데스크톱: **+ → Plugins → Manage plugins** 에서 끄거나 지운다[4] · 터미널: `/plugin` 의 Installed 탭[1] |
| 이번 세션만 전부 | (터미널 전용) `--safe-mode` 로 시작한다 — 다른 사용자 설정도 함께 꺼진다[1]. 데스크톱 앱이 여는 세션에는 이런 플래그를 줄 수 없다[7] |
| 모든 세션 전부 | `~/.claude/settings.json` 에 `"disableAllHooks": true` — 설정 훅과 직접 만든 상태줄도 함께 꺼진다[1]. 터미널과 데스크톱 로컬 세션은 같은 설정 파일을 읽는다[4] |

**화면에서 확인할 것**
**+ → Plugins** 목록에 설치한 모드가 보이고, 모드가 그리는 것(상태줄·띠·패널)이 나타난다. 세션이 열려 있는 동안 터미널(셸)에서 설치했다면 그 세션에서 `/reload-plugins` 를 실행하거나 새 세션을 연다[1][4].

**막히면**
데스크톱 Code 탭의 로컬 세션에서는 `/plugin` 같은 터미널 명령이 「사용할 수 없다」고 답한다[7]. 데스크톱에서는 **+ → Plugins** 메뉴를 쓰고, 마켓플레이스 추가가 잘 안 되면 터미널에서 추가해 둔다[11]. 터미널에서 사용자 범위로 설치한 모드는 데스크톱 로컬 세션에서도 실린다[7].

> **끄는 설정이 듣지 않는 모드도 있다.** `disableAllHooks`·`--bare`·`--safe-mode` 는 클로드 코드에 **내장된 모드**는 멈추지 않는다. 내장 모드 목록은 터미널 `/plugin` 의 Installed 탭에 Built-in 으로 따로 보인다[1].

## 3단계 — 말로 첫 모드 만들기

**할 일**
1. Code 탭에서 이렇게 요청한다.

```
.env 파일은 수정하지 못하게 막고, 셸 명령이 실패하면 상태줄에 보여 주는 모드를 만들어 줘.
```

2. 클로드가 모드 제작 스킬로 **세 파일을 바로 쓴다.** 코드를 손으로 짤 필요는 없다[7].
3. 첫 파일이 쓰이는 순간 클로드 코드가 **「이 세션에서 핫 리로딩을 켤까요?」** 를 한 번 묻는다. 「How does this work?」, 「Enable for this session」, 「Not now」 가운데 고른다[7].
4. **Enable for this session** 을 고르면 그 턴이 끝날 때 모드가 통째로 실리고, 이후 고친 내용은 고친 턴이 끝날 때마다 다시 실린다[7].

**화면에서 확인할 것**
턴이 끝난 뒤 다음 프롬프트부터 모드가 동작한다. 일부러 실패하는 명령(예: 없는 파일을 `cat`)을 시켜 보면 **상태줄에 「실패: …」** 가 뜬다.

**막히면**
**Not now** 를 골랐다면 파일은 쓰였지만 이번 세션에는 실리지 않고, **이 세션을 다음에 다시 시작할 때** 실린다 — 모드 폴더가 세션마다 따로 있기 때문이다. 문서는 이때 다음 세션 시작이나 질문 다시 띄우기만 안내한다[3][7]. 다시 묻게 하려면 클로드에게 질문을 다시 띄워 달라고 하면 된다[7]. 핫 리로딩 질문은 사람만 답할 수 있고, 권한 모드나 규칙으로 대신 켤 수 없다[7].

## 4단계 — 세 파일 읽기

**할 일**
3단계에서 만들어진(또는 아래를 그대로 옮긴) 세 파일을 연다. 이 구조는 공식 문서의 「작은 모드는 세 파일」과 같다[3][14].

`.claude-plugin/plugin.json` — 이름표다.

```json
{ "name": "guard-status", "version": "0.1.0", "description": "Blocks edits to .env files and shows failed shell commands in the status line" }
```

`hooks/hooks.json` — 코드가 어디 있는지 한 줄. **`modules` 키가 있어야 플러그인이 모드가 된다**[3]. 경로는 이 파일 기준이고 한 개만 적는다[8].

```json
{ "modules": ["./register.ts"] }
```

`hooks/register.ts` — 실제 코드다. 파일은 `register` 라는 함수 하나를 내보내고, 클로드 코드는 그 함수에 `on` 을 넘겨 부른다. `on` 을 부를 때마다 사건 하나에 핸들러(훅) 하나가 등록된다[3].

**훅의 모양은 하나다** — `($, e, next)`[7].

| 이름 | 뜻 |
|---|---|
| `$` | 클로드 코드에 일을 시키는 창구. `$.ui.status(...)` 처럼 「명사.동사」로 부른다 |
| `e` | 이번 사건의 입력. 바꿀 수 없는 값이다 |
| `next(e)` | 다음 모드와 클로드 코드 본래 동작으로 넘긴다. 넘긴 결과가 돌아온다 |

`next` 를 안 부르고 값을 돌려주면 **모드가 직접 답한 것**이 되고, `next({ ...e, 바꿀값 })` 으로 넘기면 **뒤에서 보는 입력을 고친 것**이 된다[7]. 빌드 단계는 없다 — 클로드 코드가 `.js`·`.ts`·`.tsx` 를 그대로 싣는다[7][8].

**화면에서 확인할 것**
편집기에서 폴더 구조가 위 그림과 같고, `hooks.json` 의 경로가 실제 파일 이름(`register.ts` 또는 `register.tsx`)과 같다.

**막히면**
모드 코드 안에는 **브라우저(DOM)도 Node도 없다.** Node의 `fs` 도 브라우저의 `fetch` 도 없고, 바깥의 모든 일은 `$` 를 거친다(`$.fs`, `$.http.fetch`, `$.process` 등)[7]. 또 `import()` (동적 import)가 들어 있는 파일은 실리지 않는다[7].

## 5단계 — 도구 호출 가로채기와 상태줄

**할 일**
`hooks/register.ts` 를 아래로 채운다. 이 코드는 Claude Code 2.1.300에서 검사기(`claude plugin validate`)와 타입 검사를 통과했다(작성자 확인).

```ts
import type { Register } from 'claude-code'

const PROTECTED = /(^|\/)\.env(\.|$)/

export const register: Register = on => {
  on('tool.call', { tool: 'Edit' }, ($, e, next) =>
    PROTECTED.test(e.file_path)
      ? { deny: `${$.plugin.name}: ${e.file_path} 는 이 모드가 막는 파일입니다.` }
      : next(e),
  ).catch(($, e, next) =>
    next.called ? next(e) : { deny: `${$.plugin.name}: 가드가 실패했습니다.` },
  )

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const ran = await next(e)
    const hasFailed = ran.deny === undefined && ran.isError === true

    $.ui.status(hasFailed ? `실패: ${e.command.slice(0, 40)}` : undefined)

    return ran
  })
}
```

**한 줄씩 읽기**
- `on('tool.call', { tool: 'Edit' }, …)` — 두 번째 인자는 **거르개(matcher)** 다. Edit 도구 호출에만 이 훅이 불린다. `e` 는 Edit 도구의 입력이라 `e.file_path` 가 있다[7].
- `{ deny: … }` 를 돌려주면 그 도구 호출이 **거절**된다. `next(e)` 를 돌려주면 그대로 진행된다[7].
- `.catch(…)` — **막는 훅에는 꼭 붙인다.** 훅이 예외를 던지면 기본은 「건너뛰고 계속」이라, 가드가 고장 나면 막아야 할 편집이 그냥 통과한다. `.catch` 가 그 자리에서 대신 답한다 — 아직 `next` 를 안 불렀으면 거절하고, 불렀으면 이미 정해진 결과를 다시 돌려준다[7].
- Bash 훅은 먼저 `await next(e)` 로 명령을 실행시키고, **결과를 보고** 상태줄을 바꾼다. `$.ui.status(undefined)` 는 상태줄을 지운다[7].

**화면에서 확인할 것**
클로드에게 `.env` 를 고쳐 달라고 하면 **「… 는 이 모드가 막는 파일입니다.」** 로 거절되고, 실패하는 셸 명령 뒤에는 상태줄에 **「실패: …」** 가 뜬다.

**막히면**
막았는데도 `.env` 가 바뀌었다면 먼저 **어느 도구가 바꿨는지** 본다 — 이 가드의 거르개는 `{ tool: 'Edit' }` 뿐이라, Write 도구나 Bash 명령으로 덮어쓰는 것은 막지 못한다. 경로 모양도 본다 — 이 정규식은 경로 조각이 `.env` 로 끝나거나 `.env.` 로 시작하는 것을 막는다(`.env.d/` 같은 폴더 안의 파일도 걸린다). 레퍼런스는 이런 「이름 모양 막기」가 최선의 노력일 뿐이라고 하고, 확실히 막으려면 `$.fs.stat(path, { resolve: true })` 가 돌려주는 실제 경로(`realPath`)로 허용 목록을 만들라고 권한다[7].

## 6단계 — 입력창 위 띠 그리기, 데스크톱에서는 그래프까지

**할 일**
새 모드 폴더 `turn-band` 를 만들고 네 파일을 둔다. 화면이 읽는 값을 `$.state` 에 두는 모드는 **값의 타입 계약 파일**이 하나 더 필요하다[7].

`.claude-plugin/plugin.json` — `types` 로 계약 파일을 가리킨다.

```json
{ "name": "turn-band", "version": "0.1.0", "description": "Shows the last turn's time and tool calls above the prompt", "types": "./types/index.d.ts" }
```

`hooks/hooks.json` 은 `{ "modules": ["./register.tsx"] }` 이고, `types/index.d.ts` 는 이렇다.

```ts
export type Turn = { seconds: number; tools: number }

declare module 'claude-code' {
  interface PluginState {
    'turn-band': { last: Turn | null }
  }
}
```

`hooks/register.tsx` — 화면을 그리므로 확장자가 `.tsx` 다. 역시 2.1.300에서 검사기와 타입 검사를 통과했다(작성자 확인).

```tsx
import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Turn } from '../types'

const last = atom({ plugin: 'turn-band', key: 'last' } as const, null)

export const register: Register = on => {
  let startedAt = 0
  let tools = 0

  on('prompt.submit', async ($, e, next) => {
    startedAt = await $.clock.now()
    tools = 0

    return next(e)
  })

  on('tool.call', ($, e, next) => {
    tools += 1

    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const seconds = Math.round(((await $.clock.now()) - startedAt) / 1000)
    const turn: Turn = { seconds, tools }
    await update($, last, () => turn)

    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const turn = await read($, last)

    if (e.props.hasSurvey || turn === null) {
      return next(e)
    }

    const label = `지난 턴 ${turn.seconds}초 · 도구 ${turn.tools}회`

    if (e.surface === 'desktop') {
      const { Box, Text, Svg } = $.ui.resolve(e)
      const width = Math.min(200, turn.tools * 10)
      const bar = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="10"><rect width="${width}" height="10" rx="3" fill="#E8735A"/></svg>`

      return (
        <Box gap={1}>
          <Text dimColor>{label}</Text>
          <Svg source={bar} alt={label} width={200} height={10} />
        </Box>
      )
    }

    const { Box, Text } = $.ui.resolve(e)

    return (
      <Box>
        <Text dimColor>{label}</Text>
      </Box>
    )
  })
}
```

**데스크톱 위주로 읽기**
- `ui.render` 훅은 **화면의 한 자리**를 그린다. `AbovePrompt` 는 입력창 바로 위의 띠이고, 이 자리는 터미널과 데스크톱에서만 그려진다[7].
- `e.surface` 가 지금 그리는 곳이다 — `terminal`·`desktop`·`vscode`·`mobile`[7]. 데스크톱과 터미널을 `e.surface === 'desktop'` 으로 갈라 그리는 방식은 데스크톱 모드 해설에서도 권한다[8].
- `$.ui.resolve(e)` 가 **그 화면이 가진 부품표**를 준다. 데스크톱 부품표에는 `Box`·`Text`·`Button`·`Input`·`Select`·`Svg`·`Link`·`Code`·`Markdown`·`Client` 가 있고, **`Svg` 는 터미널에 없다**(터미널에는 대신 `Raster`·`Image` 가 있다)[7]. 그래서 `e.surface` 로 좁힌 뒤에만 `Svg` 를 꺼낼 수 있다.
- `Svg` 의 `alt` 는 필수다. 데스크톱은 SVG를 이미지로 그리고, 스크립트는 어떤 경우에도 돌지 않는다[7].
- 화면이 읽는 값은 모듈 변수가 아니라 `$.state` 에 둔다(`atom`·`read`·`update`). 핫 리로드 때 모듈 변수는 처음으로 돌아가지만 `$.state` 는 남고, `update` 로 값을 쓰면 그 값을 읽은 화면만 다시 그려진다[7].

**화면에서 확인할 것**
한 턴이 끝나면 데스크톱 Code 탭 입력창 위에 **「지난 턴 12초 · 도구 3회」** 같은 줄과 **코랄색 막대**가 함께 보인다. 터미널에서 같은 모드를 열면 막대 없이 글자만 보인다.

**막히면**
띠 자리가 비어 있다면 그 자리에 설문(`hasSurvey`)이 떠 있는지 본다 — 이 코드는 설문이 있으면 양보한다. 부품표에 없는 부품을 쓰거나 받지 않는 속성을 넣으면 그 그림은 **통째로 거절**되고 클로드 코드가 제 것을 대신 그린다. 핫 리로딩 중이면 대화창에 「… refused: 이유」 한 줄이 흐리게 남으니 그 이유를 읽는다[7].

## 7단계 — 슬래시 명령과 패널

**할 일**
세 번째 모드 `tool-calls` 를 만든다. `plugin.json`·`hooks.json`·계약 파일은 6단계와 같은 모양이고(계약은 `'tool-calls': { calls: ToolCall[] }`), `register.tsx` 는 아래와 같다. 2.1.300에서 검사기와 타입 검사를 통과했다(작성자 확인).

```tsx
import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { ToolCall } from '../types'

const PANE = 'tool-calls'
const calls = atom({ plugin: 'tool-calls', key: 'calls' } as const, [])

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'tool-calls',
      description: '이 세션의 도구 호출을 패널로 보여 준다',
    })

    return next(e)
  })

  on('command.run', { command: 'tool-calls' }, async $ => {
    await $.ui.open({ id: PANE, title: '도구 호출' })

    return { text: '도구 호출 패널을 열었습니다.' }
  })

  on('tool.call', async ($, e, next) => {
    const call: ToolCall = { id: e.tool_use_id, tool: e.tool, isDone: false }
    await update($, calls, list => [...list, call].slice(-200))
    const ran = await next(e)
    await update($, calls, list =>
      list.map(one => (one.id === call.id ? { ...one, isDone: true } : one)),
    )

    return ran
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const list = await read($, calls)
    const room = Math.max(1, (e.viewport?.rows ?? 24) - 4)

    return (
      <Box flexDirection="column">
        {list.length === 0 && <Text dimColor>아직 도구 호출이 없습니다.</Text>}
        {list.slice(-room).map(call => (
          <Text dimColor={call.isDone}>
            {call.isDone ? '완료' : '실행 중'} {call.tool}
          </Text>
        ))}
      </Box>
    )
  })
}
```

**한 줄씩 읽기**
- 슬래시 명령은 **세션이 시작될 때**(`session.start`) `$.command.register` 로 등록하고, `command.run` 훅이 답한다. 돌려주는 `{ text }` 가 명령의 출력이다[7].
- 패널은 `$.ui.open({ id, title })` 로 열고, 같은 `id` 를 `requestId` 로 거르는 `ui.render` 훅이 내용을 그린다. 패널(`Pane`)은 붙어 있는 **모든 화면**에서 그려진다[7].
- 공식 문서는 모드가 띄울 수 있는 자리로 오른쪽 사이드바 패널, 대화창 오른쪽 위 토스트, 대화창 로그 한 줄, 입력창 위 띠, 입력창 아래 상태줄을 든다 — 터미널 전체화면 기준 지도이고, 데스크톱에서 그려지는 자리는 다를 수 있다[15].

**화면에서 확인할 것**
Code 탭 입력창에 `/tool-calls` 를 치면 **「도구 호출 패널을 열었습니다.」** 가 나오고, 패널에 「실행 중 Bash」→「완료 Bash」 처럼 도구 호출이 쌓인다.

**막히면**
명령이 목록에 없다면 모드가 실제로 실렸는지(3단계 핫 리로딩 질문에 **Enable** 로 답했는지) 본다 — 명령은 `session.start` 에서 등록되고, 핫 리로드는 다시 실을 때 `session.start` 를 다시 부른다[7]. 그래도 없으면 8단계의 검사기로 「answers its own command」 줄이 찍히는지 본다.

## 8단계 — 검사하고 고치기, 데스크톱 개발 환경 갖추기

**할 일**
1. 터미널에서 검사기를 돌린다. 모드가 **어떤 사건에 걸리고 무엇을 부르는지**, 클로드 코드가 거절할 것은 무엇인지 미리 보여 준다[7].

```bash
claude plugin validate <모드 폴더>
```

5단계 모드를 검사하면 이런 줄이 나온다 — 막는 훅에 `.catch` 가 붙었는지도 여기서 보인다.

```
> ./register.ts hooks: tool.call{tool=Edit}, tool.call{tool=Bash}
> ./register.ts gating hook with .catch: tool.call{tool=Edit}
> ./register.ts gating hook without .catch: tool.call{tool=Bash}
> ./register.ts calls: $.ui.status
```

Bash 훅은 아무것도 막지 않으므로 `.catch` 가 없어도 된다. 「gating hook」 줄은 경고가 아니라, 답에 따라 무언가를 거절할 수 **있는** 자리에 훅이 걸렸다는 사실 보고다[7].

2. 동작 시험은 `claude plugin test <모드 폴더>` 로 `*.test.ts` 파일을 돌리고, 원인을 찾을 때는 `claude --debug` 로 연다 — 디버그 로그에는 건너뛴 훅과 거절된 그림마다 줄이 남는다[7].
3. **데스크톱 앱에서 개발 중인 폴더를 싣는 법.** 데스크톱 앱이 시작하는 세션에는 `--plugin-dir` 같은 명령줄 플래그를 줄 수 없다. 대신 `~/.claude/settings.json` 의 `env` 블록에 폴더를 적는다[7].

```json
{
  "env": {
    "CLAUDE_CODE_PLUGIN_DIRS": "/Users/나/mods/guard-status",
    "CLAUDE_CODE_PLUGIN_DIR_WATCH": "1"
  }
}
```

`CLAUDE_CODE_PLUGIN_DIRS` 는 절대 경로(`~` 허용)를 받고, 여러 개면 운영체제의 경로 목록 구분자로 잇는다. 프로젝트 설정 파일이 아니라 **사용자 설정**(`~/.claude/settings.json`)에만 적을 수 있다. 데스크톱처럼 오래 떠 있는 세션은 `CLAUDE_CODE_PLUGIN_DIR_WATCH=1` 을 함께 두어야 저장할 때마다 다시 싣는다[7].

**화면에서 확인할 것**
검사기 마지막 줄에 **`√ Validation passed with warnings`** 가 찍힌다. 경고는 `author` 정보가 없다는 것 하나뿐이고 동작과 무관하다.

**막히면**
클로드 코드를 업데이트한 뒤 모드가 이상해졌다면 **API가 바뀐 것**일 수 있다. 모드 API는 얼리 액세스라 릴리스마다 움직이고, 정본은 그 빌드가 함께 깔아 주는 타입 선언 파일이다[7]. 직접 만들거나 `CLAUDE_CODE_PLUGIN_DIRS` 로 싣는 모드(감시를 켰을 때)라면, 실린 뒤 모드 폴더의 `.claude-plugin/types/` 에 그 빌드의 선언이 깔리므로 거기서 사건 이름(`'tool.call'` 등)을 찾아 읽는다. 마켓플레이스에서 설치한 모드 폴더에는 깔리지 않는다[7]. 업데이트 뒤 다시 볼 것을 정리한 데스크톱 모드 해설도 있다[9]. 또 모드가 도는 작업 스레드가 멈추거나 죽었을 때 원인을 한 모드로 짚으면 그 모드만 내려진다. 세 번 멈췄는데 짚지 못하면 내장 모드를 뺀 모든 모드(조직이 설치한 모드 포함)가 이번 세션 동안 내려지고, 이때는 `/reload-plugins` 로 다시 싣는다[16]. 어느 모드인지는 디버그 로그(`claude --debug`)에서 찾는다[16].

## 흔히 막히는 지점

**1. WSL 세션에서 모드를 찾는다**
데스크톱 앱의 WSL 세션에서는 플러그인을 쓸 수 없어 모드도 돌지 않는다[1]. 로컬 세션으로 연다.

**2. 데스크톱에서 `/plugin` 을 친다**
데스크톱 Code 탭의 로컬 세션에서는 `/plugin` 이 동작하지 않는다[7]. **+ → Plugins** 메뉴를 쓰거나 터미널에서 설치한다.

**3. 막는 훅에 `.catch` 를 안 붙인다**
훅이 실패하면 기본 동작은 「건너뛰고 계속」이라, 고장 난 가드는 아무것도 막지 못한다[7]. **막는(deny를 돌려주는) 훅**에 검사기의 `gating hook without .catch` 줄이 붙었는지 본다. 이 줄은 관찰만 하는 훅에도 찍히니, 막는 훅인지부터 가린다[7].

**4. 화면 값을 모듈 변수에 둔다**
핫 리로드 때마다 모듈 변수는 처음으로 돌아간다. 화면이 읽는 값은 `$.state`, 세션을 넘겨 남길 값은 `$.store` 에 둔다[7].

**5. 터미널에 없는 부품을 그린다**
`Svg` 는 터미널에만 없고(데스크톱·모바일·VS Code 부품표에는 있다), `Raster`·`Image` 는 터미널에만 있다[7]. `e.surface` 로 나누지 않고 그리면 한쪽 화면에서 그림이 거절된다.

**6. 출처를 모르는 모드를 설치한다**
모드는 샌드박스 없이 클로드 코드와 같은 권한으로 돈다[5]. 깃허브의 모드 모음에서 고를 때도 코드를 먼저 읽고, `claude plugin validate` 로 어떤 사건과 호출을 쓰는지 확인한다.

## 다음으로 할 것

1. **모델이 부르는 도구 만들기** — `$.tool.register` 로 도구를 선언하면 `mcp__<플러그인>__<이름>` 으로 모델에게 보인다[7].
2. **프롬프트 손보기** — `prompt.submit` 훅에서 `next({ ...e, text })` 로 보내는 글을 바꾸거나, `prompt.compose` 로 시스템 프롬프트에 단락을 더한다[7].
3. **배포** — 모드 폴더에 `.claude-plugin/marketplace.json` 을 두면 깃허브 저장소가 마켓플레이스가 되고, 다른 사람은 2단계의 한 줄로 설치한다[7].
4. **조직에서 쓰기** — 팀 단위로 모드를 허용·차단하는 방법은 관리자 문서를 본다[6].

## 관련 영상

아래 영상은 전부 YouTube API로 **실재·공개 여부를 확인**한 것이다. 제목·채널·길이는 확인 시점(2026-10-15)의 실제 값이다.

> 아래 설명은 **제목·채널·길이·설명란 첫머리** 기준이며, 이 가이드의 근거로는 쓰지 않았다. 근거는 전부 아래 「출처」의 문서다.

1. **Mods in Claude Code: change how Claude Code works** (3분 21초, Claude) — Anthropic 공식 채널. 설명란은 모드를 「클로드 코드가 그리는 것, 프롬프트에 들어가는 것, 도구 호출을 바꾸는 함수」로 소개한다.
2. **Claude Code 모드(Mods) 직접 써 봤습니다 | 말로 만드는 나만의 기능 + 쓸만한 모드 사례** (9분 51초, 단테, 한국어) — 3단계 「말로 만들기」와 짝지어 보기 좋다.
3. **Claude Code, 내 입맛대로 바꾸세요 | MODS 실전 예제 3가지** (7분 16초, 코난쌤 conanssam, 한국어) — 설명란에 따르면 도구 호출 카운터, 위험한 명령 가드, 컨텍스트 사용량 게이지를 다룬다. 5~7단계 다음 단계로.
4. **클로드코드 "모드"는 혁신입니다.. ㄷㄷ 미친 신기능 /mods** (8분 46초, 성공지식백과, 한국어) — 설명란에 따르면 원리와 훅, 공식 예시를 살펴본다.
5. **Claude Code Mods Can Do Basically Anything...** (7분 37초, Better Stack) — 설명란이 모드를 「클로드 코드 안에서 도는 작은 타입스크립트 플러그인」으로 소개한다.

## 출처

**공식 문서 (1차 출처)**
- [1] Mods overview — Claude Code Docs · https://code.claude.com/docs/en/plugins/mods/overview (모드 = 자바스크립트·타입스크립트 이벤트 핸들러로 된 플러그인, 설정 훅과의 비교, 데스크톱 앱의 자체 사본 v2.1.286·터미널 v2.1.287과 버전 확인법, WSL 세션 제외, 끄는 세 방법과 `disableAllHooks` 범위, 내장 모드는 꺼지지 않음, 샌드박스는 Bash만, 믿을 수 있는 출처만 설치)
- [2] Mods 개요(한국어) — Claude Code Docs · https://code.claude.com/docs/ko/plugins/mods/overview (같은 문서의 한국어판)
- [3] Create a mod — Claude Code Docs · https://code.claude.com/docs/en/plugins/mods/create (세 파일 구조, `modules` 키가 플러그인을 모드로 만든다, `register` 가 `on` 을 받는다)
- [4] Install and manage plugins — Claude Code Docs · https://code.claude.com/docs/en/plugins/install (데스크톱 Code 탭 로컬·SSH 세션의 + → Plugins → Add plugin·Manage plugins, 브라우저는 추가한 마켓플레이스만 보여 준다, 터미널·데스크톱 로컬 세션은 같은 설정 파일, 클라우드 세션 미적재, `/reload-plugins`, 셸 `--marketplace` 설치는 v2.1.292 이상)
- [5] Customize Claude Code with mods — Claude 공식 블로그 · https://claude.com/blog/claude-code-mods (모드는 플러그인에 실려 배포, 클로드 코드와 같은 권한·샌드박스 없음)
- [6] Manage mods for your organization — Claude Code Docs · https://code.claude.com/docs/en/plugins/mods/admin (조직 단위 모드 관리, 신뢰 확인 전에는 모드를 싣지 않음)
- [7] 「plugin-authoring」 스킬 문서 — Claude Code 2.1.300에 동봉된 모드 제작 스킬(SKILL·reference.md·예제 모듈 3개와 계약 파일 2개·`types/claude-code.d.ts`). 세션 안에서 스킬을 불러 읽었다 (훅 모양, 거르개, `.catch`, 화면별 부품표, `$.state`, 핫 리로딩 질문, `CLAUDE_CODE_PLUGIN_DIRS`·`CLAUDE_CODE_PLUGIN_DIR_WATCH`, 데스크톱의 마켓플레이스 추가 메뉴와 `/plugin` 미지원, validate·test·debug)
- [15] Draw in the interface — Claude Code Docs · https://code.claude.com/docs/en/plugins/mods/interface (모드가 그릴 수 있는 자리 — 사이드바 패널·토스트·로그 한 줄·입력창 위 띠·상태줄)
- [16] Troubleshoot mods — Claude Code Docs · https://code.claude.com/docs/en/plugins/mods/troubleshoot (신뢰 확인 전 미적재, 작업 스레드가 세 번 멈출 때 원인 모드만 또는 내장 외 전부 내림, `/reload-plugins`)

**해외 자료**
- [8] How to make a Claude Code mod with three files that work in the desktop app — DEV Community(Haruki Nakada) · https://dev.to/nakadadev/how-to-make-a-claude-code-mod-with-three-files-that-work-in-the-desktop-app-26mm (세 파일, Node·빌드 단계 없음, `hooks.json` 경로는 그 파일 기준 한 개, `e.surface === 'desktop'` 분기)
- [9] Claude Code mods in the desktop app: a one-page summary and what to recheck after updates — DEV Community(Haruki Nakada) · https://dev.to/nakadadev/claude-code-mods-in-the-desktop-app-a-one-page-summary-and-what-to-recheck-after-updates-23bo (데스크톱 지원은 2.1.286부터, 업데이트 뒤 다시 볼 것)
- [10] Claude Code Mods: What They Are and How to Write One — Developers Digest · https://www.developersdigest.tech/blog/claude-code-mods-guide-2026 (터미널 v2.1.287·데스크톱 v2.1.286, 기본으로 켜짐)
- [11] Claude Code Desktop Mods: Install and Build One — explainx.ai · https://www.explainx.ai/blog/claude-code-desktop-app-mods-how-to-install-and-build-guide-2026 (브라우저는 추가한 마켓플레이스만 보여 줌, 마켓플레이스는 터미널에서 추가하는 편이 확실, 클라우드 세션은 데스크톱 설치 플러그인을 싣지 않음)
- [12] Claude Code mods let you customize the interface, commands and more — IT-Connect · https://www.it-connect.tech/claude-code-mods-let-you-customize-the-interface-commands-and-more/ (클로드 코드 샌드박스는 클로드가 실행한 Bash 명령만 격리)

**국내 자료**
- [13] 클로드 코드 Mods: TypeScript로 화면과 동작 바꾸기 — Dale Seo · https://daleseo.com/claude-code-mods/ (v2.1.287부터 기본으로 켜짐, 패널·스피너 문구·도구 호출 가로채기, 모드의 훅과 설정 훅의 구분)
- [14] 모드 만들기(한국어) — Claude Code Docs · https://code.claude.com/docs/ko/plugins/mods/create ([3]의 한국어판)

> **확인 조건과 한계** — 2026-10-15 기준으로 작성했다. 5~7단계의 코드 세 벌은 이 가이드를 쓴 환경의 **Claude Code 2.1.300에서 `claude plugin validate` 와 타입 검사(`tsc`)를 통과**한 그대로다. 다만 데스크톱 앱 화면에서 실제로 띄워 보지는 않았으니, 그려지는 모습은 버전에 따라 다를 수 있다. 모드 기능의 시작 버전은 공식 개요를 따라 데스크톱 앱 사본 2.1.286, 터미널 2.1.287로 갈라 적었다[1]. 모드 API는 얼리 액세스라 릴리스마다 바뀔 수 있다 — 업데이트 뒤에는 모드 폴더의 `.claude-plugin/types/` 선언을 먼저 확인한다. 메뉴 이름과 위치는 앱 버전에 따라 바뀔 수 있으니 「무엇을 하는 메뉴인지」를 기준으로 찾으면 된다.
