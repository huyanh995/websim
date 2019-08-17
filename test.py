import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff, simulator
from data import alldata
import mysql.connector as mysql
from datetime import datetime, timedelta
import pytz


sess = requests.session()
utils.login(sess)

# select_query = "SELECT alpha_code, universe, region FROM signals"
# db = mysql.connect(**config.config_db)
# cursor = db.cursor()
# cursor.execute("SELECT count(*) FROM signals")
# num_alpha = cursor.fetchall()[0][0]
# cursor.execute(select_query)
# results = cursor.fetchall()
# count = 0
# for result in results:
#     count = count + 1
#     print("ALPHA: {}/{}".format(count, num_alpha))
#     alpha_id = simulator.simulate_alpha(sess, result[0], result[1], result[2], 1)
#     if alpha_id != None:
#         print(utils.get_alpha_info(alpha_id, sess))


    



def db_update_signals(old_alpha_id, alpha_info):
    values = (
        str(alpha_info["alpha_id"]),
        str(alpha_info["create_day"]),
        str(alpha_info["alpha_code"]).replace(" ",""),
        float(alpha_info["sharpe"]),
        float(alpha_info["fitness"]),
        int(alpha_info["longCount"]),
        int(alpha_info["shortCount"]), 
        int(alpha_info["pnl"]),
        float(alpha_info["turnover"])*100,
        int(alpha_info["theme"])
    )
    update_query = "UPDATE signals SET alpha_id = \'{}\', updated_at = {}, alpha_code = \'{}\', sharpe = {}, fitness = {}, longCount = {}, shortCount = {}, pnl = {}, turnover = {}, theme = {} WHERE alpha_id = \'{}\'".format(*values, old_alpha_id)
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(update_query)
    db.commit()
    db.close()

def re_simulate_signals():
    select_query = "SELECT alpha_id, alpha_code, universe, region FROM signals"
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM signals")
    num_alpha = cursor.fetchall()[0][0]
    cursor.execute(select_query)
    results = cursor.fetchall()
    count = 0
    for result in results:
        count = count + 1
        print("ALPHA: {}/{}".format(count, num_alpha))
        alpha_id = simulator.simulate_alpha(sess, result[1], result[2], result[3], 1)
        if alpha_id != None:
            alpha_info = utils.get_alpha_info(alpha_id, sess)
            db_update_signals(result[0], alpha_info)



def remove_space_alpha(table):
    select_query = "SELECT alpha_id, alpha_code FROM {}".format(table)
    update_query = "UPDATE" + str(table) + "SET alpha_code = \'{}\' WHERE alpha_id = \'{}\'"
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()
    for record in records:
        alpha_id = record[0]
        alpha_code = record[1].replace(" ","")
        print("ALPHA_CODE: {} | {}".format(alpha_id, alpha_code))
        cursor.execute(update_query.format(alpha_code, alpha_id))
        db.commit()
    db.close()

import ast
def update_actual_use_signals():
    select_query = "SELECT alpha_id, alpha_code, settings FROM submitted"
    update_signal_query = "UPDATE signals SET actual_use = actual_use + 1 WHERE alpha_id != \'\' and alpha_code = \'{}\' and region = \'{}\' and universe = \'{}\'"
    #select_signals_query = "SELECT alpha_id FROM signals WHERE alpha_code = \'{}\'"
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()
    for alpha in records:
        alpha_code = alpha[1]
        settings = ast.literal_eval(alpha[2])
        region = settings["region"]
        universe = settings["universe"]
        signals = alpha_code.split(";")
        signals.pop(-1)
        signals.pop(-1)
        for signal in signals:
            signal_code = signal[4:]
            if signal_code[0] == "=":
                signal_code = signal_code[1:]
            print(signal_code)
            cursor.execute(update_signal_query.format(signal_code, region, universe))
            db.commit()
            # query = select_signals_query.format(signal_code)
            # print(query)
            # cursor.execute(query)
            # result = cursor.fetchall()
            # if len(result) != 0:
            #     print(result[0][0])
    db.close()

db = mysql.connect(**config.config_db)
cursor = db.cursor()
delete_query = "DELETE FROM signals WHERE alpha_code = \'{}\' and alpha_id != \'\'";
select_query = "SELECT alpha_code FROM alpha_error WHERE message = \'Grouping data used outside of group operator.\'"
cursor.execute(select_query)
records = cursor.fetchall()
for record in records:
    alpha_code = record[0].replace(" ","")
    cursor.execute(delete_query.format(alpha_code))
    db.commit()
db.close()

