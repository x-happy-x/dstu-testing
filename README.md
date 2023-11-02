# DSTU - Testing

### ������� �����:
`rpd.py` - ������ � ���

`plan.py` - ���������� �����

`layout.py` - �������� �������

### ������� �����:

`.cache` - ����� � �����

* `RPD_API` - ��� �� ��������� ���
* `LAYOUT_BUILDER` - ��� ��� �������� ������ (�� ����� ����� ���������� ���������)

`.moodle` - �� ��� ������� moodle � docker

`.session` - ����� � ������� ��� ������ (����)

`app` - ���� ���

`dest` - ��������������� �����

`source` - �������� �����

`template` - ������� ��� ���������� ����������

### ������� �������������

#### �������� ������ ���:

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
    groups = ['B090302_', 'B090302����_', 'B090302���_', 'B090303����_', 'B090303�����_', '090402����_', '090402���_',
              '090403���_']
    for group in groups:
        if group in plan.rup_name:
            return True
    return False


def rpd_selector(rp: RP) -> bool:
    return True


rpd_app = RpdApp()
rpd_app.load_cache = True


report = rpd_app.walk(
    # �������
    department_selector=department_selector,
    discipline_selector=discipline_selector,
    plan_selector=plan_selector,
    rpd_selector=rpd_selector,
    # �����������
    files_prepare=[fp_search_fos, fp_search_files],
    fos_prepare=[fp_search_skif_test],
    summary_prepare=[fp_search_summary],
    competencies_prepare=[fp_search_competencies]
)

# ���������� ������
json.to_file(report, './source/reports.json')
```

#### �������������� gift � ����� �������� �������:

```python
from app import parser as ps

txt_test_file = None
gift_test_file = "**���� � gift-�����**"

ps.to_layout(
    txt_test_file,
    gift_test_file,
    html_convert=True,
    info=ps.json.from_file('./template/layout-info.json')['info'], 
    # �������� � ./template/layout-info.json ����������, ����������� � �.�.
)
```

#### �������������� txt � ����� �������� �������:

```python
from app import parser as ps

txt_test_file = "**���� � txt-�����**"
gift_test_file = None

ps.to_layout(
    txt_test_file,
    gift_test_file,
    html_convert=True,
    info=ps.json.from_file('./template/layout-info.json')['info'], 
    # �������� � ./template/layout-info.json ����������, ����������� � �.�.
)
```

#### �������������� txt + gift � ����� �������� �������:

```python
from app import parser as ps

txt_test_file = "**���� � txt-�����**"
gift_test_file = "**���� � gift-�����**"

ps.to_layout(
    txt_test_file,
    gift_test_file,
    html_convert=True,
    info=ps.json.from_file('./template/layout-info.json')['info'], 
    # �������� � ./template/layout-info.json ����������, ����������� � �.�.
)
```

#### ��������� ������ �����:

```python
from app.parser import json
from app import parser

# plans = parser.plan2json('./��', '����', [2, 0], save='./plan.json')
# preps = parser.preps2json("./����.xlsx", "����", [2, 0], './preps.json')

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
    "./dest/����� ����� �� � ������.xlsx"
)
```