from app.parser import json
from app.rpd import *
from app.rpd.RpdApp import RP, Plan, Discipline, Department
from app.rpd.api.BaseApi import Method


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
    group = rp.group()
    if group['name'] is not None:
        rp.app.logging(group)
    return group['name'] is not None


rpd_app = RpdApp()
rpd_app.load_cache = True


# report = rpd_app.walk(
#     # Фильтры
#     department_selector=department_selector,
#     discipline_selector=discipline_selector,
#     plan_selector=plan_selector,
#     rpd_selector=rpd_selector,
#     # Обработчики
#     files_prepare=[fp_search_fos, fp_search_files],
#     fos_prepare=[fp_search_skif_test],
#     summary_prepare=[fp_search_summary],
#     competencies_prepare=[fp_search_competencies]
# )
#
# # Сохранение отчета
# json.to_file(report, './source/reports.json')

def update_reviews(app: RpdApp, rp: RP):
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
                    'rank': new_reviewers[i]['rank'],
                    'position': new_reviewers[i]['position'],
                    'fio': new_reviewers[i]['fio'],
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

def rpd_info(app: RpdApp, rp: RP):
    return {
        'name': rp.name,
        'user': rp.user,
        'owner': rp.owner,
        'modified': rp.modified_on
    }


report = rpd_app.walk(
    # Фильтры
    department_selector=department_selector,
    discipline_selector=discipline_selector,
    plan_selector=plan_selector,
    rpd_selector=rpd_selector,
    # Обработчики
    rpd_prepare=[
        rpd_info,
        # update_reviews,
    ],
)

json.to_file(report, './dest/rp_report.json')
