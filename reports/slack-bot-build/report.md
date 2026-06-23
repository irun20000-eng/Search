---
주제: Slack 봇 직접 만들기 — Bolt·Socket Mode 실전 워크스루 (DEEP)
날짜: 2026-06-24
깊이: deep
카드모드: auto
대상수준: 실무 가이드(DEEP)
태그: [Slack, 봇개발, Bolt, SocketMode, 1인개발자, 자동화, 웹훅, 실전튜토리얼]
소스수: { 국내: 5, 해외: 9 }
위키링크: ["[[웹훅(Webhook)]]", "[[Slack]]", "[[1인 개발자]]", "[[업무 자동화]]", "[[MCP(Model Context Protocol)]]"]
갤러리URL: "#r=slack-bot-build"
---

# Slack 봇 직접 만들기 — Bolt · Socket Mode 실전 워크스루

> 작성·조회 기준일 **2026-06-24 (KST)**. 토큰·스코프·명령은 시간에 민감하므로 **공식 문서(docs.slack.dev)** 로 최종 확인할 것. 선행: [[Slack]] 완전 해부(1인 개발자편, `#r=slack-solo-developer`)에서 "봇 만들기"를 한 단계 깊게 판 실전편이다.

## TL;DR
- **Bolt**는 Slack이 만든 공식 프레임워크로, Events API·슬래시 명령·인터랙티브(버튼/모달)·Web API를 **한 라이브러리로** 묶어준다. JavaScript·Python 모두 지원 [6][10].
- 1인 개발자는 **Socket Mode**를 쓰자. Slack이 이벤트를 **WebSocket으로 푸시**해줘 **공개 URL(HTTPS 서버)이 필요 없다** — 로컬·홈서버·방화벽 뒤에서도 봇이 돈다 [2][3].
- 토큰은 셋이다: **사용자 `xoxp`, 봇 `xoxb`, 앱레벨 `xapp`**. Socket Mode는 **앱레벨 토큰(`xapp`) + `connections:write` 스코프**가 필수다 [1][3].
- 최소 스코프: 메시지 전송 **`chat:write`**, 멘션 수신 **`app_mentions:read`** + `app_mention` 이벤트 구독 [1][11].
- Bolt 초기화는 단 몇 줄: `new App({ token: BOT_TOKEN, socketMode: true, appToken: APP_TOKEN })`. 이후 `app.event`/`app.command`/`app.action`으로 리스너만 달면 된다 [6][9].

## 핵심 포인트
1. **HTTP 모드 vs Socket Mode** — 1인·로컬은 Socket Mode가 압도적으로 편하다(공개 URL 불필요) [2][3].
2. **토큰 3종 구분**이 첫 관문: `xoxb`(봇 행동), `xapp`(소켓 연결) [1].
3. **스코프는 미리 다 넣고 설치** — 빠뜨리면 재설치(reinstall) 필요 [1].
4. **3초 규칙**: 슬래시 명령·액션은 **`ack()`를 3초 안에** 호출해야 한다 [9].
5. **봇을 채널에 초대**해야 그 채널에 말할 수 있다(흔한 실수) [6].

## 1. 큰 그림 — HTTP 모드 vs Socket Mode

Slack 앱이 이벤트(멘션·명령·버튼)를 받는 방식은 두 가지다 [3][국내 스프링부트].

```
① HTTP 모드 (Request URL 방식)
   Slack ──HTTP POST──▶ [공개 HTTPS 엔드포인트(내 서버)] 
   - 공개 URL·SSL·서명검증 필요. 서버리스/프로덕션에 적합.

② Socket Mode (WebSocket 방식)   ← 1인 개발자 추천
   내 앱 ──WebSocket 연결──▶ Slack  (Slack이 이벤트를 푸시)
   - 공개 URL 불필요. 로컬·홈서버·방화벽 뒤에서 OK.
   - 앱레벨 토큰(xapp) + connections:write 필요.
```

