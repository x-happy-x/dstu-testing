from docx import Document

from app.entity import *
from app.parser import Gift


class Maket:
    path: str
    questions: dict
    skipped: list
    struct: list[dict] = None

    def __init__(self, struct=None):
        self.questions = {}
        self.groups = []
        if struct is not None:
            self.struct = []
            with open(struct, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                headers = lines[0].split(',')
                for line in lines[1:]:
                    values = line.split(',')
                    self.struct.append(
                        {headers[i].strip().lower(): values[i].strip() for i in range(min(len(values), len(headers)))})

                    self.struct[-1]['category'] = int(self.struct[-1]['category'])
                    self.struct[-1]['count'] = int(self.struct[-1]['count'])
                    self.struct[-1]['questions'] = []
                    if self.struct[-1]['group'] not in self.groups:
                        self.groups.append(self.struct[-1]['group'])

                    # group = self.struct[-1]['group']
                    # if group not in self.questions:
                    #     self.questions[group] = {}
                    # category = int(self.struct[-1]['category'])
                    # if category not in self.questions[group]:
                    #     self.questions[group][category] = []

    def add_question(self, question):
        if self.struct is not None:
            category_level = question.get_category_level()
            question_type = question.get_type()[:-2]
            add = False
            for s in self.struct:
                if s['type'] == question_type and category_level == s['category'] and len(s['questions']) < s['count']:
                    add = True
                    s['questions'].append(question)
                    break
            if not add:
                print(f"Question was skipped: {question}")
                self.skipped.append(question)
        else:
            pass

    def add_short_question(self, question):
        pass

    def add_matching_question(self, question):
        pass

    def add_multiplechoiceradio_question(self, question):
        pass

    def add_multiplechoicecheckbox_question(self, question):
        pass

    def add_essay_question(self, question):
        pass

    def build(self, template, path):
        document = Document(template)

        for s in self.struct:
            print(s['group'], s['category'])
            for question in s['questions']:
                print(question.get_type())



if __name__ == '__main__':
    x = Maket("./struct.csv")
    gift = Gift(r"Z:\Downloads\Telegram Desktop\вопросы_Мат_метод_прин_реш_УК_1_Содержание_компетенции_20231012.txt")
    for q in gift.questions:
        x.add_question(q)
    x.build("")