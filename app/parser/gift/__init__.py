from .parser import parse
from .gift import Gift


def from_file(filepath) -> Gift:
    return Gift(filepath=filepath)


def from_str(string) -> Gift:
    return Gift(content=string)
