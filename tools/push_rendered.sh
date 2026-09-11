#!/usr/bin/env bash
# 렌더 산출물 커밋을 브랜치에 밀어 넣는다 — 다른 워크플로와 부딪혀도 잃지 않는다.
#
# ■ 무엇이 문제였나
# 카드뉴스 한 편을 낼 때 카피(studio/contents/**·cardnews.yaml)와 이해편
# (concept/notes/**·studio/concepts/**)이 한 커밋에 들어간다. 루틴 지침이 그렇게
# 하라고 되어 있으므로 **한 push 가 `cardnews-render` 와 `concept-sheet-render` 를
# 반드시 함께 깨운다.** 둘은 같은 브랜치에 커밋하고, 늦게 끝난 쪽이
# `! [rejected] (fetch first)` 를 받는다.
#
# 종전 재시도는 `git pull --rebase` 3회였고 주석에 "산출물 경로가 겹치지 않으므로
# 안전하다" 고 적혀 있었다. **경로는 안 겹치지만 파일 둘이 겹친다** —
# `link-index.json` 과 `backlog.json` 은 두 워크플로가 **모두** 재생성한다.
# 그래서 rebase 가 CONFLICT 로 멈추고, 재시도 루프는 충돌을 풀 줄 몰라 exit 1 이 되며,
# **그 커밋은 러너와 함께 사라진다.** 렌더는 성공했는데 산출물만 없다.
#   2026-08-27 발견노트 EP3(개념 한 장 유실) · 2026-09-03 일머리 EP4 ·
#   2026-09-08 숫자노트 EP5(카드 컷 10장 유실, run 34173066757)
#
# ■ 어떻게 고치나 — 충돌한 산출물은 병합하지 말고 재생성한다
# LESSONS 2026-08-25 가 정한 규칙이다: "빌드 산출물이 충돌하면 병합하지 말고
# 재생성한다. 손으로 병합한 산출물은 빌더가 만든 것과 다를 수밖에 없다."
# 이 스크립트는 그것을 자동으로 한다 —
#   ① push 가 거절되면 원격을 받아 rebase 한다
#   ② 충돌 파일이 **재생성 가능 목록 안에만** 있으면 원격 것으로 일단 덮어 rebase 를 끝낸다
#      (목록 밖이 하나라도 충돌하면 중단한다. 사람이 봐야 할 충돌이다)
#   ③ **합쳐진 소스에서 산출물을 다시 만들고** 달라졌으면 커밋을 amend 한다
#   ④ 다시 push
#
# ②의 "원격 것으로 덮는다" 는 값을 고르는 것이 아니라 rebase 를 진행시키기 위한
# 자리표시일 뿐이다. 최종 값은 ③이 빌더로 만든다. 그래서 어느 쪽을 골랐는지가
# 결과에 영향을 주지 않는다 — rebase 의 --ours/--theirs 가 병합과 반대로 뒤집혀
# 있다는 함정(rebase 중 ours=업스트림, theirs=내 커밋)을 피하려고 일부러
# `git checkout FETCH_HEAD -- <파일>` 로 쓴다. 어느 쪽인지 이름으로 읽힌다.
#
# ■ 덤 — rebase 가 조용히 만들어 내던 「고정점 아닌 산출물」도 같이 막는다
# 충돌 없이 자동 병합되는 경우에도 그 결과는 빌더의 출력과 다를 수 있다.
# 그러면 `tools/verify_builders.py` 가 재는 멱등성(지금 산출물이 지금 소스의
# 고정점인가)이 깨진다. 그래서 **rebase 를 했으면 충돌 여부와 관계없이 항상**
# 재생성한다.
#
# ■ 왜 두 워크플로를 같은 concurrency 그룹으로 묶지 않았나
# 그러면 둘이 직렬화돼 애초에 안 부딪힌다. 그런데 GitHub 은 한 그룹에서
# **대기 중인 실행을 하나만 남기고 나머지를 취소한다.** 회차 중에 push 가 한 번
# 더 나가면(이 저장소에서는 실제로 일어난다 — 컷을 고쳐 다시 올리는 경우)
# 대기 중이던 렌더가 조용히 취소된다. 유실을 없애려다 유실의 새 경로를 만드는
# 셈이라 택하지 않았다. 이 스크립트는 순서와 무관하게 각 워크플로를 혼자서도
# 옳게 만든다.
#
# 사용:
#   tools/push_rendered.sh <브랜치> [재생성 명령...]
#   예) tools/push_rendered.sh "$BRANCH" python tools/build_link_index.py
#
# 종료 코드: 0 성공 · 1 실패(무엇이 막았는지 ::error:: 로 남긴다)
set -uo pipefail

BRANCH="${1:-}"
if [ -z "$BRANCH" ]; then
  echo "::error::push_rendered.sh <브랜치> [재생성 명령...] — 브랜치 이름이 필요하다" >&2
  exit 1
fi
shift

