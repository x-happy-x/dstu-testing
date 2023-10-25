from .tools import get_now_year
from .RupResultManagerApi import RupResultManagerApi
from .BaseApi import BaseApi, BaseParams as Params, Method
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
        return self.session.get('https://rpd.donstu.ru/RpdManager/Initialization')

    def get_rup_manager(self):
        if self.rup_manager is None:
            self.rup_manager = RupResultManagerApi(self.session, self.data)
        return self.rup_manager

    def get_departments(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetDepartments',
            data,
            Method.GET,
            Params.year
        )

    def get_disciplines(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetPlanEntities',
            data,
            Method.GET,
            Params.year,
            Params.dep_id,
            Params.show_only_with_rp,
            Params.hide_without_students,
        )

    def get_plans(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetPlanItemRups',
            data,
            Method.GET,
            Params.year,
            Params.dep_id,
            Params.disc_name,
            Params.show_only_with_rp,
            Params.hide_without_students,
            Params.object_type,
        )

    def get_rps(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManager/GetRps',
            data,
            Method.POST,
            Params.year,
            Params.disc_name,
            Params.rup_row_id,
            Params.rup_name,
        )

    def get_summary(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManagmentPanel/LoadSummary',
            data,
            Method.POST,
            Params.rup_row_id,
            Params.rpd_id,
        )

    def get_my_rps(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RpdManagmentPanel/GetRPCards',
            data,
            Method.GET,
            Params.year,
        )
