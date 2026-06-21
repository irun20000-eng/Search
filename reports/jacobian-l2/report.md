---
주제: 야코비안 변환 (학부) — 변수변환·확률밀도·역함수 정리
날짜: 2026-06-21
깊이: deep
대상수준: 학부
카드모드: manual
태그: [수학, 학습, 변수변환, 확률, 로보틱스, 학부]
소스수: { 국내: 4, 해외: 6 }
위키링크: ["[[야코비안 변환 개념지도]]", "[[야코비안 변환 입문]]", "[[야코비안 변환 대학원]]", "[[행렬과 다변수 미적분 학부]]"]
갤러리URL: "#r=jacobian-l2"
---

# 야코비안 변환 (학부) — 변수변환·확률·역함수

> 🎓 **눈높이**: 다변수 미적분·확률을 듣는 학부생. 입문의 '배율'을 **편미분 행렬의 행렬식**으로 정식화하고 세 가지 핵심 응용에 적용합니다. (시리즈 🔵학부 편 — 선행 [[행렬과 다변수 미적분 학부]])

## TL;DR
- **야코비 행렬** = 1차 편도함수의 `m×n` 행렬, 정사각이면 그 **행렬식이 야코비안** `det J` [1][7].
- **다중적분 변수변환**: `∬_R f dx dy = ∬_S f·|det J| du dv`. 좌표를 바꾸면 칸 넓이가 `|det J| du dv`이기 때문 [9][10].
- **확률밀도 변환**: `p_Y(y)=p_X(F⁻¹(y))·|det J_{F⁻¹}|` — 늘어나면 밀도가 낮아지므로 보정('야코비안 보정') [11][13].
- **역함수 정리**: `det J≠0`이면 국소 가역, `det J=0`이면 비가역(특이점·전단사 붕괴) [2][3].

## 핵심 포인트
1. 야코비안 = 편미분 행렬식 = 국소 부피 배율(입문 직관의 정식화) [7].
2. 적분 보정자 `|det J|`(절댓값 필수) [9].
3. 확률밀도는 **역변환** 야코비안으로 보정(방향 주의) [11].
4. `det J≠0` ⟺ 국소 가역(역함수 정리) [2].
5. 로봇: `ẋ=J q̇`, `det J=0`이 특이점 [12].

## 본문

### 1. 정의: 야코비 행렬과 야코비안
변환 `F(x₁,…,xₙ)=(f₁,…,fₘ)`의 **야코비 행렬**은 `J=[∂fᵢ/∂xⱼ]` (`m×n`) [1][7]. 정사각(`m=n`)일 때 **행렬식 `det J`가 야코비안**이며, 학부에선 이 행렬식을 그냥 야코비안이라 부른다 [4]. 2변수 표준형:
```
 ∂(x,y)/∂(u,v) = (∂x/∂u)(∂y/∂v) − (∂x/∂v)(∂y/∂u)
```
[9]. 이는 [[행렬과 다변수 미적분 학부]]의 **전미분(최선의 선형근사)을 좌표로 적은 행렬**의 행렬식이다.

### 2. 응용 ① 다중적분의 변수변환
1변수 치환 `dx=g'(t)dt`의 다변수 일반화 [9][J6]:
```
 ∬_R f(x,y) dx dy = ∬_S f(x(u,v), y(u,v)) · |∂(x,y)/∂(u,v)| du dv
```
좌표를 바꾸면 `du,dv`가 만드는 격자 칸이 원래 평면에서는 같은 크기 직사각형이 아니고, 그 실제 넓이가 `|det J| du dv`라서 보정해야 한다 [9][10].

**극좌표 검산**: `x=r cosθ, y=r sinθ`이면
```
 ∂(x,y)/∂(r,θ) = | cosθ  −r sinθ ; sinθ  r cosθ | = r cos²θ + r sin²θ = r
```
`r≥0`이라 `|J|=r`, 곧 `dx dy = r dr dθ` — 입문의 직관과 정확히 일치 [8][9]. 예: `∬√(x²+y²)dA = ∬ r·r dr dθ = ∬ r² dr dθ` [8].

### 3. 응용 ② 확률밀도함수(PDF) 변환
확률변수 `X`를 일대일 변환해 `Y=F(X)`를 얻으면 [11][13]:
```
 p_Y(y) = p_X(F⁻¹(y)) · |det J_{F⁻¹}(y)|
```
직관: 변환이 공간을 늘이면(`|J|` 큼) 같은 확률질량이 넓게 퍼져 **밀도가 낮아져야** 하므로 야코비안으로 보정한다('야코비안 보정') [11].

