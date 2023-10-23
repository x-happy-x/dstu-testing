import gradio as gr

from app.ui.gift import gift_to_docx

with gr.Blocks() as app:
    with gr.Row():
        with gr.Column():
            gr.Markdown("Загрузка данных")
            with gr.Tab("Из GIFT"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("1. Заполнить поля, пропущенные поля придется заполнять вручную в итоговом файле")
                        with gr.Row():
                            with gr.Column():
                                code = gr.Textbox(label="Код направления", placeholder="09.04.02...", lines=1)
                                disp = gr.Textbox(label="Название дисциплины", placeholder="Базы данных...", lines=1)
                                html_convert = gr.Checkbox(label="Преобразовать HTML", value=True)

                            with gr.Column():
                                comp = gr.Textbox(label="Компетенция", placeholder="ПК-1 Способен...")
                                indicator = gr.Textbox(label="Индикатор", placeholder="ПК-1.3 Владеет...")
                        output_msg = gr.Markdown()
                    with gr.Column():
                        gr.Markdown("2. Загрузить файл с вопросами")
                        file_GIFT = gr.File(label="Файл с вопросами в формате gift")
                        outfn = gr.Textbox(value="ТЕСТ_[индикатор]_[дисциплина].docx",
                                           label="Путь файла на выходе",
                                           placeholder="out.docx")
                        with gr.Accordion("Варианты написания названия файла", open=False):
                            gr.Markdown("[дисциплина] - Название дисциплины\n"
                                        "[направление] - Код направления\n"
                                        "[компетенция] - Код компетенции\n"
                                        "[индикатор] - Код индикатора\n"
                                        "[дата] - Дата создания\n"
                                        "[all] - Количество вопросов")
                with gr.Row():
                    with gr.Column():
                        btn = gr.Button("Создать карту тестовых заданий")
            #with gr.Tab("Генерация вопросов"):

        with gr.Column():
            with gr.Row():
                with gr.Column():
                    prev = gr.Dataframe(label="Предпросмотр данных")
                    gr.Markdown("Результат:")
                    ofiles = gr.Files(label="Готовый файл")

    btn.click(fn=gift_to_docx,
              inputs=[file_GIFT, outfn, disp, comp, indicator, code, html_convert],
              outputs=[ofiles, prev, output_msg])

if __name__ == "__main__":
    app.launch()
