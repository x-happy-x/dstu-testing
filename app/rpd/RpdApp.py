from docx.opc.coreprops import CoreProperties

from .Comptencies import CompetenceBoard, Competence, Indicator, Level
from .api import RpdManagerApi, RpdApi, get_now_year, Params
from app.parser.json import open_json, save_json
import json
import os
from typing import List, Any
from datetime import datetime
import docx

MAX_LENGTH = 200
MAX_WORDS = 10


class Result:
    success: bool
    message: str

    def __init__(self, data, success=True, message=None):
        self.data = data
        self.success = success
        self.message = message

    def __call__(self, key, *args, **kwargs):
        if self.success:
            return list(filter(key, self.data))
        else:
            raise ValueError(self.message)

    def __getitem__(self, index):
        if self.success:
            return self.data[index]
        else:
            raise ValueError(self.message)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Результат (success:{self.success}, message:{self.message}, data:\n{self.data})"


class RpdApp:
    version = "0.4.3.6"
    rpd_api = None

    def __init__(self, manager: RpdManagerApi = None, cache_dir: str = None, load_cache: bool = True):
        if manager is None:
            manager = RpdManagerApi()
        if cache_dir is None:
            cache_dir = "./.cache"
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)
        self.cache_dir = cache_dir
        self.load_cache = load_cache
        self.manager = manager

    def get_rpd_api(self):
        if self.rpd_api is None:
            self.rpd_api = RpdApi(session=self.manager.session)
        return self.rpd_api

    def departments(self, year=None) -> Result:
        if year is None:
            year = get_now_year()

        current_dir = os.path.join(self.cache_dir, year)
        filename = "departments.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = []
        if self.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data['data']['department']['items']
                for item in items:
                    ds.append(Department(self, current_dir, **item, year=year))
        else:
            response = self.manager.get_departments(
                {
                    Params.year: year
                }
            )
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if response_data['result']:
                        items = response_data['data']['department']['items']
                        for item in items:
                            ds.append(Department(self, current_dir, **item, year=year))
                else:
                    return Result(ds, False, response.text)
            except Exception as e:
                return Result(ds, False, str(e))
        return Result(ds, message=message)


class Department:
    id: int
    number: int
    name: str
    has_permission: bool
    year: str

    def __init__(self, app: RpdApp, path: str, **kwargs) -> None:
        self.app = app
        self.manager = app.manager
        self.path = path

        self.id = kwargs.get('id', None)
        self.number = kwargs.get('number', None)
        self.name = kwargs.get('name', None)
        self.has_permission = kwargs.get('hasPermission', None)
        self.year = kwargs.get('year', None)

    def set(self, id: int, number: int, name: str, has_permission: bool) -> None:
        self.id = id
        self.number = number
        self.name = name
        self.has_permission = has_permission

    def disciplines(self, show_only_with_rp=False, hide_without_students=False) -> Result:

        sn = self.name.strip(' \r\n\t').replace("\"", "'")
        s1 = None
        if len(sn) > MAX_LENGTH:
            s1 = sn
            sn = " ".join(sn.split(" ", MAX_WORDS)[:MAX_WORDS - 1])
        current_dir = os.path.join(self.path, sn)
        filename = f"disciplines_{show_only_with_rp}_{hide_without_students}.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = []
        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data['data']['planItems']['items']
                for item in items:
                    ds.append(Discipline(self.app, self, current_dir, **item))
        else:
            response = self.app.manager.get_disciplines(
                {
                    Params.year: self.year,
                    Params.dep_id: self.id,
                    Params.show_only_with_rp: show_only_with_rp,
                    Params.hide_without_students: hide_without_students,
                }
            )
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if s1 is not None:
                        with open(os.path.join(current_dir, 'full_name.txt'), 'w') as f:
                            f.write(s1)
                    if response_data['result']:
                        items = response_data['data']['planItems']['items']
                        for item in items:
                            ds.append(Discipline(self.app, self, current_dir, **item))
                else:
                    return Result(ds, False, response.text)
            except Exception as e:
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Кафедра (id:{self.id}, year:{self.year}, number:{self.number}, name:{self.name}, has_permission:{self.has_permission})"


