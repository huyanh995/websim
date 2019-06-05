import requests
import json
import time
import threading
import random
import traceback

from common import config
from common import utils
from data import alldata
import mysql.connector as mysql

from datetime import datetime

# Generate alphas from alldata and operators via signal_templates.
# Output: alpha_code (s). I do not decide yet.

group = ['market', 'sector', 'industry', 'subindustry']

def get_alphas(data):
    try:
        id = random.choice([0, 2, 2, 2, 4])
        alphas = []
        chosen_ids = random.sample(range(0, len(data)), 3)
        rnd_data1 = data[chosen_ids[0]]
        rnd_data2 = data[chosen_ids[1]]
        rnd_data3 = data[chosen_ids[2]]
        rnd_group = random.choice(group)

        for rndGroupNeutralize in group:
            if id % 2 == 1:
                if id <= 1:
                    alpha = config.signal_template[id].format(rnd_data1, rnd_data2, rnd_group, rndGroupNeutralize)
                else:
                    alpha = config.signal_template[id].format(rnd_data1, rnd_data2, rnd_data3, rnd_group, rndGroupNeutralize)

            else:
                if id <= 1:
                    alpha = config.signal_template[id].format(rnd_data1, rnd_data2, rndGroupNeutralize)
                else:
                    alpha = config.signal_template[id].format(rnd_data1, rnd_data2, rnd_data3, rndGroupNeutralize)
            alphas.append(alpha)

        return alphas
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_alphas", str(trace_msg), str(alphas))



