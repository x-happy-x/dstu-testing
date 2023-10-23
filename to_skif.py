from app import parser as ps


if __name__ == "__main__":
    #filepath = r"C:\Users\thend\Downloads\вопросы_Мат_метод_прин_реш_По_умолчанию_для_Дисциплина_20231001 (3).txt"
    #file = ps.Gift(filepath=filepath)
    #file.fix_names()
    #file.save(filepath+"2")

    f = r"Z:\Desktop\Работа\Тесты\Метод и средства поддержки принятия решений.txt"
    TEMPLATE_FILE = "./template/Карта тестовых заданий.docx"
    ps.txt2docx_f(TEMPLATE_FILE, f)

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
