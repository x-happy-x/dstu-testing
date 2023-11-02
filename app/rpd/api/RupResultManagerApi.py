from .BaseApi import BaseApi, Params
from .tools import get_now_year


class RupResultManagerApi(BaseApi):
    data = {
        Params.year: get_now_year(),
        Params.rup_id: 0,
        Params.direction_id: 0,
    }

    def initialization(self):
        return self.query('https://rpd.donstu.ru/RupResultManager/Initialize')

    def get_programs(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RupResultManager/GetPrograms',
            params=data,
            param_names=[
                Params.year
            ]
        )

    def get_rup_results(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RupResultManager/GetRupResults',
            params=data,
            param_names=[
                Params.rup_id,
                Params.direction_id,
            ]
        )

    def get_lms_results(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RupResultManager/GetLmsResults',
            params=data,
            param_names=[
                Params.rup_id,
                Params.direction_id,
            ]
        )

    def get_plan_item_references(self, data=None):
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/RupResultManager/GetPlanItemReferences',
            params=data,
            param_names=[
                Params.rup_id,
                Params.direction_id,
            ]
        )
