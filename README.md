# DSTU - Testing

### Главные файлы:
`rpd.py` - работа с РПД

`plan.py` - оформление плана

`layout.py` - создание макетов

### Главные папки:

`.cache` - Папка с кэшем

* `RPD_API` - кэш из менеджера РПД
* `LAYOUT_BUILDER` - кэш при создании макета (не нужен после выполнения программы)

`.moodle` - всё для запуска moodle в docker

`.session` - Папка с данными для сессии (куки)

`app` - весь код

`dest` - Сгенерированные файлы

`source` - Исходные файлы

`template` - Шаблоны для оформления документов

### Примеры использование

#### Выгрузка данных РПД:

```python
from app.parser import json
from app.rpd import *
from app.rpd.RpdApp import RP, Plan, Discipline, Department
from app.rpd.api.BaseApi import Method


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
json.to_file(report, './source/reports.json')
```

#### Преобразование gift в карту тестовых заданий:

```python
from app import parser as ps

txt_test_file = None
gift_test_file = "**путь к gift-файлу**"

ps.to_layout(
    txt_test_file,
    gift_test_file,
    html_convert=True,
    info=ps.json.from_file('./template/layout-info.json')['info'], 
    # Изменить в ./template/layout-info.json дисциплину, направление и т.д.
)
```

#### Преобразование txt в карту тестовых заданий:

```python
from app import parser as ps

txt_test_file = "**путь к txt-файлу**"
gift_test_file = None

ps.to_layout(
    txt_test_file,
    gift_test_file,
    html_convert=True,
    info=ps.json.from_file('./template/layout-info.json')['info'], 
    # Изменить в ./template/layout-info.json дисциплину, направление и т.д.
)
```

#### Преобразование txt + gift в карту тестовых заданий:

```python
from app import parser as ps

txt_test_file = "**путь к txt-файлу**"
gift_test_file = "**путь к gift-файлу**"

ps.to_layout(
    txt_test_file,
    gift_test_file,
    html_convert=True,
    info=ps.json.from_file('./template/layout-info.json')['info'], 
    # Изменить в ./template/layout-info.json дисциплину, направление и т.д.
)
```

#### Генерация таблиц плана:

```python
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
```