from app.parser import json
from app.rpd import *
from app.rpd.RpdApp import RP, Plan, Discipline, Department
from app.rpd.api.BaseApi import Method


def department_selector(d: Department) -> bool:
    return True


def discipline_selector(d: Discipline) -> bool:
    return True


def plan_selector(plan: Plan) -> bool:
    groups = [
        'B090302_',
        'B090302ВИАС_',
        'B090302ВИС_',
        'B090303ВЗПИ_',
        'B090303ВОЗПИ_',
        '090402МЗИН_',
        '090402МИН_',
        '090403МПИ_'
    ]
    for group in groups:
        if group in plan.rup_name:
            return True
    return False


def rpd_selector(rp: RP) -> bool:
    group = rp.group()
    if group['name'] is not None:
        #rp.app.logging(group['name'])
        return True
    rp.app.logging("НЕТ ПРОФИЛЯ", rp.name)
    return False


rpd_app = RpdApp()
rpd_app.load_cache = True

report = rpd_app.walk(
    # Фильтры
    department_selector=department_selector,
    discipline_selector=discipline_selector,
    plan_selector=plan_selector,
    rpd_selector=rpd_selector,
    # Обработчики
    files_prepare=[fp_search_fos, fp_search_files],
    fos_prepare=[fp_search_skif_test],
    summary_prepare=[fp_search_summary],
    competencies_prepare=[fp_search_competencies]
)

# Сохранение отчета
json.to_file(report, './source/reports.json')
rpd_app.save_log()

# report = rpd_app.walk(
#     # Фильтры
#     department_selector=department_selector,
#     discipline_selector=discipline_selector,
#     plan_selector=plan_selector,
#     rpd_selector=rpd_selector,
#     # Обработчики
#     rpd_prepare=[
#         rpd_info,
#         update_reviews,
#     ],
# )
#
# json.to_file(report, './dest/rp_report.json')
