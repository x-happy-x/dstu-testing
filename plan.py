import json
import os
import re
import pandas as pd


def plan2json(path, sheet, skip=None, save=None, pattern=r'[А-Я]+'):
    if skip is None:
        skip = [0, 0]
    files = os.listdir(path)
    out = {}
    for file in files:

        year = int('20' + file.split('.')[0][::-1].split('-')[0][::-1])
        kurs = int(file.split('_')[-1].split('-')[0])

        name = file.split('_')[0]
        match = re.search(pattern, name)
        if match:
            name = match.group()

        excel = pd.ExcelFile(os.path.join(path, file))

        df = excel.parse(sheet)
        subjs = {}
        for i in range(skip[0], len(df['Закрепленная кафедра']) - skip[1]):
            subj = df.iloc[i, 2]
            block = df.iloc[i, 1]
            kaf = df['Закрепленная кафедра'][i]

            if str(subj) == 'nan' or str(kaf) == 'nan':
                continue

            add_data = {"Кафедра": int(kaf), "Блок": block}
            if subj in subjs:
                b = subjs.pop(subj)
                b['R'] = subj
                add_data['R'] = subj
                subjs[f"{subj} ({b['Блок'].split('(')[-1].split(')')[0]})"] = b
                subjs[f"{subj} ({block.split('(')[-1].split(')')[0]})"] = add_data
                # print(file, subj, add_data, b, "повтор")
            else:
                subjs[subj] = add_data

        if name not in out:
            out[name] = {}
        if year not in out[name]:
            out[name][year] = {}
        if kurs not in out[name][year]:
            out[name][year][kurs] = {}
        out[name][year][kurs][file] = subjs

    if save is not None:
        with open(save, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False)

    return out


def preps2json(file, sheet, skip=None, save=None):
    if skip is None:
        skip = [0, 0]

    excel = pd.ExcelFile(file)
    df = excel.parse(sheet)

    pr = {}

    last_name = None
    last_id = None
    last_index = 0
    subjects = {}

    for i in range(skip[0], len(df['№']) - skip[1]):
        prep = df.iloc[i]
        if 'nan' != str(prep['Фамилия']):
            last_name = f"{prep['Фамилия'].strip()} {prep['Имя'].strip()} {prep['Отчество'].strip()}"
            if last_id is None:
                last_index = i
                subjects[last_index] = []
        if 'nan' != str(prep['№']):
            last_id = prep['№'].strip().strip('.')
            if last_name is None:
                last_index = i
                subjects[last_index] = []
        subjects[last_index].append(prep['Дисциплина'])
        if last_id is None or last_name is None:
            continue
        pr[last_index] = {'id': last_id, 'name': last_name}
        last_id = None
        last_name = None

    for i in subjects:
        pr[i]['subjs'] = subjects[i]

    preps = {}
    for i in pr:
        preps[pr[i]['name']] = {}
        for s in pr[i]['subjs']:
            if str(s) == 'nan':
                continue
            ss = s.split('[')
            preps[pr[i]['name']][ss[0].strip()] = ss[1].strip().strip(']').strip().upper().split(',') if len(
                ss) > 1 else []

    if save is not None:
        with open(save, 'w', encoding='utf-8') as f:
            json.dump(preps, f, ensure_ascii=False)

    return preps


def get_prep(preps, subj, group, short=True):
    subj = subj.strip()  # .lower()
    group = group.strip().upper()
    finded = []
    for prep in preps:
        if subj in preps[prep] and (len(preps[prep][subj]) == 0 or group in preps[prep][subj]):
            if short:
                f, i, o = prep.split(' ')
                finded.append(f"{f} {i[0]}.{o[0]}.")
                continue
            finded.append(prep)
    return None if len(finded) == 0 else ", ".join(finded)


def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_departament_name(departments, code):
    return list(filter(lambda x: x['number'] == code, departments))[0]['name']


def plan2excel(plans, preps, departments, kaf, save=None):
    if save is None:
        save = "plan"
    writer = pd.ExcelWriter(f'{save}.xlsx', engine='xlsxwriter')
    for plan_name in plans:
        for year in plans[plan_name]:
            for kurs in plans[plan_name][year]:
                plan = plans[plan_name][year][kurs]
                plan = plan[list(plan.keys())[0]]

                i = 1
                map_subjs = []
                for subj in plan:
                    kaf_name = get_departament_name(departments, plan[subj]['Кафедра'])
                    if kaf == plan[subj]['Кафедра']:
                        map_subjs.append([i, subj, get_prep(preps, subj, plan_name), kaf_name])
                    else:
                        map_subjs.append([i, subj, None, kaf_name])
                    i += 1

                df = pd.DataFrame(map_subjs,
                                  columns=['№', 'Наименование дисциплины',
                                           'Ответственный за разработку комплекта ТЗ',
                                           'Кафедра'])

                df.to_excel(writer, sheet_name=f"{plan_name} ({kurs}-{str(year)[2:]})", index=False)

    writer.close()


# plans = plan2json('./УП', 'План', [2, 0], save='./plan.json')
# preps = preps2json("./Учет.xlsx", "Учет", [2, 0], './preps.json')

plans = load_json('./plan.json')
# preps = load_json('./preps.json')
# departments = load_json('./departments.json')
#
# plan2excel(plans, preps, departments, 9, "Карта учета ОМ и тестов")

history = {}
for plan_name in plans:
    if plan_name in history:
        history[plan_name] = {}
    for year in plans[plan_name]:
        if year in history[plan_name]:
            history[plan_name][year] = {}
        kurses = sorted(plans[plan_name][year].keys())[::-1]
        first = True
        subjects = {}
        for i in range(len(kurses) - 1):

            kurs = kurses[i]

            if kurs in history[plan_name][year]:
                history[plan_name][year][kurs] = {'+': {}, '-': {}}

            if kurs == kurses[-1]:
                print(kurs)

            plan = plans[plan_name][year][kurs]
            plan = plan[list(plan.keys())[0]]

            print(plan)
            if first:
                first = False