> ⚠️ **방향 함정**: 보통 **역변환**의 야코비안을 쓴다. 정변환 야코비안을 쓰려면 그 **역수**가 들어간다(`|det J_F|`와 `|det J_{F⁻¹}|`는 서로 역수). 섞으면 `|J|`와 `1/|J|`가 뒤바뀐다 [11][2].

### 4. 응용 ③ 역함수 정리
**`det J ≠ 0`이면 그 점 근방에서 변환은 국소적으로 가역**이고 매끄러운 역함수를 가진다 [2][7]. 반대로 **`det J=0`**이면 국소 비가역·변수 비독립, 적분 치환의 전단사(일대일) 전제가 깨진다 [3].

### 5. 응용 ④ 로보틱스 (맛보기)
로봇팔에서 야코비 행렬은 **관절속도↔말단속도**를 잇는다: `ẋ = J(q) q̇` [12]. 각 열이 한 관절의 기여이고, 쌍대성으로 `τ=JᵀF`(관절토크↔말단힘)도 연결한다. `det J=0`(또는 랭크 저하) 자세가 **특이점(singularity)** — 어떤 방향으로 말단이 움직이지 못하거나 역기구학이 발산한다 [12]. (여유자유도·의사역행렬은 대학원 편)

## 흔한 실수 (체크리스트)
- ❌ 절댓값 누락(음수 넓이/확률) [9]
- ❌ 정/역변환 방향 혼동(`1/|J|` 들어감) [11]
- ❌ 적분 영역 `R→S`·구간 변환 누락 [10]
- ❌ 특이점(`r=0` 등) 간과 [3]
- ✅ 검산: 단순 선형변환으로 배율이 맞는지 먼저 확인 [5]

## 다음 단계
- 🌉 더 깊이: 비정사각 `√det(JᵀJ)`·의사역행렬·다양체 미분형식 당김 → [[야코비안 변환 대학원]]
- ⬇️ 직관 복습: [[야코비안 변환 입문]] · 선행 [[행렬과 다변수 미적분 학부]]

## 출처(인용 링크)
**국내**
- [1] 네이버 지식백과 「야코비언」 — https://terms.naver.com/entry.naver?docId=5868337 (국내)
- [2] 네이버 지식백과 「야코비 행렬식」(역함수·치환적분) — https://terms.naver.com/entry.naver?docId=4125367 (국내)
- [3] 네이버 지식백과 「자코비안」(det=0 의미) — https://terms.naver.com/entry.naver?docId=394678 (국내)
- [4] 나무위키 「야코비안」(다변수 치환·용어 관행) — https://namu.wiki/w/야코비안 (국내)

**해외**
- [5] 공돌이의 수학정리노트 「자코비안의 기하학적 의미」 — https://angeloyeo.github.io/2020/07/24/Jacobian_en.html (국내/저자블로그)
- [7] Wikipedia "Jacobian matrix and determinant" — https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant (해외)
- [8] Paul's Online Notes "Change of Variables"(극좌표 J=r) — https://tutorial.math.lamar.edu/classes/calciii/changeofvariables.aspx (해외)
- [9] LibreTexts "Change of Variables in Multiple Integrals (Jacobians)" — https://math.libretexts.org/Courses/Monroe_Community_College/MTH_212_Calculus_III/Chapter_14:_Multiple_Integration/14.7:_Change_of_Variables_in_Multiple_Integrals_(Jacobians) (해외)
- [10] OpenStax "Calculus Volume 3, §5.7" — https://openstax.org/books/calculus-volume-3/pages/5-7-change-of-variables-in-multiple-integrals (해외)
- [11] Towards Data Science "The Jacobian Adjustment"(PDF 변환 방향) — https://towardsdatascience.com/keeping-probabilities-honest-the-jacobian-adjustment/ (해외)
- [12] Modern Robotics "Velocity Kinematics and the Jacobian"(특이점·쌍대성) — https://modernrobotics.northwestern.edu/nu-gm-book-resource/velocity-kinematics-and-statics/ (해외)
- [13] Hogg–McKean–Craig "Transformations for Several Random Variables" — https://faculty.etsu.edu/gardnerr/4047/notes-Hogg-McKean-Craig/Hogg-McKean-Craig-2-7.pdf (해외)

## 후속 질문·연결
- 비정사각(`m≠n`) 변환의 부피 척도는? → [[야코비안 변환 대학원]] [7]
- 정규화 흐름은 왜 `log|det J|`를 더할까? [11]
- 연결: [[야코비안 변환 개념지도]] · [[야코비안 변환 입문]] · [[야코비안 변환 대학원]] · [[행렬과 다변수 미적분 학부]]
