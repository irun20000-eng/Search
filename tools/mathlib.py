#!/usr/bin/env python3
"""
수학사 섹션(math/) 공용 유틸.

verify_math.py / build_math_manifest.py / build_link_index.py /
sync_math_obsidian.py 가 공유한다. 별칭 생성·위키링크 해석 규칙이
스크립트마다 갈라지면 "웹에서는 연결되는데 검증에서는 미해결"
같은 어긋남이 생기므로 한 곳에 모은다.

의존: PyYAML (frontmatter가 중첩 구조 — 발전단계·출처·이미지)
"""
import re
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MATH = ROOT / "math"
NOTES = MATH / "notes"

TYPES = {"개념", "인물", "일화", "세기"}
TRACKS = {"이해편", "확장편"}
FACTUALITY = {"확실", "전승", "창작의심"}
TRACK_RE = r"(?:이해편|확장편)"


# ── 기본 문자열 처리 ──────────────────────────────────────────────

def norm(s):
    """공백 정규화. 위키링크 대상과 별칭을 같은 잣대로 비교하기 위함."""
    return re.sub(r"\s+", " ", str(s)).strip()


def strip_gloss(s):
    """괄호 병기 제거.  '야코비안 변환(Jacobian)' → '야코비안 변환'

    본문 위키링크는 영문 병기를 뺀 짧은 형태를 쓰는 경우가 많다
    ([[야코비안 변환 확장편]] ↔ '야코비안 변환(Jacobian) — 확장편(학부·대학원)').
    """
    return norm(re.sub(r"\s*\([^)]*\)\s*", " ", s))


# ── 노트 읽기 ────────────────────────────────────────────────────

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)


def split_frontmatter(text, strict=True):
    """(frontmatter dict, body str) 반환. frontmatter가 없으면 ({}, text).

    strict=True  — math/ 노트용. YAML이 깨져 있으면 ValueError.
    strict=False — 기존 reports/ 스캔용. 일부 리포트의 frontmatter는 값 안의
                   콜론이 인용되지 않아 유효한 YAML이 아니다
                   (예: '주제: 벡터(Vector) — 확장편: 벡터공간에서…').
                   본문만 필요할 때는 파싱 실패를 무시하고 넘어간다.
    """
    m = FM_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        if strict:
            raise ValueError("frontmatter YAML 파싱 실패: %s" % e)
        return {}, m.group(2)
    if not isinstance(fm, dict):
        if strict:
            raise ValueError("frontmatter가 매핑이 아님")
        return {}, m.group(2)
    return fm, m.group(2)


def body_of(text):
    """frontmatter를 파싱하지 않고 본문만 떼어낸다."""
    m = FM_RE.match(text)
    return m.group(2) if m else text


def read_note(path, strict=True):
    return split_frontmatter(Path(path).read_text(encoding="utf-8"), strict=strict)


def iter_notes(notes_dir=NOTES):
    """math/notes/<slug>/note.md 를 슬러그 순으로 순회."""
    if not Path(notes_dir).exists():
        return
    for d in sorted(Path(notes_dir).iterdir()):
        f = d / "note.md"
        if d.is_dir() and f.exists():
            yield d.name, f


# ── 별칭 ────────────────────────────────────────────────────────

def aliases_for_math(fm):
    """수학사 노트의 위키링크 별칭 집합.

    math/ 는 우리가 규약을 정하므로 결정적으로 만든다 — 추측 매칭 없음.
    """
    out = set()
    for key in ("제목", "슬러그", "볼트파일명"):
        v = fm.get(key)
        if v:
            out.add(norm(v))
    for v in (fm.get("별칭") or []):
        if v:
            out.add(norm(v))
    # 개념은 '미분법 이해편' / '미분법 확장편' 형태도 받는다
    track = fm.get("트랙")
    title = fm.get("제목")
    if track in TRACKS and title:
        t = norm(title)
        out.add("%s %s" % (t, track))
        out.add("%s%s" % (t, track))
    return {a for a in out if a}


def aliases_for_report(title, slug):
    """기존 reports/ 의 별칭 집합 (제목 형식이 5가지로 제각각이라 정규화한다).

      '행렬과 다변수 미적분 — 이해편(입문·딥)'
      '야코비안 변환(Jacobian) — 확장편(학부·대학원)'
      '벡터(Vector) — 왜 배우고, 어디까지 가나 (이해편)'
      '미적분의 발견 (이해편) — 배로·뉴턴·라이프니츠… (DEEP)'

    추측 매칭(부분일치·유사도)은 쓰지 않는다. 틀린 링크가 미해결 링크보다 나쁘다.
    해결되지 않는 것은 link-aliases.json 에 손으로 적어 넣는다.
    """
    out = set()
    t = norm(title)
    out.add(t)

    t = norm(re.sub(r"\s*\((?:DEEP|QUICK)\)\s*$", "", t))
    out.add(t)

    m = re.search(TRACK_RE, t)
    track = m.group(0) if m else None

    head = norm(re.split(r"\s+[—–]\s+", t)[0])
    head = norm(re.sub(r"\s*\(" + TRACK_RE + r"\)\s*$", "", head))
    head = norm(re.sub(r"\s*" + TRACK_RE + r"\s*$", "", head))

    for base in {head, strip_gloss(head)}:
        if not base:
            continue
        out.add(base)
        if track:
            out.add("%s %s" % (base, track))
            out.add("%s%s" % (base, track))

    out.add(slug)
    return {a for a in out if a}


