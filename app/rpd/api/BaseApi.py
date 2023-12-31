import requests

from .tools import init_session, get_now_year


class Method:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'
    DELETE = 'DELETE'
    HEAD = 'HEAD'


class Params:
    # RPD Manager
    year = 'accYear'
    dep_id = 'depId'
    show_only_with_rp = 'showOnlyWithRp'
    hide_without_students = 'hideWithoutStudents'
    disc_name = 'discName'
    rup_row_id = 'rupRowId'
    rup_name = 'rupName'
    rpd_id = 'rpdId'
    title_id = 'titleId'
    object_type = 'objType'

    # RupResult Manager
    rup_id = 'rupId'
    direction_id = 'directionId'

    # RPD
    rp_id = 'rpId'
    hash = 'hash'


class BaseApi:
    data = {
        Params.year: get_now_year(),
    }

    def __init__(self, session: requests.Session = None, data: dict = None, init=True):
        if data is not None:
            self.data.update(data)
        if session is None and init:
            session = init_session()
        self.session = session

    def set_year(self, year: str | int):
        if isinstance(year, int):
            self.data['year'] = f"{year}-{year + 1}"
        else:
            self.data['year'] = year

    def set_param(self, key: str, value):
        self.data[key] = value

    def set_params(self, *params):
        self.set_dict({key: value for key, value in params})

    def set_dict(self, data: dict):
        self.data.update(data)

    def load_params(self, *names):
        return {name: self.data[name] for name in names}

    def query(
            self,
            url: str,
            params: dict = None,
            data: dict = None,
            method: str = "GET",
            param_names: list[str] = None,
            data_names: list[str] = None
    ):

        if data is None:
            data = {}
        if data_names is not None:
            data_ = self.load_params(*data_names)
            data_.update(data)
            data = data_

        if params is None:
            params = {}
        if param_names is not None:
            params_ = self.load_params(*param_names)
            params_.update(params)
            params = params_

        print(method, url, params, data)

        if self.session is None:
            self.session = init_session()

        if method == Method.GET:
            response = self.session.get(url, params=params, data=data)
        elif method == Method.POST:
            response = self.session.post(url, params=params, data=data)
        elif method == Method.PUT:
            response = self.session.put(url, params=params, data=data)
        elif method == Method.PATCH:
            response = self.session.patch(url, params=params, data=data)
        elif method == Method.DELETE:
            response = self.session.delete(url, params=params, data=data)
        elif method == Method.HEAD:
            response = self.session.head(url, params=params, data=data)
        elif method == Method.OPTIONS:
            response = self.session.options(url, params=params, data=data)
        else:
            response = None
            print(f"Method: {method} - not supported")

        return response
