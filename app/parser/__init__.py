import os

import numpy as np
import pandas as pd

from . import gift, json, txt
from ..entity import *

from .txt.converter import txt2json

from .json.converter import json2gift
from .doc.layout import gift2layout
from .plan.parser import plan2json, plan2excel, preps2json


def txt2json_f(filepath, save=None):
    content = txt.from_file(filepath)
    jcontent = txt2json(content)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".json"
    json.to_file(jcontent, save)


def txt2gift(content):
    jdata = txt2json(content)
    return json2gift(jdata)


def txt2gift_f(filepath, save=None):
    txt_ = txt.from_file(filepath)
    questions = txt2gift(txt_)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".gift"
    questions.save(save)


def txt2layout_f(from_file, template_file=None, to_file=None, info=None, html_convert=True):
    if to_file is None:
        to_file = os.path.splitext(from_file)[0] + ".docx"
    txt_ = txt.from_file(from_file)
    gdata = txt2gift(txt_)
    return gift2layout(gdata, to_file, info, html_convert, template_file)


def json2gift_f(filepath, save=None):
    data = json.from_file(filepath)
    gift_test = json2gift(data)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".gift"
    gift_test.save(save)


def stats2df(stats):
    index = {}
    columns = []
    data = []
    for stype, value in stats.items():
        columns.append(TYPES[stype])
        for key, value2 in value.items():
            index[key] = None
    index = list(index.keys())

    for stype, value in stats.items():
        v = []
        ssum = 0
        for key in index:
            if key in value:
                ssum += value[key]
                v.append(value[key])
            else:
                v.append(0)
        data.append(v + [ssum])
    data.insert(0, index + ["Итого:"])
    df = pd.DataFrame(np.array(data).T, columns=[""] + columns)
    return df


def to_layout(
        txt_test_file=None,
        gift_test_file=None,
        out='./source/Тесты/[дисциплина]/ТЕСТ_[направление]_[индикатор]_[дисциплина].docx',
        template_file=None,
        html_convert=True,
        info=None
):
    if info is None:
        info = {}

    txt_test = None
    json_test = None
    gift_test = None

    if txt_test_file:
        txt_test = txt.from_file(txt_test_file)
        json_test = txt2json(txt_test)
        gift_test = json2gift(json_test)

    if gift_test_file:
        main = gift.from_file(gift_test_file)
        main.add(gift_test)
    else:
        main = gift_test

    if main is None:
        print('txt_test_file and gift_test_file must be specified')
        return None

    out_file = ''
    if not isinstance(info, list):
        info = [info]

    for info_data in info:
        out_file, layout, structure, questions = gift2layout(
            main,
            out,
            info=info_data,
            html_convert=html_convert,
            template_file=template_file,
        )

    dest = os.path.split(out_file)[0]

    if txt_test_file:
        txt.to_file(
            txt_test,
            os.path.join(dest, f"вопросы-{info[0]['дисциплина']}.txt")
        )
        json.to_file(
            json_test,
            os.path.join(dest, f"вопросы-{info[0]['дисциплина']}-{len(json_test)}.json")
        )

    json.to_file(
        {"info": info},
        os.path.join(dest, f"info.json")
    )
    main.save(
        os.path.join(dest, f"вопросы-{info[0]['дисциплина']}-{len(main)}.gift"),
    )
