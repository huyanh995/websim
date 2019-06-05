import requests
import json
import time
import threading
import _thread
import logging
import traceback

import mysql.connector as mysql
from datetime import datetime


from common import config, signal_generator, simulator, utils, combo_generator
from data import alldata


# 2. Simulate combos: (6 threadings)
# combo_generator() -> (alphas) -> simulate() -> (alpha_id) -> get_alpha_info()
# -> (alpha_info) -> check conditions -> db_insert_signals()
tops = ["100", "150", "200", "400", "500", "600", "800", "1000", "1200", "1500", "2000", "3000"]
print("COMBO GENERATOR\n")
print("Choose region and universe first.\n")
input_region = input("Region (1: USA 2: EUR 3: ASI): ")
assert(input_region in ["1","2","3"])
if input_region == 1:
    region = "USA"
    input_top = str(input('TOP (200, 500, 1000, 2000, 3000): '))
    top = "TOP" + str(input_top)
    assert(input_top in tops)
elif input_region == 2:
    region = "EUR"
    input_top = input('TOP (100, 400, 600, 800, 1200): ')
    top = "TOP" + str(input_top)
    assert(input_top in tops)
else:
    region = "ASI"
    input_top = input('TOP (150, 500, 1000, 1500): ')
    top = "TOP" + str(input_top)
    assert(input_top in tops)
data = alldata.data[region]
num_signals = int(input("Number of signal combination: "))
print("\n==================================================")
print("Region: {}, Universe: {}".format(region,top))
print("Number of signal combination: {}".format(num_signals)+"\n")

# Get a list contains alpha_ids from signals. Update every 20 minutes. (PENDING)
def combo_simulate(thread_num):
    try:
        list_signal = combo_generator.get_set_signals(top, region)
        # for x, y in list_signal.items():
        #     print(x, y)
        combo_alpha = combo_generator.generate_combo(list_signal, num_signals, top, region)
        # print(combo_alpha)
        alpha_id = simulator.simulate_alpha(sess, combo_alpha["alpha_code"], top, region, thread_num)
        # print("ID" + str(alpha_id))
        alpha_info = utils.get_alpha_info(alpha_id, sess)
        if alpha_info["sharpe"] >= config.min_combo[0] and alpha_info["fitness"] >= config.min_combo[1]:
            result, selfcorr, prodcorr, _ = utils.check_submission(alpha_id, sess)
            if result is True and max(selfcorr, prodcorr) <= config.min_combo[2]: 
                alpha_info["self_corr"] = selfcorr
                alpha_info["prod_corr"] = prodcorr
                utils.change_name(alpha_id, sess, "combo")
                combo_generator.update_count_used(alpha_id)
        else:
            print("Thread {}: Alpha {}: Not enough performance".format(thread_num, alpha_id))
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("combo_simulate", str(trace_msg), "")   


sess = requests.session()
utils.login(sess)


for i in range(config.num_sim[0],10):
    _thread.start_new_thread(combo_simulate, (i + 1,))

while 1:
    pass

