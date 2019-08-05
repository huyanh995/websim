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


# 2. Simulate combos: 
# combo_generator() -> (alphas) -> simulate() -> (alpha_id) -> get_alpha_info()
# -> (alpha_info) -> check conditions -> db_insert_signals()
tops = ["100", "150", "200", "400", "500", "600", "800", "1000", "1200", "1500", "2000", "3000"]
print("\nCOMBO GENERATOR\n")
print("Choose region and universe first.\n")
input_region = str(input("Region (1: USA 2: EUR 3: ASI): "))
assert(input_region in ["1","2","3"])
if input_region == "1":
    region = "USA"
    input_top = str(input('TOP (200, 500, 1000, 2000, 3000): '))
    top = "TOP" + str(input_top)
    assert(input_top in tops)
elif input_region == "2":
    region = "EUR"
    input_top = input('TOP (100, 400, 600, 800, 1200): ')
    top = "TOP" + str(input_top)
    assert(input_top in tops)
else:
    region = "ASI"
    input_top = input('TOP (150, 500, 1000, 1500): ')
    top = "TOP" + str(input_top)
    assert(input_top in tops)

num_signals = int(input("Number of signal combination: "))

# input_theme = str(input("Do you want to apply current theme (Y/N): "))
# answers = ["Y","y","N",'n']
# assert(input_theme in answers), "Wrong input!"
# if input_theme == 'Y' or input_theme == 'y':
#     theme = 1
#     answer = 'Yes'
# else: 
#     theme = 0
#     answer = 'No'
print("\n----------------------------------")
print("Region: {}, Universe: {}".format(region,top))
print("Number of signal combination: {}".format(num_signals))
# print("Apply theme: {}".format(answer)+"\n")
# Get a list contains alpha_ids from signals. Update every 20 minutes. (PENDING)
data_theme = alldata.data["Theme"]
def combo_simulate(thread_num):
    while True:
        try:
            list_signal = combo_generator.get_set_signals(top, region)
            combo_alpha, list_alpha_ids = combo_generator.generate_combo(list_signal, num_signals, top, region)
            combo_alpha["alpha_code"] = combo_alpha["alpha_code"].replace(" ","").replace("sn0","a").replace("sn1","b").replace("sn2","c").replace("alpha","d")
            combo_alpha["alpha_code"] = combo_alpha["alpha_code"].replace("d=group_neutralize(","d=").replace(",market);d",";d")
            alpha_id = simulator.simulate_alpha(sess, combo_alpha["alpha_code"], top, region, thread_num)
            utils.change_name(alpha_id, sess, name="potential")
            if alpha_id != None:
                alpha_info = utils.get_alpha_info(alpha_id, sess)
                if alpha_info["sharpe"] >= config.min_combo[0] and alpha_info["fitness"] >= config.min_combo[1]:
                    result, selfcorr, prodcorr = utils.check_submission(alpha_id, sess)
                    #print(result)
                    if result == True and max(selfcorr, prodcorr) <= config.min_combo[2]: 
                        alpha_info["self_corr"] = selfcorr
                        alpha_info["prod_corr"] = prodcorr
                        alpha_info["theme"] = utils.set_theme(alpha_info["alpha_code"], alpha_info["region"], data_theme)
                        utils.change_name(alpha_id, sess, "can_submit")
                        utils.db_insert_combo(alpha_info)
                        for signal_id in list_alpha_ids:
                            combo_generator.update_count_used(signal_id)
                else:
                    print("Thread {}: Alpha {}: Not enough performance".format(thread_num, alpha_id))
            else:
                print("Time-out")
            
        except Exception as ex:
            trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
            utils.db_insert_log("combo_simulate", str(trace_msg), str(combo_alpha["alpha_code"]))   


sess = requests.session()
utils.login(sess)

for i in range(config.num_combo_threads):
    _thread.start_new_thread(combo_simulate, (i + 1,))

while 1:
    pass

# combo_simulate(1)


