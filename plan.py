from app.parser import json
from app import parser

# plans = parser.plan2json('./УП', 'План', [2, 0], save='./plan.json')
# preps = parser.preps2json("./Учет.xlsx", "Учет", [2, 0], './preps.json')

plans = json.from_file('./source/plan.json')
preps = json.from_file('./source/preps.json')
departments = json.from_file('./.cache/RPD_API/2023-2024/departments.json')
fos_status = json.from_file('./source/reports.json')

parser.plan2excel(
    plans,
    preps,
    departments['data']['department']['items'],
    fos_status,
    9,
    "./dest/Карта учета ОМ и тестов.xlsx"
)
