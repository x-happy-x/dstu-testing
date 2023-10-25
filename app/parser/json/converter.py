import json
import os.path


def parse_json(content):
    return json.loads(content)


def open_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.loads(f.read())


def save_json(data, save: str):
    dest = os.path.split(save)[0]
    if not os.path.exists(dest):
        os.makedirs(dest)
    with open(save, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def json2gift(data):
    lines = []
    last_category = None
    answer_type = "~", "="
    tab = "\t"

    for question in data:

        if question['category'] != last_category:
            last_category = question['category']
            lines.append(f"\n// question: 0  name: Switch category to {last_category}")
            lines.append(f"$CATEGORY: {last_category}\n")

        lines.append(f"// question: 0  name: {question['id']}")
        lines.append(f"::{question['id']}:: {question['text']}")
        lines.append("{")

        if question['type'].lower() == 'multiplecheckbox':
            count_all = len(question['answers'])
            count_right = len(list(filter(lambda a: a['right'], question['answers'])))
            for answer in question['answers']:
                percent = round(100 / count_right if answer['right'] else -100 / (count_all - count_right), 2)
                lines.append(tab + f"~%{percent}% {answer['text']}")

        if question['type'].lower() in ['multipleradio', 'short']:
            for answer in question['answers']:
                lines.append(tab + f"{answer_type[answer['right']]} {answer['text']}")

        if question['type'].lower() in ['matching']:
            for answer in question['answers']:
                lines.append(tab + f"{answer_type[answer['right']]} {answer['text']}")

        lines.append("}")
        lines.append("")

    return "\n".join(lines)
