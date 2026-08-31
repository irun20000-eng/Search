# HANDOVER — 다른 자리에서 이어받을 때

이 문서는 **살아 있는 목록**이다. `CLAUDE.md`·`PIPELINE.md`·`MATH_PIPELINE.md`·`VIDEO_PIPELINE.md`는
**계약**이고 잘 바뀌지 않는다. 여기는 "지금 무엇이 열려 있나"만 적는다. 끝난 항목은 지우지 말고
취소선으로 남긴다 — 언제 무엇이 닫혔는지가 다음 판단의 근거다.

> **수학사(`math/`)의 인계는 여기가 아니라 `math/ROADMAP.md` §11** 이다.
> 무엇을 쓸지·다음 대상·부채가 전부 거기 있고, 수치는 그 안의 「자동 측정」 블록이 정본이다.
> 이 문서는 **서가를 가로지르는 것**과 **리포 바깥 일**만 맡는다.

마지막 갱신: 2026-08-31

---

## 0. 이어받는 자리에서 처음 할 것

```bash
git fetch origin main -q && git log origin/main --oneline -15   # ★ fetch 없이 보면 무의미하다
ls                                                              # 최상위 구조 변경 확인
cat LESSONS.md | sed -n '1,120p'                                # 방지 규칙 체크리스트
```

`fetch` 를 빠뜨린 채 `git log origin/main` 을 보면 **며칠 묵은 캐시**를 읽는다.
2026-08-25 에 그것 때문에 24커밋 뒤처진 상태로 작업해 충돌을 만들었다(LESSONS 참조).

**환경 전제**(클라우드/모바일 세션):
- 원문 직접 열람 불가 — `mathshistory`·`wikipedia`·`terms.naver` 전부 프록시가 `connect_rejected`.
  ROADMAP §11 이 적어 둔 네이버 원문 `curl` 요령도 **이 환경에서는 듣지 않는다.**
  → WebSearch 요약 + 네이버 MCP 스니펫 **다중 교차검증**으로 쓰고, **직접 인용은 넣지 않는다.**
- 라이브 URL 도 못 받는다 → 배포 확인은 **머지 커밋 SHA 의 `pages build and deployment` success** 로 한다.
- 학습카드 `auto` 렌더는 로컬 전용 → 클라우드는 `manual`.

---

## 1. 서가 현황 (2026-08-31)

| 서가 | 편수 | 정본 위치 |
|---|---|---|
| research | 68 | `reports/<slug>/report.md` |
| videos | 96 | `videos/notes/<ID>.md` |
| math | 72 | `math/notes/<slug>/note.md` |
| blog | 22 | `blog/notes/<slug>.md` |
| cardnews | 22 | `cardnews/` + `studio/` |
| concept | 7 | `concept/notes/<slug>.md` |
| guides | 2 | `guides/<slug>/guide.md` |
| **합계** | **289** | `link-index.json` 이 통합 조회표 |

수치를 손으로 세지 말 것 — `python3 tools/build_link_index.py` 산출물이 정본이다.

---

## 2. 열려 있는 것

### 2-1. 머지 완료 브랜치 정리 — **사용자 조치 필요**

이 세션에서는 `git push --delete` 가 권한 분류기에 막혔고 GitHub MCP 에도 브랜치 삭제 도구가 없다.
**웹의 Branches 화면이나 로컬에서** 처리해야 한다.

**내용이 main 에 전부 들어간 것을 확인한 9개**(2026-08-29 대조):

```bash
git push origin --delete \
  claude/compassionate-goldberg-ln9xvr claude/routine-merge-policy \
  claude/compassionate-goldberg-fe7a8g claude/cardnews-발견노트-EP3 \
  claude/cardnews-숫자노트-EP4 feat/math-concept-ode \
  feat/math-concept-probability feat/math-concept-series feat/math-concept-roadmap
```

