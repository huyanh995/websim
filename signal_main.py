import requests
import json
import time
import threading
import _thread
import logging
import traceback

import mysql.connector as mysql
from datetime import datetime


from common import config, signal_generator, simulator, utils
from data import alldata


# 1. Simulate signals: (4 threadings)
# signal_generator() -> (alphas) -> simulate() -> (alpha_id) -> get_alpha_info()
# -> (alpha_info) -> check conditions -> db_insert_signals()

tops = ["100", "150", "200", "400", "500", "600", "800", "1000", "1200", "1500", "2000", "3000"]
print("\nSIGNAL GENERATOR\n")
print("Choose region and universe first.\n")
input_region = str(input("Region (1: USA 2: EUR 3: ASI): "))
assert(input_region in ["1","2","3"]), "Wrong input!"
if input_region == "1":
    region = "USA"
    input_top = str(input('TOP (200, 500, 1000, 2000, 3000): '))
    top = "TOP" + str(input_top)
    assert(input_top in tops), "Wrong input!"
elif input_region == "2":
    region = "EUR"
    input_top = input('TOP (100, 400, 600, 800, 1200): ')
    top = "TOP" + str(input_top)
    assert(input_top in tops), "Wrong input!"
else:
    region = "ASI"
    input_top = input('TOP (150, 500, 1000, 1500): ')
    top = "TOP" + str(input_top)
    assert(input_top in tops), "Wrong input!"
input_theme = str(input("Do you want to apply current theme (Y/N): "))
answers = ["Y","y","N",'n']
assert(input_theme in answers), "Wrong input!"
if input_theme == 'Y' or input_theme == 'y':
    data = alldata.data['Theme']
    answer = 'Yes'
    theme = 1
else: 
    data = alldata.data[region]
    answer = 'No'
    theme = 0


print("\n==================================================")
print("Region: {}, Universe: {}".format(region,top))
print("Apply theme: {}".format(answer)+"\n")

def signal_simulate(thread_num):
    while True:
        try:      
            alpha_codes = signal_generator.get_alphas(data)
            alpha_ids, num1, num2, num3 = simulator.multi_simulate(sess, alpha_codes, top, region, thread_num)
            if alpha_ids != None:
                for alpha_id in alpha_ids: # Error in here (alphas_ids = None, exceed limit tried times.)
                    results = utils.get_alpha_info(alpha_id, sess)
                    if results["weight_test"] == 'FAIL':
                        print("Thread {}: Alpha {}: Not enough performance".format(thread_num, alpha_id))
                        break
                    elif results["sharpe"] >= config.min_signal[0] and results["fitness"] >= config.min_signal[1]:
                        selfcorr = float(utils.check_selfcorr(alpha_id, sess))
                        if  selfcorr <= config.min_signal[2]:
                            prodcorr = float(utils.check_prodcorr(alpha_id, sess))
                            if  prodcorr <= config.min_signal[2]:
                                results["self_corr"]=selfcorr
                                results["prod_corr"]=prodcorr
                                results["theme"] = theme
                                utils.db_insert_signals(results)
                                utils.change_name(alpha_id, sess, "signal")
                    else:
                        print("Thread {}: Alpha {}: Not enough performance".format(thread_num, alpha_id))
        except Exception as ex:
            trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
            utils.db_insert_log("signal_simulate", str(trace_msg), str(alpha_ids)+": "+str(num1)+": "+str(num2)+": "+str(num3))               


sess = requests.session()
utils.login(sess)


for i in range(config.num_signal_threads):
    _thread.start_new_thread(signal_simulate, (i + 1,))

while 1:
    pass



