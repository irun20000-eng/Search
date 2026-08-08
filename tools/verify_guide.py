#!/usr/bin/env python3
"""
가이드 품질 게이트.

■ 게이트 근거에 관한 정직한 기록
영상 노트 게이트는 기존 73편 코퍼스를 실측해 관측 최저값으로 정했다(근거 있음).
가이드는 코퍼스가 없어 실측 대상이 없었고, 최초 계획서의 '본문 6,000자'는
근거 없이 정한 숫자였다. 그대로 쓰면 임의의 기준으로 통과·탈락을 가르게 된다.

그래서 현재 기준은 이렇게 잡았다.
  · 구조 게이트(단계 수·확인/막히면·검증 영상·출처)  = 본질적 요건, 엄격 적용
  · 분량 게이트                                      = 영상 노트 코퍼스에 앵커링한 잠정값
     영상 노트 본문 중앙값 3,065자(공백 제외)를 기준으로,
     가이드는 그보다 얇으면 안 된다고 보아 3,000자를 잠정 하한으로 둔다.
  → 가이드 3건이 쌓이면 실측 분포로 재보정하고, 그때 근거를 여기에 남긴다.
     (LESSONS.md "게이트를 몰래 낮추지 말 것" — 낮춘 게 아니라 근거 없는 값을
      근거 있는 값으로 교체한 것이며, 그 사실을 이 주석과 출력에 남긴다.)

사용: python3 tools/verify_guide.py guides/<슬러그>/guide.md
"""
import re, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEVELS = {"입문", "중급", "고급"}

G = {
    "body_min":      3000,   # 잠정 — 영상 노트 중앙값 3,065자 앵커 (가이드 3건 후 재보정)
    "steps_min":        5,
    "pitfalls_min":     3,
    "sources_min":      5,
    "videos_min":       3,
    "summary_min":    100,
}


def check(path):
    txt = Path(path).read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', txt, re.S)
    if not m:
        return ["프론트매터 없음"], {}
    fm, body = m.groups()
    meta = {}
    for line in fm.split('\n'):
        if ': ' in line:
            k, v = line.split(': ', 1)
            meta[k.strip()] = v.strip()

    fails = []
    body_n  = len(re.sub(r'\s', '', body))
    steps   = re.findall(r'^##\s+\d단계', body, re.M)
    checks  = body.count('**화면에서 확인할 것**')
    stucks  = body.count('**막히면**')
    srcs    = len(re.findall(r'https?://', body))
    vids    = [v.strip() for v in meta.get('videos', '').strip('[]').split(',') if v.strip()]
    tags    = [t.strip() for t in meta.get('tags', '').strip('[]').split(',') if t.strip()]
    pit     = re.search(r'^##\s+흔히 막히는 지점(.*?)(?=^## |\Z)', body, re.S | re.M)
    pit_n   = len(re.findall(r'^\*\*\d+\.', pit.group(1), re.M)) if pit else 0

    M = {"body": body_n, "steps": len(steps), "checks": checks, "stucks": stucks,
         "sources": srcs, "videos": len(vids), "pitfalls": pit_n, "tags": len(tags)}

    if body_n < G["body_min"]:
        fails.append(f"본문 {body_n}자 < {G['body_min']} (잠정 기준)")
    if len(steps) < G["steps_min"]:
        fails.append(f"단계 {len(steps)} < {G['steps_min']}")
    if checks < len(steps):
        fails.append(f"'화면에서 확인할 것' {checks}개 < 단계 {len(steps)}개")
    if stucks < len(steps):
        fails.append(f"'막히면' {stucks}개 < 단계 {len(steps)}개")
    if pit_n < G["pitfalls_min"]:
        fails.append(f"'흔히 막히는 지점' {pit_n}개 < {G['pitfalls_min']}")
    if srcs < G["sources_min"]:
        fails.append(f"출처 링크 {srcs} < {G['sources_min']}")
    if len(vids) < G["videos_min"]:
        fails.append(f"관련 영상 {len(vids)} < {G['videos_min']}")
    if meta.get('level') not in LEVELS:
        fails.append(f"난이도 '{meta.get('level')}' 가 열거값 아님 ({'/'.join(sorted(LEVELS))})")
    if not re.search(r'^##\s+사전 준비물', body, re.M):
        fails.append("'사전 준비물' 섹션 없음")
    if not re.search(r'^##\s+관련 영상', body, re.M):
        fails.append("'관련 영상' 섹션 없음")
    if not re.search(r'^##\s+출처', body, re.M):
        fails.append("'출처' 섹션 없음")
    if not re.search(r'^##\s+다음으로 할 것', body, re.M):
        fails.append("'다음으로 할 것' 섹션 없음")
    for f in ("title", "date", "level", "minutes"):
        if not meta.get(f):
            fails.append(f"프론트매터 '{f}' 누락")

    # 관련 영상이 manifest에 검증된 값으로 캐시돼 있는지 (실재 확인 흔적)
    man = ROOT / "guides" / "manifest.json"
    if man.exists() and vids:
        d = json.loads(man.read_text(encoding='utf-8'))
        slug = Path(path).parent.name
        g = [x for x in d.get('guides', []) if x.get('slug') == slug]
        if g:
            cached = {v['id'] for v in g[0].get('videos', [])}
            missing = [v for v in vids if v not in cached]
            if missing:
                fails.append(f"manifest에 검증 캐시 없는 영상: {missing} (실재 확인 누락)")
    return fails, M


def main():
    paths = sys.argv[1:] or sorted(ROOT.glob("guides/*/guide.md"))
    bad = 0
    print("ℹ️  분량 게이트는 잠정값(영상 노트 중앙값 앵커). 가이드 3건 후 실측 재보정 예정.\n")
    for p in paths:
        fails, M = check(p)
        if fails:
            bad += 1
            print(f"❌ {Path(p).parent.name}")
            for f in fails:
                print(f"     · {f}")
        else:
            print(f"✅ {Path(p).parent.name}")
            print(f"   본문 {M['body']}자 · 단계 {M['steps']} · 확인 {M['checks']} · 막히면 {M['stucks']} · "
                  f"막히는지점 {M['pitfalls']} · 영상 {M['videos']} · 출처 {M['sources']} · 태그 {M['tags']}")
    print(f"\n{len(paths)}건 검사 · 통과 {len(paths)-bad} · 실패 {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
