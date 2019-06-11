import requests
import json
import time
import threading
import random
import traceback

from common import config
from common import utils
from data import alldata, operators
import mysql.connector as mysql


from datetime import datetime

# Generate alphas from alldata and operators via signal_templates.
# Output: alpha_code (s). I do not decide yet.

group = ['market', 'sector', 'industry', 'subindustry']

def get_combo_data(num, data):
    # Get combination data from operators and datas.
    # Input: num := number of {} in template. 
    # data = data available according to each region.
    try:
        rndData = []
        opes = random.sample(operators.operators(), num)
        for ope in opes:
            rndData.append(ope[0].format(*random.sample(data,ope[1])))
        return rndData
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_combo_data", str(trace_msg), str(rndData))

def get_alphas(data):
    try:
        alphas = []
        rndTemplate = random.choice(config.signal_template) 
        rndData = get_combo_data(rndTemplate[1], data) # Number of data
        rndGroup = random.choice(group)
        if rndTemplate[2] == 0:
            for rndGroupNeutralize in group:
                alphas.append(rndTemplate[0].format(*rndData, rndGroupNeutralize))
        elif rndTemplate[2] == 1:
            for rndGroupNeutralize in group:
                alphas.append(rndTemplate[0].format(*rndData, rndGroup, rndGroupNeutralize))
        return alphas
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_alphas", str(trace_msg), str(alphas))