- **HTTP 모드**: Slack이 내 공개 엔드포인트로 POST한다. 따라서 **고정 공개 URL과 HTTPS**가 필요하고 요청 서명을 검증해야 한다. 트래픽 많은 프로덕션·서버리스(Lambda)에 적합.
- **Socket Mode**: 내 앱이 Slack에 **WebSocket으로 먼저 연결**하고, Slack이 그 소켓으로 이벤트를 밀어준다. **공개 URL이 없어도** 되므로 노트북·홈서버에서 바로 개발·운영할 수 있다 [2][3]. 국내 가이드도 "소켓모드 = Slack Bolt로 로컬 서버 구동 후 슬랙에서 연결"이라고 정리한다 [국내 스트림].

**결론(1인 개발자)**: 개발·소규모 운영은 **Socket Mode**. 나중에 트래픽이 커지거나 서버리스로 가면 HTTP 모드로 전환하면 된다 — Bolt는 **같은 코드에서 `socketMode` 플래그만** 바꾸면 된다 [국내 Bolt.js].

### 왜 Bolt인가 — raw API와 비교
Slack 봇은 Bolt 없이 Web API(`chat.postMessage` 등)를 직접 호출해서도 만들 수 있다. 하지만 그러면 **이벤트 수신 서버, 요청 서명 검증, 재시도 처리, 소켓 관리**를 전부 손으로 짜야 한다. Bolt는 이 잡일을 추상화해 **"이벤트 → 리스너 함수" 한 줄**로 줄여준다. 실제로 Bolt 기반이면 **몇 시간 만에** 동작하는 봇을 띄울 수 있다는 게 공통된 평가다 [6][13]. 즉 Bolt는 "Slack과 통신하는 보일러플레이트"를 대신 짊어지고, 나는 **봇이 무슨 일을 할지(비즈니스 로직)** 에만 집중한다. 1인 개발자에게 이 시간 절약은 곧 레버리지다.

한 가지 더: Bolt는 **JS와 Python의 API가 거의 1:1로 대응**된다(`app.event`/`@app.event`, `app.command`/`@app.command`). 그래서 팀 언어가 무엇이든 같은 멘탈 모델로 옮겨갈 수 있고, 이 문서의 예제도 두 언어를 나란히 싣는다 [6][9][10].

## 2. 준비물 — 토큰 3종과 스코프

Slack 앱에는 토큰이 셋 있고, 역할이 다르다 [1][3].

| 토큰 | 접두사 | 무엇에 쓰나 | 발급 위치 |
|---|---|---|---|
| 사용자 토큰 | `xoxp` | 사용자 신원으로 API 호출 | OAuth(필요 시) |
| **봇 토큰** | **`xoxb`** | 봇이 메시지 전송·API 호출 | OAuth & Permissions |
| **앱레벨 토큰** | **`xapp`** | **Socket Mode 연결** | Basic Information → App-Level Tokens |

- **봇 토큰(`xoxb`)**: OAuth & Permissions 페이지에서 워크스페이스에 설치한 뒤 복사 [1].
- **앱레벨 토큰(`xapp`)**: Socket Mode 연결용. 발급 시 **`connections:write`** 스코프를 부여한다(이름은 "Development" 등) [1][3].
- **봇 스코프(Bot Token Scopes)**: 최소 **`chat:write`**(채널에 메시지 전송), 멘션을 받으려면 **`app_mentions:read`** [1][11].

## 3. STEP 1 — 앱 생성

1. **api.slack.com/apps → Create New App**.
2. **From scratch**(처음부터) 또는 **From an app manifest**(YAML로 한 번에) 중 선택. 처음이면 scratch가 직관적이다 [6][12].
3. 앱 이름과 설치할 **워크스페이스**(개발용으로 본인 워크스페이스 권장)를 고른다.

> 팁: manifest 방식은 스코프·이벤트·명령을 YAML 한 장으로 정의해 **재현·공유**가 쉽다. 같은 봇을 여러 워크스페이스에 깔거나 팀과 공유할 거면 manifest를 쓰자 [12].

## 4. STEP 2 — 권한·이벤트·Socket Mode 설정

앱 설정 페이지에서 다음을 켠다 [1][3][11].

