#!/usr/bin/env bash
# tools/push_rendered.sh 의 회귀 시험 — 실제 git 저장소 셋으로 경합을 재현한다.
#
# LESSONS 2026-08-25: "워크플로를 고쳤으면 로컬에서 그 셸 로직을 실제 커밋으로
# 재현해 본 뒤 올린다. YAML 파싱 통과는 로직이 맞다는 뜻이 아니다."
# 그 회차의 세 번째 결함은 재현에서만 나왔다. 그래서 이 시험이 있다.
#
# 무엇을 재현하나 — 2026-09-08 숫자노트 EP5 에서 실제로 난 것과 같은 모양:
#   러너 둘이 같은 브랜치에 커밋한다. 각자 자기 산출물(A/B)을 만들고,
#   **둘 다 공용 산출물 link-index.json 을 재생성한다.** 늦은 쪽이 push 에서
#   거절되고 rebase 가 link-index.json 에서 충돌한다.
#
# 무엇을 확인하나:
#   1. 늦은 쪽 커밋이 살아남는다(종전 로직은 여기서 죽고 커밋이 사라졌다)
#   2. 두 러너의 산출물이 **둘 다** 브랜치에 있다
#   3. 공용 산출물이 「원격 것」도 「내 것」도 아니라 **합쳐진 소스로 재생성된 값**이다
#      — 이것이 핵심이다. 한쪽을 고르기만 하면 다른 쪽 항목이 인덱스에서 사라진다
#   4. 재생성할 수 없는 파일이 충돌하면 **자동으로 풀지 않고 멈춘다**
#   5. 종전 로직(git pull --rebase 재시도)은 같은 상황에서 실제로 실패한다
#
# 사용: bash tools/test_push_rendered.sh
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$HERE/push_rendered.sh"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PASS=0
FAIL=0
ok()   { echo "  [OK] $1"; PASS=$((PASS+1)); }
bad()  { echo "  [X ] $1"; FAIL=$((FAIL+1)); }

git_q() { git -c advice.detachedHead=false "$@" >/dev/null 2>&1; }

# ── 빌더 흉내 — src/ 에 있는 파일들로 공용 산출물을 만든다 ────────────────
# 진짜 build_link_index.py 처럼 「소스 전체를 읽어 다시 만드는」 성질만 갖추면 된다.
# count 줄이 있어서 두 러너가 같은 줄을 서로 다르게 바꾼다 → 실제로 충돌한다.
make_builder() {
  cat > "$1/rebuild.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
n=$(ls src 2>/dev/null | wc -l | tr -d ' ')
{
  echo "{"
  echo "  \"count\": $n,"
  echo "  \"entries\": ["
  for f in $(ls src | sort); do echo "    \"$f\","; done
  echo "  ]"
  echo "}"
} > link-index.json
EOF
  chmod +x "$1/rebuild.sh"
}

