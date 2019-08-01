import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff, simulator
import mysql.connector as mysql
from datetime import datetime, timedelta
import pytz

# while True:
#     sess = requests.session()
#     utils.login(sess)
#     print("\n")
#     alpha_code = str(input("ALPHA: "))
#     print("\n")
#     alpha_code = alpha_code.replace(" ","").replace("sn0","a").replace("sn1","b").replace("sn2","c").replace("alpha","d")
#     alpha_code = alpha_code.replace("d=group_neutralize(","d=").replace(",market);d",";d")
#     print(alpha_code)
#     print("\n")
#     if len(alpha_code) <= 400:
#         alpha_id = simulator.simulate_alpha(sess, alpha_code, "TOP1500", "ASI", 0, "MARKET")
#         if alpha_id != None:
#                 alpha_info = utils.get_alpha_info(alpha_id, sess)
#                 if alpha_info["sharpe"] >= 1.25 and alpha_info["fitness"] > 1.0:
#                     result, selfcorr, prodcorr = utils.check_submission(alpha_id, sess)
#                     if result == True and max(selfcorr, prodcorr) <= config.min_combo[2]: 
#                         print("Alpha ID: {}".format(alpha_info["alpha_id"]))
#                         print("Sharpe: {}".format(alpha_info["sharpe"]))
#                         print("Fitness: {}".format(alpha_info["fitness"]))
#                         print("Grade: {}".format(alpha_info["grade"]))
#                         print("Self corr: {}".format(selfcorr))
#                         print("Prod corr: {}".format(prodcorr))
#                 else:
#                     print("Not enough performance")

sess = requests.session()
utils.login(sess)

select_query = "SELECT alpha_id, alpha_code FROM websim.combo where length(alpha_code) <= 500 and flag = 1"
update_query = "UPDATE combo SET flag = -2 WHERE alpha_id = \'{}\'"
db = mysql.connect(**config.config_db)
cursor = db.cursor()
cursor.execute(select_query)
results = cursor.fetchall()
for alpha in results:
    alpha_code = alpha[1]
    alpha_id_old = alpha[0]
    alpha_code = alpha_code.replace(" ","").replace("sn0","a").replace("sn1","b").replace("sn2","c").replace("alpha","d")
    alpha_code = alpha_code.replace("d=group_neutralize(","d=").replace(",market);d",";d")
    #print(alpha_code)
    if len(alpha_code) <= 400:
        print("\nFound one!\n")
        alpha_id = simulator.simulate_alpha(sess, alpha_code, "TOP1500", "ASI", 0, "MARKET")
        if alpha_id != None:
                alpha_info = utils.get_alpha_info(alpha_id, sess)
                alpha_info["theme"] = 4
                if alpha_info["sharpe"] >= 1.25 and alpha_info["fitness"] > 1.0:
                    result, selfcorr, prodcorr = utils.check_submission(alpha_id, sess)
                    if result == True and max(selfcorr, prodcorr) <= config.min_combo[2]:
                        alpha_info["self_corr"] = selfcorr
                        alpha_info["prod_corr"] = prodcorr
                        cursor.execute(update_query.format(alpha_id_old))
                        utils.db_insert_combo(alpha_info)
                else:
                    print("Not enough performance")
