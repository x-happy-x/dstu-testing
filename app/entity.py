SHORT: str = "Short()"
MULTIPLE_CHOICE_RADIO: str = "MultipleChoiceRadio()"
MULTIPLE_CHOICE_CHECKBOX: str = "MultipleChoiceCheckbox()"
MATCHING: str = "Matching()"

CATEGORY = {
    -1: "Неизвестные",
    1: "Простые",
    2: "Средне-сложные",
    3: "Сложные",
}

TYPES: dict[str, str] = {
    MULTIPLE_CHOICE_RADIO: "Закрытые",
    MATCHING: "На соответствие",
    SHORT: "Открытые",
}

STYLES = {
    "question": "!СКИФ-ЗТ-Вопрос",
    "answer": "!СКИФ-ЗТ-Ответ",
    "title": "!СКИФ-Категория",
    "table": "!СКИФ-Соответствие",
    "key_num": "!СКИФ-Ключ-Номер",
    "key_answer": "!СКИФ-Ключ-Ответ",
}


class FindFunc:
    EQUALS = lambda a, b: a == b
    START = lambda a, b: a.startswith(b)
    END = lambda a, b: a.endswith(b)
    CONTAINS = lambda a, b: a.find(b) >= 0