1. **OAuth & Permissions → Bot Token Scopes**: `chat:write`, `app_mentions:read` 추가(필요에 따라 `commands`, `channels:history` 등).
2. **Socket Mode → Enable Socket Mode: ON**.
3. **Basic Information → App-Level Tokens → Generate**: `connections:write` 스코프로 `xapp` 토큰 발급 [1][3].
4. **Event Subscriptions → Enable**: Bot Events에 **`app_mention`** 구독 추가(앱이 @멘션될 때 이벤트 수신) [11].
5. (선택) **Slash Commands → Create**: 예 `/status`(설명·사용법 입력).
6. **Install App**: 워크스페이스에 설치하고 **봇 토큰(`xoxb`) 복사**.

> ⚠️ **스코프를 바꾸면 재설치(reinstall)** 해야 적용된다. 처음에 필요한 스코프를 한 번에 넣는 게 편하다 [1].

## 5. STEP 3 — 토큰을 환경변수로

토큰은 절대 코드·리포에 평문으로 두지 않는다. `.env`에 담고 git에서 제외한다 [국내 스트림].

```bash
# .env  (반드시 .gitignore에 추가)
SLACK_BOT_TOKEN=xoxb-...      # 봇 토큰
SLACK_APP_TOKEN=xapp-...      # 앱레벨 토큰(Socket Mode)
```

## 6. STEP 4 — 첫 봇 (Bolt for JavaScript)

Node 프로젝트에서 Bolt를 설치하고, Socket Mode로 띄운다 [6][13].

```bash
npm init -y
npm install @slack/bolt dotenv
```

```javascript
// app.js
require('dotenv').config();
const { App } = require('@slack/bolt');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,    // xoxb
  socketMode: true,                      // ← 공개 URL 불필요
  appToken: process.env.SLACK_APP_TOKEN, // xapp
});

// @봇 멘션에 반응
app.event('app_mention', async ({ event, say }) => {
  await say(`안녕하세요 <@${event.user}>! 무엇을 도와드릴까요?`);
});

// "ping" 이 포함된 메시지에 반응
app.message('ping', async ({ say }) => {
  await say('pong 🏓');
});

(async () => {
  await app.start();
  console.log('⚡️ Slack 봇 실행 중 (Socket Mode)');
})();
```

```bash
node app.js   # 공개 URL 없이 바로 동작
```

- `socketMode: true` + `appToken`만 주면 **Bolt가 WebSocket 연결을 알아서** 관리한다 [6].
- 봇을 사용할 채널에서 **`/invite @봇이름`으로 초대**해야 그 채널에 말할 수 있다(흔한 함정) [6].

## 7. STEP 5 — 같은 봇 (Bolt for Python)

파이썬이 편하면 동일 기능을 이렇게 쓴다 [9][10].

```bash
pip install slack_bolt
```

```python
# app.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])  # xoxb

@app.event("app_mention")
def handle_mention(event, say):
    say(f"안녕하세요 <@{event['user']}>! 무엇을 도와드릴까요?")

@app.message("ping")
def handle_ping(message, say):
    say("pong 🏓")

if __name__ == "__main__":
    # 앱레벨 토큰(xapp)으로 Socket Mode 시작
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

- `@app.event("app_mention")` 데코레이터로 멘션 이벤트를 잡는다 [11].
- `say()`는 문자열(평문)이나 dict(블록 메시지)를 받는다 [9].
- async 앱이면 모든 리스너를 async로, `await ack()`/`await say()`처럼 **await 필수** [9].

## 8. STEP 6 — 슬래시 명령 (`/status`)

슬래시 명령은 **반드시 `ack()`를 3초 안에** 호출해 Slack에 "받았다"를 알린 뒤 응답한다 [9].

```javascript
// JS — /status 명령
app.command('/status', async ({ command, ack, respond }) => {
  await ack();                                   // ① 3초 내 필수
  // command.text 로 인자 접근 가능 (예: /status prod)
  await respond(`✅ 서비스 정상 · 요청자: <@${command.user_id}>`);
});
```

```python
# Python — /status 명령
@app.command("/status")
def status_cmd(ack, respond, command):
    ack()                                          # ① 3초 내 필수
    respond(f"✅ 서비스 정상 · 요청자: <@{command['user_id']}>")
