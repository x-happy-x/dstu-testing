from app.parser import stats2df, gift2layout

TEMPLATE_FILE = "./template/LayoutTest.docx"


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

    out, layout, structure, questions = gift2layout(
        questions_file=file_input,
        layout_file=f"./dest/{filename}",
        template_file=TEMPLATE_FILE,
        info={
            "дисциплина": disp,
            "компетенция": comp,
            "индикатор": indicator,
            "направление": code,
        },
        html_convert=html_convert
    )

    df_stat = stats2df(layout.stats)

    return out, df_stat, ""
