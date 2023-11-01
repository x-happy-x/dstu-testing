import os

import numpy as np
import pandas as pd

from . import gift, json, txt
from .gift import Gift
from ..entity import *

from .txt.converter import txt2json

from .json.converter import json2gift
from .doc.layout import gift2layout


def txt2json_f(filepath, save=None):
    content = txt.from_file(filepath)
    jcontent = txt2json(content)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".json"
    json.to_file(jcontent, save)


def txt2gift(content):
    jdata = txt2json(content)
    gdata = json2gift(jdata)
    return Gift(content=gdata)


def txt2gift_f(filepath, save=None):
    txt_ = txt.from_file(filepath)
    questions = txt2gift(txt)
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
    content = json2gift(data)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".gift"
    txt.to_file(content, save)


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
