<!-- 표지 — templates/fluor 가 렌더한 표지. 여기서 다시 내보내지 않는다. -->
  <img class="cover" src="assets/09-ai-domain-literacy/thumb.png" alt="표지" width="800" height="800">

  <h1>챗GPT 잘 쓰는 사람의 공통점, 프롬프트가 아닙니다</h1>
  <p class="lead">연수나 상담 자리에서 AI 이야기가 나오면 질문이 거의 하나로 모여요. "프롬프트(AI에게 주는 지시문)를 어떻게 써야 잘 나오나요?" 그런데 현장에서 여러 선생님·학부모님이 같은 챗GPT를 쓰는 걸 곁에서 보면, 결과를 가르는 건 지시문 솜씨가 아니었어요. 결론부터 말하면, AI를 잘 쓰는 사람은 결국 <strong>자기 분야를 아는 사람</strong>이었어요.</p>

  <h2>같은 챗GPT를 쓰는데 왜 결과가 다를까</h2>
  <p>두 분이 똑같이 "고1 이차함수 서술형 문항 5개 만들어 줘"라고 물었다고 해 볼게요. 나온 화면은 거의 똑같아요. 갈리는 건 그다음 3초예요.</p>
  <p>한 분은 훑어보고 "잘 나왔네" 하며 그대로 인쇄해요. 다른 한 분은 3번 문항에서 손이 멈춰요. "이 조건이면 답이 두 개인데?" "이건 고1 범위가 아니라 고2 내용인데?" 그 3초를 만든 건 프롬프트가 아니라 <strong>이차함수를 아는 눈</strong>이에요.</p>
  <p>이건 챗GPT만의 얘기가 아니에요. 클로드든 제미나이든, 우리가 쓰는 생성형 AI(글·그림을 만들어 주는 AI)는 다 같은 성질을 가지고 있어요. 그럴듯하게 잘 쓰지만, 그럴듯하게 틀리기도 해요. 그래서 마지막에 "이게 맞나?"를 판정하는 자리는 늘 사람에게 남아요.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <svg viewBox="0 0 720 636" width="720" height="636" aria-label="같은 지시문과 같은 답을 받은 두 사람이 검토 지점에서 갈리는 흐름도">
      <text x="0" y="32" font-size="28" fill="var(--ink)" font-weight="800">갈리는 건 입력이 아니라 ‘그다음 3초’</text>

      <rect x="0" y="54" width="720" height="88" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="94" font-size="26" fill="var(--ink-soft)" font-weight="700">같은 지시문</text>
      <text x="28" y="128" font-size="27" fill="var(--ink)" font-weight="700">“이차함수 서술형 5문항 만들어 줘”</text>

      <text x="360" y="170" font-size="26" fill="var(--green)" font-weight="800" text-anchor="middle">▼</text>

      <rect x="0" y="184" width="720" height="88" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="224" font-size="26" fill="var(--ink-soft)" font-weight="700">같은 답</text>
      <text x="28" y="258" font-size="27" fill="var(--ink)" font-weight="700">화면에는 매끄러운 문항 5개</text>

      <text x="360" y="300" font-size="26" fill="var(--amber)" font-weight="800" text-anchor="middle">▼ 여기서 갈려요</text>

      <rect x="0" y="318" width="720" height="130" rx="16" fill="#ffffff" stroke="var(--line)" stroke-width="3"/>
      <text x="28" y="360" font-size="27" fill="var(--ink-soft)" font-weight="800">A · 훑어보고 그대로 인쇄</text>
      <text x="28" y="398" font-size="25" fill="var(--ink-soft)">“잘 나왔네”</text>
      <text x="28" y="432" font-size="25" fill="var(--ink-soft)">→ 틀린 문항이 그대로 아이 손에</text>

      <rect x="0" y="464" width="720" height="160" rx="16" fill="#fdeee0" stroke="var(--amber)" stroke-width="3"/>
      <text x="28" y="506" font-size="27" fill="var(--ink)" font-weight="800">B · 3번에서 손이 멈춤</text>
      <text x="28" y="544" font-size="25" fill="var(--ink)">“이 조건이면 답이 두 개인데?”</text>
      <text x="28" y="578" font-size="25" fill="var(--ink)">“이건 고1 범위가 아닌데?”</text>
      <text x="28" y="612" font-size="25" fill="var(--amber)" font-weight="800">→ 고쳐서 쓸 수 있는 자료가 됨</text>
    </svg>
  </div>
  <div class="caption">같은 도구를 써도 결과가 갈리는 지점은 입력이 아니라, 나온 답을 검토하는 그 3초예요.</div>

  <h2>값이 싸진 것과, 값이 오른 것</h2>
  <p>예전에는 자료를 <strong>만드는 일 자체</strong>가 오래 걸렸어요. 학습지 초안 한 장, 가정통신문 한 장을 쓰는 데 저녁이 통째로 갔죠. 그래서 '잘 만드는 사람'이 곧 실력자였어요.</p>
  <p>지금은 그 일이 몇 초에 끝나요. 그러니까 값이 싸진 건 <strong>만들기</strong>예요. 대신 값이 오른 게 있어요. "이게 맞나? 뭐가 빠졌나? 우리 반 아이들한테 맞나?" — <strong>판단</strong>이에요.</p>
  <p>병목이 옮겨간 거예요. 만드는 게 병목이던 시절에는 만드는 능력이 대접받았고, 검토가 병목이 된 지금은 검토하는 능력이 대접받아요. 그런데 검토는 그냥 꼼꼼함이 아니에요. <strong>틀린 걸 틀렸다고 알아보려면 맞는 걸 알고 있어야</strong> 해요. 그 아는 것이 바로 내 분야의 지식이고요.</p>

  <div class="fig" data-export="png" data-name="fig-02">
    <svg viewBox="0 0 720 486" width="720" height="486" aria-label="만들기의 값은 내려가고 판단의 값은 올라간다는 대비도">
      <text x="0" y="32" font-size="28" fill="var(--ink)" font-weight="800">값이 싸진 것 · 값이 오른 것</text>

      <rect x="0" y="54" width="720" height="158" rx="16" fill="#ffffff" stroke="var(--line)" stroke-width="3"/>
      <text x="28" y="100" font-size="30" fill="var(--ink-soft)" font-weight="800">만들기 &#160;&#160;↓ 값이 싸짐</text>
      <text x="28" y="142" font-size="25" fill="var(--ink-soft)">학습지 초안 한 장 = 저녁 한 번</text>
      <text x="28" y="180" font-size="25" fill="var(--ink-soft)">→ 지금은 몇 초</text>

      <rect x="0" y="230" width="720" height="158" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="276" font-size="30" fill="var(--green-deep)" font-weight="800">판단 &#160;&#160;↑ 값이 오름</text>
      <text x="28" y="318" font-size="25" fill="var(--ink)">“이게 맞나? 뭐가 빠졌나?”</text>
      <text x="28" y="356" font-size="25" fill="var(--ink)">“우리 반 아이들한테 맞나?”</text>

      <rect x="0" y="404" width="720" height="78" rx="16" fill="#fdeee0" stroke="var(--amber)" stroke-width="3"/>
      <text x="360" y="452" font-size="27" fill="var(--amber)" font-weight="800" text-anchor="middle">틀린 걸 알아보려면 맞는 걸 알아야 해요</text>
    </svg>
  </div>
  <div class="caption">AI가 값싸게 만든 건 '생성'이고, 값이 오른 건 '판단'이에요.</div>

  <h2>곱셈으로 보면 분명해져요</h2>
  <p>이걸 곱셈으로 그려 보면 이해가 쉬워요. 더하기가 아니라 곱하기예요.</p>
  <p>내 분야의 전문성이 10이어도 AI를 전혀 안 쓰면, 같은 일을 하는 데 남보다 몇 배 시간이 들어요. 반대로 AI는 능숙한데 그 분야를 모르면, 그럴듯한 오답을 그대로 실행해요. 이 두 번째가 더 위험해요. 첫 번째는 느릴 뿐이지만, 두 번째는 <strong>틀린 걸 빠르게</strong> 하거든요.</p>
  <p>여기서 '도메인'은 어려운 말이 아니에요. 내가 오래 해 온 분야를 뜻해요. 수학 수업이든, 학급 운영이든, 아이의 공부 습관을 지켜본 시간이든요. 그 분야를 아는 힘 위에 AI를 얹는 걸 요즘은 <strong>도메인 리터러시</strong>라고 부르기도 해요. 흔히 말하는 <strong>AI 리터러시</strong>가 'AI를 어디까지 믿고 어떻게 쓸지 아는 능력'이라면, 도메인 리터러시는 거기에 '내 분야에서 무엇이 맞는 답인지 아는 눈'을 더한 셈이에요. 앞의 것만으로는 판정을 못 해요.</p>

  <div class="fig" data-export="png" data-name="fig-03">
    <svg viewBox="0 0 720 500" width="720" height="500" aria-label="전문성과 AI 역량의 곱셈 세 가지 경우">
      <text x="0" y="32" font-size="28" fill="var(--ink)" font-weight="800">더하기가 아니라 곱하기</text>

      <rect x="0" y="54" width="720" height="126" rx="16" fill="#ffffff" stroke="var(--line)" stroke-width="3"/>
      <text x="28" y="100" font-size="30" fill="var(--ink)" font-weight="800">전문성 10 &#160;×&#160; AI 0</text>
      <text x="28" y="140" font-size="27" fill="var(--ink-soft)" font-weight="700">= 느려요</text>
      <text x="28" y="172" font-size="24" fill="var(--ink-soft)">아는 건 많은데 같은 일에 몇 배 시간이 들어요</text>

      <rect x="0" y="198" width="720" height="126" rx="16" fill="#fdeee0" stroke="var(--amber)" stroke-width="3"/>
      <text x="28" y="244" font-size="30" fill="var(--ink)" font-weight="800">전문성 0 &#160;×&#160; AI 10</text>
      <text x="28" y="284" font-size="27" fill="var(--amber)" font-weight="800">= 위험해요</text>
      <text x="28" y="316" font-size="24" fill="var(--ink)">그럴듯한 오답을 ‘빠르게’ 실행해요</text>

      <rect x="0" y="342" width="720" height="146" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="390" font-size="30" fill="var(--green-deep)" font-weight="800">전문성 ○ &#160;×&#160; AI ○</text>
      <text x="28" y="430" font-size="27" fill="var(--green-deep)" font-weight="800">= 증폭돼요</text>
      <text x="28" y="464" font-size="24" fill="var(--ink)">아는 눈으로 걸러 내니 속도가 실력이 돼요</text>
    </svg>
  </div>
  <div class="caption">더하기가 아니라 곱하기예요 — 어느 한쪽이 0이면 결과도 0에 가까워져요.</div>

  <h2>왜 하필 '내 분야를 아는 것'이 열쇠일까</h2>
  <p>생성형 AI는 방대한 글에서 <strong>가장 그럴듯한 다음 말</strong>을 이어 붙이는 도구예요. 그래서 평균적인 답에는 강하지만, 평균을 넘는 정답과 평균처럼 보이는 오답을 스스로 가르지는 못해요. "교과서적으로는 맞는데 우리 학교 진도에서는 틀렸다" 같은 판별은 학습 데이터에 없거든요. 그건 현장에 있는 사람의 머릿속에만 있어요.</p>
  <p>이건 필자의 감상만은 아니에요. 교실 밖에서도 같은 이야기가 나오고 있거든요. 잠깐만 학교 담장 밖을 볼게요.</p>
  <p>2026년 경영학 학술지 <em>Management Science</em>에 실린 와튼스쿨 탐베(P. Tambe) 교수의 연구는, AI가 분야 전문성(도메인 전문성)을 대체하는 게 아니라 <strong>보완한다</strong>고 봤어요. 그러면서 AI 활용 능력이 전산 부서에만 몰려 있을 때보다 <strong>현업 전문가들에게 널리 퍼져 있을 때</strong> 조직이 AI에서 더 큰 가치를 얻는다는 걸 인력 데이터 두 종으로 보였어요.</p>
  <p>비슷한 흐름이 연구 현장에서도 보여요. 학술 논문을 미리 공개하는 사이트에 2026년 올라온 한 리뷰 연구는, AI를 쓰는 연구자에게 필요한 역량을 문헌 40편에서 8가지로 추려 냈어요. 그중 <strong>가장 자주 언급된 것이 '분야 전문성과 AI 결과에 대한 감독'</strong>이었고요. 주제를 제대로 알고, 체계적으로 의심하고, 출처를 확인하고, 결과에 책임지는 것 말이에요. 동료 심사를 거치기 전 공개본이라 확정된 결론으로 읽을 건 아니지만, 흐름을 보여 주기엔 충분해 보여요.</p>

  <h2>이 블로그의 AI 글 세 편이 사실 같은 말을 하고 있었어요</h2>
  <p>돌아보니 그동안 쓴 AI 글이 전부 이 이야기의 한 조각이었어요.</p>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>지난 글</th><th>무엇을 다뤘나</th><th>그때 필요했던 판단</th></tr>
      <tr><td><strong>챗GPT로 수학 문제 만들기</strong></td><td>AI가 만든 문항을 교사가 검증하는 절차</td><td>“이 조건이면 답이 두 개다”를 아는 눈</td></tr>
      <tr><td><strong>챗GPT 수학 오류 검증</strong></td><td>AI 답이 왜 틀리는지와 검증 3단계</td><td>풀이가 매끄러워도 답이 어긋난 걸 잡는 계산 감각</td></tr>
      <tr><td><strong>교사의 챗GPT 수업자료 3가지</strong></td><td>사실·편향·저작권 세 곳을 점검하는 법</td><td>무엇이 우리 반에 맞는 자료인지 아는 기준</td></tr>
    </table>
  </div>
  <div class="caption">세 편 모두 도구 사용법이 아니라 '나온 결과를 무엇으로 판정할 것인가'를 다루고 있었어요.</div>

  <p>세 편의 주제는 문항·풀이·수업자료로 서로 달랐지만, 실제로 하는 일은 같았어요. <strong>AI가 만든 것을 내 분야의 기준으로 되짚는 일.</strong> 그래서 검증 방법을 아무리 많이 외워도, 그 기준이 내 안에 없으면 검증은 형식으로만 남아요.</p>
  <p>책임의 자리도 마찬가지예요. 유네스코가 2024년에 낸 「교사를 위한 AI 역량 프레임워크」는 다섯 개 영역에 걸쳐 열다섯 가지 역량을 정리하면서, <strong>교육적 판단의 책임은 여전히 교사에게 남는다</strong>는 점을 분명히 해 뒀어요. AI를 썼다는 이유로 책임이 옮겨 가지는 않는다는 뜻이에요.</p>

  <h2>그래서 오늘부터 무엇을 하면 될까요</h2>
  <p>거창한 준비는 필요 없어요. 세 가지면 충분해요.</p>
  <p>첫째, <strong>검증을 습관으로 만드는 것</strong>이에요. AI 리터러시를 기르겠다고 강의부터 찾을 필요는 없어요. AI 답을 받으면 인쇄 버튼 대신 네 가지를 먼저 물어보는 걸로 충분해요. 출처가 실제로 있나 / 반대 사례는 없나 / 빠진 게 뭔가 / 우리 상황에 맞나. 이 네 줄을 화면 옆에 붙여 두는 것만으로도 달라져요.</p>
  <p>둘째, <strong>질문을 다듬는 시간을 아끼지 않는 것</strong>이에요. AI는 답하는 도구지 문제를 찾아 주는 도구가 아니에요. 무엇이 진짜 문제인지 정하는 건 여전히 사람 몫이라, 문제를 잘못 잡으면 엉뚱한 답을 아주 빠르게 받게 돼요.</p>
  <p>셋째, <strong>한 우물은 계속 파는 것</strong>이에요. AI로 학습 속도를 올리는 건 좋지만, 이해 자체를 AI에 넘기면 검증할 기준이 사라져요. 학생에게도 같은 말을 해 주면 좋겠어요. AI가 답을 주는 시대일수록, 그 답을 알아볼 수 있는 사람이 되라고요.</p>

  <h2>내 전문성은 쓸모없어지지 않아요</h2>
  <p>AI를 배우면서 가장 자주 듣는 불안이 "내가 쌓아 온 게 쓸모없어지는 것 아니냐"는 말이에요. 지금까지 살펴본 바로는 오히려 반대에 가까워요. 내가 아는 분야가 있다는 건, AI가 내놓은 답을 판정할 수 있다는 뜻이니까요. 그건 지금 AI를 쓰는 데 필요한 조건에 가깝고요.</p>

  <div class="box">
    <p><strong>3줄 정리</strong></p>
    <ul>
      <li>같은 챗GPT를 써도 결과가 갈리는 건 프롬프트 솜씨가 아니라, 나온 답을 검토하는 눈이에요.</li>
      <li>AI가 값싸게 만든 건 '생성'이고 값이 오른 건 '판단'이에요. 판단의 재료가 바로 내 분야의 지식이고요. (챗GPT만이 아니라 클로드·제미나이도 같아요.)</li>
      <li>전문성 × AI 역량은 곱셈이라 한쪽이 0이면 0이에요. 검증 습관 · 문제 정의 · 한 우물, 이 셋부터 시작하면 돼요.</li>
    </ul>
  </div>

  <p>그러니 프롬프트 문장을 더 찾아다니기 전에, 오늘 AI에게 받은 답 하나를 골라 내 분야의 눈으로 다시 읽어 보시길 권해요. 그 3초가 시작이에요.</p>
