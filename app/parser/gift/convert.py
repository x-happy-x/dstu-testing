import re


def fix_numeration(content: str) -> str:
    lines = []
    num = 1
    for line in content.splitlines():
        lines.append(re.sub("^::.*::", f"::{num}.::", line))
    return "\n".join(lines)