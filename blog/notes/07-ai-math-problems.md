<!-- 썸네일 (800×800 PNG) — AI 필라: 회로·노드 모티프 -->
  

  <h1>챗GPT로 수학 문제 만들기 — 교사가 검증까지 하는 법</h1>
  <p class="lead">챗GPT에게 "이 단원 연습문제 10개 만들어줘" 하면 3초 만에 뚝딱 나와요. 그런데 그걸 그대로 프린트해서 나눠줬다가, 답이 틀린 걸 학생이 먼저 발견하는 순간이 옵니다.</p>

  <p>AI로 문제를 만드는 건 정말 쉬워요. 어려운 건 그다음, <strong>"이 문제가 쓸 만한지 걸러내는 일"</strong>이에요. 오늘은 만드는 프롬프트부터 교사의 눈으로 검증하는 절차까지, 실제로 쓸 수 있는 순서로 정리해 볼게요.</p>

  <h2>AI는 계산하지 않아요, '예측'할 뿐이에요</h2>
  <p>먼저 이걸 알아야 왜 검증이 필요한지 납득이 돼요. 우리가 쓰는 생성형 AI(챗GPT·클로드 같은, 글을 만들어 주는 AI)는 사실 <strong>계산기가 아니에요.</strong> 다음에 올 글자를 확률로 예측하는 도구예요.</p>
  <p>그래서 이건 챗GPT만의 얘기가 아니에요. 클로드·제미나이처럼 글을 만들어 주는 AI는 원리가 같아서, 문제를 만들 때도 답·조건이 어긋날 수 있어요.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <svg viewBox="0 0 820 300" width="740" height="271" aria-label="계산기와 생성형 AI의 차이 개념도">
      <!-- 계산기 -->
      <rect x="20" y="40" width="360" height="220" rx="16" fill="#eaf1fd" stroke="#2563eb" stroke-width="2"/>
      <text x="200" y="82" text-anchor="middle" font-size="26" font-weight="800" fill="#16233a">계산기</text>
      <text x="200" y="140" text-anchor="middle" font-size="34" font-weight="800" fill="#16233a">3 + 8</text>
      <text x="200" y="180" text-anchor="middle" font-size="18" fill="#51647e">규칙대로 계산</text>
      <text x="200" y="228" text-anchor="middle" font-size="34" font-weight="800" fill="#2563eb">= 11 (항상)</text>
      <!-- 생성형 AI -->
      <rect x="440" y="40" width="360" height="220" rx="16" fill="#0b1220" stroke="#2563eb" stroke-width="2"/>
      <text x="620" y="82" text-anchor="middle" font-size="26" font-weight="800" fill="#e8eef7">생성형 AI</text>
      <text x="620" y="140" text-anchor="middle" font-size="34" font-weight="800" fill="#e8eef7">3 + 8</text>
      <text x="620" y="180" text-anchor="middle" font-size="18" fill="#93c5fd">'그럴듯한 다음 글자' 예측</text>
      <text x="620" y="228" text-anchor="middle" font-size="30" font-weight="800" fill="#7cc0ff">≈ 11 (가끔 딴 값)</text>
    </svg>
    <div class="caption">AI는 규칙으로 '계산'하는 게 아니라 학습한 패턴으로 '예측'해요.</div>
  </div>

  <p>숫자도 AI에게는 그냥 글자 하나예요. 그래서 자릿수가 길어지거나 계산이 여러 단계면, 중간에 한 글자만 어긋나도 뒤가 전부 틀어져요. 사람은 문장에서 오타 하나쯤은 뜻이 통하지만, 숫자는 한 자리만 달라도 답이 완전히 달라지죠. <strong>"언어를 잘하도록 만들어진 도구에 계산을 시키고 있다"</strong> — 이게 AI가 수학에서 자주 실수하는 이유예요.</p>

  <p>예를 들어 "이차방정식 $x^2-5x+6=0$의 해를 구하는 문제와 답을 만들어 줘"라고 하면, 풀이는 인수분해 과정을 그럴듯하게 써 놓고 답을 "$x=2$ 또는 $x=4$"라고 적어 놓는 식이에요. (바른 답은 $2$와 $3$이죠.) 풀이가 매끄러워서 얼핏 보면 넘어가기 쉬운데, 실제로 이런 어긋남이 답 부분에서 자주 나와요. 그러니 문제를 만들 때도 답과 조건을 <strong>사람이 다시 확인</strong>해야 해요.</p>

  <div class="box warn">
    <p style="margin:0;">오해는 마세요. AI가 쓸모없다는 얘기가 아니에요. 빈 종이에서 시작하는 것보다 <strong>초안을 빠르게 뽑아 주는 것</strong>은 분명한 강점이에요. 다만 그 초안을 "완성된 자료"로 착각하지 않는 것, 딱 거기서 갈려요.</p>
  </div>

  <h2>1단계 — 좋은 문제를 뽑는 프롬프트</h2>
  <p>무작정 챗GPT에 "문제 만들어줘"라고 하면 난이도도 제각각이고 원하는 유형도 안 나와요. <strong>원본 문제 하나를 예시로 붙여 주고, 조건을 구체적으로 지정</strong>하는 게 핵심이에요. 아래를 복사해서 대괄호만 바꿔 쓰세요.</p>

  <div class="prompt" data-export="png" data-name="fig-02">
<pre>아래 예시 문제와 같은 유형의 변형 문제를 만들어 줘.

<span class="tag">[예시 문제 붙여넣기]</span>

