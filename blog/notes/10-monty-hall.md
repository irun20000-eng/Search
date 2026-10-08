<!-- 표지 — templates/fluor 가 렌더한 형광안 표지. 여기서 다시 내보내지 않는다. -->
  <img class="cover" src="assets/10-monty-hall/thumb.png" alt="표지" width="800" height="800">

  <h1>몬티홀 문제, 세특에 쓰기 전에 직접 계산해 보세요</h1>
  <p class="lead">"문을 바꾸는 쪽이 유리하대요." 몬티홀 문제를 이렇게 결론만 아는 경우가 많아요. 그런데 "왜 유리한데?"라고 물으면 대부분 막혀요.<br>
  세특(세부능력 및 특기사항)에 이 문제를 쓰는 학생도 적지 않은데, 결론만 옮겨 적으면 읽는 사람 눈에는 금방 티가 나요.<br>
  오늘은 바꾸면 왜 2배 유리한지 <strong>직접 세어서</strong> 보이고, 많은 글이 빠뜨리는 <strong>숨은 전제</strong> 하나까지 짚어 볼게요. 세특에 적을 '나만의 과정'이 여기서 나와요.</p>

  <h2>문제부터 정확히 — 규칙이 결과를 만들어요</h2>
  <p>상황은 이래요. 문이 세 개 있고, 하나 뒤에는 자동차가, 나머지 둘 뒤에는 염소가 있어요. 참가자가 문 하나를 골라요. 그러면 진행자가 <strong>남은 두 문 중 염소가 있는 문 하나를 열어</strong> 보여 주고, "바꾸시겠어요?"라고 물어요.</p>
  <p>여기서 많은 글이 그냥 넘어가는 부분이 있어요. 바로 <strong>진행자의 행동 규칙</strong>이에요. 결과를 정확히 계산하려면 네 가지를 못 박아야 해요. ①진행자는 <strong>자동차가 어디 있는지 알아요.</strong> ②참가자가 고르지 않은 문 중에서, <strong>반드시 염소가 있는 문</strong>을 열어요. ③그런 문이 두 개면(참가자가 처음에 자동차를 골랐을 때) 그중 아무거나 열어요. ④그리고 <strong>항상</strong> 바꿀 기회를 줘요. 이 규칙이 바뀌면 답도 바뀌어요. 그래서 계산보다 규칙을 먼저 적는 게 순서예요.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <svg viewBox="0 0 720 470" width="720" height="470" aria-label="문 3개 중 참가자가 1번을 고르고 진행자가 3번 염소 문을 연 상황도">
      <!-- 문 1 : 내 선택 -->
      <text x="145" y="70" font-size="30" fill="var(--green)" font-weight="700" text-anchor="middle">내 선택</text>
      <rect x="55" y="90" width="180" height="310" rx="10" fill="var(--green-soft)" stroke="var(--green)" stroke-width="5"/>
      <text x="145" y="215" font-size="86" fill="var(--green)" font-weight="800" text-anchor="middle">1</text>
      <text x="145" y="300" font-size="40" fill="var(--green-deep)" font-weight="700" text-anchor="middle">?</text>
      <circle cx="210" cy="250" r="7" fill="var(--green-deep)"/>
      <!-- 문 2 : 남은 문 -->
      <text x="360" y="70" font-size="30" fill="var(--ink-soft)" font-weight="700" text-anchor="middle">남은 문</text>
      <rect x="270" y="90" width="180" height="310" rx="10" fill="#ffffff" stroke="var(--ink-soft)" stroke-width="4"/>
      <text x="360" y="215" font-size="86" fill="var(--ink-soft)" font-weight="800" text-anchor="middle">2</text>
      <text x="360" y="300" font-size="40" fill="var(--ink-soft)" font-weight="700" text-anchor="middle">?</text>
      <circle cx="425" cy="250" r="7" fill="var(--ink-soft)"/>
      <!-- 문 3 : 진행자가 연 염소 문 -->
      <text x="575" y="70" font-size="30" fill="var(--amber)" font-weight="700" text-anchor="middle">진행자가 열었어요</text>
      <rect x="485" y="90" width="180" height="310" rx="10" fill="#f0efe9" stroke="var(--ink-soft)" stroke-width="3" stroke-dasharray="10 8"/>
      <text x="575" y="205" font-size="86" fill="#b9b4a6" font-weight="800" text-anchor="middle">3</text>
      <text x="575" y="285" font-size="40" fill="var(--amber)" font-weight="800" text-anchor="middle">염소</text>
      <text x="575" y="335" font-size="27" fill="var(--ink-soft)" text-anchor="middle">(꽝)</text>
      <!-- 하단 안내 -->
      <text x="360" y="445" font-size="30" fill="var(--ink)" font-weight="700" text-anchor="middle">바꿀까요, 그대로 둘까요?</text>
    </svg>
  </div>
  <div class="caption">진행자는 '알고' 염소 문을 열어요 — 이 규칙이 뒤의 계산을 좌우해요.</div>

  <h2>직접 계산 ① 경우의 수로 2/3을 보여요</h2>
  <p>감탄만 하면 세특이 안 돼요. 세어 볼게요. 참가자가 <strong>1번 문을 골랐다</strong>고 하고(어느 문을 고르든 대칭이라 결과는 같아요), 자동차 위치를 세 경우로 나눠요. 각 경우가 일어날 확률은 똑같이 $\dfrac{1}{3}$이에요.</p>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>자동차 위치<br>(각 1/3)</th><th>진행자가<br>여는 문</th><th>바꾸면</th><th>그대로 두면</th></tr>
      <tr><td><strong>1번</strong><br>(내가 맞힘)</td><td>2번 또는 3번</td><td>패배</td><td><strong>승리</strong></td></tr>
      <tr><td><strong>2번</strong></td><td>3번뿐</td><td><strong>승리</strong></td><td>패배</td></tr>
      <tr><td><strong>3번</strong></td><td>2번뿐</td><td><strong>승리</strong></td><td>패배</td></tr>
      <tr><td>합계</td><td>—</td><td><strong>2/3 승</strong></td><td>1/3 승</td></tr>
    </table>
  </div>
  <div class="caption">세 경우를 세어 보면 바꾸기는 두 번 이기고, 그대로 두기는 한 번 이겨요.</div>

  <ul>
    <li>자동차가 <strong>1번</strong>(참가자가 맞힘): 진행자는 2번이나 3번(둘 다 염소)을 열어요. 바꾸면 남은 염소 문이라 <strong>패배</strong>, 그대로 두면 <strong>승리</strong>.</li>
    <li>자동차가 <strong>2번</strong>: 진행자는 염소가 있는 3번을 열 수밖에 없어요. 바꾸면 2번이라 <strong>승리</strong>, 그대로 두면 패배.</li>
    <li>자동차가 <strong>3번</strong>: 진행자는 2번을 열 수밖에 없어요. 바꾸면 3번이라 <strong>승리</strong>, 그대로 두면 패배.</li>
  </ul>
  <p>바꾸기는 세 경우 중 두 번 이기고, 그대로 두기는 한 번 이겨요. 그러니까 이렇게 정리돼요.</p>

  <div class="eq" data-export="png" data-name="eq-01">
    $$P(\text{바꾸기 승리})=\frac{2}{3},\qquad P(\text{그대로 승리})=\frac{1}{3}$$
  </div>
  <div class="caption">바꾸면 승률이 정확히 2배예요 — 느낌이 아니라 세어서 나온 값이에요.</div>

  <h2>직접 계산 ② 남은 문이 둘인데 왜 50:50이 아닐까요</h2>
  <p>가장 흔한 오해가 "문이 두 개 남았으니 반반 아니냐"예요. 그렇지 않아요. 핵심은 <strong>처음 고른 문의 확률은 진행자가 문을 열어도 변하지 않는다</strong>는 데 있어요. 처음에 1번이 자동차일 확률은 $\dfrac{1}{3}$이고, 진행자가 염소 문을 열어 보여 줘도 이 값은 그대로 $\dfrac{1}{3}$이에요. 그런데 전체 확률의 합은 1이어야 하니까, 나머지 $\dfrac{2}{3}$이 <strong>열리지 않고 남은 한 문</strong>에 통째로 몰려요. 진행자가 염소 문 하나를 걷어내 주면서, 안 고른 쪽의 $\dfrac{2}{3}$을 한 문에 모아 준 셈이에요.</p>

  <div class="fig" data-export="png" data-name="fig-02">
    <svg viewBox="0 0 720 590" width="720" height="590" aria-label="참가자 1번 선택 후 자동차 위치별로 갈라지는 나무그림, 각 가지 확률과 바꾸기 결과 표시">
      <!-- 루트 -->
      <rect x="250" y="25" width="220" height="60" rx="10" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="360" y="63" font-size="29" fill="var(--green-deep)" font-weight="700" text-anchor="middle">참가자 1번 선택</text>
      <!-- 가지 -->
      <line x1="360" y1="85" x2="135" y2="150" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <line x1="360" y1="85" x2="360" y2="150" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <line x1="360" y1="85" x2="585" y2="150" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <text x="205" y="120" font-size="26" fill="var(--green)" font-weight="700" text-anchor="middle">1/3</text>
      <text x="378" y="120" font-size="26" fill="var(--green)" font-weight="700" text-anchor="middle">1/3</text>
      <text x="515" y="120" font-size="26" fill="var(--green)" font-weight="700" text-anchor="middle">1/3</text>
      <!-- 1단: 자동차 위치 -->
      <g text-anchor="middle">
        <rect x="45" y="150" width="180" height="56" rx="9" fill="#ffffff" stroke="var(--ink-soft)" stroke-width="2.5"/>
        <text x="135" y="186" font-size="27" fill="var(--ink)" font-weight="700">자동차 1번</text>
        <rect x="270" y="150" width="180" height="56" rx="9" fill="#ffffff" stroke="var(--ink-soft)" stroke-width="2.5"/>
        <text x="360" y="186" font-size="27" fill="var(--ink)" font-weight="700">자동차 2번</text>
        <rect x="495" y="150" width="180" height="56" rx="9" fill="#ffffff" stroke="var(--ink-soft)" stroke-width="2.5"/>
        <text x="585" y="186" font-size="27" fill="var(--ink)" font-weight="700">자동차 3번</text>
      </g>
      <!-- 연결선 -->
      <line x1="135" y1="206" x2="135" y2="268" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <line x1="360" y1="206" x2="360" y2="268" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <line x1="585" y1="206" x2="585" y2="268" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <!-- 2단: 진행자가 연 문 -->
      <g text-anchor="middle">
        <text x="135" y="296" font-size="25" fill="var(--ink-soft)">진행자: 2·3번 중</text>
        <text x="360" y="296" font-size="25" fill="var(--ink-soft)">진행자: 3번</text>
        <text x="585" y="296" font-size="25" fill="var(--ink-soft)">진행자: 2번</text>
      </g>
      <line x1="135" y1="315" x2="135" y2="380" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <line x1="360" y1="315" x2="360" y2="380" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <line x1="585" y1="315" x2="585" y2="380" stroke="var(--ink-soft)" stroke-width="2.5"/>
      <!-- 3단: 바꾸면 결과 -->
      <g text-anchor="middle">
        <rect x="55" y="380" width="160" height="60" rx="9" fill="#f0efe9" stroke="var(--ink-soft)" stroke-width="2.5"/>
        <text x="135" y="411" font-size="25" fill="var(--ink-soft)" font-weight="700">바꾸면 패</text>
        <text x="135" y="433" font-size="22" fill="var(--ink-soft)">(1/3)</text>
        <rect x="280" y="380" width="160" height="60" rx="9" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3.5"/>
        <text x="360" y="411" font-size="25" fill="var(--green-deep)" font-weight="800">바꾸면 승</text>
        <text x="360" y="433" font-size="22" fill="var(--green-deep)">(1/3)</text>
        <rect x="505" y="380" width="160" height="60" rx="9" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3.5"/>
        <text x="585" y="411" font-size="25" fill="var(--green-deep)" font-weight="800">바꾸면 승</text>
        <text x="585" y="433" font-size="22" fill="var(--green-deep)">(1/3)</text>
      </g>
      <!-- 결론 -->
      <rect x="150" y="495" width="420" height="66" rx="12" fill="var(--green)" />
      <text x="360" y="538" font-size="31" fill="#ffffff" font-weight="800" text-anchor="middle">바꾸기 승리 = 1/3 + 1/3 = 2/3</text>
    </svg>
  </div>
  <div class="caption">가지를 따라가면, 바꿔서 이기는 경우가 세 갈래 중 두 갈래예요.</div>

  <p>조건부확률로 한 번 더 확인해 볼게요. 참가자가 1번을 골랐고 진행자가 3번(염소)을 열었다고 해요. 자동차가 1번이면 진행자가 3번을 열 확률은 $\dfrac{1}{2}$(2·3번 중 선택), 자동차가 2번이면 3번을 열 확률은 1(3번밖에 못 염), 자동차가 3번이면 0이에요. 베이즈 정리로 묶으면 이렇게 나와요.</p>

  <div class="eq" data-export="png" data-name="eq-02">
    $$P(\text{차2}\mid\text{염3})=\frac{1\cdot\frac{1}{3}}{\frac{1}{2}\cdot\frac{1}{3}+1\cdot\frac{1}{3}}=\frac{\frac{1}{3}}{\frac{1}{2}}=\frac{2}{3}$$
  </div>
  <div class="caption">바꿔서 가는 2번 문의 확률이 2/3 — 손으로 센 값과 정확히 같아요.</div>

  <p>손으로 세는 방법과 조건부확률이 같은 답을 주죠. 세특에서는 이렇게 <strong>두 방법으로 같은 결론에 닿는 과정</strong>을 보여 주는 게 강점이 돼요.</p>

  <h2>숨은 전제 — 진행자가 '몰랐다면' 결과가 뒤집혀요</h2>
  <p>이제 앞에서 못 박은 규칙이 왜 중요한지 보여 줄게요. 만약 진행자가 자동차 위치를 <strong>모르고</strong>, 남은 두 문 중 하나를 <strong>무작위로</strong> 연다고 해 볼게요. 그러면 가끔 자동차가 있는 문을 열어 버려서 게임 자체가 성립하지 않아요. 그런 경우를 빼고 <strong>염소가 열린 경우만</strong> 모아서 따지면, 바꾸기와 그대로 두기가 <strong>각각 $\dfrac{1}{2}$</strong>로 수렴해요. 이때는 정말로 50:50이에요.</p>
  <p>무엇이 달라졌을까요? 문의 개수가 아니라 <strong>진행자가 가진 정보</strong>예요. 진행자가 답을 알고 일부러 염소 문을 열면, 그 행동이 '안 고른 쪽에 대한 정보'를 흘려서 확률이 한 문에 쏠려요. 반대로 아무것도 모르고 열면 새 정보가 없어서 반반이 돼요. "남은 문 2개는 반반"이라는 직관은 <strong>무작위로 여는 진행자</strong>에서만 맞는 말이었던 거예요.</p>

  <div class="fig" data-export="png" data-name="fig-03">
    <svg viewBox="0 0 720 470" width="720" height="470" aria-label="아는 진행자일 때 바꾸기 2/3 대 무작위 진행자일 때 바꾸기 1/2 비교">
      <!-- 패널 A : 아는 진행자 -->
      <text x="40" y="55" font-size="29" fill="var(--green-deep)" font-weight="800">진행자가 알고 염소 문을 열 때</text>
      <rect x="40" y="80" width="640" height="56" rx="8" fill="#f0efe9"/>
      <rect x="40" y="80" width="427" height="56" rx="8" fill="var(--green)"/>
      <text x="253" y="117" font-size="28" fill="#ffffff" font-weight="800" text-anchor="middle">바꾸기 2/3</text>
      <text x="573" y="117" font-size="27" fill="var(--ink-soft)" font-weight="700" text-anchor="middle">그대로 1/3</text>
      <text x="40" y="178" font-size="26" fill="var(--ink)">→ 바꾸는 쪽이 2배 유리해요.</text>
      <!-- 구분선 -->
      <line x1="40" y1="222" x2="680" y2="222" stroke="var(--ink-soft)" stroke-width="1.5" stroke-dasharray="6 6"/>
      <!-- 패널 B : 무작위 진행자 -->
      <text x="40" y="283" font-size="29" fill="var(--amber)" font-weight="800">진행자가 모르고 무작위로 열 때</text>
      <text x="40" y="314" font-size="23" fill="var(--ink-soft)">(염소가 열린 경우만 모았을 때)</text>
      <rect x="40" y="330" width="640" height="56" rx="8" fill="#f0efe9"/>
      <rect x="40" y="330" width="320" height="56" rx="8" fill="var(--amber)"/>
      <line x1="360" y1="330" x2="360" y2="386" stroke="#ffffff" stroke-width="3"/>
      <text x="200" y="367" font-size="28" fill="#ffffff" font-weight="800" text-anchor="middle">바꾸기 1/2</text>
      <text x="520" y="367" font-size="27" fill="var(--ink)" font-weight="700" text-anchor="middle">그대로 1/2</text>
      <text x="40" y="428" font-size="26" fill="var(--ink)">→ 이때는 바꿔도 이득이 없어요.</text>
    </svg>
  </div>
  <div class="caption">똑같이 문이 둘 남아도, 진행자의 규칙에 따라 승률이 달라져요.</div>

  <h2>세특에 쓸 때 — 결론만 베끼면 티 나는 이유</h2>
  <p>세특 평가에서 아쉬운 경우는 대개 비슷해요. "바꾸면 2/3이라 신기하다"로 끝나거나, 유명한 결과를 소개만 하고 자기 계산이 없는 글이에요. 결과는 검색하면 다 나오니까, 읽는 사람은 <strong>학생이 직접 한 게 무엇인지</strong>를 봐요. 고등학교 확률과 통계에서 배운 조건부확률을 실제로 굴려 보는 소재로 몬티홀만 한 게 드문데, 그만큼 '소개'가 아니라 '탐구'로 써야 값을 해요. 깊이를 더하고 싶다면 이 순서를 권해요.</p>
  <ul>
    <li><strong>① 손계산:</strong> 경우의 수나 나무그림으로 바꾸기 2/3을 직접 세요.</li>
    <li><strong>② 시뮬레이션:</strong> 프로그램(예: 파이썬)으로 수천 번 돌려 2/3에 가까워지는지 검증해요.</li>
    <li><strong>③ 베이즈 재유도:</strong> 같은 결론을 베이즈 정리로 다시 이끌어내 봐요.</li>
    <li><strong>④ 실생활 확장:</strong> 질병 검사에서 양성이 나와도 실제 환자일 확률이 생각보다 낮은 '기저율' 이야기와 연결하면, 조건부확률이라는 한 줄기로 묶여요.</li>
  </ul>
  <p>흔한 실수 세 가지도 미리 알려 둘게요. 첫째, <strong>진행자 규칙을 안 적는 것</strong>. 규칙을 생략하면 왜 2/3인지 설명이 공중에 떠요(이 글의 '숨은 전제'가 그래서 중요해요). 둘째, <strong>"문이 둘이니 반반"을 검증 없이 쓰는 것</strong>. 셋째, <strong>결론을 먼저 써 두고 끼워 맞추는 것</strong> — 과정이 결론을 끌고 가야지, 결론이 과정을 끌면 티가 나요.</p>

  <h2>3줄 정리</h2>
  <ul>
    <li>몬티홀은 결과(바꾸면 $\dfrac{2}{3}$)보다 <strong>직접 세어 보이는 과정</strong>이 중요해요 — 경우의 수와 조건부확률로 같은 답에 닿아 보세요.</li>
    <li>"남은 문 2개=반반"은 <strong>진행자가 무작위로 열 때만</strong> 맞아요. 진행자가 알고 열면 확률이 한 문에 몰려요.</li>
    <li>세특에 쓸 땐 손계산 → 시뮬레이션 → 베이즈 → 실생활 확장의 <strong>나만의 과정</strong>을 남기세요. 결론 복붙은 금방 티가 나요.</li>
  </ul>