setup() {
  rm -rf "$WORK"/*
  git init -q --bare "$WORK/origin.git"

  git init -q "$WORK/seed" && cd "$WORK/seed"
  git config user.email t@t; git config user.name t
  mkdir src && echo base > src/base.md
  make_builder "$WORK/seed"
  ./rebuild.sh
  git add -A && git commit -qm "seed"
  git branch -M work
  git push -q "$WORK/origin.git" work

  for r in a b; do
    git clone -q "$WORK/origin.git" "$WORK/$r"
    cd "$WORK/$r"
    git config user.email "$r@t"; git config user.name "$r"
    git checkout -q work
  done
}

# 러너가 렌더를 마치고 커밋한 상태를 만든다(아직 push 는 안 했다)
render_and_commit() {
  local dir="$1" name="$2"
  cd "$dir"
  echo "$name" > "src/$name.md"      # 그 러너만의 산출물
  ./rebuild.sh                        # 공용 산출물 재생성
  git add -A
  git commit -qm "chore: $name 렌더 반입"
}

echo "=== 1. 경합 — 늦은 쪽이 살아남고 산출물이 합쳐지는가 ==="
setup
render_and_commit "$WORK/a" cardnews
render_and_commit "$WORK/b" concept
cd "$WORK/b" && git push -q origin work        # b 가 먼저 이긴다
cd "$WORK/a"
if bash "$SCRIPT" work ./rebuild.sh > "$WORK/log-a.txt" 2>&1; then
  ok "늦은 쪽 push 가 성공했다"
else
  bad "늦은 쪽 push 가 실패했다"; sed 's/^/      /' "$WORK/log-a.txt"
fi
cd "$WORK/seed" && git fetch -q "$WORK/origin.git" work && git_q checkout FETCH_HEAD
if [ -f src/cardnews.md ] && [ -f src/concept.md ]; then
  ok "두 러너의 산출물이 둘 다 브랜치에 있다"
else
  bad "산출물이 유실됐다: $(ls src | tr '\n' ' ')"
fi
COUNT=$(grep -o '"count": [0-9]*' link-index.json | grep -o '[0-9]*')
if [ "$COUNT" = "3" ]; then
  ok "공용 산출물이 합쳐진 소스로 재생성됐다 (count=3)"
else
  bad "공용 산출물이 재생성되지 않았다 (count=$COUNT, 기대 3) — 한쪽을 고르기만 한 것이다"
fi
if grep -q 'cardnews.md' link-index.json && grep -q 'concept.md' link-index.json; then
  ok "인덱스가 두 항목을 모두 담고 있다"
else
  bad "인덱스에 빠진 항목이 있다"
fi

echo "=== 2. 충돌이 없는 평범한 경우 ==="
setup
render_and_commit "$WORK/a" cardnews
cd "$WORK/a"
if bash "$SCRIPT" work ./rebuild.sh > "$WORK/log-plain.txt" 2>&1; then
  ok "경합이 없으면 그냥 push 한다"
else
  bad "경합이 없는데 실패했다"; sed 's/^/      /' "$WORK/log-plain.txt"
fi

echo "=== 3. 재생성할 수 없는 파일이 충돌하면 멈추는가 ==="
setup
cd "$WORK/a"; echo "A 판" > src/base.md; git commit -qam "a: base 수정"
cd "$WORK/b"; echo "B 판" > src/base.md; git commit -qam "b: base 수정"
cd "$WORK/b" && git push -q origin work
cd "$WORK/a"
if bash "$SCRIPT" work ./rebuild.sh > "$WORK/log-stop.txt" 2>&1; then
  bad "사람이 봐야 할 충돌인데 자동으로 풀고 push 했다"
else
  if grep -q "재생성할 수 없는 파일이 충돌했다" "$WORK/log-stop.txt"; then
    ok "재생성 불가 충돌에서 멈추고 이유를 남겼다"
  else
    bad "멈추긴 했는데 이유가 다르다"; sed 's/^/      /' "$WORK/log-stop.txt"
  fi
fi
cd "$WORK/a"
if [ ! -d .git/rebase-merge ] && [ ! -d .git/rebase-apply ]; then
  ok "실패해도 rebase 상태를 남기지 않는다"
else
  bad "rebase 가 중간 상태로 남았다"
fi

echo "=== 4. 선언한 산출물 하나가 아직 없는 저장소 ==="
# 실제로 걸렸던 결함이다 — 선언 목록을 그대로 `git add` 에 넘기면 아직 없는 파일
# 하나 때문에 add 가 통째로 실패하고, 그 실패를 안 보면 amend 가 아무것도 담지 않은 채
# 성공해 **낡은 산출물이 그대로 push 된다**. 이 시험 저장소에는 backlog.json 이 없다.
setup
render_and_commit "$WORK/a" cardnews
render_and_commit "$WORK/b" concept
cd "$WORK/b" && git push -q origin work
cd "$WORK/a"
if bash "$SCRIPT" work ./rebuild.sh > "$WORK/log-missing.txt" 2>&1; then
  cd "$WORK/a"
  if [ "$(git show HEAD:link-index.json | grep -o '"count": [0-9]*' | grep -o '[0-9]*')" = "3" ]; then
    ok "선언 목록에 없는 파일이 있어도 재생성 결과가 커밋에 담긴다"
  else
    bad "amend 가 빈 채로 성공했다 — 낡은 산출물이 push 됐다"
  fi
else
  bad "실패했다"; sed 's/^/      /' "$WORK/log-missing.txt"
fi

echo "=== 5. 종전 로직(git pull --rebase 재시도)은 같은 상황에서 실패하는가 ==="
setup
render_and_commit "$WORK/a" cardnews
render_and_commit "$WORK/b" concept
cd "$WORK/b" && git push -q origin work
cd "$WORK/a"
OLD_OK=0
for i in 1 2 3; do
  if git push -q origin work 2>/dev/null; then OLD_OK=1; break; fi
  git pull --rebase -q origin work >/dev/null 2>&1 || true
done
if [ "$OLD_OK" = "0" ]; then
  ok "종전 로직은 실제로 실패한다 — 재현됐다(이 시험이 지키는 결함)"
  git rebase --abort >/dev/null 2>&1 || true
else
  bad "종전 로직이 성공해 버렸다 — 시험이 결함을 재현하지 못한다"
fi

echo
echo "통과 $PASS · 실패 $FAIL"
[ "$FAIL" -eq 0 ]