class Discipline:
    num: int
    name: str
    dep_id: int
    object_type: int
    is_practice: bool
    is_module: bool

    def __init__(self, app: RpdApp, department: Department, path: str, **kwargs) -> None:
        self.app = app
        self.manager = app.manager
        self.department = department
        self.path = path

        self.num = kwargs.get('num', None)
        self.name = kwargs.get('name', None)
        self.dep_id = kwargs.get('depId', None)
        self.object_type = kwargs.get('objectType', None)
        self.is_practice = kwargs.get('isPractice', None)
        self.is_module = kwargs.get('isModule', None)

    def set(self, num: int, name: str, dep_id: int, object_type: int, is_practice: bool, is_module: bool) -> None:
        self.num = num
        self.name = name
        self.dep_id = dep_id
        self.object_type = object_type
        self.is_practice = is_practice
        self.is_module = is_module

    def plans(self, show_only_with_rp=False, hide_without_students=False) -> Result:

        sn = self.name.strip(' \r\n\t').replace("\"", "'")
        s1 = None
        if len(sn) > MAX_LENGTH:
            s1 = sn
            sn = " ".join(sn.split(" ", MAX_WORDS)[:MAX_WORDS - 1])
        current_dir = os.path.join(self.path, sn)
        filename = f"plans_{show_only_with_rp}_{hide_without_students}.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = []

        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data['data']['rup']['items']
                for item in items:
                    ds.append(Plan(self.app, self, current_dir, **item))
        else:
            response = self.manager.get_plans(
                {
                    Params.year: self.department.year,
                    Params.dep_id: self.department.id,
                    Params.show_only_with_rp: show_only_with_rp,
                    Params.hide_without_students: hide_without_students,
                    Params.disc_name: self.name,
                    Params.object_type: self.object_type
                }
            )
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if s1 is not None:
                        with open(os.path.join(current_dir, 'full_name.txt'), 'w') as f:
                            f.write(s1)
                    if response_data['result']:
                        items = response_data['data']['rup']['items']
                        for item in items:
                            ds.append(Plan(self.app, self, current_dir, **item))
                else:
                    return Result(ds, False, response.text)
            except Exception as e:
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (f"Дисциплина (num:{self.num}, name:{self.name}, dep_id:{self.dep_id}, object_type:{self.object_type}, "
                f"is_practice:{self.is_practice}, is_module:{self.is_module})")


class Plan:
    rup_row_id: int
    rup_id: int
    has_draft: bool
    is_draft_currupted: bool
    index: str
    rup_name: str
    fgos_type_name: str
    study_form: str
    study_level: str
    spec_name: str
    sub_spec_name: str
    nagr_rows: list[str]
    rp_count: int
    url: str

    def __init__(self, app: RpdApp, discipline: Discipline, path: str, **kwargs) -> None:
        self.app = app
        self.manager = app.manager
        self.discipline = discipline
        self.path = path

        self.rup_row_id = kwargs.get('rupRowId', None)
        self.rup_id = kwargs.get('rupId', None)
        self.has_draft = kwargs.get('hasDraft', None)
        self.is_draft_currupted = kwargs.get('isDraftCurrupted', None)
        self.index = kwargs.get('index', None)
        self.rup_name = kwargs.get('rupName', None)
        self.fgos_type_name = kwargs.get('fgosTypeName', None)
        self.study_form = kwargs.get('studyForm', None)
        self.study_level = kwargs.get('studyLevel', None)
        self.spec_name = kwargs.get('specName', None)
        self.sub_spec_name = kwargs.get('subSpecName', None)
        self.nagr_rows = kwargs.get('nagrRows', None)
        self.rp_count = kwargs.get('rpCount', None)
        self.url = kwargs.get('url', None)

    def set(self, rup_row_id: int, rup_id: int, has_draft: bool, is_draft_currupted: bool, index: str, rup_name: str,
            fgos_type_name: str, study_form: str, study_level: str, spec_name: str, sub_spec_name: str,
            nagr_rows: List[Any], rp_count: int, url: str) -> None:
        self.rup_row_id = rup_row_id
        self.rup_id = rup_id
        self.has_draft = has_draft
        self.is_draft_currupted = is_draft_currupted
        self.index = index
        self.rup_name = rup_name
        self.fgos_type_name = fgos_type_name
        self.study_form = study_form
        self.study_level = study_level
        self.spec_name = spec_name
        self.sub_spec_name = sub_spec_name
        self.nagr_rows = nagr_rows
        self.rp_count = rp_count
        self.url = url

    def rps(self) -> Result:

        current_dir = os.path.join(self.path, self.rup_name.strip(' \r\n\t').replace("\"", "'"))
        filename = f"rps.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = []

        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data['data']['rps']['items']
                for item in items:
                    ds.append(RP(self.app, self, current_dir, **item))
        else:
            response = self.manager.get_rps(
                {
                    Params.year: self.discipline.department.year,
                    Params.rup_row_id: self.rup_row_id,
                    Params.rup_name: self.rup_name,
                    Params.disc_name: self.discipline.name,
                }
            )
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if response_data['result']:
                        items = response_data['data']['rps']['items']
                        for item in items:
                            ds.append(RP(self.app, self, current_dir, **item))
                else:
                    return Result(ds, False, response.text)
            except Exception as e:
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (f"Учебный план (rup_row_id:{self.rup_row_id}, rup_id:{self.rup_id}, has_draft:{self.has_draft}, "
                f"is_draft_currupted:{self.is_draft_currupted}, index:{self.index}, rup_name:{self.rup_name}, "
                f"fgos_type_name:{self.fgos_type_name}, study_form:{self.study_form}, study_level:{self.study_level}, "
                f"spec_name:{self.spec_name}, sub_spec_name:{self.sub_spec_name}, nagr_rows:{self.nagr_rows}, "
                f"rp_count:{self.rp_count}, url:{self.url})")


