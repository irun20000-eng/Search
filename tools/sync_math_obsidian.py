#!/usr/bin/env python3
"""
math/notes/*/note.md → 옵시디언 볼트 002-수학사/

볼트 규약(실측):
    000-수집/00X-분류/        분류 폴더는 번호 접두
    Concepts/                 원자 노트 1,598편 (평면)
    _MOC/_MOC_<주제>.md       지도 노트

■ 폴더·파일명을 정한 근거
  · 002-수학사 — 001-주제리서치 다음 번호. 00x 대역이 주제 리서치 계열이다.
  · 파일명에 유형 접두어(개념_/인물_/일화_/세기_)를 붙인다.
    001-주제리서치는 <YYYYMMDD>_제목 을 쓰지만 수학사는 참고자료라 수집일이
    의미가 없다. 더 중요한 이유는 위키링크 충돌 방지다 — Concepts/ 에 1,598편이
    있어 [[미분법]]이 모호해질 수 있으나 [[개념_미분법]]은 충돌하지 않는다.

■ 이미지
  본문의 상대경로(../../assets/figures/x.svg)는 볼트에서 깨지므로,
  참조된 자산을 002-수학사/_assets/ 로 복사하고 링크를 ../_assets/x.svg 로 고친다.
  (노트가 02-개념/ 안에 있으므로 ../_assets/ 가 맞는 상대경로다.)

사용:
  python3 tools/sync_math_obsidian.py            # 볼트에 쓴다
  python3 tools/sync_math_obsidian.py --dry-run  # 무엇이 바뀌는지만 본다
  python3 tools/sync_math_obsidian.py --vault <경로>
"""
import sys
import re
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mathlib as M          # noqa: E402

DEFAULT_VAULT = Path(r"G:\내 드라이브\00_Obsidian_Second Brain\Insight Miner")
SUBDIR = {"세기": "01-세기", "개념": "02-개념", "인물": "03-인물", "일화": "04-일화"}
GALLERY = "https://irun20000-eng.github.io/Search/math/#n="


def vault_paths(vault):
    root = Path(vault) / "000-수집" / "002-수학사"
    return root, root / "_assets", Path(vault) / "000-수집" / "_MOC" / "_MOC_수학사.md"


def transform(fm, body, slug):
    """볼트용 본문. 이미지 경로를 고치고 갤러리 역링크를 머리에 붙인다."""
    body = re.sub(r"!\[([^\]]*)\]\((?:\.\./)+assets/([^)]+)\)",
                  lambda m: "![%s](../_assets/%s)" % (m.group(1), Path(m.group(2)).name),
                  body)
    head = "> [!info] 수학사 아카이브\n> 갤러리에서 보기 — %s%s\n\n" % (GALLERY, slug)
    # 첫 H1 바로 뒤에 넣는다
    m = re.match(r"(\s*#\s+[^\n]*\n)", body)
    if m:
        return m.group(1) + "\n" + head + body[m.end():]
    return head + body


def fm_block(fm):
    """볼트 노트의 frontmatter — 원본 그대로 쓰되 YAML 안전하게 다시 덤프한다."""
    import yaml
    return "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False,
                                    default_flow_style=False, width=100) + "---\n\n"


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    vault = DEFAULT_VAULT
    if "--vault" in args:
        vault = Path(args[args.index("--vault") + 1])

    if not Path(vault).exists():
        print("볼트를 찾을 수 없다: %s" % vault)
        print("--vault <경로> 로 지정한다.")
        return 1

    root, assets, moc = vault_paths(vault)
    notes = list(M.iter_notes())
    if not notes:
        print("math/notes/ 가 비어 있다.")
        return 0

    made, copied = [], set()
    for slug, path in notes:
        try:
            fm, body = M.read_note(path, strict=True)
        except ValueError as e:
            print("✗ %s: %s" % (slug, e))
            return 1

        typ = fm.get("유형")
        name = fm.get("볼트파일명") or ("%s_%s" % (typ, fm.get("제목")))
        dest = root / SUBDIR.get(typ, "99-기타") / (name + ".md")
        text = fm_block(fm) + transform(fm, body, slug)

        if not dry:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
        made.append((typ, dest, len(text)))

        for im in (fm.get("이미지") or []):
            f = im.get("파일")
            if not f or str(f).startswith("http"):
                continue
            src = M.MATH / f
            if not src.exists():
                print("! 자산 없음: math/%s" % f)
                continue
            if not dry:
                assets.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, assets / src.name)
            copied.add(src.name)

    # ── MOC ──
    lines = ["---", "제목: 수학사 MOC", "태그: [MOC, 수학사]", "---", "",
             "# 수학사", "",
             "갤러리: %s" % GALLERY.rsplit("#", 1)[0], "",
             "> 이 문서는 tools/sync_math_obsidian.py 가 생성한다. 직접 고치지 않는다.", ""]
    by_type = {}
    for slug, path in notes:
        fm, _ = M.read_note(path, strict=True)
        by_type.setdefault(fm.get("유형"), []).append(fm)
    for typ in ("세기", "개념", "인물", "일화"):
        items = by_type.get(typ) or []
        if not items:
            continue
        lines.append("## %s (%d)" % (typ, len(items)))
        lines.append("")
        for fm in sorted(items, key=lambda x: str(x.get("제목"))):
            cents = ", ".join("%s세기" % c for c in (fm.get("세기") or []))
            lines.append("- [[%s]] — %s%s" % (
                fm.get("볼트파일명"), fm.get("요약", "")[:70],
                (" *(%s)*" % cents if cents else "")))
        lines.append("")
    if not dry:
        moc.parent.mkdir(parents=True, exist_ok=True)
        moc.write_text("\n".join(lines) + "\n", encoding="utf-8")

    tag = "[미리보기] " if dry else ""
    print("%s볼트 동기화: %d편" % (tag, len(made)))
    for typ, dest, n in made:
        print("   %-4s %-46s %6d자" % (typ, dest.name, n))
    print("%s자산 %d개 → %s" % (tag, len(copied), assets))
    print("%sMOC → %s" % (tag, moc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
