from .parser import parse
from .gift import Gift


def open_gift(filepath):
    with open(filepath, "r", encoding='utf-8') as f:
        return parse(f.read())
