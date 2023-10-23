import re

from bs4 import BeautifulSoup


def contains_html(text):
    return bool(BeautifulSoup(text, "html.parser").find())


def clean_string_regex(s):
    """
    Функция очищает слова в квадратных скобках,
    находящихся в начале строки с помощью регулярных выражений

    :param s: строка для очистки
    :return: очищенная строка
    """
    pattern = r"^\[[a-zA-Z]+\]\s*"
    match = re.search(pattern, s)
    if match:
        # Найдено вхождение паттерна, очищаем строку
        s = s[match.end():].lstrip()
    return s