```

- **`say()` vs `respond()`**: `say()`는 채널에 일반 메시지를 올리고, `respond()`는 명령의 `response_url`로 응답(본인에게만 보이게 `response_type` 조절 가능) [9].
- `command.text`로 인자를 받는다(`/status prod` → `"prod"`).

## 9. STEP 7 — 인터랙티브(버튼·Block Kit)

알림에서 끝나지 않고 **버튼으로 행동**하게 만든다. Block Kit으로 버튼을 그리고 `app.action`으로 클릭을 처리한다 [6][13].

```javascript
// 버튼이 있는 메시지 보내기
app.command('/deploy', async ({ ack, say }) => {
  await ack();
  await say({
    text: '배포를 진행할까요?',
    blocks: [{
      type: 'actions',
      elements: [
        { type: 'button', text: { type: 'plain_text', text: '🚀 배포' },
          style: 'primary', action_id: 'deploy_go' },
        { type: 'button', text: { type: 'plain_text', text: '취소' },
          action_id: 'deploy_cancel' },
      ],
    }],
  });
});

// 버튼 클릭 처리
app.action('deploy_go', async ({ ack, say, body }) => {
  await ack();
  await say(`🚀 <@${body.user.id}> 가 배포를 시작했습니다…`);
  // 여기서 실제 배포 스크립트 트리거
});
```

이렇게 하면 Slack이 **운영 콘솔**이 된다 — 멘션으로 조회하고, 버튼으로 배포·롤백을 실행한다. Block Kit은 버튼 외에도 드롭다운(static_select)·날짜 선택·텍스트 입력(모달) 같은 요소를 제공하므로, 간단한 사내 도구의 **UI를 Slack 안에서** 만들 수 있다. 별도 프런트엔드를 만들 여력이 없는 1인 개발자에게는 "Slack 메시지가 곧 관리자 화면"이 되는 셈이라 가성비가 높다. 다만 복잡한 폼이 필요해지면 그때는 모달(`views.open`)로 분리하거나 웹 대시보드로 넘어가는 게 낫다 [6][13].

## 10. Worked 통합 예 — "운영 봇" 만들기

[[Slack]] 1인 개발자편의 "운영 상황실"을 봇으로 한 단계 끌어올린다. 시나리오: **@봇으로 서버 상태를 묻고, `/rollback` 버튼으로 되돌린다.**

```
[설계]
@봇 status   → app_mention 리스너가 헬스체크 API 호출 → 결과를 스레드로 답
/rollback    → ack → "정말 롤백?" 버튼 메시지
  └ [확인] 클릭 → app.action('rollback_go') → 배포 스크립트 실행 → 결과 보고
