import pandas as pd


def create_excel(stats, file):
    writer = pd.ExcelWriter(file)
    for sheetname, stat in stats:
        table = [['Компетенции'], ["Изменение", "Индикатор", "Новое", "Старое"]]
        last_len = len(table)
        for operation in stat['Компетенции']:
            for comp in stat['Компетенции'][operation]:
                if operation in ['+', '-']:
                    table.append([operation, comp, stat['Компетенции'][operation][comp]])
                else:
                    table.append(
                        ['*', comp, stat['Компетенции'][operation][comp]['new'], stat['Компетенции'][operation][comp]['old']])
        if len(table) == last_len:
            table.append(['Нет изменений'])
        table += [[], ['Индикаторы'], ["Изменение", "Индикатор", "Новое", "Старое"]]
        last_len = len(table)
        for operation in stat['Индикаторы']:
            for comp in stat['Индикаторы'][operation]:
                if operation in ['+', '-']:
                    table.append([operation, comp, stat['Индикаторы'][operation][comp]])
                else:
                    table.append(['*', comp, stat['Индикаторы'][operation][comp]['new'],
                                  stat['Индикаторы'][operation][comp]['old']])
        if len(table) == last_len:
            table.append(['Нет изменений'])

        table += [[], ['Дисциплины'], ["Изменение", "Индикатор", "Дисциплина"]]
        last_len = len(table)
        for operation in stat['Дисциплины']:
            for disp in stat['Дисциплины'][operation]:
                table.append([operation, disp['индикатор'], disp['дисциплина']])
        if len(table) == last_len:
            table.append(['Нет изменений'])
        df_stat = pd.DataFrame(table)
        df_stat.to_excel(writer, sheet_name=sheetname, header=False, index=False)
    writer.close()
    return df_stat