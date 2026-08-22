<!-- 썸네일 (800×800 PNG) — AI 필라: 회로·노드 모티프 -->
  <!-- 표지 — templates/fluor 가 렌더한 새 표지. 여기서 다시 내보내지 않는다.
       (옛 .thumb 섹션에는 data-export 가 붙어 있어 재렌더 시 새 표지를 덮어썼다.) -->
  <img class="cover" src="assets/07-ai-teaching-materials/thumb.png" alt="표지" width="800" height="800">


  <h1>교사의 챗GPT 수업자료, 그대로 쓰면 안 되는 3가지</h1>
  <p class="lead">"이 단원 설명자료랑 PPT 초안 만들어 줘." 요청 한 줄이면 3분 만에 그럴듯한 자료가 나와요. 그런데 그 매끄러움이 오히려 함정이에요. 문제가 있어도 겉보기엔 완성본처럼 보이거든요.</p>

  <p>수업자료를 AI로 만드는 일이 흔해졌어요. 설명자료, PPT 초안, 서술형·수행평가 문항, 학습지 텍스트까지요. 오늘은 '만드는 법'이 아니라, 그렇게 나온 자료를 <strong>그대로 쓰면 안 되는 이유 세 가지</strong>와 프린트·업로드 전 교사가 3분 안에 거르는 법을 정리해 볼게요.</p>

  <h2>AI가 준 건 '완성 자료'가 아니라 '초안'이에요</h2>
  <p>먼저 관점부터 하나 바꿔야 해요. 우리가 쓰는 생성형 AI(챗GPT·클로드 같은, 글을 만들어 주는 AI)는 <strong>다음에 올 그럴듯한 문장을 예측</strong>해서 이어 붙이는 도구예요. 그래서 결과물은 늘 '매끄럽게 읽히는 초안'이지, '검증된 완성 자료'가 아니에요.</p>
  <p>수학 문제의 계산이 틀리는 문제는 지난 글에서 따로 다뤘어요. 오늘 짚을 건 자료 <strong>'전체'</strong>예요. 설명 문장, 인용한 통계, 예시, 난이도, 출처까지 — 계산 말고도 어긋날 수 있는 곳이 훨씬 많거든요. 함정은 크게 세 갈래예요.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <svg viewBox="0 0 720 454" width="720" height="454" aria-label="AI 초안에서 교사 점검을 거쳐 완성 자료가 되는 3단계 개념도">
      <rect x="0" y="12" width="720" height="118" rx="18" fill="var(--green-deep)"/>
      <circle cx="58" cy="71" r="30" fill="rgba(255,255,255,.2)"/>
      <text x="58" y="82" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="800">1</text>
      <text x="112" y="63" font-size="34" fill="#ffffff" font-weight="800">AI 초안</text>
      <text x="112" y="101" font-size="24" fill="rgba(255,255,255,.8)">3분 만에 뚝딱 나와요</text>
      <path d="M 58 130 V 160" stroke="var(--green)" stroke-width="4"/>
      <polygon points="58,168 49,152 67,152" fill="var(--green)"/>
      <rect x="0" y="168" width="720" height="118" rx="18" fill="var(--green)"/>
      <circle cx="58" cy="227" r="30" fill="rgba(255,255,255,.2)"/>
      <text x="58" y="238" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="800">2</text>
      <text x="112" y="219" font-size="34" fill="#ffffff" font-weight="800">교사 점검</text>
      <text x="112" y="257" font-size="24" fill="rgba(255,255,255,.8)">사실 · 편향 · 저작권 — 여기서 신뢰가 갈려요</text>
      <path d="M 58 286 V 316" stroke="var(--green)" stroke-width="4"/>
      <polygon points="58,324 49,308 67,308" fill="var(--green)"/>
      <rect x="0" y="324" width="720" height="118" rx="18" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <circle cx="58" cy="383" r="30" fill="var(--green)"/>
      <text x="58" y="394" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="800">3</text>
      <text x="112" y="375" font-size="34" fill="var(--green-deep)" font-weight="800">완성 자료</text>
      <text x="112" y="413" font-size="24" fill="var(--ink-soft)">배포해도 안심할 수 있어요</text>
    </svg>
  
  </div>
  <div class="caption">AI는 초안까지, '완성 자료'로 만드는 건 교사의 점검이에요.</div>

  <h2>함정 ① 사실·출처 오류 — 그럴듯한 가짜</h2>
  <p>가장 자주 마주치는 함정이에요. 생성형 AI는 <strong>없는 사실을 아주 자연스럽게 지어내기도</strong> 해요. 이걸 '환각(할루시네이션)', 즉 그럴듯하게 지어낸 오답이라고 불러요.</p>
  <p>수업자료에서는 이렇게 드러나요. 실제로 없는 통계 수치를 "○○년 조사에 따르면"처럼 붙여 놓거나, 실존 인물의 하지도 않은 말을 인용문으로 만들거나, 참고문헌으로 아예 존재하지 않는 책·논문을 적어 놓는 식이에요. 한 연구에서는 AI가 만든 인용 목록의 <strong>상당수가 실재하지 않는 출처</strong>였다는 보고도 있어요. 이건 챗GPT만의 문제가 아니라, 글을 지어내는 생성형 AI 전반에서 나타나는 경향이에요.</p>

  <div class="fig" data-export="png" data-name="fig-02">
    <svg viewBox="0 0 720 580" width="720" height="580" aria-label="사실과 출처 오류가 숨는 세 자리 — 수치, 참고문헌, 인용문">
      <text x="0" y="32" font-size="28" fill="var(--ink)" font-weight="800">가짜가 숨는 단골 자리</text>
      <rect x="0" y="56" width="720" height="154" rx="18" fill="#f6efe4" stroke="var(--amber)" stroke-width="3"/>
      <text x="30" y="106" font-size="34" fill="var(--ink)" font-weight="800">수치</text>
      <text x="30" y="148" font-size="24" fill="var(--amber)" font-weight="700">"73%가 그렇다고 응답"</text>
      <text x="30" y="186" font-size="24" fill="var(--ink-soft)" >어느 조사인지 밝히지 않아요</text>
      <rect x="0" y="236" width="720" height="154" rx="18" fill="#f6efe4" stroke="var(--amber)" stroke-width="3"/>
      <text x="30" y="286" font-size="34" fill="var(--ink)" font-weight="800">참고문헌</text>
      <text x="30" y="328" font-size="24" fill="var(--amber)" font-weight="700">"김○○(2019)" — 없는 책 제목</text>
      <text x="30" y="366" font-size="24" fill="var(--ink-soft)" >그럴듯한 서지가 만들어져요</text>
      <rect x="0" y="416" width="720" height="154" rx="18" fill="#f6efe4" stroke="var(--amber)" stroke-width="3"/>
      <text x="30" y="466" font-size="34" fill="var(--ink)" font-weight="800">인용문</text>
      <text x="30" y="508" font-size="24" fill="var(--amber)" font-weight="700">위인이 한 적 없는 "명언"</text>
      <text x="30" y="546" font-size="24" fill="var(--ink-soft)" >출처가 확인되지 않아요</text>
    </svg>
  
  </div>
  <div class="caption">숫자·인용·참고문헌 — 이 세 곳이 가짜가 숨는 단골 자리예요.</div>

  <p>잡는 법은 단순해요. 자료에 들어간 <strong>숫자·고유명사·인용문·참고문헌은 원 출처를 직접 확인하기 전까지 '미확인'으로</strong> 두는 거예요. 확인이 안 되면 빼거나, 교과서·공신력 있는 자료로 바꾸면 돼요. 특히 학생이 그대로 받아 적을 설명자료일수록 이 확인이 중요해요.</p>

  <h2>함정 ② 편향·수준 불일치 — 누구의 관점, 누구의 눈높이</h2>
  <p>두 번째는 눈에 잘 안 띄어서 더 까다로워요. 사실 오류는 아닌데, <strong>'치우쳐 있거나' '우리 반에 안 맞는'</strong> 경우예요.</p>
  <p>편향은 관점이 한쪽으로 쏠리는 걸 말해요. 학습 데이터가 특정 문화·다수자 관점에 치우쳐 있어서, 예시나 인물, 설명의 무게중심이 은근히 한쪽으로 기울 때가 있어요. 수준 불일치는 눈높이 문제예요. AI는 우리 반 학생들의 배경지식을 모르니까, 초등 자료인데 대학 용어가 섞이거나 반대로 고등 자료가 너무 얕게 나오기도 해요. 번역투 문장이 그대로 남는 것도 여기에 속해요.</p>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>축</th><th>이렇게 드러나요</th><th>이렇게 점검해요</th></tr>
      <tr><td><strong>관점 편향</strong></td><td>예시·인물이 한쪽으로 쏠림</td><td>"다른 관점·사례도 넣을 수 있나?"</td></tr>
      <tr><td><strong>수준 불일치</strong></td><td>학년에 비해 어렵거나 얕음</td><td>"우리 반 학생이 읽고 바로 이해할까?"</td></tr>
      <tr><td><strong>표현·문화</strong></td><td>번역투·낯선 사례</td><td>"학생에게 익숙한 맥락으로 바꿨나?"</td></tr>
    </table>
  
  </div>
  <div class="caption">사실은 맞아도 '치우침'과 '눈높이'는 따로 봐야 해요.</div>

  <p>점검 질문은 딱 두 개예요. <strong>"이 자료는 누구의 관점으로 쓰였나?"</strong> 그리고 <strong>"우리 반 학생이 이대로 읽고 이해할까?"</strong> 이 둘만 물어도 대부분 걸러져요. AI가 만든 자료는 '평균적인 학생'을 상상하고 쓴 거라, 우리 교실에 맞추는 일은 결국 교사 몫이에요.</p>

  <h2>함정 ③ 저작권·표절 — 책임은 결국 교사에게</h2>
  <p>세 번째는 법률 자문은 아니고, 알아 두면 사고를 피하는 <strong>'안전 습관'</strong> 이야기예요. 저작권은 나라·서비스 약관마다 다르고 아직 정리 중인 영역이라, 여기서는 원칙과 조심할 지점만 짚을게요.</p>
  <p>교사가 특히 주의할 경로는 세 가지예요. 첫째, 저작권이 있는 지문·삽화·문항을 프롬프트에 통째로 넣고 "이거 변형해 줘"라고 하는 경우예요. 원저작물을 바탕으로 한 2차 창작이라 다툼의 소지가 생길 수 있어요. 둘째, AI가 출처 없이 가져온 문장·이미지가 자료에 섞이는 경우예요. 원문을 그대로 옮긴 표절이 될 수 있는데, AI는 출처를 잘 안 밝혀요. 셋째, 무엇보다 이 자료로 생긴 문제의 <strong>책임은 AI가 아니라 자료를 배포한 교사</strong>에게 돌아온다는 점이에요.</p>

  <div class="fig" data-export="png" data-name="fig-03">
    <svg viewBox="0 0 720 532" width="720" height="532" aria-label="저작권 위험 두 경로와 최종 책임은 배포한 교사에게 있다는 점">
      <rect x="0" y="8" width="720" height="154" rx="18" fill="#f6efe4" stroke="var(--amber)" stroke-width="3"/>
      <text x="30" y="58" font-size="34" fill="var(--ink)" font-weight="800">원저작물을 통째로</text>
      <text x="30" y="100" font-size="24" fill="var(--amber)" font-weight="700">"변형했다"고 해도</text>
      <text x="30" y="138" font-size="24" fill="var(--ink-soft)" >2차 창작 다툼의 소지가 있어요</text>
      <rect x="0" y="188" width="720" height="154" rx="18" fill="#f6efe4" stroke="var(--amber)" stroke-width="3"/>
      <text x="30" y="238" font-size="34" fill="var(--ink)" font-weight="800">출처 없이 옮긴 문장·이미지</text>
      <text x="30" y="280" font-size="24" fill="var(--amber)" font-weight="700">표절이 될 수 있어요</text>
      <text x="30" y="318" font-size="24" fill="var(--ink-soft)" >AI 는 출처를 잘 밝히지 않아요</text>
      <rect x="0" y="368" width="720" height="154" rx="18" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="30" y="418" font-size="34" fill="var(--green-deep)" font-weight="800">최종 책임은 배포한 교사</text>
      <text x="30" y="460" font-size="24" fill="var(--green)" font-weight="700">확인은 사람 몫이에요</text>
      <text x="30" y="498" font-size="24" fill="var(--ink-soft)" >프린트 전 3분이면 됩니다</text>
    </svg>
  
  </div>
  <div class="caption">AI는 출처를 잘 안 밝혀요. 최종 책임은 배포한 사람에게 남아요.</div>

  <p>안전 습관도 어렵지 않아요. <strong>저작권 자료는 프롬프트에 통째로 넣기보다 "이런 유형으로 새로" 만들게</strong> 하고, 인용·이미지는 출처를 직접 확인해 표기하고, 평가·배포용 자료일수록 원본성을 한 번 더 챙기는 거예요. 학교·교육청에 AI 활용 지침이 있다면 그 기준을 먼저 따르는 게 가장 안전해요.</p>

  <h2>프린트·업로드 전, 교사의 3분 점검표</h2>
  <p>세 함정을 한 번에 거르는 체크리스트예요. 자료를 내보내기 직전에 이 표만 훑어도 큰 사고는 막을 수 있어요.</p>

  <div data-export="png" data-name="table-02">
    <table>
      <tr><th>함정</th><th>확인할 것</th></tr>
      <tr><td><strong>사실·출처</strong></td><td>숫자·인용·참고문헌의 원 출처를 확인했다</td></tr>
      <tr><td><strong>편향</strong></td><td>관점이 한쪽으로 치우치지 않았다</td></tr>
      <tr><td><strong>수준</strong></td><td>우리 반 눈높이에 맞게 고쳤다</td></tr>
      <tr><td><strong>저작권</strong></td><td>남의 원문·이미지를 무단으로 쓰지 않았다</td></tr>
      <tr><td><strong>최종</strong></td><td>이대로 배포해도 내가 책임질 수 있다</td></tr>
    </table>
  
  </div>
  <div class="caption">내보내기 전 3분, 이 다섯 줄이 세 함정을 걸러 줘요.</div>

  <p>한 가지만 기억하면 돼요. AI가 만든 수업자료는 시간을 크게 아껴 주는 훌륭한 '초안'이에요. 하지만 그 초안을 <strong>'완성 자료'로 바꾸는 마지막 한 걸음</strong>, 즉 사실·관점·저작권을 확인하는 일은 교사만 할 수 있어요. 그 3분이 자료의 신뢰를 지켜 줘요.</p>

  <h2>3줄 정리</h2>
  <div class="box">
    <p style="margin:0 0 8px;">• 생성형 AI가 만든 수업자료는 '완성본'이 아니라 <strong>'초안'</strong>이에요. 매끄러워 보여도 세 곳이 어긋날 수 있어요.</p>
    <p style="margin:0 0 8px;">• 세 함정: ① 그럴듯한 가짜 사실·없는 출처 ② 관점 편향·눈높이 불일치 ③ 저작권·표절. <strong>책임은 배포한 교사</strong>에게 남아요.</p>
    <p style="margin:0;">• 프린트·업로드 전 <strong>3분 점검표</strong>로 사실·편향·수준·저작권·책임 다섯 줄만 확인하면 대부분 걸러져요.</p>
  </div>

  <p>수학 문제를 만들거나 풀 때 AI가 틀리는 순간은 앞선 두 글에서 다뤘어요. 자료를 만들 때든 문제를 낼 때든, <strong>AI 옆에는 늘 확인하는 교사</strong>가 필요하답니다.</p>
