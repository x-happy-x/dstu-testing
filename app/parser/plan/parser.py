import datetime
import math

import pandas as pd


def isnan(x):
    try:
        return math.isnan(float(x))
    except ValueError:
        return False


def get_type(competencies, index):
    if not isnan(competencies['Индекс'][index]):
        return 1, competencies['Индекс'][index]
    if not isnan(competencies['Unnamed: 1'][index]):
        return 2, competencies['Unnamed: 1'][index]
    if not isnan(competencies['Unnamed: 2'][index]):
        return 3, competencies['Unnamed: 2'][index]
    return 4, ""


def get_competencies(page: pd.DataFrame):
    competencies = {}
    last_type = {}
    for i in range(0, len(page)):
        level, title = get_type(page, i)
        text = page['Содержание'][i]
        if level == 1:
            last_type['type'] = title.split('-')[0].replace('_x000d_', '').strip(' \n;.\t,')
            last_type['title1'] = title.replace('_x000d_', '').strip(' \n;.\t,')
            if last_type['type'] not in competencies:
                competencies[last_type['type']] = {}
            competencies[last_type['type']][last_type['title1']] = {
                'text': text.replace('_x000d_', '').strip(' \n;.\t,'),
                'sub': {}
            }
        elif level == 2:
            last_type['title2'] = title.replace('_x000d_', '').strip(' \n;.\t,')
            competencies[last_type['type']][last_type['title1']]['sub'][last_type['title2']] = {
                'text': text.replace('_x000d_', '').strip(' \n;.\t,'),
                'sub': []
            }
        else:
            competencies[last_type['type']][last_type['title1']]['sub'][last_type['title2']]['sub'].append(text.replace('_x000d_', '').strip(' \n;.\t,'))
    return competencies


def get_info(page):
    study_form = page['Unnamed: 2'][40].split(':')[-1].strip().split(' ')[0]
    study_code, study_name = page['Unnamed: 3'][27].strip().split(' ', 1)
    study_direction = page['Unnamed: 3'][28]
    study_code = study_code.replace('.', '')
    return {
        'code': study_code.replace('_x000d_', '').strip(' \n;.\t,'),
        'name': study_name.replace('_x000d_', '').strip(' \n;.\t,'),
        'form': study_form.replace('_x000d_', '').strip(' \n;.\t,'),
        'direction': study_direction.replace('_x000d_', '').strip(' \n;.\t,'),
        'year': str(page['Unnamed: 22'][38]).replace('_x000d_', '').strip(' \n;.\t,'),
    }

def get_name(group, info):
    year = int(info['year'])
    current_year = datetime.datetime.now().year
    return f"__ИД_{group}_{current_year-year+1}к__23-24.docx"


def load_plan(group, path):
    excel = pd.ExcelFile(path)

    info = get_info(excel.parse('Титул'))
    competencies = get_competencies(excel.parse('Компетенции'))
    filename = get_name(group, info)

    return {
        'filename': filename,
        'info': info,
        'competencies': competencies,
    }
