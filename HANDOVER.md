# HANDOVER — 다른 자리에서 이어받을 때

이 문서는 **살아 있는 목록**이다. `CLAUDE.md`·`PIPELINE.md`·`MATH_PIPELINE.md`·`VIDEO_PIPELINE.md`는
**계약**이고 잘 바뀌지 않는다. 여기는 "지금 무엇이 열려 있나"만 적는다. 끝난 항목은 지우지 말고
취소선으로 남긴다 — 언제 무엇이 닫혔는지가 다음 판단의 근거다.

> **수학사(`math/`)의 인계는 여기가 아니라 `math/ROADMAP.md` §11** 이다.
> 무엇을 쓸지·다음 대상·부채가 전부 거기 있고, 수치는 그 안의 「자동 측정」 블록이 정본이다.
> 이 문서는 **서가를 가로지르는 것**과 **리포 바깥 일**만 맡는다.

마지막 갱신: 2026-08-29

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

## 1. 서가 현황 (2026-08-29)

| 서가 | 편수 | 정본 위치 |
|---|---|---|
| research | 66 | `reports/<slug>/report.md` |
| videos | 96 | `videos/notes/<ID>.md` |
| math | 72 | `math/notes/<slug>/note.md` |
| blog | 22 | `blog/notes/<slug>.md` |
| cardnews | 22 | `cardnews/` + `studio/` |
| concept | 7 | `concept/notes/<slug>.md` |
| guides | 2 | `guides/<slug>/guide.md` |
| **합계** | **287** | `link-index.json` 이 통합 조회표 |

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

⚠️ **원격에는 그 밖에도 브랜치가 열두 개쯤 더 있고 그것들은 대조하지 않았다**
(`blissful-pascal-*` · `video-gallery-mobile-automation-*` · `feat/math-history-archive` 등).
커밋 수가 60~100 으로 찍히는데 **스쿼시 머지 뒤 남은 옛 이력일 가능성이 크다** — 세어 본 숫자로
판단하지 말고 `git diff origin/main origin/<브랜치>` 로 **내용**을 대조한 뒤 지울 것.

### 2-2. `claude/cardnews-plan` — 판단 필요

이 브랜치에만 `CARDNEWS_PIPELINE.md` 가 있다(2026-08-22, "상태: 계획, 구현 전").
그 계획은 **이미 전부 구현됐고**(`cardnews/` 서가 · `studio/` · ingest · link-index 연결),
운영 정본은 `routines/cardnews-weekly.md` + `studio/CLAUDE.md` 로 넘어갔다.
**설계 근거 기록으로 main 에 남길지 버릴지**는 사용자 판단.

### 2-3. frontmatter 상호참조 단방향 67건

`python3 tools/verify_math.py --symmetry` 가 보고한다. **게이트가 아니다.**
다수가 이해편/확장편 쌍의 기존 관례라 **설계상 정상일 수 있다** — 줄이기 전에 관례부터 정할 것.

### 2-4. 평문으로만 불리는 이름에 위키링크 걸기

유클리드 79회 · 아르키메데스 38회 · 카르다노 19회가 본문에 있는데 **위키링크가 0건**이라
검사기에 안 보인다. 링크를 걸면 그 순간 백로그에 뜬다. 여러 문서에 걸친 일이라 회차를 나눠 할 것.

---

## 3. 닫힌 것 (2026-08-29 확인)

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