class RP:
    id: int
    title_id: int
    rup_row_id: int
    name: str
    modified_on: datetime
    user: str
    owner: str
    has_draft: bool
    is_draft_currupted: bool
    direction_oop_id: int
    direction_oop_code: str
    direction_oop_name: str
    status: None

    def __init__(self, app: RpdApp, plan: Plan, path: str, **kwargs) -> None:
        self.app = app
        self.manager = app.manager
        self.api = app.get_rpd_api()
        self.plan = plan
        self.path = path

        self.id = kwargs.get('id', None)
        self.title_id = kwargs.get('titleId', None)
        self.rup_row_id = kwargs.get('rupRowId', None)
        self.name = kwargs.get('name', None)
        self.modified_on = kwargs.get('modifiedOn', None)
        self.user = kwargs.get('user', None)
        self.owner = kwargs.get('owner', None)
        self.has_draft = kwargs.get('hasDraft', None)
        self.is_draft_currupted = kwargs.get('isDraftCurrupted', None)
        self.direction_oop_id = kwargs.get('directionOOPId', None)
        self.direction_oop_code = kwargs.get('directionOOPCode', None)
        self.direction_oop_name = kwargs.get('directionOOPName', None)
        self.status = kwargs.get('status', None)

    def set(self, id: int, title_id: int, rup_row_id: int, name: str, modified_on: datetime, user: str, owner: str,
            has_draft: bool, is_draft_currupted: bool, direction_oop_id: int, direction_oop_code: str,
            direction_oop_name: str, status: None) -> None:
        self.id = id
        self.title_id = title_id
        self.rup_row_id = rup_row_id
        self.name = name
        self.modified_on = modified_on
        self.user = user
        self.owner = owner
        self.has_draft = has_draft
        self.is_draft_currupted = is_draft_currupted
        self.direction_oop_id = direction_oop_id
        self.direction_oop_code = direction_oop_code
        self.direction_oop_name = direction_oop_name
        self.status = status

    def summary(self):

        self.api.set_dict({
            Params.rup_row_id: self.rup_row_id,
            Params.rp_id: self.id,
        })

        sn = self.name.strip(' \r\n\t').replace("\"", "'")
        s1 = None
        if len(sn) > MAX_LENGTH:
            s1 = sn
            sn = " ".join(sn.split(" ", MAX_WORDS)[:MAX_WORDS - 1])
        current_dir = os.path.join(self.path, f"{self.id}_{sn}/")
        filename = f"summary.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = {}

        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data
                ds = items
        else:
            response = self.api.get_summary()
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if s1 is not None:
                        with open(os.path.join(current_dir, 'full_name.txt'), 'w') as f:
                            f.write(s1)
                    if response_data['result']:
                        items = response_data
                        ds = items
                else:
                    print(response.status_code, response.text)
                    return Result(ds, False, response.text)
            except Exception as e:
                print(e)
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def FOS(self):
        self.api.set_dict({
            Params.rup_row_id: self.rup_row_id,
            Params.rp_id: self.id,
        })

        sn = self.name.strip(' \r\n\t').replace("\"", "'")
        s1 = None
        if len(sn) > MAX_LENGTH:
            s1 = sn
            sn = " ".join(sn.split(" ", MAX_WORDS)[:MAX_WORDS - 1])
        current_dir = os.path.join(self.path, f"{self.id}_{sn}/")
        filename = f"fos.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = {}

        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data['data']
                ds['Контрольные вопросы и задания'] = items['field1']
                ds['Темы письменных работ'] = items['field2']
                ds['Оценочные материалы'] = items['field3']
                ds['Перечень видов оценочных средств'] = items['field4']
                ds['Ссылка на СКИФ.Тест'] = items['field5']
        else:
            response = self.api.get_fos()
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if s1 is not None:
                        with open(os.path.join(current_dir, 'full_name.txt'), 'w') as f:
                            f.write(s1)
                    if response_data['result']:
                        items = response_data['data']
                        ds['Контрольные вопросы и задания'] = items['field1']
                        ds['Темы письменных работ'] = items['field2']
                        ds['Оценочные материалы'] = items['field3']
                        ds['Перечень видов оценочных средств'] = items['field4']
                        ds['Ссылка на СКИФ.Тест'] = items['field5']
                else:
                    return Result(ds, False, response.text)
            except Exception as e:
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def competencies_board(self):
        self.api.set_dict({
            Params.rup_row_id: self.rup_row_id,
            Params.rp_id: self.id,
        })

        sn = self.name.strip(' \r\n\t').replace("\"", "'")
        s1 = None
        if len(sn) > MAX_LENGTH:
            s1 = sn
            sn = " ".join(sn.split(" ", MAX_WORDS)[:MAX_WORDS - 1])
        current_dir = os.path.join(self.path, f"{self.id}_{sn}/")
        filename = f"competencies.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = CompetenceBoard(self)

        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result'] and not response_data['data']['isEmpty']:
                items = response_data['data']['items']
                for item in items:
                    ds.add_item(item)
        else:
            response = self.api.get_competencies_of_disciplines()
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if s1 is not None:
                        with open(os.path.join(current_dir, 'full_name.txt'), 'w') as f:
                            f.write(s1)
                    if response_data['result'] and not response_data['data']['isEmpty']:
                        items = response_data['data']['items']
                        for item in items:
                            ds.add_item(item)
                else:
                    print(response.status_code, response.text)
                    return Result(ds, False, response.text)
            except Exception as e:
                print(e)
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def literatures(self):
        self.api.set_dict({
            Params.rup_row_id: self.rup_row_id,
            Params.rp_id: self.id,
        })

        sn = self.name.strip(' \r\n\t').replace("\"", "'")
        s1 = None
        if len(sn) > MAX_LENGTH:
            s1 = sn
            sn = " ".join(sn.split(" ", MAX_WORDS)[:MAX_WORDS - 1])
        current_dir = os.path.join(self.path, f"{self.id}_{sn}/")
        filename = f"books.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = []

        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data['data']['cards']
                for item in items:
                    ds.append(Book(self, current_dir, **item))
        else:
            response = self.api.get_appx()
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if s1 is not None:
                        with open(os.path.join(current_dir, 'full_name.txt'), 'w') as f:
                            f.write(s1)
                    if response_data['result']:
                        items = response_data['data']['cards']
                        for item in items:
                            ds.append(Book(self, current_dir, **item))
                else:
                    return Result(ds, False, response.text)
            except Exception as e:
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def appxs(self):
        self.api.set_dict({
            Params.rup_row_id: self.rup_row_id,
            Params.rp_id: self.id,
        })

        sn = self.name.strip(' \r\n\t').replace("\"", "'")
        s1 = None
        if len(sn) > MAX_LENGTH:
            s1 = sn
            sn = " ".join(sn.split(" ", MAX_WORDS)[:MAX_WORDS - 1])
        current_dir = os.path.join(self.path, f"{self.id}_{sn}/")
        filename = f"appx.json"
        filepath = os.path.join(current_dir, filename)

        message = None
        ds = []

        if self.app.load_cache and os.path.exists(filepath):
            message = 'from cache'
            response_data = open_json(filepath)
            if response_data['result']:
                items = response_data['data']['cards']
                for item in items:
                    ds.append(Appx(self.app, self, current_dir, **item))
        else:
            response = self.api.get_appx()
            try:
                if response.status_code == 200:
                    response_data = json.loads(response.text)
                    save_json(response_data, filepath)
                    if s1 is not None:
                        with open(os.path.join(current_dir, 'full_name.txt'), 'w') as f:
                            f.write(s1)
                    if response_data['result']:
                        items = response_data['data']['cards']
                        for item in items:
                            ds.append(Appx(self.app, self, current_dir, **item))
                else:
                    return Result(ds, False, response.text)
            except Exception as e:
                return Result(ds, False, str(e))
        return Result(ds, message=message)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (f"Рабочая программа (id:{self.id}, title_id:{self.title_id}, rup_row_id:{self.rup_row_id}, "
                f"name:{self.name}, modified_on:{self.modified_on}, user:{self.user}, owner:{self.owner}, "
                f"has_draft:{self.has_draft}, is_draft_currupted:{self.is_draft_currupted}, "
                f"direction_oop_id:{self.direction_oop_id}, direction_oop_code:{self.direction_oop_code}, "
                f"direction_oop_name:{self.direction_oop_name}, status:{self.status})")


