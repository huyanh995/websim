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
#group = ['market']
def get_combo_data(num,data):
    try:
        rndData = []
        for count in range(0, num):
            num_ope = int(random.choice(config.num_max_ope))
            rndOpe = random.sample(operators.operators(), num_ope)
            if num_ope > 1:
                filled_data = "add("
                for ope in rndOpe:
                    if ope[2] == 0:
                        filled_data = filled_data + ope[0].format(*random.sample(data,ope[1])) + ", "
                    else:
                        rndGroup = random.choice(group)
                        filled_data = filled_data + ope[0].format(*random.sample(data,ope[1]), rndGroup) + ", "
                filter = random.choice(['true', 'false'])
                filled_data = filled_data + "filter = " + filter + ")"
                rndData.append(filled_data)
            else:
                if rndOpe[0][2] == 0:
                    rndData.append(rndOpe[0][0].format(*random.sample(data,rndOpe[0][1])))
                else:
                    rndGroup = random.choice(group)
                    rndData.append(rndOpe[0][0].format(*random.sample(data,rndOpe[0][1]), rndGroup))
        return rndData
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_combo_data", str(trace_msg), str(rndData)+str(rndOpe))


def get_alphas(data):
    try:
        #alphas = []
        rndTemplate = random.choice(config.signal_template) 
        rndData = get_combo_data(rndTemplate[1], data) # Number of data
        rndGroup = random.choice(group)
        if rndTemplate[2] == 0:
            # for rndGroupNeutralize in group:
            #     alphas.append(rndTemplate[0].format(*rndData, rndGroupNeutralize))
            alpha = rndTemplate[0].format(*rndData, rndGroup)
        elif rndTemplate[2] == 1:
            # for rndGroupNeutralize in group:
            #     alphas.append(rndTemplate[0].format(*rndData, rndGroup, rndGroupNeutralize))
            rndGroup_2 = random.choice(group)
            alpha = rndTemplate[0].format(*rndData, rndGroup_2, rndGroup)
        #return alphas
        return alpha
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        #utils.db_insert_log("get_alphas", str(trace_msg), str(alphas))
        utils.db_insert_log("get_alphas", str(trace_msg), str(alpha))
