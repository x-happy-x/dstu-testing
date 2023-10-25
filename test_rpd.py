import json
import os
import time
from datetime import datetime
import random

from app.parser.json import save_json, open_json
from app.rpd.RpdApp import Department, Discipline, Plan, RP, Appx, get_now_year, Params
from app.rpd import api, RpdApp

testing_mode = True

if testing_mode:
    rpdapi = api.RpdApi(data={
        Params.rup_row_id: 3019716
    })
    response = rpdapi.session.get("https://rpd.donstu.ru/Rp/Initialize?rupRowId=3019716")
    if response.status_code == 200:
        data = json.loads(response.text)
        response = rpdapi.session.post("https://rpd.donstu.ru/Title/AddAuthor?rupRowId=3019716", data={
            'rank': '1',
            'position': '2',
            'fio': '3',
            'hash': data['data']['commonState']['hash'],
        })
        if response.status_code == 200:
            print(response.text)
            # with open('file.txt', 'r') as f:
            #     s.cookies['.AspNetCore.Cookies'] = ''
            #
            # with open('file.txt', 'w') as f:
            #     f.write(s.cookies['.AspNetCore.Cookies'])
        else:
            print(response.text)
    else:
        print(response.text)
    exit()


def department_selector(d: Department) -> bool:
    return d.id == 9


def discipline_selector(d: Discipline) -> bool:
    return True


def plan_selector(plan: Plan) -> bool:
    groups = ['B090302_', 'B090302ВИАС_', 'B090302ВИС_', 'B090303ВЗПИ_', 'B090303ВОЗПИ_', '090402МЗИН_', '090402МИН_',
              '090403МПИ_']
    for group in groups:
        if group in plan.rup_name:
            return True
    return False


def rpd_selector(rp: RP) -> bool:
    return True


def file_selector(f: Appx) -> bool:
    return 'ФОС' in f.name


department: Department
discipline: Discipline
plan: Plan
rpd: RP
file: Appx

app = RpdApp()

FOS_DATA = {}
PAUSE_TIME = 0.0

# Учебный год
for year in [get_now_year()]:
    print("Год", year)
    FOS_DATA_YEAR = {}
    departments = app.departments(year)
    time.sleep(random.random() * PAUSE_TIME)  # Пауза до {PAUSE_TIME} сек

    # Кафедра
    for department in departments(department_selector):
        print("\tКафедра", department.name)
        FOS_DATA_DEPARTMENT = {}
        disciplines = department.disciplines()
        time.sleep(random.random() * PAUSE_TIME)  # Пауза до {PAUSE_TIME} сек

        # Дисциплина (модуль)
        for discipline in disciplines(discipline_selector):
            # if not discipline.name.startswith("М"):
            #     continue
            print("\t\tДисциплина", discipline.name)
            FOS_DATA_DISCIPLINE = {}
            plans = discipline.plans()
            time.sleep(random.random() * PAUSE_TIME)  # Пауза до {PAUSE_TIME} сек

            # Учебный план
            for plan in plans(plan_selector):
                print("\t\t\tУчебный план", plan.rup_name)
                FOS_DATA_PLAN = {}
                rps = plan.rps()
                time.sleep(random.random() * PAUSE_TIME)  # Пауза до {PAUSE_TIME} сек

                # Рабочая программа
                for rpd in rps(rpd_selector):
                    print(f"\t\t\t\tРабочая программа {rpd.id}:", rpd.name)

                    FOS_DATA_RPD = None

                    # Приложение
                    files = rpd.appxs()
                    fos = files(file_selector)

                    # Проверка состояния ФОСа
                    new = False
                    loaded = False
                    fn = None
                    if len(fos) == 1:
                        file = fos[0]
                        fn = str(file)
                        if file.modified is not None:
                            new = file.modified > datetime(2023, 1, 1)
                            if new:
                                FOS_DATA_RPD = f"Фос: {file.name} новый (дата в РПД: {file.modified})"
                            else:
                                FOS_DATA_RPD = f"Фос: {file.name} старый (дата в РПД: {file.modified})"
                        else:
                            if not file.exists():
                                file.save()
                            loaded = True
                            prop = file.metadata()
                            if isinstance(prop.modified, datetime):
                                new = prop.modified > datetime(2023, 1, 1)
                            else:
                                print(prop.modified)

                            if new:
                                FOS_DATA_RPD = f"Фос: {file.name} новый (дата в метаданных: {prop.modified})"
                            else:
                                FOS_DATA_RPD = f"Фос: {file.name} старый (дата в метаданных: {prop.modified})"
                    elif len(fos) == 0:
                        FOS_DATA_RPD = "Нет фоса"
                    else:
                        fn = str(files.data)
                        FOS_DATA_RPD = "Нужно проверить вручную"

                    FOS_DATA_PLAN[rpd.id] = {"Состояние ФОСа": FOS_DATA_RPD,
                                             "filename": fn,
                                             "download": loaded,
                                             "new": new,
                                             "test": rpd.FOS()["Ссылка на СКИФ.Тест"],
                                             "url": f"https://rpd.donstu.ru/Rp?rupRowId={rpd.rup_row_id}&rpId={rpd.id}"}
                FOS_DATA_DISCIPLINE[plan.rup_name] = FOS_DATA_PLAN
            FOS_DATA_DEPARTMENT[discipline.name] = FOS_DATA_DISCIPLINE
        FOS_DATA_YEAR[department.name] = FOS_DATA_DEPARTMENT
    FOS_DATA[year] = FOS_DATA_YEAR

save_json(FOS_DATA, './fos_status.json')
