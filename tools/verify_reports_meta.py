#!/usr/bin/env python3
"""reports/manifest.json 이 report.md 와 어긋났는지 잰다 — **다시 짓지는 않는다.**

왜 rebuild 빌더가 아닌가 (2026-09-09).
    `verify_builders` 를 네 서가로 넓히며 「reports 에는 rebuild 빌더가 없다, 만드는 것이 다음
    회차」라고 적었다. 만들려고 재 봤더니 **필드마다 사정이 달랐다.**

    | 필드 | 소스 | 다시 지을 수 있나 |
    |---|---|---|
    | `date`    | frontmatter `날짜` (72/72 일치) | 예 → 잠근다 |
    | `depth`   | frontmatter `깊이` (72/72) | 예 → 잠근다 |
    | `tags`    | frontmatter `태그` | 예 → 잠근다 |
    | `sources` | frontmatter `소스수` **와 실제 `## 출처` 목록** (72/72 파싱) | **값은 잠근다**(아래 ⚠) |
    | `title`   | `주제` + 접미사인데 규칙이 셋이고 일부는 손질됨 | 아니오 → 허용목록으로 반만 |
    | `tldr`    | 본문 `## TL;DR` 절과 **다른 문장**이다 | 아니오 |
    | `cover`   | **소스가 아예 없다**(72편 중 1편만 보유) | 아니오 |

    ⚠ **`sources` 를 한 번 잘못 분류했다(2026-09-09 검수가 잡았다).** manifest 표기가
    `int` 12편 / `dict` 60편으로 갈려 있는 것을 보고 「소스가 없다」로 묶었는데, 그것은
    **manifest 쪽 표기 불일치**일 뿐이고 값은 `소스수` 에서 그대로 나온다.
    **형태 통일(사람 몫)과 값 대조(기계 몫)는 별개인데 하나로 묶어 값 대조까지 포기했었다.**
    대조를 넣자마자 어긋남 5편이 나왔고, 그중 **넷은 `report.md` 의 `소스수` 가 거짓**이었다
    (정본이라고 선언한 쪽이 틀린 자리다). 표기 통일은 여전히 사람이 정할 일이라 여기서는
    두 형태를 모두 받아 **숫자만** 본다.

    `title`·`tldr` 을 규칙 하나로 다시 지었으면 **갤러리 카드에 그대로 나가는 제목 16개와
    요약 72개를 덮었을 것**이다. 그래서 rebuild 대신 대조로 방향을 바꿨다.

    ⚠⚠ **그리고 한 번 더 틀렸다(같은 날 두 번째 검수).** 위 대조는 `소스수` 와 manifest 라는
    **사본 둘**만 맞대 본다 — 그래서 **둘이 함께 틀리면 초록이었다.** 실제 `## 출처` 목록을
    세어 보니 두 편이 그 상태로 통과하고 있었다(`chrome-extensions-work` 13≠14,
    `jacobian-advanced` 16≠15). 사본끼리의 합치는 사실이 아니다 — **세 번째 증인**으로
    목록 자체를 센다(아래 ④-b). `tldr` 이 본문에 적어 둔 출처 수도 같은 이유로 본다(④-c):
    사본을 고치고 문장을 안 따라가면 카드 한 장 안에서 숫자가 엇갈린다(실제로 그랬다).

무엇을 잠그나 (FAIL).
    ① manifest ↔ 디스크 양방향 고아 · ② `path` · ③ `date`·`depth`·`tags`
    ④ `sources` — (a) manifest ↔ `소스수` · (b) `소스수` ↔ **실제 `## 출처` 목록 항목 수**
      · (c) `tldr` 이 문장으로 적은 출처 수
    ⑤ `cover` 가 가리키는 파일의 실재
    ⑥ **소스에 그 필드가 아예 없는 것도 FAIL** 이다 — 「소스가 없다」와 「소스가 맞다」를 같은
      결과로 내보내면 frontmatter 를 통째로 날린 파일이 초록으로 지나간다(첫 판이 그랬다).
    ⑦ `title` 은 **손질 허용목록** 밖에서 `주제` 로 시작하지 않으면 FAIL — 56편이 잠긴다.

무엇을 못 잡나 — 여기 적어 두는 이유는 초록이 그 자리까지 보증하는 것처럼 읽히기 때문이다.
    `tldr` 의 **문장 내용**(출처 수만 본다 — 나머지는 소스와 다른 문장이라 기준이 없다) ·
    `cover` 의 유무 자체 · 허용목록에 실린 16편의 `title` 내용 ·
    `sources` 의 **표기 형태**(int/dict) · 최상위 `generated`(아무도 안 읽는다) ·
    출처 목록의 **국내/해외 갈래**(항목 수만 세고 어느 구획에 있는지는 안 본다 —
    `jacobian-advanced` 는 네이버 블로그가 `**해외**` 아래 있었다. `소스수` 의 국내·해외를
    서로 맞바꿔도 총계가 같으면 통과한다) ·
    **출처 항목의 실재**(URL 없이 「국내 블로그 다수」처럼 뭉뚱그린 줄도 한 항목으로 센다 —
    `ai-engineering-evolution-graph` 가 그렇다. 무환각 잣대는 사람이 볼 일이다).

쓰기.
    python3 tools/verify_reports_meta.py            # 게이트 (어긋나면 exit 1)
    python3 tools/verify_reports_meta.py --report   # 보고만, 언제나 exit 0
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = ROOT / 'reports/manifest.json'
USAGE = '쓰기: python3 tools/verify_reports_meta.py [--report]'

# 카드용으로 손질돼 `주제` 와 다른 제목들. 손질이 나은 경우가 있어 되돌리지 않는다
# (예: 주제 「부정형을 미분으로 뚫는 법」 → 카드 「0/0·∞/∞을 미분으로 뚫는 법」).
# ⚠ 목록에 넣는 것은 **그 편의 제목 대조를 포기한다**는 뜻이다. 새 보고서를 여기 넣지 말 것 —
#   그러라고 있는 목록이 아니라, 이미 손질된 것을 기록해 **나머지 56편을 잠그려고** 있는 것이다.
RESHAPED_TITLES = {
    'ai-engineering-evolution-graph', 'gemini-spark-agent', 'hermes-agent-windows',
    'infinity-set-theory', 'infinity-set-theory-advanced', 'jacobian-advanced',
    'lhopital-rule', 'math-function-terms-advanced', 'matrix-diagonalization',
    'matrix-multivariable-advanced', 'milk-yogurt-history', 'n8n-automation-guide',
    'polynomial-functions-advanced', 'prosecution-reform-2026',
    'spherical-geometry-curvature-advanced', 'vector',
}


def split_note(path):
    """(frontmatter, 본문). 실제 출처 목록을 세려면 본문이 필요하다."""
    s = path.read_text(encoding='utf-8')
    if s.startswith('---'):
        parts = s.split('---', 2)
        return parts[1], (parts[2] if len(parts) > 2 else '')
    return '', s


def field(fm, key):
    # ⚠ `\s*` 를 쓰면 re.M 에서도 **개행을 먹어** 빈 값이 다음 줄을 훔친다
    #   (`태그:` 만 있으면 그 아래 `소스수:` 줄이 태그 값으로 잡혔다 — 2026-09-09 검수).
    m = re.search(r'^%s:[^\S\n]*(.*)$' % re.escape(key), fm, re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"') or None


def taglist(raw):
    return [t.strip() for t in (raw or '').strip('[]').split(',') if t.strip()]


def src_counts(fm):
    kr = re.search(r'국내\s*:\s*(\d+)', fm)
    it = re.search(r'해외\s*:\s*(\d+)', fm)
    return (int(kr.group(1)), int(it.group(1))) if kr and it else None


def listed_sources(body):
    """`## 출처` 절의 실제 항목 수. 못 읽으면 None (그 경우도 FAIL 로 보고한다).

    ⚠ 절 제목을 `출처` 로 **줄머리에 고정**해야 한다. `^##.*출처` 로 느슨하게 잡으면
      `## 10. 배포 3단계 — 출처만 바뀐다` 같은 본문 절이 먼저 걸려 「파싱 불가」가 된다
      (첫 판이 그래서 claude-plugins-build 를 못 읽었다).
    ⚠ 표기가 두 가지다 — `- [12] …` 와 `1. (국내) …`. 둘 다 읽고 많이 잡히는 쪽을 쓴다.
      라벨에 글자가 섞인 것도 항목이다(`jacobian-advanced` 의 `[J6]`).
    ⚠ **라벨 없는 `- 매체 「제목」 — URL` 도 항목이다.** 처음에는 `- [n]` 만 셌는데,
      그러면 라벨 없이 붙인 출처가 **세 사본 어디에도 안 세어진다** — `hermes-agent-quick`
      이 실제로 그 상태였다(목록 8인데 셋 다 6). 세 번째 증인을 두는 뜻이 없어지므로
      줄머리 `- ` 를 전부 센다. 각주 정의(`- [^라벨]:`)만 뺀다.
    """
    m = re.search(r'^##\s*출처[^\n]*\n(.*?)(?=^## |\Z)', body, re.M | re.S)
    if not m:
        return None
    sec = m.group(1)
    dashed = re.findall(r'^-\s+(?!\[\^)\S', sec, re.M)
    numbered = re.findall(r'^\s*\d+\.\s', sec, re.M)
    n = max(len(dashed), len(numbered))
    return n or None


def tldr_claim(tldr, kr, intl):
    """tldr 이 문장으로 적은 출처 수가 실제와 다르면 그 문구를 돌려준다.

    세 표기를 쓴다 — `출처 13(국내5·해외8)` · `14개 출처` · `출처 14개`.
    사본(소스수·manifest)을 고치고 이 문장을 안 따라가면 **카드 한 장 안에서 숫자가
    엇갈린다** — 실제로 네 편이 그랬다(2026-09-09 검수).

    ⚠ 첫 판은 `(국내a·해외b)` 를 **캡처해 놓고 총계만 비교했다.** 총계가 맞으면
      내역이 뒤바뀌어도 통과한다(검수가 심어서 보였다). 잡은 값은 다 쓴다.
    """
    total = kr + intl
    off = []
    m = re.search(r'출처\s*(\d+)\s*\(국내\s*(\d+)[^0-9]*해외\s*(\d+)\)', tldr or '')
    if m and (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (total, kr, intl):
        off.append(m.group(0))
    for pat in (r'(\d+)\s*개\s*출처', r'출처\s*(\d+)\s*개'):
        for mm in re.finditer(pat, tldr or ''):
            if int(mm.group(1)) != total:
                off.append(mm.group(0))
    return off


def man_counts(v):
    """manifest 는 int 와 dict 두 형태를 쓴다. 표기 통일은 사람 몫이라 값만 본다."""
    if isinstance(v, dict):
        return v.get('kr'), v.get('intl')
    if isinstance(v, int):
        return None, v          # 합계만 아는 형태
    return None, None


def main(argv):
    args = argv[1:]
    if {'-h', '--help'} & set(args):
        print(__doc__.strip())
        return 0
    report_only = '--report' in args
    unknown = [a for a in args if a != '--report']
    if unknown:
        print('모르는 인자: %s\n%s' % (' '.join(unknown), USAGE))
        return 2

    data = json.loads(MAN.read_text(encoding='utf-8'))
    entries = data.get('reports', [])
    on_disk = {p.parent.name for p in (ROOT / 'reports').glob('*/report.md')}
    in_man = {r.get('slug') for r in entries}

    bad = []
    for slug in sorted(in_man - on_disk):
        bad.append('%s — manifest 에 있는데 report.md 가 없다' % slug)
    for slug in sorted(on_disk - in_man):
        bad.append('%s — report.md 가 있는데 manifest 에 없다 (갤러리에 안 뜬다)' % slug)

    suffix, reshaped, shapes = {}, [], {}
    for r in sorted(entries, key=lambda x: x.get('slug', '')):
        slug = r.get('slug')
        if not slug:
            bad.append('%r — slug 가 없는 항목' % r.get('title', '?'))
            continue
        p = ROOT / 'reports' / slug / 'report.md'
        want = 'reports/%s/report.md' % slug
        if r.get('path') != want:
            bad.append('%s — path 가 %r 인데 실제는 %r' % (slug, r.get('path'), want))
        if not p.is_file():
            continue
        fm, body = split_note(p)

        # ── 소스가 있는 것: 잠근다. **없는 것도 FAIL** 이다(있는 줄 알고 통과시키면 안 된다).
        for mkey, fkey in (('date', '날짜'), ('depth', '깊이')):
            src = field(fm, fkey)
            if src is None:
                bad.append('%s — 소스에 `%s:` 가 없다 (게이트가 잠글 대상이 사라진다)' % (slug, fkey))
            elif src != r.get(mkey):
                bad.append('%s — %s: manifest %r ≠ 소스 %r' % (slug, mkey, r.get(mkey), src))

        raw_tags = field(fm, '태그')
        if raw_tags is None:
            bad.append('%s — 소스에 `태그:` 가 없다' % slug)
        else:
            src_tags = taglist(raw_tags)
            if src_tags != r.get('tags'):
                only_src = [t for t in src_tags if t not in (r.get('tags') or [])]
                only_man = [t for t in (r.get('tags') or []) if t not in src_tags]
                how = '순서만 다름' if not (only_src or only_man) else ' · '.join(filter(None, [
                    ('소스에만 %s' % only_src) if only_src else '',
                    ('manifest 에만 %s' % only_man) if only_man else '']))
                bad.append('%s — tags: %s' % (slug, how))

        sc = src_counts(fm)
        if sc is None:
            bad.append('%s — 소스에 `소스수: { 국내, 해외 }` 가 없다' % slug)
        else:
            m_kr, m_it = man_counts(r.get('sources'))
            if m_kr is None and m_it is not None:          # 합계만 있는 형태
                if m_it != sc[0] + sc[1]:
                    bad.append('%s — sources: manifest 합 %s ≠ 소스 %d+%d=%d'
                               % (slug, m_it, sc[0], sc[1], sc[0] + sc[1]))
            elif (m_kr, m_it) != sc:
                bad.append('%s — sources: manifest {국내 %s, 해외 %s} ≠ 소스 {국내 %d, 해외 %d}'
                           % (slug, m_kr, m_it, sc[0], sc[1]))

            # (b) **세 번째 증인** — 사본 둘이 함께 틀린 것을 여기서 잡는다.
            total = sc[0] + sc[1]
            listed = listed_sources(body)
            if listed is None:
                bad.append('%s — `## 출처` 절의 항목을 못 읽었다 (표기가 새로 생겼으면 '
                           'listed_sources 를 늘릴 것 — 못 세는 것을 통과로 두지 않는다)' % slug)
            elif listed != total:
                bad.append('%s — 소스수 %d(국내 %d·해외 %d) 인데 `## 출처` 목록은 %d항목이다'
                           % (slug, total, sc[0], sc[1], listed))

            # (c) 카드에 보이는 문장까지 같은 수인가
            for phrase in tldr_claim(r.get('tldr'), sc[0], sc[1]):
                bad.append('%s — tldr 의 「%s」 가 실제 %d(국내 %d·해외 %d) 과 다르다 '
                           '(카드 안에서 숫자가 엇갈린다)' % (slug, phrase, total, sc[0], sc[1]))

        # ⚠ cover 는 **보고서 폴더 기준**이다(`comics/card.png`). 유일한 소비자인
        #   `research/index.html:502` 이 `r.path` 의 폴더에 이어 붙이므로 그 기준만 옳다.
        #   리포 루트 폴백을 뒀다가 검수가 잡았다 — **렌더러가 못 읽는 형태를 게이트가
        #   통과시키면 게이트가 거짓을 보증한다.**
        cover = r.get('cover')
        if cover and not (p.parent / cover).is_file():
            bad.append('%s — cover 가 가리키는 %r 가 보고서 폴더에 없다 (갤러리가 못 읽는다)'
                       % (slug, cover))

        # ── title: 손질 허용목록 밖은 잠근다
        topic = field(fm, '주제')
        if topic is None:
            bad.append('%s — 소스에 `주제:` 가 없다' % slug)
        else:
            title = r.get('title', '')
            starts = title.startswith(topic)
            key = title[len(topic):] if starts else '<손질됨>'
            suffix[key] = suffix.get(key, 0) + 1
            if not starts:
                reshaped.append(slug)
                if slug not in RESHAPED_TITLES:
                    bad.append('%s — title 이 `주제` 로 시작하지 않는다. 의도된 손질이면 '
                               'RESHAPED_TITLES 에 넣고, 아니면 둘 중 하나를 고칠 것\n'
                               '        주제: %s\n        카드: %s' % (slug, topic, title))
            elif slug in RESHAPED_TITLES:
                bad.append('%s — RESHAPED_TITLES 에 있는데 지금은 `주제` 로 시작한다 (목록에서 뺄 것)'
                           % slug)
        shapes[type(r.get('sources')).__name__] = shapes.get(type(r.get('sources')).__name__, 0) + 1

    print('reports %d편 · manifest %d편' % (len(on_disk), len(entries)))
    print()
    print('── 이 검사기도 verify_builders 도 못 잡는 자리 ' + '─' * 20)
    print('  title  = 주제 + %s' % ' · '.join('%r×%d' % (k, v) for k, v in
                                              sorted(suffix.items(), key=lambda x: -x[1])))
    print('         손질 허용목록 %d편 — 그 편들의 제목 내용은 아무도 안 본다' % len(reshaped))
    print('  sources 표기가 %s 로 갈려 있다 — **값은 위에서 잠갔고 형태 통일만 사람 몫이다**'
          % ', '.join('%s %d편' % (k, v) for k, v in sorted(shapes.items())))
    print('  tldr 은 본문 `## TL;DR` 절과 **다른 문장**이라 문장 내용은 기준이 없다')
    print('         — 다만 거기 적힌 **출처 수**는 위에서 잠갔다.  cover 는 소스가 없다.')
    print('  출처 목록의 국내/해외 **갈래**는 안 본다 — 항목 수만 센다.')
    print('  최상위 `generated` 는 아무 빌더도 갤러리도 안 읽는다.')
    print()

    if bad:
        print('FAIL — 소스와 어긋난 곳 %d건:' % len(bad))
        for b in bad:
            print('  ✗ %s' % b)
        print('\n  정본은 report.md 다(CLAUDE.md 「단일 진실의 원천」) — 다만 소스가 틀린 적도 있다.')
        print('  실제 출처 목록을 세어 어느 쪽이 거짓인지 확인하고 고칠 것.')
        return 0 if report_only else 1

    print('OK — date · depth · tags · sources(사본 둘 + 실제 목록 + tldr) · title · path ·')
    print('     cover · 고아 모두 소스와 일치한다.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
