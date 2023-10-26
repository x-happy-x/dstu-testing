from .BaseApi import BaseApi, Params, Method


class RpdApi(BaseApi):
    data = {
        Params.rup_row_id: 0,
        Params.rp_id: 0,
        Params.hash: '',
    }

    def default_query(self, url, *names, **kwargs):
        return self.query(
            f"https://rpd.donstu.ru/{url}",
            kwargs,
            kwargs.get('method', Method.GET),
            Params.rup_row_id,
            Params.rp_id, *names
        )

    def get(self, **kwargs):
        """
        Много всего из РПД.
        ИТ: Перечень профессиональных баз данных и информационных справочных систем
        МТО: Полностью (load_mto - херня, всё тут)
        МУ: Полностью
        :param kwargs: rup_row_id и rp_id - обязательные аргументы (hash возможно тоже)
        :return: Response
        """
        return self.default_query('Rp/Load', **kwargs)

    def get_drafts(self, **kwargs):
        """
        Черновики
        :param kwargs: обязательных нет, но возможны rup_row_id, rpd_id и title_id
        :return: Response
        """
        return self.query('https://rpd.donstu.ru/RpdBase/GetDrafts', kwargs, Method.GET)

    def get_reports(self, **kwargs):
        """
        Менеджер отчетов
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('RpReportManager/GetReports', **kwargs)

    def get_title(self, **kwargs):
        """
        Титул. Содержимое
        :param kwargs: rup_row_id и rp_id - обязательные аргументы (hash возможно тоже)
        :return: Response
        """
        return self.default_query('Title/GetTitle', Params.hash, **kwargs)

    def get_objectives_discipline(self, **kwargs):
        """
        РП-1-2. Содержимое
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Rp12/Load', **kwargs)

    def get_competencies_of_disciplines(self, **kwargs):
        """
        РП-3. Компетенции дисциплины (модуля)
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Rp3/Load', **kwargs)

    def get_competence_cards(self, **kwargs):
        """
        РП-3. Карточки компетенций
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Rp3/GetUpResultRupItems', **kwargs)

    def get_prof_standarts(self, **kwargs):
        """
        РП-3. Профессиональные стандарты
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Rp3/GetProfStandards', **kwargs)

    def get_fos(self, **kwargs):
        """
        ФОС. Содержимое
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Fos/Load', **kwargs)

    def get_it(self, **kwargs):
        """
        ИТ. Содержимое
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('ItIndex/GetRefs', **kwargs)

    def get_mto(self, **kwargs):
        """
        МТО. Содержимое (Херня, load грузит МТО)
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('MtoIndex/Load', **kwargs)

    def get_appx(self, **kwargs):
        """
        Приложение. Содержимое
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('AppxIndex/Load', **kwargs)

    def get_summary(self, data=None):
        """
        Панель часов
        :param data: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        if data is None:
            data = {}
        return self.query(
            'https://rpd.donstu.ru/Content/GetSummary',
            data,
            Method.POST,
            Params.rup_row_id,
            Params.rp_id
        )

    def get_literature(self, data=None):
        if data is None:
            data = {}
        return self.default_query('LitIndex/GetCards', **data)

    def get_content(self, data=None):
        if data is None:
            data = {}
        return self.default_query('Content/Load', **data)

    def get_comps(self, data=None):
        if data is None:
            data = {}
        return self.default_query('/UpResultsIndex/GetCards', **data)

    def get_internet_literatures(self, data=None):
        if data is None:
            data = {}
        return self.default_query('ResIndex/GetCards', **data)

    def init_litmanager(self, data=None):
        if data is None:
            data = {}
        return self.default_query('LitManager/Initialize', **data)

    def init_content(self, data=None):
        if data is None:
            data = {}
        return self.default_query('Content/Initialize', **data)

    # Заголовки (НИКОГДА НЕ ПРИГОДИТСЯ, ХЗ ЗАЧЕМ ПИСАЛ =) )

    def init(self, **kwargs):
        """
        Общая инициализация редактора РПД
        :param kwargs: rup_row_id и rp_id - обязательные аргументы (hash возможно тоже)
        :return: Response
        """
        return self.default_query('Rp/Initialize', **kwargs)

    def init_title(self, **kwargs):
        """
        Титул. Заголовки
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Title/Initialize', **kwargs)

    def init_rp12(self, **kwargs):
        """
        РП-1-2. Заголовки
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Rp12/Initialize', **kwargs)

    def init_rp3(self, **kwargs):
        """
        РП-3. Заголовки
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Rp3/Initialize', **kwargs)

    def init_fos(self, **kwargs):
        """
        ФОС. Заголовки
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('Fos/Initialize', **kwargs)

    def init_mto(self, **kwargs):
        """
        МТО. Заголовки
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('MtoIndex/Initialize', **kwargs)

    def init_appx(self, **kwargs):
        """
        Приложение. Заголовки
        :param kwargs: rup_row_id и rp_id - обязательные аргументы
        :return: Response
        """
        return self.default_query('AppxIndex/Initialize', **kwargs)
