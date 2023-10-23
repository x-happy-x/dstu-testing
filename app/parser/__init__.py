import json
import os
import random
from datetime import datetime

import docx
import docxtpl
import numpy as np
import pandas as pd
import regex as re

from . import gift
from .gift import Gift
from .doc import fill_test_template
from ..entity import *

from .txt import txt2json, open_txt, parse_txt, save_txt
from .json import json2gift, open_json, parse_json, save_json


def txt2json_f(filepath, save=None):
    content = open_txt(filepath)
    jcontent = txt2json(content)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".json"
    save_json(jcontent, save)


def txt2gift(content):
    jdata = txt2json(content)
    gdata = json2gift(jdata)
    return Gift(content=gdata)


def txt2gift_f(filepath, save=None):
    txt = open_txt(filepath)
    questions = txt2gift(txt)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".gift"
    questions.save(save)


def txt2docx_f(template_file, from_file, to_file=None, info=None, styles=None, html_convert=True):
    if info is None:
        info = {}
    if styles is None:
        styles = STYLES
    if to_file is None:
        to_file = os.path.splitext(from_file)[0] + ".docx"
    txt = open_txt(from_file)
    gdata = txt2gift(txt)
    return gift2docx(template_file, gdata, to_file, info, styles, html_convert)


def json2gift_f(filepath, save=None):
    data = open_json(filepath)
    content = json2gift(data)
    if save is None:
        save = os.path.splitext(filepath)[0] + ".gift"
    save_txt(content, save)


def gift2docx(template_file, from_file, to_file, info, styles, html_convert=True, custom_groups=None):
    if isinstance(from_file, str):
        with open(from_file, 'r', encoding="utf-8") as file:
            text = file.read()
            test = gift.parse(text)
    else:
        test = from_file
    template = docx.Document(template_file)
    if custom_groups is None:
        custom_groups = {
            "GROUP_1": [
                {
                    "type": MULTIPLE_CHOICE_RADIO,
                    "category": 1,
                    "count": 5
                },
                {
                    "type": MULTIPLE_CHOICE_RADIO,
                    "category": 2,
                    "count": 17
                },
                {
                    "type": MULTIPLE_CHOICE_CHECKBOX,
                    "category": 2,
                    "count": 10
                },
                {
                    "type": MULTIPLE_CHOICE_RADIO,
                    "category": 3,
                    "count": 3
                }
            ],
            "GROUP_2": [
                {
                    "type": MATCHING,
                    "category": 1,
                    "count": 2
                },
                {
                    "type": MATCHING,
                    "category": 2,
                    "count": 7
                },
                {
                    "type": MATCHING,
                    "category": 3,
                    "count": 1
                }
            ],
            "GROUP_3": [
                {
                    "type": SHORT,
                    "category": 1,
                    "count": 7
                },
                {
                    "type": SHORT,
                    "category": 2,
                    "count": 24
                },
                {
                    "type": SHORT,
                    "category": 3,
                    "count": 4
                }
            ]
        }
    q_sorted, stats, q_skipped = fill_test_template(template, {
        MULTIPLE_CHOICE_CHECKBOX: "MultipleChoiceCheckbox",
        MULTIPLE_CHOICE_RADIO: "MultipleChoiceRadio",
        SHORT: "Short",
        MATCHING: "Matching",
    }, test, styles=styles, html_convert=html_convert, custom_groups=custom_groups)

    temp_file = f'./tmp/temp-{datetime.now():%Y_%m_%d %H_%M_%S%z}.docx'
    template.save(temp_file)
    context = {
        "simple_c": stats[MULTIPLE_CHOICE_RADIO][CATEGORY[1]] if CATEGORY[1] in stats[MULTIPLE_CHOICE_RADIO] else 0,
        "simple_a": stats[MATCHING][CATEGORY[1]] if CATEGORY[1] in stats[MATCHING] else 0,
        "simple_o": stats[SHORT][CATEGORY[1]] if CATEGORY[1] in stats[SHORT] else 0,
        "medium_c": stats[MULTIPLE_CHOICE_RADIO][CATEGORY[2]] if CATEGORY[2] in stats[MULTIPLE_CHOICE_RADIO] else 0,
        "medium_a": stats[MATCHING][CATEGORY[2]] if CATEGORY[2] in stats[MATCHING] else 0,
        "medium_o": stats[SHORT][CATEGORY[2]] if CATEGORY[2] in stats[SHORT] else 0,
        "hard_c": stats[MULTIPLE_CHOICE_RADIO][CATEGORY[3]] if CATEGORY[2] in stats[MULTIPLE_CHOICE_RADIO] else 0,
        "hard_a": stats[MATCHING][CATEGORY[3]] if CATEGORY[2] in stats[MATCHING] else 0,
        "hard_o": stats[SHORT][CATEGORY[3]] if CATEGORY[2] in stats[SHORT] else 0,
    }
    context["all_c"] = context["simple_c"] + context["medium_c"] + context["hard_c"]
    context["all_a"] = context["simple_a"] + context["medium_a"] + context["hard_a"]
    context["all_o"] = context["simple_o"] + context["medium_o"] + context["hard_o"]
    context["all_simple"] = context["simple_c"] + context["simple_a"] + context["simple_o"]
    context["all_medium"] = context["medium_c"] + context["medium_a"] + context["medium_o"]
    context["all_hard"] = context["hard_c"] + context["hard_a"] + context["hard_o"]
    context["all"] = context["all_simple"] + context["all_medium"] + context["all_hard"]
    context.update(info)
    template = docxtpl.DocxTemplate(temp_file)
    template.render(context)
    for key, value in context.items():
        if key.lower() == "индикатор" or key.lower() == "компетенция":
            to_file = to_file.replace("[" + key.lower() + "]", str(value).split(" ")[0])
        else:
            to_file = to_file.replace("[" + key.lower() + "]", str(value))
    to_file = to_file.replace("[дата]", f"{datetime.now():%Y_%m_%d %H_%M_%S%z}")
    if not to_file.endswith(".docx") and not to_file.endswith(".doc"):
        to_file += ".docx"
    to_file = to_file.replace("\n", " ")
    template.save(to_file)
    os.remove(temp_file)
    return to_file, test, q_sorted, q_skipped, stats


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
