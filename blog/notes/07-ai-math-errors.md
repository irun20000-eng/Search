<h1>챗GPT 수학 오류, AI 답 검증 3단계 — 그대로 믿으면 안 되는 이유</h1>
  <p class="lead">AI가 풀어준 수학 답, 그대로 베꼈다가 나중에 틀린 걸 알게 된 적 없나요? 풀이는 술술 매끄러운데 마지막 숫자만 어긋나 있는 경우가 생각보다 자주 있어요.</p>
  <p>AI가 왜 수학에서 자주 틀리는지(계산이 아니라 '예측'을 하기 때문)는 지난 글에서 자세히 다뤘어요. 오늘은 한 걸음 더 나가서, 그 답을 실제로 어떻게 걸러내고 AI를 어떻게 똑똑하게 쓰는지 — 학생·학부모 눈높이의 실전편이에요. (참고로 이건 챗GPT만이 아니라 클로드·제미나이 같은 생성형 AI 공통이에요.)</p>
  <p>핵심을 먼저 말하면 이래요. AI가 준 답은 '정답'이 아니라 <strong>'초안'</strong>으로 받고, 간단한 통과 검사를 거친 것만 믿는 거예요. 그 검사를 어떻게 하는지, 그리고 검사 다음에 AI를 어떻게 공부에 활용하는지를 순서대로 볼게요.</p>

  <h2>30초 실험 — "9.11과 9.9, 어느 게 클까?"</h2>
  <p>말보다 눈으로 보는 게 빨라요. AI에게 "9.11과 9.9 중 어느 게 더 커?"라고 물어보세요. "9.11이 더 크다"고 자신 있게 답하는 경우가 널리 알려져 있어요. 버전 번호처럼 인식해 버리는 거예요.</p>
  <p>바른 답은 9.9예요. 소수 둘째 자리까지 맞춰 9.90과 9.11로 비교하면 9.90이 크죠. 여기서 얻을 교훈은 하나예요. AI는 <strong>틀릴 때조차 아주 자신 있게</strong> 말한다는 것. 그러니 '그럴듯함'을 '정답'으로 착각하지 않는 게 실력의 시작이에요.</p>

  <div class="fig" data-export="png" data-name="fig-02">
    <svg viewBox="0 0 760 220" width="760" height="220" aria-label="수직선에서 9.9가 9.11보다 오른쪽(큼)">
      <line x1="60" y1="120" x2="710" y2="120" stroke="#16233a" stroke-width="3"/>
      <g font-family="Pretendard, sans-serif" font-size="18" fill="#51647e" text-anchor="middle">
        <line x1="60" y1="112" x2="60" y2="128" stroke="#16233a" stroke-width="3"/><text x="60" y="152">9.0</text>
        <line x1="385" y1="112" x2="385" y2="128" stroke="#16233a" stroke-width="3"/><text x="385" y="152">9.5</text>
        <line x1="710" y1="112" x2="710" y2="128" stroke="#16233a" stroke-width="3"/><text x="710" y="152">10.0</text>
      </g>
      <circle cx="131" cy="120" r="9" fill="#93c5fd" stroke="#2563eb" stroke-width="3"/>
      <text x="131" y="96" text-anchor="middle" font-family="Pretendard, sans-serif" font-size="22" font-weight="800" fill="#51647e">9.11</text>
      <circle cx="645" cy="120" r="11" fill="#2563eb"/>
      <text x="645" y="94" text-anchor="middle" font-family="Pretendard, sans-serif" font-size="24" font-weight="800" fill="#2563eb">9.9</text>
      <text x="645" y="188" text-anchor="middle" font-family="Pretendard, sans-serif" font-size="18" fill="#2563eb">= 9.90 · 더 큼</text>
    </svg>
    <div class="caption">9.9 = 9.90. 자리를 맞춰 보면 9.9가 더 크다는 게 한눈에 보여요.</div>
  </div>

  <p>이런 함정은 소수 비교에만 있는 게 아니에요. 자릿수가 긴 곱셈이나 여러 단계를 거치는 계산도 비슷하게 미끄러져요. 공통점은 '길고 복잡할수록 위험하다'는 거예요. 그래서 답을 걸러내는 나만의 절차가 필요해요.</p>

  <h2>AI 답, 이 3단계로 검증하세요</h2>
  <p>답을 그대로 믿는 대신, 30초짜리 루틴 하나만 몸에 붙이면 돼요. 순서대로 하면 됩니다.</p>
  <p><strong>1단계, 되묻기.</strong> 답이 나오면 "왜 그렇게 생각했어?"라고 근거를 설명하게 하세요. 어디서 어긋났는지 스스로 드러나는 경우가 많아요.</p>
  <p><strong>2단계, 계산은 코드로.</strong> 숫자 계산 자체는 AI의 <strong>코드 실행 기능</strong>(파이썬으로 직접 계산하게 하는 기능)이나 계산기에 맡기세요. "계산은 코드로 실제 실행해서 확인해 줘"라고 하면 숫자는 계산기가 맞춰 줘요.</p>
  <p><strong>3단계, 다른 방법으로 대조.</strong> "같은 문제를 다른 방법으로 한 번 더 풀어 줘"라고 시켜 두 답을 비교하세요. 같으면 신뢰가 올라가고, 다르면 둘 중 하나는 틀린 거니 바로 걸러낼 수 있어요.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <svg viewBox="0 0 760 250" width="760" height="250" aria-label="AI 답 검증 3단계 플로우">
      <g font-family="Pretendard, sans-serif">
        <rect x="8" y="60" width="220" height="150" rx="18" fill="#eaf1fd" stroke="#2563eb" stroke-width="2"/>
        <rect x="270" y="60" width="220" height="150" rx="18" fill="#f7faff" stroke="#d7e2f0"/>
        <rect x="532" y="60" width="220" height="150" rx="18" fill="#f7faff" stroke="#d7e2f0"/>
        <circle cx="48" cy="98" r="20" fill="#2563eb"/><text x="48" y="106" text-anchor="middle" font-size="24" font-weight="800" fill="#fff">1</text>
        <circle cx="310" cy="98" r="20" fill="#2563eb"/><text x="310" y="106" text-anchor="middle" font-size="24" font-weight="800" fill="#fff">2</text>
        <circle cx="572" cy="98" r="20" fill="#2563eb"/><text x="572" y="106" text-anchor="middle" font-size="24" font-weight="800" fill="#fff">3</text>
        <text x="88" y="105" font-size="27" font-weight="800" fill="#16233a">되묻기</text>
        <text x="350" y="105" font-size="27" font-weight="800" fill="#16233a">코드로 계산</text>
        <text x="612" y="105" font-size="27" font-weight="800" fill="#16233a">다른 방법</text>
        <text x="38" y="160" font-size="20" fill="#51647e">"왜 그렇게</text><text x="38" y="186" font-size="20" fill="#51647e">생각했어?"</text>
        <text x="300" y="160" font-size="20" fill="#51647e">숫자는 계산기</text><text x="300" y="186" font-size="20" fill="#51647e">·코드에 맡기기</text>
        <text x="562" y="160" font-size="20" fill="#51647e">다시 풀어</text><text x="562" y="186" font-size="20" fill="#51647e">두 답 대조</text>
        <text x="249" y="140" text-anchor="middle" font-size="34" fill="#2563eb">→</text>
        <text x="511" y="140" text-anchor="middle" font-size="34" fill="#2563eb">→</text>
      </g>
    </svg>
    <div class="caption">답을 믿기 전 30초. 이 세 단계만 거치면 대부분의 오답이 걸려요.</div>
  </div>

  <p>예를 들어 이차방정식이라면, 먼저 AI가 왜 그렇게 풀었는지 설명을 듣고, 나온 해를 원래 식에 다시 넣어 0이 되는지 확인하고, 인수분해 대신 근의 공식으로도 풀어 답이 같은지 보는 식이에요. 세 번 다 통과하면 그제야 믿어도 돼요. 손이 많이 가는 것 같지만, 익숙해지면 정말 30초면 끝나요.</p>

  <h2>AI는 '정답기'가 아니라 '과외선생님'</h2>
  <p>여기서 오해를 하나 풀어야 해요. AI가 수학에 쓸모없다는 얘기가 절대 아니에요. '정답을 뽑는 기계'로 믿는 게 문제일 뿐, '옆에서 설명해 주는 과외선생님'으로 쓰면 정말 강력해요.</p>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>마음껏 믿어도 되는 것</th><th>사람이 꼭 확인할 것</th></tr>
      <tr><td>개념을 쉬운 말로 설명</td><td><strong>최종 정답 숫자</strong></td></tr>
      <tr><td>내가 틀린 이유 짚기</td><td>긴 계산 결과</td></tr>
      <tr><td>다른 풀이 보여주기</td><td>"검산했다"는 말</td></tr>
      <tr><td>비슷한 문제 변형</td><td>문제의 조건·단위</td></tr>
    </table>
    <div class="caption">왼쪽은 마음껏 쓰고, 오른쪽만 사람이 확인하면 돼요.</div>
  </div>

  <p>포인트는 이거예요. AI에게 '정답'을 구걸하지 말고 '설명'을 요청하세요. "이 문제를 단계별로 이유까지 설명해 줘", "내가 어디서 틀렸는지 짚어 줘"처럼요. 답을 베끼는 게 아니라 이해가 남아요. 그게 진짜 공부고요.</p>
  <p>반대로 시험이 코앞이라 답만 급할 때도, 최소한 그 답 하나는 손으로 검산하고 넘어가세요. 급할수록 틀린 답을 그대로 외워 버리는 게 제일 위험하거든요.</p>

  <h2>AI로 공부할 때, 3가지 습관</h2>
  <p>특히 학생이 혼자 AI로 공부할 때, 이 세 가지만 지키면 '베끼는 공부'가 '느는 공부'로 바뀌어요. 처음엔 조금 번거로워도, 한두 주만 지나면 자연스러운 리듬이 돼요.</p>

  <div data-export="png" data-name="table-02">
    <table>
      <tr><th>#</th><th>AI로 공부할 때 3가지 습관</th></tr>
      <tr><td>1</td><td>답 말고 <strong>'과정'을 묻기</strong> (결과보다 풀이 이유)</td></tr>
      <tr><td>2</td><td>하루 한 문제는 <strong>손으로 직접 풀어</strong> AI 답과 대조</td></tr>
      <tr><td>3</td><td>"AI도 틀린다"를 전제로, <strong>이상하면 다시</strong> 물어보기</td></tr>
    </table>
    <div class="caption">AI를 답지가 아니라 연습 상대로 — 이 세 습관이 실력을 지켜요.</div>
  </div>

  <p>학부모님이 자녀의 AI 학습을 봐 주신다면 딱 한 가지만 기억해 주세요. "답이 이상하면 AI가 틀렸을 수도 있다"고 함께 의심해 보는 태도, 그 습관 자체가 요즘 가장 중요한 공부예요.</p>

  <h2>3줄 정리</h2>
  <p>AI는 틀릴 때조차 자신 있게 말해요. '그럴듯함'을 걸러내는 게 실력의 시작이에요. 검증은 3단계 — 되묻기, 계산은 코드로, 다른 방법으로 대조. AI는 정답기가 아니라 과외선생님이에요. 설명은 AI에게, 정답 확인은 내가.</p>
  <p>AI가 수학에서 왜 틀리는지, 그리고 AI로 문제를 '만들' 때 검증하는 법은 지난 글에서 이어 보실 수 있어요. 만들 때도 풀 때도, 마지막 한 걸음은 늘 사람의 확인이에요.</p>