```

```javascript
// @봇 에게 "status" 라고 멘션하면 헬스체크
app.event('app_mention', async ({ event, say }) => {
  if (event.text.includes('status')) {
    const ok = await checkHealth();         // 내 헬스체크 함수
    await say({ thread_ts: event.ts,
      text: ok ? '🟢 모든 서비스 정상' : '🔴 장애 감지 — 로그 확인 요망' });
  }
});
```

- **핵심**: 봇 로직 안에서 **내 인프라 함수(`checkHealth`, 배포 스크립트)** 를 호출한다. Slack은 입출력 창구일 뿐, 실제 일은 내 코드가 한다.
- **안전장치**: 되돌리기 어려운 행동(배포·롤백)은 **버튼 확인 단계**를 둔다(앞 워크플로우편의 "승인 게이트"와 동일 철학).
- **확장**: 여기에 [[MCP(Model Context Protocol)]]·LLM을 붙이면 "에러 로그를 요약해 원인 후보를 스레드에 달아주는" AI 운영 봇으로 진화한다.

## 11. 배포·운영 — 어디서 돌리나

Socket Mode 봇은 **공개 URL이 없어도** 되므로 선택지가 넓다 [3][국내 파이썬].

| 환경 | 적합도 | 비고 |
|---|---|---|
| 로컬(노트북) | 개발·테스트 | 끄면 봇도 멈춤 |
| 홈서버·라즈베리파이 | 소규모 상시 | 전기만 있으면 24/7 |
| VPS·EC2 | 안정 상시 운영 | `pm2`/`systemd`로 데몬화 |
| 컨테이너(Docker) | 이식·재현 | 토큰은 시크릿으로 주입 |
| 서버리스(Lambda) | 대규모·간헐 | 보통 **HTTP 모드**가 더 맞음 |

- **상시 운영**: `pm2 start app.js` 또는 systemd 유닛으로 죽으면 자동 재시작.
- **토큰 보안**: `xoxb`/`xapp`는 **환경변수/시크릿 매니저**로. 노출되면 즉시 재발급(Revoke) — 노출 토큰으로 누구나 내 워크스페이스를 조작할 수 있다 [1][국내 스트림].
- **마이그레이션 주의**: 구(舊) 클래식 앱은 지원 종료(2026-03-31 안내)이므로 **신 플랫폼/Bolt 기준**으로 새로 만든다 [3].

## 12. 흔한 오해 · FAQ

- **"공개 서버(도메인·SSL)가 꼭 있어야 봇을 만들 수 있나?"** — 아니다. **Socket Mode**면 내 앱이 Slack에 먼저 연결하므로 공개 URL이 필요 없다. 노트북에서 `node app.js` 한 줄로 동작한다 [3].
- **"토큰이 왜 두 개(`xoxb`·`xapp`)나 필요한가?"** — 역할이 다르다. `xoxb`는 **봇이 행동(메시지 전송 등)** 할 때, `xapp`은 **Socket Mode로 Slack에 연결**할 때 쓴다. Socket Mode 봇은 둘 다 필요하다 [1][3].
- **"명령을 쳤는데 `/status failed`처럼 실패로 뜬다."** — 십중팔구 **`ack()`를 3초 안에 호출하지 않은** 것이다. 무거운 작업은 `ack()` 먼저 하고 그 뒤에 처리하라 [9].
- **"`missing_scope` 에러가 난다."** — 필요한 스코프를 안 넣었거나, 스코프 추가 후 **재설치를 안 한** 것이다. 스코프 변경은 reinstall이 필요하다 [1].
- **"봇이 채널에서 말을 못 한다."** — 그 채널에 봇을 **초대(`/invite @봇`)** 하지 않았기 때문이다. 또는 `chat:write` 스코프 누락 [6][1].
- **"HTTP 모드와 Socket Mode를 나중에 바꿔도 되나?"** — 된다. Bolt는 `socketMode` 플래그와 토큰만 바꾸면 동일 로직이 양쪽에서 돈다. 처음엔 Socket Mode로 시작해 필요할 때 전환하는 게 1인 개발자에게 합리적이다 [국내 Bolt.js][3].

## 13. 흔한 함정 · 체크리스트

**DO**
- **Socket Mode + `xapp`(connections:write)** 로 공개 URL 없이 시작 [1][3].
- 슬래시 명령·액션은 **`ack()` 3초 내 호출** [9].
- 봇을 쓸 채널에 **`/invite @봇`** 초대 [6].
- 스코프는 **미리 다 넣고 설치**(바꾸면 재설치) [1].
- 토큰은 **`.env`/시크릿**, `.gitignore` 필수 [국내 스트림].

**DON'T**
- 토큰을 코드·리포·스크린샷에 노출하지 말 것(노출 즉시 Revoke) [1].
- `ack()`를 빠뜨리거나 늦게 호출하지 말 것(명령 실패로 보임) [9].
- 스코프 없이 API 호출하지 말 것(`missing_scope` 에러) [1].
- 1인·로컬인데 굳이 HTTP 모드로 공개 서버를 띄우지 말 것(불필요한 복잡도) [3].

## 한눈 요약
- **Bolt**(JS/Python)로 Events·명령·인터랙티브를 한 라이브러리로 [6][10].
- 1인은 **Socket Mode**(공개 URL 불필요): `xapp`+`connections:write` [1][3].
- 스코프 `chat:write`·`app_mentions:read`, 토큰은 `.env`로 [1].
- 멘션=`app.event('app_mention')`, 명령=`app.command`(+`ack` 3초), 버튼=`app.action` [9][6].
- 봇 안에서 **내 인프라 함수 호출** → Slack이 운영 콘솔, 위험 행동엔 버튼 확인 [국내 Bolt.js].

## 출처

**국내**
1. (국내) Claude 한국어 가이드, "Claude API 슬랙봇 만들기: Bolt.js + Claude 통합", 네이버 블로그, 2026-05-10 — Bolt.js `socketMode` true/false 전환, 동일 코드. https://blog.naver.com/the_unemployed/224280546472
2. (국내) Sung-Dong's blog, "스트림 형식 히스토리 기반 슬랙 앱 구현", 네이버 블로그, 2025-09-24 — Socket Mode로 Bolt 로컬 서버 구동·.env 설정. https://blog.naver.com/sdkim817/224020297956
3. (국내) 토니네, "스프링부트로 슬랙봇 만들기", 네이버 블로그, 2022-07-29 — HTTP 방식 vs 소켓모드 개념 정리. https://blog.naver.com/ndskr/222833245252
4. (국내) Hyeri's Diary, "챗지피티 슬랙봇 만들기(파이썬·Socket Mode)", 네이버 블로그, 2025-11-24 — Python Socket Mode 파일 업로드 봇. https://blog.naver.com/nidldltkatka/224085707495
5. (국내) 길에서찾는인생, "슬랙봇 만들기 — 슬랙과 대화하며 테스트", 네이버 블로그, 2025-01-07 — 소켓모드 토큰(xapp)·봇 토큰(xoxb) 발급 실례. https://blog.naver.com/genycho/223717464819

**해외**
6. (해외) Slack Developer Docs, "Quickstart with Bolt for JavaScript" — Bolt 초기화·Socket Mode·리스너. https://docs.slack.dev/tools/bolt-js/getting-started/
7. (해외) Slack Developer Docs, "Using Socket Mode" — 소켓 모드 연결·앱레벨 토큰. https://docs.slack.dev/apis/events-api/using-socket-mode/
8. (해외) Slack, "Socket Mode" — `connections:write`·WebSocket 푸시·공개 URL 불필요. https://api.slack.com/apis/socket-mode
9. (해외) Slack Developer Docs, "Listening & responding to commands (Bolt Python)" — `ack`·`say` vs `respond`·async. https://docs.slack.dev/tools/bolt-python/concepts/commands/
10. (해외) slackapi/bolt-python, GitHub — Bolt for Python 프레임워크. https://github.com/slackapi/bolt-python
11. (해외) Slack, "Tutorial: Responding to app mentions" — `app_mentions:read`·`app_mention` 이벤트. https://api.slack.com/tutorials/tracks/responding-to-app-mentions
12. (해외) Slack Developer Docs, "Creating an app with Bolt for JavaScript" — 앱 manifest·scratch 생성. https://docs.slack.dev/tools/bolt-js/creating-an-app/
13. (해외) Hemaks, "Building Slack Bots on Node.js with Bolt API: From Zero to Production" — 토큰·스코프·버튼 실전. https://hemaks.org/posts/building-slack-bots-on-nodejs-with-bolt-api-from-zero-to-production/
14. (해외) DEV Community(Isak Solheim), "Creating a Slackbot With JavaScript Bolt" — 입문 워크스루. https://dev.to/isaksolheim/creating-a-slackbot-with-javascript-bolt-1kp7

## 후속 질문·연결
- 봇에 LLM을 붙여 **AI 운영 봇**으로? → [[MCP(Model Context Protocol)]]
- 알림만 빠르게 → [[웹훅(Webhook)]] (Incoming Webhook)
- 선행: [[Slack]] 완전 해부(1인 개발자편, `#r=slack-solo-developer`)
- 관련: [[1인 개발자]] · [[업무 자동화]]
