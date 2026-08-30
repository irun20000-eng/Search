<!-- 표지 — 원천의 thumb 섹션을 같은 그림의 img 로 바꾼 것 -->
  <img class="cover" src="assets/07-quadratic-max-min/thumb.png" alt="표지" width="800" height="800">


  <h1>이차함수 최댓값 최솟값, 그래프 한 장으로 끝내기 (고1)</h1>
  <p class="lead">"개념은 아는데, 범위가 붙으면 꼭 틀려요."<br>
  수학 상담을 하다 보면 이차함수 최대·최소에서 이 말을 정말 자주 들어요.<br>
  사실 이 단원, 외울 건 거의 없습니다. <strong>답이 될 수 있는 후보가 딱 두 곳뿐</strong>이라는 것만 알면 돼요. 오늘 그래프 한 장으로 정리해 볼게요.</p>

  <h2>포물선은 산 아니면 골짜기예요</h2>
  <p>이차함수 그래프(포물선)는 딱 두 가지 모양뿐이에요. 이차항 계수 $a$가 양수면 아래로 볼록한 <strong>골짜기</strong>, 음수면 위로 볼록한 <strong>산</strong>이죠.</p>

  <div class="fig" data-export="png" data-name="fig-01">
    <svg viewBox="0 0 800 330" width="740" height="305" aria-label="a가 양수인 골짜기 포물선과 a가 음수인 산 포물선">
      <!-- 왼쪽: a>0 골짜기 -->
      <path d="M 60 40 Q 200 480 340 40" fill="none" stroke="#2f6f4f" stroke-width="5"/>
      <circle cx="200" cy="270" r="9" fill="#2f6f4f"/>
      <text x="200" y="308" text-anchor="middle" font-size="22" fill="#1f2933" font-weight="700">최솟값</text>
      <text x="200" y="30" text-anchor="middle" font-size="24" fill="#52606d">a &gt; 0 (골짜기)</text>
      <!-- 오른쪽: a<0 산 -->
      <path d="M 460 280 Q 600 -160 740 280" fill="none" stroke="#b3542f" stroke-width="5"/>
      <circle cx="600" cy="60" r="9" fill="#b3542f"/>
      <text x="600" y="38" text-anchor="middle" font-size="22" fill="#1f2933" font-weight="700">최댓값</text>
      <text x="600" y="320" text-anchor="middle" font-size="24" fill="#52606d">a &lt; 0 (산)</text>
    </svg>
    <div class="caption">a&gt;0이면 골짜기 바닥(최솟값), a&lt;0이면 산꼭대기(최댓값)가 생겨요.</div>
  </div>

  <p>골짜기 바닥이 가장 낮은 곳, 산꼭대기가 가장 높은 곳. 그러니까 <strong>최댓값·최솟값 문제는 결국 꼭짓점 찾기 문제</strong>예요. 식만 보고도 "아, $a$가 음수니까 최댓값이 있겠구나"까지 판단되면 절반은 끝난 거예요.</p>

  <h2>1단계 — 표준형으로 바꾸기 (여기서 제일 많이 물어봐요)</h2>
  <p>꼭짓점을 바로 보여주는 꼴이 표준형 $y=a(x-p)^2+q$이고, 꼭짓점은 $(p,\,q)$예요. 문제는 대부분 일반형 $y=ax^2+bx+c$로 나오니까, 완전제곱식으로 바꾸는 과정이 필요해요. 지식iN에서도 "변형 과정을 모르겠다"는 질문이 유독 많이 보이는데, 한 단계도 건너뛰지 않고 보여드릴게요.</p>

  <div class="eq" data-export="png" data-name="eq-01">
    $$\begin{aligned} y &= x^2-4x+1 \\ &= (x^2-4x+4)-4+1 \\ &= (x-2)^2-3 \end{aligned}$$
    <p style="text-align:center; margin:10px 0 0;">검산: $x=2$ 대입 → $4-8+1=-3$ ✓</p>
    <div class="caption">이차항·일차항을 완전제곱으로 묶고, 더한 만큼(+4)을 반드시 빼 주는 게 핵심이에요.</div>
  </div>

  <p>여기서 시험 실수 1위가 나와요. <strong>더해 준 수를 다시 빼 주는 상수 보정을 빼먹는 것.</strong> 변형이 끝나면 꼭짓점 $x$값을 원래 식에 대입해서 검산하는 습관을 들이면 이 실수가 사라져요.</p>

  <h2>2단계 — 범위가 없을 때는 꼭짓점이 그대로 답</h2>
  <p>$x$에 아무 조건이 없다면 답은 꼭짓점에서 바로 나와요.</p>

  <div data-export="png" data-name="table-01">
    <table>
      <tr><th>$y=a(x-p)^2+q$</th><th>최솟값</th><th>최댓값</th></tr>
      <tr><td>$a&gt;0$ (골짜기)</td><td>$x=p$일 때 $q$</td><td><strong>없음</strong></td></tr>
      <tr><td>$a&lt;0$ (산)</td><td><strong>없음</strong></td><td>$x=p$일 때 $q$</td></tr>
    </table>
    <div class="caption">범위가 없으면 한쪽 값은 "존재하지 않는다"까지 답해야 해요.</div>
  </div>

  <p>주의할 점 하나. 골짜기($a&gt;0$)는 위로 끝없이 뻗으니까 <strong>최댓값이 "없다"</strong>가 정답이에요. "없음"도 답이 된다는 걸 처음 배울 때 많이 어색해하는데, 시험에서 그대로 물어봐요.</p>

  <h2>3단계 — 범위가 있을 때: 후보는 딱 두 곳뿐</h2>
  <p>이 글의 핵심이에요. $\alpha \le x \le \beta$처럼 범위가 주어지면, 최댓값·최솟값 후보는 <strong>① 꼭짓점(범위 안에 있을 때) ② 범위의 양 끝</strong> — 이 두 종류밖에 없어요. 포물선은 꼭짓점에서 방향을 딱 한 번 바꾸는 곡선이라, 그 사이에서 값이 가장 커지거나 작아지는 지점이 따로 생길 수 없거든요.</p>

  <div class="fig" data-export="png" data-name="fig-02">
    <svg viewBox="0 0 940 360" width="760" height="291" aria-label="꼭짓점이 범위 안, 왼쪽 밖, 오른쪽 밖인 세 가지 경우">
      <!-- 케이스 1: 꼭짓점 범위 안 (범위 100~240, 꼭짓점 150 포함) -->
      <g>
        <rect x="100" y="20" width="140" height="260" fill="#e8f2ec"/>
        <path d="M 20 60 Q 150 420 280 60" fill="none" stroke="#2f6f4f" stroke-width="4"/>
        <circle cx="150" cy="240" r="8" fill="#2f6f4f"/>
        <circle cx="100" cy="213" r="8" fill="#52606d"/>
        <circle cx="240" cy="154" r="8" fill="#b3542f"/>
        <text x="150" y="315" text-anchor="middle" font-size="22" fill="#1f2933" font-weight="700">① 꼭짓점이 범위 안</text>
        <text x="150" y="345" text-anchor="middle" font-size="19" fill="#52606d">최소=꼭짓점, 최대=끝점</text>
      </g>
      <!-- 케이스 2: 꼭짓점이 범위 왼쪽 밖 (범위 170~270, 꼭짓점 150 제외) -->
      <g transform="translate(320,0)">
        <rect x="170" y="20" width="100" height="260" fill="#e8f2ec"/>
        <path d="M 20 60 Q 150 420 280 60" fill="none" stroke="#2f6f4f" stroke-width="4"/>
        <circle cx="150" cy="240" r="7" fill="#d9e2ec" stroke="#52606d" stroke-width="2"/>
        <circle cx="170" cy="236" r="8" fill="#b3542f"/>
        <circle cx="270" cy="87" r="8" fill="#b3542f"/>
        <text x="195" y="315" text-anchor="middle" font-size="22" fill="#1f2933" font-weight="700">② 꼭짓점이 왼쪽 밖</text>
        <text x="195" y="345" text-anchor="middle" font-size="19" fill="#52606d">양 끝만 후보 (구간 증가)</text>
      </g>
      <!-- 케이스 3: 꼭짓점이 범위 오른쪽 밖 (범위 30~130, 꼭짓점 150 제외) -->
      <g transform="translate(640,0)">
        <rect x="30" y="20" width="100" height="260" fill="#e8f2ec"/>
        <path d="M 20 60 Q 150 420 280 60" fill="none" stroke="#2f6f4f" stroke-width="4"/>
        <circle cx="150" cy="240" r="7" fill="#d9e2ec" stroke="#52606d" stroke-width="2"/>
        <circle cx="30" cy="87" r="8" fill="#b3542f"/>
        <circle cx="130" cy="236" r="8" fill="#b3542f"/>
        <text x="105" y="315" text-anchor="middle" font-size="22" fill="#1f2933" font-weight="700">③ 꼭짓점이 오른쪽 밖</text>
        <text x="105" y="345" text-anchor="middle" font-size="19" fill="#52606d">양 끝만 후보 (구간 감소)</text>
      </g>
    </svg>
    <div class="caption">어떤 경우든 후보는 꼭짓점과 양 끝뿐 — 이 한 장이 이 단원의 전부예요.</div>
  </div>

  <p>그래서 풀이 순서는 항상 같아요. <strong>표준형으로 바꾸고 → 꼭짓점이 범위 안인지 확인하고 → 후보들(꼭짓점·양 끝)을 대입해 비교.</strong> 예제로 확인해 볼게요.</p>

  <div class="eq" data-export="png" data-name="eq-02">
    <p style="text-align:center; margin:0 0 6px; font-weight:700;">예제 1) $0 \le x \le 3$에서 $y=x^2-4x+1$</p>
    $$y=(x-2)^2-3,\quad \text{꼭짓점 } (2,\,-3) \; \rightarrow \; x=2 \text{는 범위 안}$$
    $$y(0)=1,\quad y(2)=-3,\quad y(3)=-2$$
    $$\therefore\ \text{최댓값 } 1\ (x=0),\quad \text{최솟값 } -3\ (x=2)$$
    <div class="caption">후보 세 점만 대입하면 끝 — 그래프를 다 그릴 필요도 없어요.</div>
  </div>

  <p>그럼 <strong>꼭짓점이 범위 밖</strong>이면 어떻게 될까요? 같은 함수로 범위만 바꿔 볼게요. $3 \le x \le 5$에서 $y=(x-2)^2-3$의 최대·최소를 구해 보면, 꼭짓점의 $x$값인 $2$가 범위 밖에 있죠. 이러면 후보에서 꼭짓점이 탈락하고 <strong>양 끝 두 점만 남아요.</strong></p>

  <div class="eq" data-export="png" data-name="eq-03">
    <p style="text-align:center; margin:0 0 6px; font-weight:700;">예제 2) $3 \le x \le 5$에서 $y=(x-2)^2-3$</p>
    $$\text{꼭짓점 } x=2 \text{는 범위 밖} \; \rightarrow \; \text{후보는 양 끝뿐}$$
    $$y(3)=-2,\quad y(5)=6$$
    $$\therefore\ \text{최솟값 } -2\ (x=3),\quad \text{최댓값 } 6\ (x=5)$$
    <div class="caption">골짜기 바닥(x=2)을 지난 오른쪽 구간이라 그래프가 계속 올라가기만 해요.</div>
  </div>

  <p>범위 하나 바뀌었을 뿐인데 답의 구조가 완전히 달라지죠. 그래서 "꼭짓점이 범위 안인가?"를 <strong>가장 먼저</strong> 확인해야 해요.</p>

  <h2>시험에서 틀리는 건 늘 이 3가지예요</h2>
  <p>상담하면서 오답을 모아 보면 놀랄 만큼 같은 자리에서 틀려요.</p>

  <div data-export="png" data-name="table-02">
    <table>
      <tr><th>실수 유형</th><th>무슨 일이 벌어지나</th><th>예방법</th></tr>
      <tr><td>상수 보정 누락</td><td>$(x-2)^2$ 만들며 더한 $+4$를 안 빼서 꼭짓점 $y$값이 틀림</td><td>변형 후 꼭짓점 검산 대입</td></tr>
      <tr><td>범위 확인 생략</td><td>꼭짓점이 범위 밖인데 꼭짓점 값을 답으로 씀</td><td>표준형 다음 "범위 안?"부터 확인</td></tr>
      <tr><td>경계 대입 실수</td><td>양 끝 중 한 곳만 대입하고 비교를 끝냄</td><td>후보를 표로 전부 나열 후 비교</td></tr>
    </table>
    <div class="caption">세 실수 모두 "후보 두 곳 원칙"만 지키면 자동으로 막을 수 있어요.</div>
  </div>

  <p>특히 두 번째 유형이 제일 아까워요. 계산은 다 해 놓고 마지막에 범위 확인 한 줄을 생략해서 틀리거든요. 문제에 범위가 보이면 <strong>표준형을 만들자마자 꼭짓점의 $x$값에 동그라미</strong>를 치고 범위와 비교하는 습관을 추천해요.</p>

  <div class="box">
    <p style="margin:0;">자녀 공부를 봐 주시는 학부모님이라면, 풀이를 일일이 이해하실 필요는 없어요. 채점할 때 딱 두 줄만 확인해 주세요. <strong>① 완전제곱식을 만들면서 더한 수를 다시 뺐는지, ② 꼭짓점의 $x$값을 범위와 비교하는 표시가 풀이에 있는지.</strong> 이 두 흔적이 답안지에 보이면 개념이 잡힌 것이고, 안 보이면 위 표의 실수가 반복되고 있을 가능성이 높아요.</p>
  </div>

  <h2>3줄 정리</h2>
  <div class="box">
    <p style="margin:0 0 8px;">• 포물선의 최대·최소는 <strong>꼭짓점 찾기</strong> — 표준형 $y=a(x-p)^2+q$로 바꾸는 게 시작이에요.</p>
    <p style="margin:0 0 8px;">• 범위가 없으면 꼭짓점이 답 (반대쪽은 "없음"), <strong>범위가 있으면 후보는 꼭짓점과 양 끝뿐</strong>이에요.</p>
    <p style="margin:0;">• 실수는 상수 보정·범위 확인·경계 대입, 이 세 자리에서 나와요. 검산 대입으로 다 막을 수 있어요.</p>
  </div>

  <p>다음 글에서는 지식iN에서 자주 보이는 심화 유형, <strong>"꼭짓점이 움직이는" 이차함수의 최대·최소</strong>(예: $y=x^2-2px+4p$)를 다뤄 볼게요. 오늘 배운 "후보 두 곳" 원칙이 거기서도 그대로 통한답니다.</p>
