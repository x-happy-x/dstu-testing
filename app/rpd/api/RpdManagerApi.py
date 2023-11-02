from .tools import get_now_year
from .RupResultManagerApi import RupResultManagerApi
from .BaseApi import BaseApi, Params, Method
from .RpdApi import RpdApi


class RpdManagerApi(BaseApi):
    data = {
        Params.year: get_now_year(),
        Params.dep_id: 9,
        Params.show_only_with_rp: False,
        Params.hide_without_students: False,
        Params.disc_name: '',
        Params.rup_row_id: 0,
        Params.rup_name: '',
        Params.rpd_id: '',
        Params.title_id: '',
        Params.object_type: 2,
    }
    rup_manager = None

    def initialization(self):
        return self.query('https://rpd.donstu.ru/RpdManager/Initialization')

    def get_rup_manager(self):
        if self.rup_manager is None:
            self.rup_manager = RupResultManagerApi(self.session, self.data, init=self.session is not None)
        return self.rup_manager

    def get_departments(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetDepartments',
            params=data,
            param_names=[
                Params.year,
            ],
            method=Method.GET,
        )

    def get_disciplines(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetPlanEntities',
            params=data,
            param_names=[
                Params.year,
                Params.dep_id,
                Params.show_only_with_rp,
                Params.hide_without_students,
            ],
            method=Method.GET,
        )

    def get_plans(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetPlanItemRups',
            params=data,
            param_names=[
                Params.year,
                Params.dep_id,
                Params.disc_name,
                Params.show_only_with_rp,
                Params.hide_without_students,
                Params.object_type,
            ],
            method=Method.GET,
        )

    def get_rps(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetRps',
            data=data,
            data_names=[
                Params.year,
                Params.disc_name,
                Params.rup_row_id,
                Params.rup_name,
            ],
            method=Method.POST,
        )

    def get_summary(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManagmentPanel/LoadSummary',
            data=data,
            data_names=[
                Params.rup_row_id,
                Params.rpd_id,
            ],
            method=Method.POST,
        )

    def get_my_rps(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManagmentPanel/GetRPCards',
            params=data,
            param_names=[
                Params.year,
            ],
            method=Method.GET,
        )
