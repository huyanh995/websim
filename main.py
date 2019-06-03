import requests
import json
import time
import threading
import _thread
import mysql.connector as mysql
from datetime import datetime


from common import config, signal_generator, simulator, utils
from data import alldata


# Main part to run the whole project. It can be separated into two parts.


# 1. Simulate signals: (4 threadings)
# signal_generator() -> (alphas) -> simulate() -> (alpha_id) -> get_alpha_info()
# -> (alpha_info) -> check conditions -> db_insert_signals()



# 2. Simulate combos: (6 threadings)
# combo_generator() -> (alphas) -> simulate() -> (alpha_id) -> get_alpha_info()
# -> (alpha_info) -> check conditions -> db_insert_signals()
# tops = ["100", "150", "200", "400", "500", "600", "800", "1000", "1200", "1500", "2000", "3000"]
# print("Choose region and universe first.\n")
# input_region = input("Region (1: USA 2: EUR 3: ASI): ")
# assert(input_region in ["1","2","3"])
# if input_region == 1:
#     region = "USA"
#     input_top = str(input('TOP (200, 500, 1000, 2000, 3000): '))
#     top = "TOP" + str(input_top)
#     assert(input_top in tops)
# elif input_region == 2:
#     region = "EUR"
#     input_top = input('TOP (100, 400, 600, 800, 1200): ')
#     top = "TOP" + str(input_top)
#     assert(input_top in tops)
# else:
#     region = "ASI"
#     input_top = input('TOP (150, 500, 1000, 1500): ')
#     top = "TOP" + str(input_top)
#     assert(input_top in tops)
# print("\n==================================================")
# print("Region: {}, Universe: {}".format(region,top)+"\n")
# # Constant
# max_threads = 4

# data = alldata.data[region]
sess = requests.session()
utils.login(sess)


# def signal_simulate(thread_num): # Xem lai thread_num nhu the nao, cach van hanh.
#     try:
#         while True:
#             alpha_codes = signal_generator.get_alphas(data)
#             for alpha in alpha_codes:
#                 alpha_id = simulator.simulate_alpha(sess, alpha, top, region, thread_num)
#                 results = utils.get_alpha_info(alpha_id, sess)
#                 if results["sharpe"] >= config.min_signal[0] and results["fitness"] >= config.min_signal[1]:
#                     selfcorr = utils.check_selfcorr(alpha_id, sess)
#                     if  selfcorr <= config.min_signal[2]:
#                         prodcorr = utils.check_prodcorr(alpha_id, sess)
#                         if  prodcorr <= config.min_signal[2]:
#                             utils.db_insert_signals(results, selfcorr, prodcorr)
#                 else:
#                     print("Thread {}: Not enough performance".format(thread_num))
#     except Exception as ex:
#         utils.db_insert_log("signal_simulate", str(ex), "")

def signal_simulate(thread_num):
    try:
        while True:
            alpha_codes = signal_generator.get_alphas(alldata.data["ASI"])
            alpha_ids = simulator.multi_simulate(sess, alpha_codes, "TOP1000", "ASI", thread_num)
            for alpha_id in alpha_ids:
                results = utils.get_alpha_info(alpha_id, sess)
                if results["sharpe"] >= config.min_signal[0] and results["fitness"] >= config.min_signal[1]:
                    selfcorr = utils.check_selfcorr(alpha_id, sess)
                    if  selfcorr <= config.min_signal[2]:
                        prodcorr = utils.check_prodcorr(alpha_id, sess)
                        if  prodcorr <= config.min_signal[2]:
                            utils.db_insert_signals(results, selfcorr, prodcorr)
                else:
                    print("Thread {}: Not enough performance".format(thread_num))
    except Exception as ex:
        utils.db_insert_log("signal_simulate", str(ex), "")               

for i in range(config.num_sim[0]):
    _thread.start_new_thread(signal_simulate, (i + 1,))

while 1:
    pass

