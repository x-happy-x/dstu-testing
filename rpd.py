import json

from app.parser import save_json
from app.rpd import *
from app.rpd.RpdApp import RP, Plan, Discipline, Department


def department_selector(d: Department) -> bool:
    return True


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
save_json(report, 'report.json')
