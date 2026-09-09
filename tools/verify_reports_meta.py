#!/usr/bin/env python3
"""reports/manifest.json 이 report.md 와 어긋났는지 잰다 — **다시 짓지는 않는다.**

왜 rebuild 빌더가 아닌가 (2026-09-09, 실측하고 방향을 바꿨다).
    `verify_builders` 를 네 서가로 넓히며 「reports 에는 소스에서 다시 짓는 빌더가 없다,
    만드는 것이 다음 회차」라고 적었다. 그래서 만들려고 **먼저 쟀더니 만들면 안 되는 것**이었다.
    manifest 의 필드가 소스에서 기계적으로 나오지 않는다:

    | 필드 | 소스와의 관계 | 다시 지을 수 있나 |
    |---|---|---|
    | `date`   | frontmatter `날짜` 와 **72/72 일치** | 예 → 여기서 게이트로 잰다 |
    | `depth`  | frontmatter `깊이` 와 **72/72 일치** | 예 → 게이트 |
    | `tags`   | frontmatter `태그` (드리프트 7편을 이 검사기가 처음 찾았다) | 예 → 게이트 |
    | `title`  | `주제` + `' (DEEP)'` 32편 · 접미사 없음 24편 · **아예 손질된 것 16편** | **아니오** |
    | `sources`| `소스수` 에서 오는데 manifest 타입이 **int 12 / dict 60** 으로 갈림 | 아니오(형태 미통일) |
    | `tldr`   | **71/72 가 본문 어디에도 없다 — 손으로 쓴 문장** | 아니오 |
    | `cover`  | 소스 없음(72편 중 1편만 보유) | 아니오 |

    즉 「rebuild」를 밀어붙였으면 **손으로 다듬은 카드 제목 16개와 손으로 쓴 tldr 71개를
    덮어썼을 것이다.** 갤러리 카드에 그대로 나가는 문장들이다. 그래서 방향을 바꿨다 —
    **소스가 있는 것만 게이트로 잠그고, 없는 것은 「없다」고 보고한다.**
    (`title` 을 한 규칙으로 통일하고 `sources` 형태를 맞추는 것은 발행물의 표시가 바뀌는
     일이라 사람이 정할 자리다. 이 검사기는 그 판단을 대신하지 않고 목록만 보여 준다.)

무엇을 잠그나 (FAIL).
    ① manifest ↔ 디스크 양방향 고아(`reports/<슬러그>/report.md` 유무)
    ② `path` 가 실제 경로와 다른가
    ③ `date` · `depth` · `tags` 가 frontmatter 와 다른가

무엇을 보고만 하나 (통과에 영향 없음).
    `title` 접미사 분포와 손질된 편 · `sources` 타입 분열 · `tldr`/`cover` 는 소스가 없다는 사실.
    ⚠ **이 셋은 이 검사기도 `verify_builders` 도 못 잡는다.** 보고서 제목이나 요약을 고쳐도
    manifest 는 그대로일 수 있고, 그것을 잡을 방법은 지금 리포에 없다.

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


def frontmatter(path):
    s = path.read_text(encoding='utf-8')
    return s.split('---', 2)[1] if s.startswith('---') else ''


def field(fm, key):
    m = re.search(r'^%s:\s*(.+)$' % re.escape(key), fm, re.M)
    return m.group(1).strip().strip('"') if m else None


def taglist(raw):
    return [t.strip() for t in (raw or '').strip('[]').split(',') if t.strip()]


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
    entries = data['reports']
    on_disk = {p.parent.name for p in (ROOT / 'reports').glob('*/report.md')}
    in_man = {r['slug'] for r in entries}

    bad = []
    for slug in sorted(in_man - on_disk):
        bad.append('%s — manifest 에 있는데 report.md 가 없다' % slug)
    for slug in sorted(on_disk - in_man):
        bad.append('%s — report.md 가 있는데 manifest 에 없다 (갤러리에 안 뜬다)' % slug)

    suffix = {}
    reshaped, shapes = [], {}
    for r in sorted(entries, key=lambda x: x['slug']):
        slug = r['slug']
        p = ROOT / 'reports' / slug / 'report.md'
        want = 'reports/%s/report.md' % slug
        if r.get('path') != want:
            bad.append('%s — path 가 %r 인데 실제는 %r' % (slug, r.get('path'), want))
        if not p.is_file():
            continue
        fm = frontmatter(p)

        # ── 소스가 있는 셋: 잠근다
        for mkey, fkey in (('date', '날짜'), ('depth', '깊이')):
            src = field(fm, fkey)
            if src is not None and src != r.get(mkey):
                bad.append('%s — %s: manifest %r ≠ 소스 %r' % (slug, mkey, r.get(mkey), src))
        src_tags = taglist(field(fm, '태그'))
        if src_tags and src_tags != r.get('tags'):
            only_src = [t for t in src_tags if t not in r.get('tags', [])]
            only_man = [t for t in r.get('tags', []) if t not in src_tags]
            how = '순서만 다름' if not (only_src or only_man) else (
                ' · '.join(filter(None, [
                    ('소스에만 %s' % only_src) if only_src else '',
                    ('manifest 에만 %s' % only_man) if only_man else ''])))
            bad.append('%s — tags: %s' % (slug, how))

        # ── 소스가 없거나 규칙이 하나가 아닌 것: 세기만 한다
        topic = field(fm, '주제') or ''
        suffix[r['title'][len(topic):] if r['title'].startswith(topic) else '<손질됨>'] = \
            suffix.get(r['title'][len(topic):] if r['title'].startswith(topic) else '<손질됨>', 0) + 1
        if not r['title'].startswith(topic):
            reshaped.append(slug)
        shapes[type(r.get('sources')).__name__] = shapes.get(type(r.get('sources')).__name__, 0) + 1

    print('reports %d편 · manifest %d편' % (len(on_disk), len(entries)))
    print()
    print('── 보고만 (이 검사기도 verify_builders 도 못 잡는 자리) ' + '─' * 12)
    print('  title  = 주제 + %s' % ' · '.join('%r×%d' % (k, v) for k, v in
                                              sorted(suffix.items(), key=lambda x: -x[1])))
    if reshaped:
        print('         손질된 %d편: %s%s' % (len(reshaped), ', '.join(reshaped[:6]),
                                            ' …' if len(reshaped) > 6 else ''))
    print('  sources 타입 분열: %s  (소스는 `소스수: { 국내, 해외 }` 하나뿐이다)'
          % ', '.join('%s %d편' % (k, v) for k, v in sorted(shapes.items())))
    print('  tldr · cover 는 소스가 없다 — 손으로 쓴 것이라 고쳐도 아무 게이트가 안 잡는다.')
    print()

    if bad:
        print('FAIL — 소스와 어긋난 곳 %d건:' % len(bad))
        for b in bad:
            print('  ✗ %s' % b)
        print('\n  manifest 를 소스에 맞추거나, 소스가 틀렸으면 report.md 를 고칠 것.')
        print('  (정본은 report.md 다 — CLAUDE.md 「단일 진실의 원천」.)')
        return 0 if report_only else 1

    print('OK — date · depth · tags · path · 양방향 고아 모두 소스와 일치한다.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
