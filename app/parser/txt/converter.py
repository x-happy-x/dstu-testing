import os
import random
import re


class HEAD:

    block_start = "###### HEAD START ######"
    block_end = "######  HEAD END  ######"

    r_delimiter_questions = "\n\n\n"
    r_delimiter_question_and_answers = "\n\n"
    r_delimiter_question_and_id = " "

    r_delimiter_answers = "\n"
    r_delimiter_answer_and_id = ""

    r_answer_id_end = "\\."

    r_right_answer = "^\\+"
    i_right_answer_position = 0

    b_random_questions = False
    b_random_answers = False
    b_sort_answers = False

    def __init__(self, lines: list[str]):
        for line in lines:
            try:
                key, value = line.split("=")
                key = key.strip().lower()
                value = value[value.find("\"") + 1:-(value[::-1].find("\"") + 1)]
                if key.startswith("b_"):
                    value = bool(value)
                if key.startswith("i_"):
                    value = int(value)
                self.__setattr__(key, value)
            except Exception as e:
                if len(line.strip()) > 0:
                    print("Не удалось прочитать заголовок", line)

    def get_questions(self, lines):
        questions = []
        last_type = None
        last_category = None
        for question in re.split(self.r_delimiter_questions, "\n".join(lines)):
            if question.strip().startswith("//"):
                info, question = question.strip().split("\n", 1)
                info = info[2:].strip().split("||")
                for line in info:
                    k, v = line.strip().split(" ", 1)
                    if k.lower().strip() == "type":
                        last_type = v.strip()
                    elif k.lower().strip() == "category":
                        last_category = v.strip()
            q_id, qa = re.split(self.r_delimiter_question_and_id, question.strip(), 1)
            q_text, q_answers = re.split(self.r_delimiter_question_and_answers, qa.strip(), 1)
            answers = []
            for q_answer in re.split(self.r_delimiter_answers, q_answers.strip()):
                q_answer_id, q_answer_text = re.split(self.r_delimiter_answer_and_id, q_answer.strip(), 1)
                if q_answer_id == "":
                    qq = q_answer_text
                    q_answer_text = re.sub(self.r_right_answer, "", q_answer_text)
                else:
                    qq = [q_answer_id, q_answer_text][self.i_right_answer_position]
                    if self.i_right_answer_position == 1:
                        q_answer_text = re.sub(self.r_right_answer, "", q_answer_text)
                    else:
                        q_answer_id = re.sub(self.r_right_answer, "", q_answer_id)
                right = re.match(self.r_right_answer, qq) is not None
                answers.append({
                    'id': str(HEAD.get_number(re.sub(r'[^[:alnum:]]+', "", q_answer_id), ['az', 'ая', '19'])) if len(
                        q_answer_id) > 0 else str(len(answers) + 1),
                    'text': q_answer_text,
                    'right': right
                })
            questions.append(
                {
                    'id': str(HEAD.get_number(re.sub(r'[^[:alnum:]]+', "", q_id), ['az', 'ая', '19'])) if len(
                        q_id) > 0 else str(len(questions) + 1),
                    'type': last_type,
                    'category': last_category,
                    'text': q_text,
                    'answers': answers
                }
            )
        if self.b_random_questions:
            random.shuffle(questions)
            q_id = 1
            for q in questions:
                q['id'] = str(q_id)
                q_id += 1
        if self.b_random_answers:
            for q in questions:
                random.shuffle(q['answers'])
                a_id = 1
                for a in q['answers']:
                    a['id'] = str(a_id)
                    a_id += 1
        if self.b_sort_answers:
            for q in questions:
                q['answers'] = sorted(q['answers'], key=lambda ans: not ans['right'])
                a_id = 1
                for a in q['answers']:
                    a['id'] = str(a_id)
                    a_id += 1
        return questions

    @staticmethod
    def get_number(q_id, alphabets_range=None, alphabets=None):
        if alphabets is None:
            alphabets = []
        if alphabets_range is None:
            alphabets_range = []
        q_id = q_id.lower()[0]
        char = ord(q_id)
        for alphabet in alphabets_range:
            start = ord(alphabet[0].lower())
            end = ord(alphabet[1].lower())
            if start <= char <= end:
                return char - start + 1
        for alphabet in alphabets:
            alphabet = alphabet.lower()
            if q_id in alphabet:
                for i in range(alphabet):
                    if ord(alphabet[i]) == char:
                        return i + 1

    @staticmethod
    def get_head(lines):

        start = -1
        end = -1

        for i in range(len(lines)):
            line = lines[i]
            if start < 0:
                if HEAD.block_start == line.strip():
                    start = i
            elif end < 0:
                if HEAD.block_end == line.strip():
                    end = i
                    break
        if start >= 0 and end >= 0:
            return HEAD(lines[start + 1:end]), lines[end + 1:]
        return HEAD([]), lines


def from_file(filepath) -> str:
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError as e:
        with open(filepath, "r") as f:
            return f.read()


def to_file(content, filepath):
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(content)


def parse(content):
    lines = content.splitlines()
    head, lines = HEAD.get_head(lines)
    questions = head.get_questions(lines)
    return questions


def txt2json(content):
    return parse(content)