조건:
- 단원: <span class="tag">[예: 고1 이차함수]</span>
- 난이도: [기본 / 응용 / 심화] 중 <span class="tag">[기본]</span> 수준으로
- 개수: 5문항
- 숫자만 바꾸지 말고 상황·조건도 바꿔서 유형이 겹치지 않게
- 각 문항 아래에 '풀이'와 '정답'을 따로 표시
- 정답은 한 번 더 계산해서 검산 결과도 같이 적어 줘</pre>
    <div class="caption">복사해서 대괄호만 바꿔 쓰는 문제 생성 프롬프트예요.</div>
  </div>

  <p>마지막 두 줄이 중요해요. <strong>풀이·정답을 분리</strong>하게 하고, <strong>검산까지 시키면</strong> 나중에 확인하기가 훨씬 쉬워져요. 그래도 "검산했다"는 말을 그대로 믿으면 안 돼요. 어디까지나 다음 단계가 남아 있어요.</p>

  <p>한 번에 완벽한 세트가 안 나와도 괜찮아요. "3번 문항 난이도를 한 단계 낮춰 줘", "2번은 조건이 부족해 보이니 다시" 처럼 <strong>대화하듯 고쳐 나가면</strong> 품질이 올라가요. 처음부터 10문항을 통째로 받기보다, <strong>3~5문항씩 끊어서</strong> 받고 그때그때 확인하는 편이 오히려 빠르고 정확해요.</p>

  <h2>2단계 — AI가 수학에서 틀리는 4가지</h2>
  <p>만들어진 문제를 훑을 때, 아무 데나 보는 게 아니라 <strong>잘 틀리는 자리</strong>만 집중해서 보면 빨라요. 현장에서 모아 보면 늘 이 네 곳에서 사고가 나요.</p>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>틀리는 유형</th><th>어떻게 드러나나</th><th>잡는 법</th></tr>
      <tr><td><strong>① 정답 오류</strong></td><td>풀이는 그럴듯한데 답 숫자가 틀림</td><td>직접 한 문제씩 검산</td></tr>
      <tr><td><strong>② 난이도 뒤섞임</strong></td><td>'기본'이라 했는데 심화가 섞임</td><td>첫 2문항 풀어 보고 기준 맞추기</td></tr>
      <tr><td><strong>③ 중복·유사</strong></td><td>숫자만 바뀐 사실상 같은 문제</td><td>유형이 겹치는지 나란히 비교</td></tr>
      <tr><td><strong>④ 조건 누락·모순</strong></td><td>답이 안 나오거나 여러 개</td><td>문제만 보고 풀리는지 확인</td></tr>
    </table>
    <div class="caption">네 곳만 봐도 대부분의 오류가 걸려요.</div>
  </div>

  <p>특히 ①정답 오류가 제일 위험해요. 풀이 과정은 매끄럽게 써 놓고 <strong>마지막 답 숫자만 틀리는</strong> 경우가 많거든요. 풀이가 그럴듯해 보인다고 답까지 맞다고 넘기면 안 되고, 짧은 문제라도 <strong>직접 손으로 한 번 풀어 보는 게</strong> 가장 확실해요. 시간이 없으면 계산이 복잡한 문항만이라도요.</p>

  <h2>프린트 전, 5줄 체크리스트</h2>
  <p>자료로 내보내기 직전에 이 다섯 줄만 지키면 큰 사고는 막을 수 있어요.</p>

  <div data-export="png" data-name="table-02">
    <table>
      <tr><th>#</th><th>프린트 전 확인</th></tr>
      <tr><td>1</td><td>정답을 직접 검산했는가 (최소한 계산이 복잡한 문항)</td></tr>
      <tr><td>2</td><td>난이도가 요청한 수준으로 고른가</td></tr>
      <tr><td>3</td><td>겹치는 문제는 없는가</td></tr>
      <tr><td>4</td><td>문제만으로 풀리는가 (조건 충분)</td></tr>
      <tr><td>5</td><td>학생 눈높이 표현인가 (불필요한 대학 용어·어색한 번역투 없는지)</td></tr>
    </table>
    <div class="caption">프린트 전 30초, 이 다섯 줄이 오답 배포를 막아요.</div>
  </div>

  <p>학부모님이 자녀의 AI 학습을 봐 주신다면, 딱 한 가지만 기억해 주세요. <strong>AI가 만든 문제와 답은 "초안"이지 "정답지"가 아니에요.</strong> 아이가 AI로 문제를 만들어 풀 때, 답이 이상하면 "AI가 틀렸을 수도 있다"고 함께 의심해 보는 것 — 그 태도 자체가 요즘 가장 중요한 공부예요.</p>

  <h2>3줄 정리</h2>
  <div class="box">
    <p style="margin:0 0 8px;">• 챗GPT 같은 생성형 AI는 계산기가 아니라 <strong>예측기</strong>라서, 수학 답·조건을 자주 틀려요. 그래서 <strong>만들기 다음에 검증</strong>이 반드시 붙어야 해요.</p>
    <p style="margin:0 0 8px;">• 만들 때는 <strong>원본 예시 + 구체 조건(단원·난이도·개수·유형·답지 분리·검산)</strong> 프롬프트로. 그래도 "검산했다"는 말은 믿지 말고요.</p>
    <p style="margin:0;">• 검증은 <strong>네 곳(정답·난이도·중복·조건)</strong> 집중 + <strong>프린트 전 5줄 체크리스트</strong>. 30초 투자로 오답 배포를 막아요.</p>
  </div>

  <p>다음 글에서는 오늘의 반대편, <strong>AI가 수학 문제를 '풀' 때 틀리는 순간들 — 그대로 믿으면 안 되는 이유</strong>를 실제 사례로 다뤄 볼게요. 만들 때든 풀 때든, AI 옆에는 늘 확인하는 사람이 필요하답니다.</p>
