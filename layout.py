from app import parser as ps

"""
###### HEAD START ######

R_DELIMITER_QUESTIONS = "\n\n\n" - Разделитель между вопросами
R_DELIMITER_QUESTION_AND_ANSWERS = "\n\n" - Разделитель между вопросом и ответами
R_DELIMITER_QUESTION_AND_ID = " " - Разделитель в вопросе между нумерацией и ответом

R_DELIMITER_ANSWERS = "\n" - Разделитель между ответами
R_DELIMITER_ANSWER_AND_ID = "" - Разделитель в ответе между нумерацией и ответом

R_ANSWER_ID_END = "\." - не помню

R_RIGHT_ANSWER = "^\+" - Как искать правильный ответ
I_RIGHT_ANSWER_POSITION = "0" - Позиция правильного указателя в ответе (0 перед нумер., 1 в ответе, если нет нумер. - 0)

B_RANDOM_QUESTIONS = "False" - Смешать вопросы
B_RANDOM_ANSWERS = "False" - Смешать ответы
B_SORT_ANSWERS = "True" - Отсортировать ответы от правильных к неправильным
######  HEAD END  ######


// type MultipleCheckbox || category Средне-сложные
1. вопрос
ответ
+ответ
+ответ

"""

if __name__ == "__main__":
    # filepath = r"C:\Users\thend\Downloads\вопросы_Мат_метод_прин_реш_По_умолчанию_для_Дисциплина_20231001 (3).txt"
    # file = ps.Gift(filepath=filepath)
    # file.fix_names()
    # file.save(filepath+"2")

    file = './source/Тесты/Мобильная разработка.txt'
    TEMPLATE_FILE = "./template/LayoutTest.docx"
    ps.txt2layout_f(
        from_file=file,
        to_file='./dest/ddd.docx',
        info={

        }
    )

    # questions_file = r"""
    # Z:\Downloads\гифт моделирование бизнес процессов.txt
    # """.strip()
    # layout_file = "./dest/d.docx"
    #
    # file, layout, structure, questions = ps.gift2layout(questions_file, layout_file)
    # print(layout.stats)
    # print("Было всего вопросов:", len(questions.questions))
    # print("Пропущено из-за каких-то ошибок:", len(layout.skipped))
    # print("Пропущено из-за структуры:", len(structure.skipped))

    # txt2json_f(filepath)

    # filepath = "Z:/Desktop/1. Метод принятия решений не предпо — копия.json"
    # json2gift_f(filepath)

    # import app.parser.gift as gift
    # filepath = "Z:/Desktop/1. Метод принятия решений не предпо — копия.gift"
    # with open(filepath, "r", encoding="utf8") as f:
    #     questions = gift.parse(f.read())
    #
    # for question in questions.questions:
    #     print(question)
