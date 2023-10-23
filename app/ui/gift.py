from app.entity import STYLES
from app.parser import gift2docx, stats2df

TEMPLATE_FILE = "./template/Карта тестовых заданий.docx"


def gift_to_docx(file, filename, disp, comp, indicator, code, html_convert):
    if file is None:
        return None, None, "Не выбран файл"

    if disp is None or len(disp.strip()) == 0:
        disp = "{{ дисциплина }}"
    else:
        disp = disp.strip().replace("\n", " ").replace("\t", " ")
        while "  " in disp:
            disp = disp.replace("  ", " ")

    if comp is None or len(comp.strip()) == 0:
        comp = "{{ компетенция }}"
    else:
        comp = comp.strip().replace("\n", " ").replace("\t", " ")
        while "  " in disp:
            comp = comp.replace("  ", " ")

    if indicator is None or len(indicator.strip()) == 0:
        indicator = "{{ индикатор }}"
    else:
        indicator = indicator.strip().replace("\n", " ").replace("\t", " ")
        while "  " in disp:
            indicator = indicator.replace("  ", " ")

    if code is None or len(code.strip()) == 0:
        code = "{{ направление }}"
    else:
        code = code.strip().replace("\n", " ").replace("\t", " ")
        while "  " in code:
            code = code.replace("  ", " ")

    file_input = file.name.replace("\n", " ")
    filename = filename.replace("\n", " ")
    out, test, quest_n, quest_s, stats = gift2docx(TEMPLATE_FILE, file_input, f"./dest/{filename}", {
        "дисциплина": disp,
        "компетенция": comp,
        "индикатор": indicator,
        "направление": code,
    }, STYLES, html_convert)
    df_stat = stats2df(stats)

    return out, df_stat, ""
