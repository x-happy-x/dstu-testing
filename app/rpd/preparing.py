from datetime import datetime

from app.rpd import RpdApp
from app.rpd.RpdApp import (
    RP,
    Appx,
    CompetenceBoard,
    Result,
    Summary
)


def search_fos(file: Appx):
    return 'ФОС' in file.name


def fp_search_(app: RpdApp, rpd: RP, result: Result):
    report = None
    if result.success:
        pass
    else:
        app.logging('При обработке раздела ФОС возникла ошибка:', result.message)
    return report


def fp_search_competencies(app: RpdApp, rpd: RP, result: Result):
    report = 'Всё есть'
    if result.success:
        cb: CompetenceBoard = result.data
        for c in cb.competencies():
            for i in c.indicators():
                if len(i.levels()) < 3:
                    return 'Не прописаны все уровни'
                elif len(i.levels()) > 3:
                    return 'Больше 3-х уровней'

    else:
        app.logging('При обработке раздела ФОС возникла ошибка:', result.message)
    return report


def fp_search_files(app: RpdApp, rpd: RP, result: Result, save=False, reload=False):
    report = None
    if result.success:
        report = {'files': []}
        for file in result.data:
            file: Appx
            modified = 'None'
            if file.modified is None or save:
                if reload or not file.exists():
                    file.save()
                try:
                    prop = file.metadata()
                    if prop is not None:
                        modified = prop.modified
                    else:
                        modified = 'Файл не документ Word'
                except ValueError as e:
                    modified = f"Не удалось проверить: {e}"
            report['files'].append({
                'name': file.name,
                'modified_site': str(file.modified),
                'url': file.link(),
                'modified_local': str(modified),
                'path': file.localpath()
            })
    else:
        app.logging('При обработке раздела ФОС возникла ошибка:', result.message)
    return report


def fp_search_summary(app: RpdApp, rpd: RP, result: Result):
    report = None
    if result.success:
        summary: Summary = result.data
        report = {
            'Правильность часов:': summary.is_right(),
            'Контроль:': [
                {
                    'Тип контроля': ct['вид'],
                    'Семестр': ct['terms'],
                } for ct in summary.control_types
            ],
        }
    else:
        app.logging('При обработке раздела ФОС возникла ошибка:', result.message)
    return report


def fp_search_skif_test(app: RpdApp, rpd: RP, result: Result):
    report = {}
    if result.success:
        url = result['Ссылка на СКИФ.Тест']
        if url is None or len(url.strip()) < 10 or 'skif' not in url:
            report['url'] = url
            report['exist'] = False
        else:
            report['url'] = url
            report['exist'] = True
    else:
        app.logging('При обработке раздела ФОС возникла ошибка:', result.message)
        report['url'] = None
        report['exist'] = False
        report['data'] = result.data
    return report


def fp_search_fos(app: RpdApp, rpd: RP, result: Result):
    report = None
    if result.success:
        fos_files = result(search_fos)

        # Проверка состояния ФОСа
        is_new = False
        is_loaded = False
        filenames = None
        if len(fos_files) == 1:

            file = fos_files[0]
            filenames = str(file)

            # Если указана дата редактирования
            if file.modified is not None:

                # Ищем за 2023 год
                is_new = file.modified > datetime(2023, 1, 1)
                if is_new:
                    report = f"Фос: {file.name} новый (дата в РПД: {file.modified})"
                else:
                    report = f"Фос: {file.name} старый (дата в РПД: {file.modified})"

            # Если нет
            else:
                # Если файл ещё не был скачан, то качаем
                if not file.exists():
                    file.save()

                is_loaded = True

                # Смотрим дату его изменения
                prop = file.metadata()
                if prop is not None:
                    if isinstance(prop.modified, datetime):
                        is_new = prop.modified > datetime(2023, 1, 1)
                    else:
                        app.logging("Неизвестное значение вместо даты редактирования ФОСа:", prop.modified)

                    if is_new:
                        report = f"Фос: {file.name} новый (дата в метаданных: {prop.modified})"
                    else:
                        report = f"Фос: {file.name} старый (дата в метаданных: {prop.modified})"
                else:
                    is_new = True
                    report = "Фос не документ Word"

        # Если такого файла нет
        elif len(fos_files) == 0:
            report = "Нет фоса"
            filenames = str(result.data)

        # Если таких файлов много
        else:
            filenames = str(result.data)
            report = "Их больше одного, лучше взглянуть самому"

        # Формирование отчета
        report = {"Состояние ФОСа": report,
                  "filename": filenames,
                  "download": is_loaded,
                  "new": is_new,
                  "url": f"https://rpd.donstu.ru/Rp?rupRowId={rpd.rup_row_id}&rpId={rpd.id}"}
    else:
        app.logging('При обработке приложения в поисках ФОСа возникла ошибка:', result.message)
    return report

def rp_update_reviews(app: RpdApp, rp: RP):
    new_reviewers = [
        {
            'rank': '',
            'position': 'генеральный директор ООО «Современные измерительные технологии»',
            'fio': 'Померов Кирилл Николаевич',
        },
        {
            'rank': '',
            'position': 'генеральный директор ООО «IT-Компания «Союз»',
            'fio': 'Сотниченко Дмитрий Михайлович',
        },
    ]

    app.load_cache = False
    data = rp.title()

    ndata = data
    reviwers = data['data']['reviwers']
    for i in range(max(len(reviwers), 2)):

        hash = ndata['data']['commonState']['hash']
        if i >= 2:
            response = rp.api.delete_reviewer(
                data={
                    'id': reviwers[i]['id'],
                    'hash': hash,
                }
            )
            ndata = response.json()

        elif i < len(reviwers):
            response = rp.api.update_reviewer(
                data={
                    'id': reviwers[i]['id'],
                    'rank': new_reviewers[i]['rank'],
                    'academicRank': '',
                    'position': new_reviewers[i]['position'],
                    'depId': '',
                    'fio': new_reviewers[i]['fio'],
                    'company': '',
                    'hash': hash,
                }
            )
            ndata = response.json()

        else:
            response = rp.api.add_reviewer(
                data={
                    'rank': reviwers[i]['rank'],
                    'position': reviwers[i]['position'],
                    'fio': reviwers[i]['fio'],
                    'hash': hash,
                },
            )
            ndata = response.json()

    hash = ndata['data']['commonState']['hash']
    response = rp.api.save(
        data={
            'hash': hash,
        }
    )

    app.load_cache = True
    return {
        'status': response.status_code,
        'message': response.text
    }