**2026-08-30 — 나머지도 전수 대조했다. 22개 중 21개가 삭제 안전이다.**
`blissful-pascal-*` 5 · `compassionate-goldberg-*` 4 · `inspiring-ramanujan-5k4njo` ·
`video-gallery-mobile-automation-oz2e3p` · `feat/math-history-archive` ·
`chore/vault-sync-20260828` · `iran-us-conflict-timeline-vr6mv0`(머지 77건) 전부 머지된
PR 을 갖는다. 남은 하나가 §2-2 의 `claude/cardnews-plan`(PR #100 **CLOSED**)이다.

⚠️ **파일 내용 대조로 판단하면 안 된다.** `git diff` 나 파일 해시로 재면 21개 중 19개가
"미반영" 으로 찍힌다 — **스쿼시 머지 뒤 그 파일들이 더 바뀌었기 때문**이고, 브랜치 작업이
안 들어간 게 아니다. 정확한 판정은 **PR 이력**이다:

```bash
gh pr list --state all --limit 300 --json number,headRefName,state,mergedAt
# 브랜치별로 state=MERGED 인 PR 이 있으면 삭제 안전
```

### 2-2. `claude/cardnews-plan` — 판단 필요

이 브랜치에만 `CARDNEWS_PIPELINE.md` 가 있다(2026-08-22, "상태: 계획, 구현 전").
그 계획은 **이미 전부 구현됐고**(`cardnews/` 서가 · `studio/` · ingest · link-index 연결),
운영 정본은 `routines/cardnews-weekly.md` + `studio/CLAUDE.md` 로 넘어갔다.
**설계 근거 기록으로 main 에 남길지 버릴지**는 사용자 판단.

### 2-2-1. 컷툰 그림 넣기 — **PC 환경에서 이어서** (2026-08-29 사용자 결정)

`studio/sandbox/` 는 발행되지 않는 실험대다(`out/` 은 git 무시). 지금 들어 있는 것:
개념 한 장 판형 A/B/C, A4 여섯 컷 컷툰, A 판형 동일성 검사.

> **2026-08-30 — 컷아웃 배치·렌더는 끝났다.** `E:\AI_Project\Shorts_Flow\characters\cutouts\`
> 의 5종을 아래 이름으로 두고 `python studio/sandbox/render.py cuttoon` 을 돌렸다.
> 대역 경고 없이 통과했고(컷 높이 3종·겹침 0·얼굴 가림 0) 여섯 컷에 QED프렌즈가 들어갔다.
> **남은 것은 배경컷뿐이다** — 스펙이 "그림은 아직 없다, 각 컷의 `shot` 이 Flow 프롬프트의
> 씨앗"이라 적어 둔 그 단계(README 의 ②)이고, 컷 1·6 이 넓게 비어 보이는 것은 그 때문이다.
> 사용자가 Flow 에서 여섯 장을 받아 오면 스펙의 `img` 에 경로를 적고 다시 돌리면 된다.
> ⚠️ **컷아웃은 gitignore 라 이 PC 에만 있다.** 다른 자리에서는 아래를 다시 해야 한다.

**배관은 끝나 있다. PC 에서 할 일은 파일을 두고 한 줄 돌리는 것뿐이다.**

```bash
# Shorts_Flow 의 characters/cutouts_*.png 5종을 이 이름으로 둔다
#   studio/sandbox/assets/characters/{dr-pi,root,zero,coco,mu}.png
python3 studio/sandbox/render.py cuttoon        # 그러면 그 자리에 그대로 들어간다
```

- 스펙(`specs/cuttoon-logarithm.py`)의 `figures` 가 이미 그 경로를 가리킨다.
  코드는 더 손댈 것이 없다.
- **이 폴더는 gitignore 다.** Search 는 공개 리포이고(API 로 `private:false` 확인)
  QED프렌즈는 비공개 Shorts_Flow 자산이라, 커밋하면 그대로 웹에 공개된다.
- 대역 실루엣(`--stubs`)이 깔려 있으면 렌더가 매번 경고한다. 진짜 컷아웃으로
  덮으면 해시가 달라 저절로 조용해진다.

**왜 클라우드에서 못 했나** — 두 경로가 다 막혔다. 다시 시도해 시간 쓰지 말 것.
1. Drive MCP 다운로드는 base64 로 컨텍스트에 들어온다. 5장 563KB → 디스크에 쓰려면
   그것을 한 번 더 뱉어야 해서 실질 2배, 한 장에 약 7만 토큰이다.
2. 링크 공유 후 curl 도 안 된다 — **에이전트 프록시가 정책으로 Drive 를 막는다**
   (`drive.google.com:443 connect_rejected`, 403). 공유를 켰어도 못 받았다.

**그림이 들어가는 자리는 둘**이고 섞어 쓸 수 있다 — `img`(컷 전체를 채우는 Flow
배경컷, cover) / `figures`(배경 없는 컷아웃을 바닥에 세움, contain). 자세한 것은
`studio/sandbox/README.md`.

#### 판형 B/C

**아직 발행에 쓰지 않는다.** `studio/concept_sheet.py` 와 러너 워크플로는 그대로
A 만 그린다 — 실험대에서 골라 본 뒤 옮기는 것이 순서. 판형 CSS 를 건드렸으면
`render.py same` 을 반드시 돌릴 것(발행분 다섯 장이 A 이고, 기준 커밋은
`render.py` 의 `BASELINE` 에 못박혀 있다).

#### 손대지 않은 디자인 지적 하나

개념 한 장은 **모든 편이 4칸 단계 + 3칸 정리로 똑같다.** 판형 B/C 는 겉만 바꾸고
뼈대는 그대로다. 스키마를 바꾸면 발행분 일곱 장이 전부 흔들리므로 별건으로 두었다.

### 2-5. 볼트 사본 2편에 「갤러리 안내」 콜아웃이 빠져 있다 — 작음, 손으로 3줄

2026-08-31 에 발행한 `derivative-rate-of-change`(이해편)·`-advanced`(확장편)를
클라우드에서 **Drive MCP 로 직접** 볼트에 넣었다. 본문은 리포 원본과 **바이트 길이가
정확히 일치**한다(34,189 / 31,626). 다만 `sync_obsidian.py` 가 H1 뒤에 끼워 넣는
`> [!info] 주제 리서치 …` 콜아웃 3줄이 없다.

**왜 채우지 않았나** — Drive MCP 에는 이어붙이기가 없어 3줄을 넣으려면 66KB 를 통째로
다시 옮겨 적어야 한다. 그것이 바로 LESSONS 2026-08-17·19 가 적어 둔 **조용한 손상**
경로다(길이 검사를 통과하면서 한글 몇 자가 그럴듯하게 바뀐다). 3줄을 얻자고 감수할
위험이 아니라고 판단했다.

**고치는 법**: 볼트에서 두 노트의 H1 바로 밑에 아래를 붙이면 끝이다.

```
> [!info] 주제 리서치
> 갤러리에서 보기 — https://irun20000-eng.github.io/Search/research/#r=<슬러그>
> 이 노트는 리포에서 왔습니다. 여기에 링크·메모를 더해도 동기화가 덮지 않습니다.
```

⚠️ **`sync_obsidian.py --force` 로 밀지 말 것.** 판정이 볼트 내용 기준이라 두 편은
이미 "있음" 으로 걸러지고, `--force` 는 볼트 전체를 덮어 토요일 위키링크 작업을 날린다.

> **일반화** — 클라우드에서 Drive MCP 로 볼트에 직접 쓰면 `sync_obsidian.py` 가 얹는
> 것들이 빠진다. 다음에 같은 일을 할 때는 **콜아웃까지 포함해 한 번에 써 넣을 것**
> (본문을 옮겨 적는 김에 3줄을 같이 얹으면 추가 비용이 0이다).

### 2-3. frontmatter 상호참조 단방향 67건

`python3 tools/verify_math.py --symmetry` 가 보고한다. **게이트가 아니다.**
다수가 이해편/확장편 쌍의 기존 관례라 **설계상 정상일 수 있다** — 줄이기 전에 관례부터 정할 것.

### 2-4. ~~평문 이름에 위키링크 걸기~~ → **대상 노트 쓰기로 넘어갔다**

~~유클리드·아르키메데스·카르다노가 본문에만 있고 위키링크가 0건~~ — #168 이 걸었다.
실측 `[[유클리드]]` 11 · `[[카르다노]]` 5 · `[[아르키메데스]]` 4.

**상태가 "안 보임" 에서 "보이는데 비어 있음" 으로 옮겨 갔다.** 셋 다 대상 노트가 없어
미해결 위키링크 백로그(8종 26회)에 정상적으로 떠 있다. 남은 일은 링크가 아니라
**그 인물 노트를 쓰는 것**이고, 셋 다 17세기 이전이라 `math/ROADMAP.md` §11 의
`century-16c` 권고와 같은 곳을 가리킨다.

---

## 3. 닫힌 것 (2026-08-29 확인 · 2026-08-30 추가)

- ~~**math 서가의 날짜가 전부 "빌드한 날" 이던 것**~~ — 고쳤다(2026-08-31). math 노트에만
  날짜 필드가 없어 `build_link_index.py` 가 매니페스트의 `generated` 를 72편에 복사했다.
  허브 「최근」 12칸 중 5칸이 math 인데 그 다섯이 실제 최신이 아니었고(적분법·무한급수·복소수
  = 8/21), 날이 바뀔 때마다 `link-index.json` 73줄이 churn 이라 진짜 변경을 덮었다.
  frontmatter `날짜` 를 72편에 백필(git 최초 커밋일)하고 빌더·게이트를 맞췄다.

- ~~**블로그 서가 도해가 검게 뭉갠 것**~~ — 고쳤다(#166). 노트 SVG 가 색을 `var(--green)`
  류로 부르는데 그 정의(`brand.css`)가 이관을 안 따라와 **미정의 `var()` 가 SVG 에서
  검정으로 떨어졌다** — 19/22편·499자리·라이트와 다크 양쪽. 콘솔 오류도 깨진 이미지도
  없어 조용히 두 달을 갔다. 정본 팔레트를 필라별로 심고, 다크는 색을 뒤집는 대신
  도해에만 제 지면을 깔았다(`math/` 도해와 같은 규약). 표지 누락 3편은
  `ingest_blog.py` 에서 고쳤다 — **노트를 손으로 고치면 자동 인제스트가 되돌린다.**

- ~~**`youtube-math-skill` manifest 패치**~~ — 사용자가 적용했다. `output/manifest.json` **70편**.
  허브 「학습자료」 바깥 서가가 살아 있다.
- ~~**카드뉴스·블로그를 바깥 서가로 둘 것인가**~~ — 둘 다 **Search 안으로 들어왔다**.
  허브 `ORDER` 가 7서가로 확장됐고 `EXTRA`(바깥 서가)에는 학습자료 하나만 남았다.
- ~~**`cardnews-render.yml` 스텝 순서 버그**~~ — 고쳐졌다. `doctor` 가 `playwright install` 뒤로 갔고,
  동시 워크플로 push 경합(rebase 3회 재시도)과 Actions PR 생성 거부 로깅도 함께 들어갔다.
- ~~**허브 검색이 서가를 가로지르지 못하던 것**~~ — `link-index.json` 항목에 `검색어` 를 실어 해결(#144).
  「묶어 읽기」 여섯 중 다섯이 다서가가 됐다.
- ~~**ROADMAP 부채표가 손으로 관리돼 낡던 것**~~ — `tools/build_math_status.py` 가 수치를 쓴다(#156).

---

## 4. 이 저장소에서 자주 틀리는 것 — 짧은 목록

전체는 `LESSONS.md` 의 「방지 규칙 체크리스트」를 볼 것. 최근 반복된 것만 추린다.

- **`fetch` 없는 `origin/main` 확인은 점검하지 않은 것과 같다.**
- **"N년 뒤/만에" 를 쓸 때마다 그 자리에서 뺄셈을 해 본다.** 3회 이상 재발했다.
- **2차 문헌이 인용한 3차 인용을 2차 문헌의 말로 옮기지 않는다.** 인용 블록 앞 한 줄을 읽을 것.
- **저장소가 이미 정한 사실과 충돌하는지 확인한다.** 출처 충돌보다 이게 더 무겁다.
- **절을 끼워 넣었으면 그 문서의 `§n` 을 전수 대조한다.** 검사기가 세지 않는다.
  번호를 미는 치환은 **내림차순이나 단일 스캔**으로 — 오름차순 연쇄가 앞의 결과를 다시 바꾼다.
- **분량 게이트 미달이면 절을 새로 끼우기 전에 기존 절을 깊게 쓴다.** 구조를 건드리면 참조가 깨진다.
- **인용하기 전에 그 자료를 실제로 열어 봤는지 확인한다.** 계획 단계에서 떠올린 문서를
  검색도 하지 않고 출처 목록에 적을 뻔한 일이 있었다(2026-08-29).
- **다른 리포에서 본문을 옮겨 올 때 색·폰트 정의가 따라왔는지 본다.** 옮긴 HTML 이
  `var(--…)` 로 색을 부르면 정의는 원천 스타일시트에 있다. 안 따라오면 **SVG 는 검정으로
  떨어지고 조용하다** — 콘솔 오류도 깨진 이미지도 없다. 블로그 서가가 그렇게 두 달 갔다.
- **파일 무결성 검사는 화면 정상을 뜻하지 않는다.** 이관·갤러리 변경 뒤에는 실제 브라우저로
  한 편 열어 눈으로 본다. 계측기만 믿지 말 것 — 이번에도 오탐 둘이 진짜를 덮을 뻔했다.
- **`blog/notes/*.md` 를 손으로 고치지 않는다.** Blog 리포 워크플로가 Search 를 체크아웃해
  `tools/ingest_blog.py` 로 다시 쓴다. 고칠 자리는 노트가 아니라 그 스크립트다.
- **산출물을 손으로 고치지 않는다** — `manifest.json` · `link-index.json` · ROADMAP 「자동 측정」 블록.
  충돌 나면 `git checkout origin/main -- <파일>` 뒤 빌더를 다시 돌린다.

---

## 5. 완료의 정의

보고서·노트 요청 하나가 끝나려면 여기까지다. **별도 언급이 없어도 끝까지 간다.**

```
작성 → 게이트 측정 → 검수(별도 패스, self-approve 금지) → 빌더 실행(순서 고정)
     → 커밋 → 푸시 → PR → main 머지 → Pages 배포 확인 → 옵시디언 볼트
```

볼트 폴더: 리서치 `001-주제리서치` · 수학사 `002-수학사` · 개념노트 `003-카드뉴스학습자료` ·
영상노트/가이드 `011-보고따라해`. **볼트는 사본이고 정본은 언제나 리포다.**
클라우드에서는 로컬 `G:\` 경로가 없으므로 **구글드라이브 MCP 로 같은 폴더에 직접 쓴다**
(`002-수학사` = `1taNZtvL3n9Nz10xety7ncN7hRtggkjby`, 그 아래 `01-세기`·`02-개념`·`03-인물`·`04-일화`).
