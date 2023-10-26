from .BaseApi import BaseApi, Params
from .tools import get_now_year


class RupResultManagerApi(BaseApi):
    data = {
        Params.year: get_now_year(),
        Params.rup_id: 0,
        Params.direction_id: 0,
    }

    def initialization(self):
        return self.session.get('https://rpd.donstu.ru/RupResultManager/Initialize')

    def get_programs(self, **kwargs):
        params = self.load_params(Params.year)
        params.update(kwargs)
        return self.session.get('https://rpd.donstu.ru/RupResultManager/GetPrograms', params=params)

    def get_rup_results(self, **kwargs):
        params = self.load_params(
            Params.rup_id,
            Params.direction_id,
        )
        params.update(kwargs)
        return self.session.get('https://rpd.donstu.ru/RupResultManager/GetRupResults', params=params)

    def get_lms_results(self, **kwargs):
        params = self.load_params(
            Params.rup_id,
            Params.direction_id,
        )
        params.update(kwargs)
        return self.session.get('https://rpd.donstu.ru/RupResultManager/GetLmsResults', params=params)

    def get_plan_item_references(self, **kwargs):
        params = self.load_params(
            Params.rup_id,
            Params.direction_id,
        )
        params.update(kwargs)
        return self.session.get('https://rpd.donstu.ru/RupResultManager/GetPlanItemReferences', params=params)
