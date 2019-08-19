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
import time
# Re-checking submission all combo from combo DB to get the precise self and prod correlation.
# Recommend using after a day. 
def db_update_signals(old_alpha_id, alpha_info):
    if alpha_info["fitness"] == None:
        alpha_info["fitness"] = -1
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
    update_query = "UPDATE signals SET alpha_id = \'{}\', updated_at = \'{}\', alpha_code = \'{}\', sharpe = {}, fitness = {}, longCount = {}, shortCount = {}, pnl = {}, turnover = {}, theme = {} WHERE alpha_id = \'{}\'".format(*values, old_alpha_id)
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(update_query)
    db.commit()
    db.close()

def re_simulate_signals():
    try:
        websim_time = datetime.now(pytz.timezone('EST5EDT'))
        day_ws_time = str(websim_time).split(" ")[0]
        num_days = int(day_ws_time.split("-")[-1])
        select_query = "SELECT alpha_id, alpha_code, universe, region FROM signals WHERE datediff(\'{}\',updated_at) > 30".format(num_days)
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute("SELECT count(*) FROM signals WHERE WHERE datediff(\'{}\',updated_at) > 30".format(num_days))
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
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("re-simulate", str(trace_msg),"")
            
print("\nRE-CHECKING ALPHAS IN COMBO DB\n")
print("Mode 1: Recheck the combo(es) after submitting.")
print("Mode 2: Recheck failed combo after checking submission.")
print("Mode 3: Recheck failed signal.")
print("Mode 4: Re-simulate signal")
mode = str(input("\nChoose mode: "))
sess = requests.session()
utils.login(sess)
if mode == "1":
    input = input("Number of qualified alphas (Default: 15): ")
    if input == "":
        stuff.re_check(sess) # Default
    elif input == "all":
        stuff.re_check_all(sess) # Check all combos
    else:
        qual_num = int(input)
        stuff.re_check(sess, qual_num)
    print("----------------------------------")
elif mode == "2":
    select_query = 'SELECT alpha_id FROM combo WHERE self_corr < 0 OR prod_corr <0'
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()
    for alpha_id in records:
        result, selfcorr, prodcorr = utils.check_submission(alpha_id[0], sess)
        if result == True:
            print("Pass : " + str(selfcorr) + " : " +str(prodcorr))
            cursor.execute(stuff.update_query.format(selfcorr, prodcorr, alpha_id[0]))
            db.commit()
        elif result == False:
            print("Fail : " + str(selfcorr) + " : " +str(prodcorr))
            cursor.execute(stuff.delete_query.format(alpha_id[0]))
            db.commit()
            utils.change_name(alpha_id[0], sess, name = 'FAILED')
    db.close()
elif mode == "3":
    # Sua lai check selfcorr truoc (query rieng) >> Check prodcorr.
    select_query = 'SELECT alpha_id, self_corr, prod_corr FROM signals WHERE self_corr < 0 OR prod_corr < 0'
    update_query = 'UPDATE signals SET self_corr = {}, prod_corr = {} WHERE alpha_id = \'{}\''
    delete_query = 'DELETE FROM signals WHERE alpha_id = \'{}\''
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()
    for alpha_id in records:
        if alpha_id[1] < 0:
            selfcorr = utils.check_selfcorr(alpha_id[0], sess)
            if selfcorr <= config.min_signal[2]: 
                print("Pass: {}".format(selfcorr))
                cursor.execute(update_query.format(selfcorr, "prod_corr", alpha_id[0])) # Kiem tra lai
                db.commit()
            else: # Greater than threshold >> Delete
                print("Fail: {}".format(selfcorr))
                cursor.execute(delete_query.format(alpha_id[0]))
                db.commit()
                utils.change_name(alpha_id[0], sess)
        if alpha_id[2] < 0:
            prodcorr = utils.check_prodcorr(alpha_id[0], sess)
            if prodcorr <= config.min_signal[2]:
                print("Pass: {}".format(prodcorr))
                cursor.execute(update_query.format("self_corr", prodcorr, alpha_id[0]))
                db.commit()
            else:
                print("Fail: {}".format(prodcorr))
                cursor.execute(delete_query.format(alpha_id[0]))
                db.commit()
                utils.change_name(alpha_id[0], sess)
    db.close()
elif mode == "4":
    re_simulate_signals()

        

