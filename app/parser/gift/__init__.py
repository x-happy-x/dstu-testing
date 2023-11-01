from .parser import parse
from .gift import Gift


def from_file(filepath) -> Gift:
    with open(filepath, "r", encoding='utf-8') as f:
        return parse(f.read().replace('\n}\n', '\n}\n\n'))
