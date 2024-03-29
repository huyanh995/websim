import requests
import json
import time
import threading
import logging
from common import config, utils
import mysql.connector as mysql
import random
import traceback

from datetime import datetime
# Generate combos from signals stored in Database.
# Read count value in Vu's codes.


def update_count_used(alpha_id):
    # Update count value for each signal in alpha_ids.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        last_used = str(datetime.now()).split(" ")[0]
        query = "UPDATE signals SET count_used = count_used + 1, last_used = \'{}\' WHERE alpha_id = \'{}\'".format(last_used, alpha_id) 
        cursor.execute(query)
        db.commit()
        db.close() 
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("update_count_used", str(trace_msg), str(query))

def get_set_signals(top, region):
    # Return a dictionary contains alpha_id and alpha_code of signals.
    # For prepare combination step.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "SELECT alpha_id, alpha_code FROM signals WHERE count_used <= {} AND universe = \'{}\'".format(config.max_signal_count, top)
        cursor.execute(query)
        records = cursor.fetchall()
        diction = dict((x,y) for x,y in records) 
        db.close()
        return diction
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_set_signals", str(trace_msg), str(query))

def generate_combo(signals, num_signal, top, region):
    try:
        rnd_signals = random.sample(signals.items(), num_signal) # Get a list contains alpha_id and alpha_code of (num_signal) signal.
        combo_signal= ""
        combo = {"alpha_code":"", "region":region, "top":top} # Get a dictionary contains alpha_code, region and top.
        index = 0
        list_alpha_ids = [] # Get list of signal's alpha_id to increase count if combo is qualified.
        combo_code = ""
        for signal in rnd_signals:
            combo_signal = combo_signal + "sn" + str(index) + "=" + signal[1] + "; "
            combo_code = combo_code + "sn" + str(index) + ", "
            list_alpha_ids.append(signal[0])
            index = index + 1
        rndCombo = random.choice(config.combo_template).format(combo_signal, combo_code)
        combo["alpha_code"]=rndCombo
        return combo, list_alpha_ids
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("generate_combo", str(trace_msg), combo_code)


