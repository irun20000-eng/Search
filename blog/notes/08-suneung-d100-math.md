<!-- 표지 — templates/fluor 가 렌더한 새 표지. 여기서 다시 내보내지 않는다.
       (옛 .thumb 섹션에는 data-export 가 붙어 있어 재렌더 시 새 표지를 덮어썼다.) -->
  <img class="cover" src="assets/08-suneung-d100-math/thumb.png" alt="표지" width="800" height="800">


  <h1>수능 D-100 수학, 버릴 단원 잡을 단원 고르기</h1>
  <p class="lead">D-100이 되면 많은 학생이 같은 계산을 해요. "100일이면 전 범위를 한 번 더 돌 수 있겠지."<br>
  그런데 현장에서 보면 그 계획은 대개 10월 초에 멈춰요. 남은 100일은 '새로 채우는 시간'이 아니라 <strong>'이미 배운 걸 점수로 바꾸는 시간'</strong>이라서, 전 단원을 똑같은 힘으로 다시 도는 방식과는 맞지 않아요.<br>
  그래서 마무리의 핵심은 진도가 아니라 판단이에요. 무엇을 버리고 무엇을 잡을지, 그 기준을 감이 아니라 숫자로 세우는 방법을 정리해 볼게요.</p>

  <h2>왜 '전 단원 다시'가 실패하나 — D-100의 진짜 함정</h2>
  <p>100일은 생각보다 짧아요. 참고로 2027학년도 수능은 <strong>2026년 11월 19일(목)</strong>이고, D-100은 8월 11일 무렵이에요. 그 사이엔 <strong>9월 2일(수) 모의평가</strong>와 수시 원서 기간이 끼어 있어서, 온전히 수학에만 쓰는 날은 더 줄어요.</p>
  <p>그래서 100일을 '한 덩어리'로 보지 말고 세 구간으로 나눠서 봐요. 앞 구간은 <strong>선택과 집중</strong>(버릴·잡을 단원을 정하고 잡을 것에 힘을 싣기), 가운데는 <strong>실전과 오답</strong>(시간 재고 풀고 틀린 걸 회귀시키기), 마지막은 <strong>정리와 컨디션</strong>(새 문제보다 손에 익은 걸 유지)이에요. 지금 어느 구간인지만 알아도 오늘 할 일의 성격이 달라져요.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <!-- 세로 타임라인. 구간 길이가 정보이므로 블록 높이로 기간 비율을 유지한다
         (22일:50일:28일 ≒ 112:212:132). viewBox 폭 720 = 본문 가용폭이라 배율 1.0. -->
    <svg viewBox="0 0 720 646" width="720" height="646" aria-label="100일을 선택과집중 22일, 실전과오답 50일, 정리와컨디션 28일 세 구간으로 나눈 세로 타임라인. 9월 2일 모의평가가 첫 구간 끝에 온다">
      <text x="0" y="30" font-size="24" fill="var(--ink-soft)" font-weight="700">D-100 · 8월 11일</text>

      <!-- 1구간 22일 -->
      <rect x="0" y="48" width="720" height="112" rx="16" fill="var(--green-deep)"/>
      <text x="30" y="100" font-size="34" fill="#ffffff" font-weight="800">선택과 집중</text>
      <text x="30" y="136" font-size="24" fill="rgba(255,255,255,.75)">버릴 단원·잡을 단원을 정해요</text>
      <text x="690" y="100" font-size="26" fill="rgba(255,255,255,.6)" text-anchor="end" font-weight="700">22일</text>

      <!-- 9월 모평은 1구간이 끝나는 자리 -->
      <text x="0" y="196" font-size="24" fill="var(--amber)" font-weight="700">9월 2일 모의평가</text>
      <line x1="0" y1="210" x2="720" y2="210" stroke="var(--amber)" stroke-width="3" stroke-dasharray="9 7"/>

      <!-- 2구간 50일 -->
      <rect x="0" y="228" width="720" height="212" rx="16" fill="var(--green)"/>
      <text x="30" y="280" font-size="34" fill="#ffffff" font-weight="800">실전과 오답</text>
      <text x="30" y="316" font-size="24" fill="rgba(255,255,255,.82)">시간 재고 풀고, 틀린 걸 회귀시켜요</text>
      <text x="690" y="280" font-size="26" fill="rgba(255,255,255,.62)" text-anchor="end" font-weight="700">50일</text>
      <text x="30" y="396" font-size="24" fill="rgba(255,255,255,.82)">가장 긴 구간이에요</text>

      <!-- 3구간 28일 -->
      <rect x="0" y="452" width="720" height="132" rx="16" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <text x="30" y="504" font-size="34" fill="var(--green-deep)" font-weight="800">정리 · 컨디션</text>
      <text x="30" y="540" font-size="24" fill="var(--ink-soft)">새 문제보다 손에 익은 걸 유지해요</text>
      <text x="690" y="504" font-size="26" fill="var(--green)" text-anchor="end" font-weight="700">28일</text>

      <text x="720" y="624" font-size="24" fill="var(--ink-soft)" font-weight="700" text-anchor="end">수능 11월 19일</text>
    </svg>
  
  </div>
  <div class="caption">100일을 세 구간으로 나누면, 지금은 새로 채울 때가 아니라 '고를 때'라는 게 보여요.</div>

  <p>'전 단원 다시'가 위험한 건 게을러서가 아니라, 이미 되는 단원에까지 똑같은 시간을 쓰느라 정작 오를 여지가 큰 단원을 놓치기 때문이에요. 마무리 국면에선 '다 하는 것'보다 <strong>'고르는 것'</strong>이 점수를 만들어요.</p>

  <h2>버릴 단원·잡을 단원을 가르는 한 가지 기준</h2>
  <p>그럼 무엇을 잡아야 할까요. 두 가지를 곱해서 봐요. 하나는 그 단원이 시험에서 차지하는 <strong>배점 비중</strong>, 다른 하나는 지금부터 남은 기간에 <strong>정답률을 얼마나 올릴 수 있는가</strong>(상승 여지)예요. 이 둘을 곱한 값을 '기대 회복 점수'라고 부를게요.</p>

  <div class="eq" data-export="png" data-name="eq-01">
    $$\text{기대 회복 점수} = (\text{배점 비중}) \times (\text{도달 가능 정답률} - \text{현재 정답률})$$
    <p style="text-align:center; margin:10px 0 0;">예시(가상 값) — 단원 A: $12 \times (0.8 - 0.4) = 4.8$점 &nbsp;·&nbsp; 단원 B: $8 \times (0.9 - 0.75) = 1.2$점</p>
  
  </div>
  <div class="caption">배점이 커도 이미 잘 맞히면 오를 여지가 작고, 여지가 커도 배점이 작으면 회수가 적어요. 둘을 곱해서 봐요.</div>

  <p>배점만 보면 둘 다 해야 할 것 같지만, 회복 여지를 곱하면 A(4.8점)가 B(1.2점)보다 네 배 커요. 이미 0.75를 맞히는 B는 '버린다'기보다 <strong>유지만</strong> 하고, 남는 힘을 A에 싣는 게 마무리의 선택과 집중이에요. (위 숫자는 이해를 돕기 위한 예시일 뿐, 실제 통계가 아니에요.)</p>

  <h2>시간이 없을수록 '시간당 회복 점수'로 다시 본다</h2>
  <p>그런데 D-100엔 변수가 하나 더 있어요. 바로 <strong>드는 시간</strong>이에요. 회복 점수가 커도 그 단원을 끌어올리는 데 시간이 너무 많이 들면, 남은 100일에선 손해일 수 있어요. 그래서 기대 회복 점수를 필요한 시간으로 한 번 더 나눠 봐요.</p>

  <div class="eq" data-export="png" data-name="eq-02">
    $$\text{시간당 회복 점수} = \frac{\text{기대 회복 점수}}{\text{필요 학습 시간}}$$
    <p style="text-align:center; margin:10px 0 0;">예시 — 단원 A: $4.8 \div 12 = 0.4$ &nbsp;·&nbsp; 단원 C: $3.0 \div 4 = 0.75$ &nbsp;(단위: 점/시간)</p>
  
  </div>
  <div class="caption">남은 시간이 적을수록, 총점보다 '시간당 회수'가 우선순위를 결정해요.</div>

  <p>단원 A는 4.8점을 얻는 데 12시간이 든다면 시간당 0.4점이에요. 반면 단원 C가 3.0점을 4시간이면 올릴 수 있다면 시간당 0.75점이 돼요. 총점은 A가 크지만, 시간이 정말 부족하다면 <strong>C를 먼저</strong> 잡는 게 효율적이에요. 남은 날이 많을 땐 총점으로, 정말 촉박할 땐 시간당으로 본다 — 이 두 렌즈면 대부분의 우선순위가 정해져요.</p>

  <h2>성적대·목표별 버릴·잡을 기준표</h2>
  <p>같은 수식이라도 내 위치에 따라 답이 달라져요. 현장에서 자주 쓰는 기준을 성적대별로 정리하면 이래요.</p>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>구분</th><th>집중해서 잡을 것</th><th>유지만 할 것</th><th>지금은 미룰 것</th></tr>
      <tr><td><strong>안정 상위권</strong></td><td>최고난도 1~2유형 정확도, 실수 봉쇄</td><td>잘 되는 중·기본 유형</td><td>거의 안 나오는 지엽·과한 확장</td></tr>
      <tr><td><strong>중위권</strong></td><td>배점 크고 여지 큰 중간 난도</td><td>이미 되는 기본 유형</td><td>아직 안 풀리는 최고난도</td></tr>
      <tr><td><strong>기초 회복</strong></td><td>자주 나오는 기본·중간 유형 정답률</td><td>맞히는 기본 유형</td><td>지금 못 푸는 최고난도(과감히 뒤로)</td></tr>
    </table>
  
  </div>
  <div class="caption">목표가 다르면 같은 단원도 잡을 것과 버릴 것이 바뀌어요. 내 줄에서 시작해요.</div>

  <p>여기서 '버린다'는 건 영원히가 아니라, <strong>지금 이 100일에선 우선순위를 뒤로 둔다</strong>는 뜻이에요. 안 되는 걸 붙잡고 시간을 다 쓰는 대신, 오를 여지가 큰 곳에 힘을 몰아주는 거예요.</p>

  <h2>실전 감각은 '매일 조금씩' 유지한다</h2>
  <p>단원을 골랐으면 실전 감각은 따로 챙겨요. 다만 매일 한 세트를 통째로 다 풀 필요는 없어요. 감각은 양보다 <strong>주기</strong>로 유지돼요. 시간을 재고 앞부분만 푸는 '미니 세트', 특정 배점대만 골라 푸는 '부분 세트'로도 실전 리듬은 살아요. 오히려 매일 전 세트를 풀면 채점·오답에 쓸 시간이 사라져요.</p>
  <p>그리고 9월 2일 모평은 '한 번 더 보는 시험'이 아니라 <strong>리허설</strong>로 써요. 시험 순서대로 시간을 배분해 보고, 어디서 시간이 부족했는지·어떤 실수가 반복되는지를 기록하면, 그게 남은 두 달의 우선순위 표를 갱신해 줘요.</p>

  <h2>오답은 버리지 말고 '회귀'시킨다</h2>
  <p>마무리에서 점수를 가장 확실히 올리는 건 새 문제가 아니라 오답이에요. 그런데 오답노트를 '쓰기만' 하면 다시 틀려요. 핵심은 틀린 문제를 <strong>간격을 두고 다시 만나게</strong> 하는 거예요.</p>

  <div class="fig" data-export="png" data-name="fig-02">
    <!-- 세로형. viewBox 폭을 본문 가용폭(720)과 같게 두면 배율이 1.0 이라
         라벨 34px 이 모바일(배율 .43)에서도 14.6px 로 본문 글자와 대등하다. -->
    <svg viewBox="0 0 720 610" width="720" height="610" aria-label="오답 회귀 루프: 틀림에서 원인 분류, 간격 재출제, 판정으로 이어지고 틀리면 다시 돌아오는 순환 다이어그램">
      <!-- ① 틀림 -->
      <rect x="0" y="12" width="560" height="118" rx="18" fill="var(--green-deep)"/>
      <circle cx="58" cy="71" r="30" fill="rgba(255,255,255,.18)"/>
      <text x="58" y="82" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="800">1</text>
      <text x="112" y="63" font-size="34" fill="#ffffff" font-weight="800">틀림</text>
      <text x="112" y="101" font-size="24" fill="rgba(255,255,255,.75)">틀린 문제에 표시만 해둬요</text>
      <!-- ② 원인 분류 -->
      <rect x="0" y="168" width="560" height="118" rx="18" fill="var(--green)"/>
      <circle cx="58" cy="227" r="30" fill="rgba(255,255,255,.2)"/>
      <text x="58" y="238" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="800">2</text>
      <text x="112" y="219" font-size="34" fill="#ffffff" font-weight="800">원인 분류</text>
      <text x="112" y="257" font-size="24" fill="rgba(255,255,255,.82)">개념 · 실수 · 시간 셋 중 하나로</text>
      <!-- ③ 간격 재출제 -->
      <rect x="0" y="324" width="560" height="118" rx="18" fill="var(--green)"/>
      <circle cx="58" cy="383" r="30" fill="rgba(255,255,255,.2)"/>
      <text x="58" y="394" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="800">3</text>
      <text x="112" y="375" font-size="34" fill="#ffffff" font-weight="800">간격 재출제</text>
      <text x="112" y="413" font-size="24" fill="rgba(255,255,255,.82)">3일 뒤 · 7일 뒤로 예약</text>
      <!-- ④ 판정 (결과라 밝게) -->
      <rect x="0" y="480" width="560" height="118" rx="18" fill="var(--green-soft)" stroke="var(--green)" stroke-width="3"/>
      <circle cx="58" cy="539" r="30" fill="var(--green)"/>
      <text x="58" y="550" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="800">4</text>
      <text x="112" y="531" font-size="34" fill="var(--green-deep)" font-weight="800">판정</text>
      <text x="112" y="569" font-size="24" fill="var(--ink-soft)">맞으면 졸업, 틀리면 다시</text>
      <!-- 단계 사이 화살표 -->
      <g stroke="var(--green)" stroke-width="4" fill="var(--green)">
        <path d="M 58 130 V 160"/><polygon points="58,168 49,152 67,152"/>
        <path d="M 58 286 V 316"/><polygon points="58,324 49,308 67,308"/>
        <path d="M 58 442 V 472"/><polygon points="58,480 49,464 67,464"/>
      </g>
      <!-- 회귀: 판정에서 원인 분류로 되돌아감 -->
      <path d="M 560 539 C 672 539, 672 227, 560 227" fill="none"
            stroke="var(--amber)" stroke-width="4" stroke-dasharray="9 7"/>
      <polygon points="560,227 576,218 576,236" fill="var(--amber)"/>
      <text x="640" y="372" font-size="24" fill="var(--amber)" font-weight="700" text-anchor="middle">맞을</text>
      <text x="640" y="402" font-size="24" fill="var(--amber)" font-weight="700" text-anchor="middle">때까지</text>
    </svg>
  
  </div>
  <div class="caption">오답노트의 목적은 기록이 아니라 '다시 만나기'예요. 맞을 때까지 간격을 두고 회귀시켜요.</div>

  <p>틀린 이유를 개념·실수·시간 셋 중 하나로 분류하는 것부터 시작해요. 개념이면 그 개념만 다시, 실수면 같은 유형을 며칠 뒤 다시, 시간이면 시간을 재고 다시 풀어요. 그리고 3일 뒤·7일 뒤에 그 문제를 <strong>예약 재출제</strong>해서 맞으면 졸업, 또 틀리면 루프를 한 번 더 돌려요. 이렇게 회귀시킨 오답은 시험장에서 '봤던 문제'가 돼요.</p>

  <h2>3줄 정리</h2>
  <div class="box">
    <p style="margin:0 0 8px;">• 남은 100일은 채우는 시간이 아니라 <strong>고르는 시간</strong> — 전 단원 다시 대신 선택과 집중이에요.</p>
    <p style="margin:0 0 8px;">• 잡을 단원은 <strong>기대 회복 점수(배점 × 상승 여지)</strong>로, 촉박하면 <strong>시간당 회복 점수</strong>로 다시 정렬해요.</p>
    <p style="margin:0;">• 실전 감각은 미니·부분 세트로 매일 조금씩, 오답은 간격을 두고 <strong>회귀</strong>시켜 시험장에서 다시 만나요.</p>
  </div>

  <p>100일은 무언가를 새로 완성하기엔 짧지만, 이미 가진 것을 점수로 바꾸기엔 충분한 시간이에요. 다 하려다 지치지 말고, 오늘 내 표에서 '잡을 한 단원'부터 골라 보세요. 마무리는 거기서 시작돼요.</p>
