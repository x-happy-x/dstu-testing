from .editor import *

__STR_FOR_NUMERATION__ = 'num_'
__PATTERN_FOR_NUMERATION__ = "{{ " + __STR_FOR_NUMERATION__ + "{i} }}"
__PATTERN_FOR_NUMERATION_REGEX__ = r"{{\s" + __STR_FOR_NUMERATION__ + r".*\s}}"


def fill_test_template(document, keys, test, styles=None, question_id=1, html_convert=True, custom_groups=None):
    questions = test.questions

    paragraphs = {}
    stats = {}

    for q_type in keys:
        key = keys[q_type]
        paragraph_id = find_paragraph_id(document, "{{ " + str(key) + " }}", find_types["equal"], 0)
        if paragraph_id > 0:
            paragraphs[q_type] = document.paragraphs[paragraph_id]
            stats[q_type] = {}
        else:
            print(key, "не найден")

    last_paragraphs = {}
    for q_type in paragraphs:
        last_paragraphs[q_type] = {}

    skipped_questions = []
    for i in range(len(questions)):

        question = questions[i]
        q_type = question.get_type()
        category = question.get_category()
        text = question.get_text()
        if html_convert and not text.startswith("[html]") and contains_html(text):
            text = f"[html]{text}"
        answers = question.get_answers()

        # Выбор категории

        cat = category.split(" (")[0].strip()
        if cat not in stats[q_type]:
            stats[q_type][cat] = 1
        else:
            stats[q_type][cat] += 1

        if cat == 'Неизвестные':
            skipped_questions.append(i)
            continue

        if category not in last_paragraphs[q_type]:
            if len(last_paragraphs[q_type]) == 0:
                paragraph = paragraphs[q_type]
                paragraph.text = category
                paragraph.style = styles["title"]
                paragraph = insert_paragraph_after(paragraph, "", styles['title'])
                last_paragraphs[q_type][category] = paragraph
            else:
                paragraph = last_paragraphs[q_type][list(last_paragraphs[q_type].keys())[-1]]
                paragraph = insert_paragraph_after(paragraph, category, styles['title'])
                paragraph = insert_paragraph_after(paragraph, "", styles['title'])
                last_paragraphs[q_type][category] = paragraph
        else:
            paragraph = last_paragraphs[q_type][category]

        # Тип вопроса
        if q_type == SHORT:
            paragraph = add_short_question(text, paragraph, styles, question)
        elif q_type in [MULTIPLE_CHOICE_RADIO, MULTIPLE_CHOICE_CHECKBOX]:
            paragraph = add_multiple_question(text, paragraph, styles, question)
        elif q_type == MATCHING:
            paragraph = add_matching_question(document, paragraph, question, text, styles)
        last_paragraphs[q_type][category] = paragraph

    questions_sorted = []
    for paragraph in document.paragraphs:
        match = re.match(r"{{\snum_.*\s}}", paragraph.text)
        if match is not None:
            q_id = match.group(0).replace("num_", "")[2:-2].strip()
            paragraph.text = paragraph.text.replace(match.group(0), str(question_id))
            question_id += 1
            questions_sorted.append(q_id)

    key_table = document.tables[-1]
    i = 1
    q_i = 0
    column_num = 0
    column_text = 1
    while q_i < len(questions_sorted):
        row = key_table.rows[i]
        row.cells[column_num].text = str(q_i + 1)
        row.cells[column_num].paragraphs[0].style = styles["key_num"]
        row.cells[column_text].text = test.find(questions_sorted[q_i]).get_right_answer()
        row.cells[column_text].paragraphs[0].style = styles["key_answer"]
        i += 1
        q_i += 1
        if i >= len(key_table.rows):
            i = 0
            column_num = 4
            column_text = 5

    return questions_sorted, stats, skipped_questions


def add_short_question(text, paragraph, styles, question):
    paragraph = insert_text_after(
        text,
        paragraph,
        styles['question'],
        text_prepare=lambda text: f"{__PATTERN_FOR_NUMERATION__.replace('{i}', question.name.strip())}\t{text}"
    )
    return insert_paragraph_after(paragraph, "", styles['question'])


def add_multiple_question(text, paragraph, styles, question):
    is_html = text.strip().startswith("[html]")
    is_markdown = text.strip().startswith("[markdown]")
    is_moodle = text.strip().startswith("[moodle]")

    paragraph = insert_text_after(
        text,
        paragraph,
        styles['question'],
        text_prepare=lambda text: f"{__PATTERN_FOR_NUMERATION__.replace('{i}', question.name.strip())}\t{text}"
    )
    answers_start = ord("А")
    for answer in question.get_answers():
        prefix = ""
        if answer.text.strip() != clean_string_regex(answer.text.strip()):
            prefix = ""
        elif is_html:
            prefix = "[html]"
        elif is_markdown:
            prefix = "[markdown]"
        elif is_moodle:
            prefix = "[moodle]"
        # print(answer.text)
        paragraph = insert_text_after(
            prefix + answer.text,
            paragraph,
            styles['answer'],
            text_prepare=lambda text: f"{chr(answers_start)})\t{text}"
        )
        answers_start += 1
    return insert_paragraph_after(paragraph, "", styles['question'])


def add_matching_question(document, paragraph, question, text, styles):
    paragraph = insert_paragraph_after(
        paragraph,
        f"{__PATTERN_FOR_NUMERATION__.replace('{i}', question.name.strip())}\tУстановите соответствие",
        styles['question']
    )
    paragraph = insert_text_after(
        text,
        paragraph,
        styles['question'],
    )

    table = document.add_table(rows=1, cols=2)
    answers_start = 0
    answers_start_col1 = 1
    answers_start_col2 = ord("А")
    row = None

    is_html = text.strip().startswith("[html]")
    is_markdown = text.strip().startswith("[markdown]")
    is_moodle = text.strip().startswith("[moodle]")

    for answer in question.get_answers():
        if row is None:
            row = table.rows[0]
        else:
            row = table.add_row()
        row.cells[0].width = Inches(3)
        row.cells[1].width = Inches(4.5)
        columns = answer.text.strip().split("->")
        style_ = [styles['table'], styles['key_answer']]
        start_column = [answers_start_col1, answers_start_col2]
        column_func = [lambda x: x, lambda x: chr(x) + ")"]
        prefix = ""
        if answer.text.strip() != clean_string_regex(answer.text.strip()):
            prefix = ""
        elif is_html:
            prefix = "[html]"
        elif is_markdown:
            prefix = "[markdown]"
        elif is_moodle:
            prefix = "[moodle]"

        for k, _ in enumerate(columns):
            if columns[k].strip() == "":
                continue
            replace_text(f"{prefix}{columns[k]}", row.cells[k].paragraphs[0], style_[k])
            r = row.cells[k].paragraphs[0]
            r.text = str(column_func[k](start_column[k] + answers_start)) + " " + r.text.strip()

        answers_start += 1

    paragraph2 = insert_paragraph_after(paragraph, "", styles['question'])
    move_table_after(table, paragraph)
    return paragraph2