def try_parse_date(date):
    d = None
    try:
        d = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    except Exception:
        try:
            d = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            d = None  # datetime.min
    return d


class Appx:
    id: int
    name: str
    created: datetime | None
    modified: datetime | None
    download_link: str
    length: float
    type: int

    def __init__(self, app: RpdApp, rp: RP, path: str, **kwargs) -> None:
        self.app = app
        self.manager = app.manager
        self.api = app.get_rpd_api()
        self.rp = rp
        self.path = path

        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)

        self.created = try_parse_date(kwargs.get('created', None))
        self.modified = try_parse_date(kwargs.get('modified', None))

        self.download_link = kwargs.get('downloadLink', None)
        self.length = kwargs.get('length', None)
        self.type = kwargs.get('type', None)

    def set(self, id: int, name: str, created: datetime, modified: datetime, download_link: str, length: float,
            type: int) -> None:
        self.id = id
        self.name = name
        self.created = created
        self.modified = modified
        self.download_link = download_link
        self.length = length
        self.type = type

    def __str__(self):
        return self.__repr__()

    def exists(self, path=None) -> bool:
        if path is None:
            path = self.path
        return os.path.exists(os.path.join(path, self.name))

    def save(self, path=None):
        if path is None:
            path = self.path
        response = self.api.session.get("https://rpd.donstu.ru" + self.download_link)
        if response.status_code == 200:
            with open(os.path.join(path, self.name), "wb") as f:
                f.write(response.content)
                print("Файл сохранен:", os.path.join(path, self.name))
        else:
            print(response.status_code, response.content)

    def metadata(self, path=None) -> CoreProperties:
        if path is None:
            path = self.path
        file = open(os.path.join(path, self.name), 'rb')
        doc = docx.Document(file)
        file.close()
        prop = doc.core_properties
        return prop

    def __repr__(self):
        return (f"Приложение (id:{self.id}, name:{self.name}, created:{self.created}, "
                f"modified:{self.modified}, download_link:{self.download_link}, "
                f"length:{self.length}, type:{self.type})")