# 재생성 명령. 기본값은 링크 인덱스 빌더이며 그 안에서 backlog.json 도 함께 만든다
# (build_link_index.py 가 __main__ 에서 build_backlog.build() 를 이어 부른다).
REBUILD=("$@")
if [ ${#REBUILD[@]} -eq 0 ]; then
  REBUILD=(python tools/build_link_index.py)
fi

# 충돌해도 되는 파일 = 소스에서 다시 만들 수 있는 것.
# 이 목록 밖이 충돌하면 사람이 봐야 하는 충돌이므로 중단한다.
REGENERABLE=(link-index.json backlog.json)

MAX_TRY=3

is_regenerable() {
  local f="$1" r
  for r in "${REGENERABLE[@]}"; do
    [ "$f" = "$r" ] && return 0
  done
  return 1
}

rebuild_and_amend() {
  echo "재생성: ${REBUILD[*]}"
  if ! "${REBUILD[@]}"; then
    echo "::error::산출물 재생성이 실패했다 — 반쪽 트리를 push 하지 않는다" >&2
    return 1
  fi

  # 무엇이 바뀌었는지는 **실측**한다. 선언 목록을 그대로 `git add` 에 넘기면
  # 아직 없는 파일 하나 때문에 add 가 통째로 실패하고(`pathspec ... did not match`),
  # 그 실패를 안 보면 amend 가 **아무것도 담지 않은 채 성공**한다.
  # 그러면 낡은 산출물이 그대로 push 된다 — 이 시험(test_push_rendered.sh)이 잡은 결함이다.
  local -a dirty=() mine=() extra=()
  mapfile -t dirty < <(git status --porcelain --untracked-files=all | sed 's/^...//')
  local f
  for f in "${dirty[@]}"; do
    if is_regenerable "$f"; then mine+=("$f"); else extra+=("$f"); fi
  done

  if [ ${#extra[@]} -gt 0 ]; then
    echo "::error::재생성이 선언 목록 밖의 파일을 건드렸다: ${extra[*]}" >&2
    echo "::error::REGENERABLE 목록이 실제 빌더와 어긋난다는 뜻이다 — 조용히 넘기지 않는다" >&2
    return 1
  fi

  if [ ${#mine[@]} -eq 0 ]; then
    echo "재생성 결과가 같다 — amend 하지 않는다"
    return 0
  fi

  if ! git add -- "${mine[@]}"; then
    echo "::error::git add 실패: ${mine[*]}" >&2
    return 1
  fi
  if ! git commit --amend --no-edit --quiet; then
    echo "::error::git commit --amend 실패" >&2
    return 1
  fi
  echo "재생성 결과를 커밋에 반영했다(amend): ${mine[*]}"
}

resolve_rebase_conflict() {
  local conflicts f
  mapfile -t conflicts < <(git diff --name-only --diff-filter=U)
  if [ ${#conflicts[@]} -eq 0 ]; then
    echo "::error::rebase 가 멈췄는데 충돌 파일이 없다 — 손으로 볼 것" >&2
    return 1
  fi
  for f in "${conflicts[@]}"; do
    if ! is_regenerable "$f"; then
      echo "::error::재생성할 수 없는 파일이 충돌했다: $f" >&2
      echo "::error::자동으로 풀지 않는다. 충돌 목록: ${conflicts[*]}" >&2
      return 1
    fi
  done
  echo "::notice::충돌은 전부 빌드 산출물이다(${conflicts[*]}) — 병합하지 말고 재생성한다"
  for f in "${conflicts[@]}"; do
    # 값을 고르는 것이 아니라 rebase 를 진행시키기 위한 자리표시다. 최종 값은 빌더가 만든다.
    git checkout FETCH_HEAD -- "$f"
    git add -- "$f"
  done
  if GIT_EDITOR=true git rebase --continue; then
    return 0
  fi
  # 남길 변경이 없어지는 경우(내 커밋이 산출물만 건드렸을 때)는 skip 이 정답이다
  if git diff --cached --quiet && git diff --quiet; then
    echo "::notice::남는 변경이 없다 — 이 커밋은 건너뛴다"
    GIT_EDITOR=true git rebase --skip
    return $?
  fi
  echo "::error::rebase --continue 가 실패했다" >&2
  return 1
}

for try in $(seq 1 "$MAX_TRY"); do
  if git push origin "HEAD:refs/heads/$BRANCH"; then
    echo "push 성공(시도 $try/$MAX_TRY)"
    exit 0
  fi

  if [ "$try" -eq "$MAX_TRY" ]; then
    break
  fi

  echo "::notice::push 거절($try/$MAX_TRY) — 다른 워크플로가 같은 브랜치에 밀어 넣었다. 받아서 다시 얹는다"

  if ! git fetch origin "$BRANCH"; then
    echo "::error::fetch 실패 — 네트워크나 권한 문제다" >&2
    exit 1
  fi

  if ! git rebase FETCH_HEAD; then
    if ! resolve_rebase_conflict; then
      git rebase --abort 2>/dev/null || true
      echo "::error::rebase 를 자동으로 풀지 못했다 — 산출물이 브랜치에 없다" >&2
      exit 1
    fi
  fi

  # 충돌이 있었든 없었든 항상 재생성한다.
  # 자동 병합된 산출물은 빌더의 출력과 다를 수 있고, 그러면 verify_builders 의
  # 멱등성(고정점) 검사가 나중에 깨진다.
  if ! rebuild_and_amend; then
    exit 1
  fi
done

echo "::error::${MAX_TRY}회 시도했는데도 push 하지 못했다 — 렌더 산출물이 브랜치에 없다" >&2
echo "::error::이 실행의 로그에서 렌더는 성공했는지 확인할 것. 성공했다면 같은 브랜치에 빈 수정 없이 다시 push 하면 재렌더된다." >&2
exit 1
