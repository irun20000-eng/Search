<!-- 표지 — templates/fluor 가 렌더한 새 표지. 여기서 다시 내보내지 않는다. -->
  <img class="cover" src="assets/09-ai-error-notes/thumb.png" alt="표지" width="800" height="800">

  <h1>챗GPT 오답노트 정리, 교사가 시키는 프롬프트 3가지</h1>
  <p class="lead">9월 모의고사는 끝났어요. 채점도 했고 등급도 나왔죠. 그런데 정작 제일 중요한 오답노트 앞에서 손이 멈춰요. 틀린 문제를 다시 보긴 봐야 하는데, 어디서부터 왜 틀렸는지 정리하는 게 막막하거든요. 그래서 요즘은 챗GPT에게 도움을 받는 학생이 많아요. 오늘은 오답노트를 AI로 정리하는 순서를 프롬프트(AI에게 주는 지시문) 세 가지로 정리해 볼게요. 그리고 현장에서 학생들에게 꼭 함께 시키는, AI 답을 검증하는 습관까지요.</p>

  <h2>먼저 짚을 것 — 생성형 AI는 '정답지'가 아니에요</h2>
  <p>프롬프트를 보기 전에 딱 하나만 짚고 갈게요. 우리가 쓰는 생성형 AI(챗GPT·클로드·제미나이처럼 글을 만들어 주는 AI)는 <strong>다음에 올 그럴듯한 말을 이어 붙이는</strong> 도구예요. 계산기처럼 정확히 계산하거나 해설지처럼 검증된 답을 꺼내 오는 게 아니라, '말이 되게 이어지는 문장'을 만드는 거죠.</p>
  <p>그래서 생성형 AI는 <strong>틀린 답도 아주 자신 있게</strong> 말해요. 실제로 "무료 버전에 산수 문제를 물었더니 다 틀린 답을 정답처럼 알려줬다", "같은 수학 문제인데 물어볼 때마다 답이 달랐다"는 학생 후기가 흔해요. 중요한 건 이게 챗GPT만의 문제가 아니라 글을 지어내는 생성형 AI 전반의 특성이라는 점이에요. 그러니 오답노트에 AI를 쓰더라도, AI는 '정리를 도와주는 조교'지 '정답지'가 아니라는 선을 먼저 그어 두는 게 좋아요.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <svg viewBox="0 0 720 420" width="720" height="420" aria-label="생성형 AI 가 다음에 올 단어를 확률로 이어 붙이는 원리">
      <text x="0" y="34" font-size="30" fill="var(--ink)" font-weight="800">AI 는 ‘다음 단어’를 확률로 이어 붙여요</text>
      <rect x="0" y="60" width="720" height="96" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="112" font-size="30" fill="var(--ink)" font-weight="700">“이차함수의 최댓값은 &#160;&#160;___ ”</text>
      <text x="28" y="146" font-size="22" fill="var(--ink-soft)">빈칸 뒤에 올 말을 ‘확률’로 고른다</text>
      <rect x="0" y="176" width="230" height="120" rx="14" fill="#ffffff" stroke="var(--green)" stroke-width="3"/>
      <text x="24" y="222" font-size="30" fill="var(--green-deep)" font-weight="800">“ 8 ”</text>
      <text x="24" y="264" font-size="26" fill="var(--green)" font-weight="700">63%</text>
      <rect x="246" y="176" width="230" height="120" rx="14" fill="#ffffff" stroke="var(--line)" stroke-width="2"/>
      <text x="270" y="222" font-size="30" fill="var(--ink)" font-weight="700">“ 12 ”</text>
      <text x="270" y="264" font-size="26" fill="var(--ink-soft)" font-weight="700">21%</text>
      <rect x="492" y="176" width="228" height="120" rx="14" fill="#ffffff" stroke="var(--line)" stroke-width="2"/>
      <text x="516" y="222" font-size="30" fill="var(--ink)" font-weight="700">“ 없다 ”</text>
      <text x="516" y="264" font-size="26" fill="var(--ink-soft)" font-weight="700">9%</text>
      <rect x="0" y="320" width="720" height="86" rx="16" fill="#fdeee0" stroke="var(--amber)" stroke-width="3"/>
      <text x="28" y="356" font-size="24" fill="var(--ink)" font-weight="700">가장 확률 높은 말을 고를 뿐,</text>
      <text x="28" y="390" font-size="24" fill="var(--amber)" font-weight="800">틀린 값도 자신 있게 고를 수 있어요.</text>
    </svg>
  </div>
  <div class="caption">AI는 사실을 '찾는' 게 아니라 그럴듯한 다음 말을 '잇는' 도구라, 자신 있게 틀리기도 해요.</div>

  <h2>오답이유 → 정답근거 → 보완포인트, 프롬프트 3가지</h2>
  <p>좋은 오답노트는 '틀린 문제를 옮겨 적은 노트'가 아니라 '왜 틀렸고 다음엔 어떻게 막을지'를 적은 노트예요. 그 뼈대가 바로 <strong>오답이유 → 정답근거 → 보완포인트</strong> 세 단계예요. 이 순서를 그대로 프롬프트 세 개로 나눠 물으면, AI가 오답노트의 칸을 하나씩 채워 줘요. 틀린 문제 하나를 예로 이렇게 물어보면 돼요.</p>
  <p>먼저 <strong>오답이유</strong>. 내 풀이를 그대로 보여 주고 어디서 어긋났는지 짚게 해요.</p>
  <blockquote>"이 문제를 내가 이렇게 풀었는데 틀렸어. (내 풀이 붙여넣기) 어디서부터, 왜 틀렸는지 단계별로 짚어 주고, 틀린 이유가 개념 오해·계산 실수·조건 놓침·시간 부족 중 무엇에 가까운지 한 줄로 분류해 줘."</blockquote>
  <p>다음은 <strong>정답근거</strong>. 정답이 왜 그 답인지, 어떤 개념·공식을 쓰는지 논리를 받아요.</p>
  <blockquote>"이 문제의 정답이 왜 이 답인지, 사용된 개념과 공식을 순서대로 설명해 줘. 각 단계가 어떤 근거로 넘어가는지, 그리고 교과서 어느 단원 개념인지도 알려 줘."</blockquote>
  <p>마지막은 <strong>보완포인트</strong>. 약점을 한 줄로 압축하고, 내가 스스로 확인할 변형문제를 만들어요.</p>
  <blockquote>"위 풀이에서 내가 약한 부분을 한 문장으로 정리해 줘. 그리고 같은 개념을 쓰는 확인문제를 숫자만 바꿔 2개 만들어 줘. 답은 바로 알려주지 말고 내가 먼저 풀게 해 줘."</blockquote>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>단계</th><th>이런 지시를 준다</th><th>얻는 것</th></tr>
      <tr><td><strong>① 오답이유</strong></td><td>내 풀이를 붙여넣고, 어디서 왜 틀렸는지 단계별로 + 원인 유형 분류</td><td>틀린 지점과 원인 유형</td></tr>
      <tr><td><strong>② 정답근거</strong></td><td>정답의 개념·공식·근거를 순서대로 + 교과서 단원</td><td>정답의 논리 사슬</td></tr>
      <tr><td><strong>③ 보완포인트</strong></td><td>약점 한 줄 + 숫자 바꾼 확인문제 2개(답은 나중에)</td><td>약점 요약과 자가 점검 문제</td></tr>
    </table>
  </div>
  <div class="caption">세 프롬프트가 각각 오답노트의 '왜 틀렸나·왜 이게 답인가·다음엔 어떻게'를 채워 줘요.</div>

  <p>세 번째 프롬프트에서 "답은 바로 알려주지 말고"를 꼭 붙이세요. 이 한 줄이 AI를 정답기에서 조교로 되돌려요. 변형문제를 스스로 풀 수 있으면 이해한 거고, 막히면 아직 베낀 거예요.</p>

  <div class="fig" data-export="png" data-name="fig-02">
    <svg viewBox="0 0 720 470" width="720" height="470" aria-label="오답노트의 뼈대인 오답이유 정답근거 보완포인트 세 단 흐름">
      <text x="0" y="32" font-size="28" fill="var(--ink)" font-weight="800">오답노트의 뼈대 — 세 단</text>
      <rect x="0" y="52" width="720" height="106" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="98" font-size="32" fill="var(--green-deep)" font-weight="800">① 오답이유</text>
      <text x="28" y="136" font-size="24" fill="var(--ink-soft)">내가 왜 틀렸나</text>
      <text x="700" y="112" font-size="24" fill="var(--ink)" font-weight="700" text-anchor="end">→ 틀린 지점·원인 유형</text>
      <text x="360" y="182" font-size="26" fill="var(--green)" font-weight="800" text-anchor="middle">▼</text>
      <rect x="0" y="196" width="720" height="106" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="242" font-size="32" fill="var(--green-deep)" font-weight="800">② 정답근거</text>
      <text x="28" y="280" font-size="24" fill="var(--ink-soft)">왜 이게 답인가</text>
      <text x="700" y="256" font-size="24" fill="var(--ink)" font-weight="700" text-anchor="end">→ 정답의 논리 사슬</text>
      <text x="360" y="326" font-size="26" fill="var(--green)" font-weight="800" text-anchor="middle">▼</text>
      <rect x="0" y="340" width="720" height="106" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="28" y="386" font-size="32" fill="var(--green-deep)" font-weight="800">③ 보완포인트</text>
      <text x="28" y="424" font-size="24" fill="var(--ink-soft)">다음엔 어떻게 막나</text>
      <text x="700" y="400" font-size="24" fill="var(--ink)" font-weight="700" text-anchor="end">→ 약점 요약·확인문제</text>
    </svg>
  </div>
  <div class="caption">오답노트의 뼈대는 이 세 단이에요. 프롬프트도 이 순서대로 나눠 물어요.</div>

  <h2>교사라면 반드시 시키는 것 — AI 답 검증 체크리스트</h2>
  <p>여기가 이 글의 진짜 핵심이에요. 앞에서 말했듯 생성형 AI는 자신 있게 틀려요. 그런데 오답노트는 '틀린 걸 바로잡는' 노트라, AI가 낸 설명이 틀렸는데 그대로 옮겨 적으면 <strong>틀린 걸 틀린 채로 외우는</strong> 최악이 돼요.</p>
  <p>실제로 AI를 아무 조건 없이 쥐여 주면, 연습문제는 술술 풀려 점수가 오르는 것처럼 보여도 정작 시험에서는 그 이득이 잘 남지 않는다는 지적이 여러 곳에서 나와요. AI가 대신 풀어 주니 '아는 것 같은 착각'만 남기 쉬운 거죠. 반대로 답을 바로 주는 대신 스스로 확인하게 이끌면, 같은 도구라도 실력에 남는 게 달라져요. 정리하면 — <strong>잘 다루면 도움이 되지만, 사람이 검증하는 단계를 빼면 안 된다</strong>는 거예요.</p>
  <p>그래서 현장에서는 AI 답을 오답노트에 옮기기 전에 이 네 가지를 확인하게 해요.</p>

  <div class="fig" data-export="png" data-name="fig-03">
    <svg viewBox="0 0 720 560" width="720" height="560" aria-label="AI 답을 오답노트에 옮기기 전 확인하는 검증 체크리스트 네 칸">
      <text x="0" y="32" font-size="28" fill="var(--ink)" font-weight="800">옮기기 전, 검증 4칸</text>
      <rect x="0" y="52" width="720" height="92" rx="14" fill="#ffffff" stroke="var(--green)" stroke-width="3"/>
      <rect x="26" y="80" width="36" height="36" rx="6" fill="none" stroke="var(--green)" stroke-width="3"/>
      <text x="84" y="98" font-size="26" fill="var(--ink)" font-weight="700">① 해설지·교과서의 정답과</text>
      <text x="84" y="130" font-size="26" fill="var(--ink)" font-weight="700">&#160;&#160;&#160;AI 가 말한 답이 같은가</text>
      <rect x="0" y="156" width="720" height="92" rx="14" fill="#ffffff" stroke="var(--green)" stroke-width="3"/>
      <rect x="26" y="184" width="36" height="36" rx="6" fill="none" stroke="var(--green)" stroke-width="3"/>
      <text x="84" y="202" font-size="26" fill="var(--ink)" font-weight="700">② AI 가 쓴 계산을 내가</text>
      <text x="84" y="234" font-size="26" fill="var(--ink)" font-weight="700">&#160;&#160;&#160;직접 한 번 다시 해봤는가</text>
      <rect x="0" y="260" width="720" height="92" rx="14" fill="#ffffff" stroke="var(--green)" stroke-width="3"/>
      <rect x="26" y="288" width="36" height="36" rx="6" fill="none" stroke="var(--green)" stroke-width="3"/>
      <text x="84" y="306" font-size="26" fill="var(--ink)" font-weight="700">③ 쓴 공식·정의가 교과서</text>
      <text x="84" y="338" font-size="26" fill="var(--ink)" font-weight="700">&#160;&#160;&#160;표기와 일치하는가</text>
      <rect x="0" y="364" width="720" height="92" rx="14" fill="#ffffff" stroke="var(--green)" stroke-width="3"/>
      <rect x="26" y="392" width="36" height="36" rx="6" fill="none" stroke="var(--green)" stroke-width="3"/>
      <text x="84" y="410" font-size="26" fill="var(--ink)" font-weight="700">④ 같은 질문을 한 번 더 물어도</text>
      <text x="84" y="442" font-size="26" fill="var(--ink)" font-weight="700">&#160;&#160;&#160;답이 흔들리지 않는가</text>
      <rect x="0" y="476" width="720" height="72" rx="14" fill="#fdeee0" stroke="var(--amber)" stroke-width="3"/>
      <text x="360" y="520" font-size="27" fill="var(--amber)" font-weight="800" text-anchor="middle">넷 중 하나라도 걸리면 옮기지 않기</text>
    </svg>
  </div>
  <div class="caption">이 네 칸을 통과한 설명만 오답노트에 옮겨요. 특히 ④는 AI 답이 오락가락하는지 잡아 줘요.</div>

  <p>포인트는 부모님이나 선생님이 문제를 직접 못 풀어도 검증을 도울 수 있다는 거예요. "해설지랑 같아?", "숫자 바꾼 문제도 혼자 풀려?", "한 번 더 물으면 답이 같아?" 이 세 마디면 충분해요. AI는 오답노트를 빨리 채워 주는 조교일 뿐, 맞는지 판정하는 건 해설지와 교과서, 그리고 학생 자신이에요.</p>

  <h2>오답노트는 AI가 대신 못 써요</h2>
  <p>정리할게요. 챗GPT는 오답노트를 '더 빨리, 더 구조적으로' 정리하게 도와줘요. 하지만 '대신' 써 주지는 못해요. 틀린 이유를 내 손으로 분류하고, AI 설명을 해설지와 대조하고, 변형문제를 스스로 푸는 그 과정에서 실력이 남으니까요.</p>

  <div class="box">
    <p><strong>3줄 정리</strong></p>
    <ul>
      <li>오답노트는 오답이유 → 정답근거 → 보완포인트 3단이 뼈대예요. 프롬프트도 이 순서로 나눠 물어요.</li>
      <li>생성형 AI는 자신 있게 틀려요(챗GPT만이 아니라 클로드·제미나이도요). 그래서 해설지·교과서와 대조하는 검증 4칸이 필수예요.</li>
      <li>AI는 정리를 돕는 조교, 정답을 판정하는 건 해설지·교과서와 학생 자신이에요.</li>
    </ul>
  </div>

  <p>AI가 낸 답이 맞는지 학생 스스로 검증하는 더 구체적인 방법은 지난 글 '챗GPT 수학 오류 검증'에서, 선생님이 수업 자료를 만드는 프롬프트는 '교사 챗GPT 수업자료 3가지'에서 따로 다뤘어요. 오늘 글은 그 사이, 시험이 끝난 뒤 틀린 문제를 다루는 이야기였어요. 도구를 막기보다 잘 쓰는 법을 익히는 게, 결국 다음 시험에 남는답니다.</p>