class Book:
    rp: RP
    path: str
    selected: bool
    code: str
    lit_type: int
    lit_id: int
    adress: str
    count: int
    name: str
    isbn: None
    lib_number: str
    edition: None
    copies_in_lib: int
    library: str
    is_periodic: bool
    editors: str
    keywords: str
    rubric: str
    is_electron: bool
    name_prolong: str
    authors: str
    year: int
    volume: str
    publishing: str
    modefied_on: datetime
    validity: None
    details: None
    file_id: None
    deleted: bool

    def __init__(self, rp: RP, path: str, **kwarg):
        self.rp = rp
        self.path = path
        self.selected = kwarg.get('selected')
        self.code = kwarg.get('code')
        self.lit_type = kwarg.get('litType')
        self.lit_id = kwarg.get('litId')
        self.adress = kwarg.get('adress')
        self.count = kwarg.get('count')
        self.name = kwarg.get('name')
        self.isbn = kwarg.get('isbn')
        self.lib_number = kwarg.get('libNumber')
        self.edition = kwarg.get('edition')
        self.copies_in_lib = kwarg.get('copiesInLib')
        self.library = kwarg.get('library')
        self.is_periodic = kwarg.get('isPeriodic')
        self.editors = kwarg.get('editors')
        self.keywords = kwarg.get('keywords')
        self.rubric = kwarg.get('rubric')
        self.is_electron = kwarg.get('isElectron')
        self.nameProlong = kwarg.get('nameProlong')
        self.authors = kwarg.get('authors')
        self.year = kwarg.get('year')
        self.volume = kwarg.get('volume')
        self.publishing = kwarg.get('publishing')
        self.modefied_on = kwarg.get('modefiedOn')
        self.validity = kwarg.get('validity')
        self.details = kwarg.get('details')
        self.file_id = kwarg.get('fileId')
        self.deleted = kwarg.get('deleted')

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
