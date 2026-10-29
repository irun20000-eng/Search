r"""프론트매터 문자열 값의 YAML 안전 직렬화/역직렬화.

배경: 영상 제목이 `[`·`"`·`'` 로 시작하거나 `: ` 를 포함하면 따옴표 없는 값은
YAML 문법 오류가 되어 옵시디언 속성 패널이 깨진다.
규칙: 문자열 값(title, channel 등)은 항상 큰따옴표로 감싸고 내부 `\` 와 `"` 를 이스케이프한다.
읽는 쪽(build_manifest, verify_video)은 unq() 로 따옴표·이스케이프를 푼다.
따옴표 없는 기존 값은 그대로 돌려준다(하위 호환).
"""
import re


def yq(s):
    s = str(s).replace('\\', '\\\\').replace('"', '\\"')
    s = s.replace('\r', '').replace('\n', ' ')
    return '"' + s + '"'


_ESC = {'n': '\n', 't': '\t', '"': '"', '\\': '\\', '/': '/', 'r': '\r', '0': '\0'}


def unq(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return re.sub(r'\\(.)', lambda m: _ESC.get(m.group(1), '\\' + m.group(1)), v[1:-1])
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1].replace("''", "'")
    return v