def prefer_intro(slug_a, slug_b):
    """맨 제목([[행렬의 대각화]])이 이해편·확장편 양쪽에 걸릴 때 이해편을 고른다.

    맨 제목은 그 주제의 '입구'를 가리키는 것으로 본다.
    """
    a_adv = slug_a.endswith("-advanced")
    b_adv = slug_b.endswith("-advanced")
    if a_adv != b_adv:
        return slug_b if a_adv else slug_a
    return sorted([slug_a, slug_b])[0]


# ── 본문 분석 ────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"\[\[([^\]\[|]+?)(?:\|([^\]\[]*))?\]\]")


def extract_wikilinks(body):
    """[(대상, 표시텍스트)] 반환. 코드블록/인라인코드 안은 제외."""
    stripped = strip_code(body)
    out = []
    for m in WIKILINK_RE.finditer(stripped):
        target = norm(m.group(1))
        label = norm(m.group(2)) if m.group(2) else target
        if target:
            out.append((target, label))
    return out


def strip_code(body):
    """펜스 코드블록과 인라인 코드를 공백으로 치환 (길이 보존은 하지 않음)."""
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = re.sub(r"`[^`\n]*`", " ", body)
    return body


def extract_citations(body):
    """본문에서 쓰인 인용 번호 집합. [1] [3][7] 형태."""
    out = set()
    for m in re.finditer(r"\[(\d{1,3})\]", strip_code(body)):
        out.add(int(m.group(1)))
    return out


def parse_body_sources(body):
    """기존 reports/ 용 — 본문 '## 출처' 섹션에서 {번호: 텍스트} 추출.

    math/ 노트는 frontmatter의 출처가 원본이고 본문 섹션은 렌더러가 만든다.
    """
    m = re.search(r"^##+\s*출처\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).split("\n"):
        mm = re.match(r"^\s*(?:\[(\d{1,3})\]|(\d{1,3})[.)])\s+(.*)$", line)
        if mm:
            num = int(mm.group(1) or mm.group(2))
            out[num] = norm(mm.group(3))
    return out


def count_sections(body):
    """'## ' 로 시작하는 절 개수 (LESSONS.md의 측정 방식과 동일)."""
    return len(re.findall(r"^##\s+\S", body, re.M))


def count_chars(body):
    """자수 = 공백 포함 문자 수.  LC_ALL=C.UTF-8 wc -m 과 같은 기준.

    LESSONS.md가 게이트 수치를 이 공식으로 정했으므로 검사도 같은 공식을 쓴다.
    """
    return len(body)


def count_lines(body):
    return len(body.rstrip("\n").split("\n"))


def count_visuals(body):
    """시각화 개수 = 마크다운 표 + 이미지/그림.

    calculus-discovery 가 표 7 + 다이어그램 3 으로 게이트를 통과한 전례를 따른다.
    표는 구분선(|---|)이 있는 블록 하나를 1점으로 센다.
    """
    b = re.sub(r"```.*?```", " ", body, flags=re.S)
    tables = len(re.findall(r"^\s*\|[\s:|-]+\|\s*$", b, re.M))
    images = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", b))
    figures = len(re.findall(r"<figure\b", b))
    return tables + images + figures


# ── 링크 인덱스 ──────────────────────────────────────────────────

def load_link_index(path=None):
    """{별칭: 항목} 조회표. link-index.json 은 alias(별칭→항목인덱스) 형태로 저장한다."""
    p = Path(path) if path else (ROOT / "link-index.json")
    if not p.exists():
        return {}
    d = json.loads(p.read_text(encoding="utf-8"))
    entries = d.get("entries", [])
    return {norm(a): entries[i]
            for a, i in d.get("alias", {}).items()
            if isinstance(i, int) and 0 <= i < len(entries)}


def dump_json(path, obj):
    # newline="\n" 이 없으면 윈도우에서 \n 이 \r\n 으로 바뀐다.
    # 그러면 내용이 같아도 빌드를 돌릴 때마다 파일 전체가 바뀐 것으로 잡힌다
    # (블롭은 .gitattributes 가 LF 로 정규화하므로 작업본만 어긋난다).
    Path(path).write_text(
        json.dumps(obj, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8", newline="\n"
    )
