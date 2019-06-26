import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff
import mysql.connector as mysql

from datetime import datetime, timedelta
import pytz

headers = {
    'content-type': 'application/json'
}
max_tried_time = 1000

def submit_alpha(alpha_id, sess):
    # Submit alpha, using alpha_id as input.
    # Return ... 
    tried_time = 1
    submit_url = 'https://api.worldquantvrc.com/alphas/{}/submit'.format(alpha_id)
    print("SUBMITTING Alpha ID: {}".format(alpha_id))
    try:
        sess.post(submit_url)
        while tried_time < max_tried_time:
            response = sess.get(submit_url) # POST lan 1, cac lan sau GET.
            if utils.ERRORS(sess, response.text, "submit_alpha"):
                time.sleep(1)
            elif 'checks' in response.text:
                if 'FAIL' in response.text:
                    return False, -1, -1, tried_time
                else:
                    res_info_submitted = json.loads(response.content)
                    checks = res_info_submitted["is"]["checks"]
                    for check in checks:
                        if 'SELF_CORRELATION' in str(check):
                            selfcorr = check["value"]
                        if 'PROD_CORRELATION' in str(check):
                            prodcorr = check["value"]
                    return True, selfcorr, prodcorr, tried_time
            time.sleep(0.5)
            tried_time = tried_time + 1
        return False, -1, -1, tried_time
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("submit",str(trace_msg), response.text)
        return False, -2, -2, tried_time

def db_move_combo(alpha_id, selfcorr, prodcorr, sess):
    # After submitting an alpha sucessfully, this function will copy alpha_info from combo table to submitted table with dateSubmitted
    # then delete the alpha from combo table.
    try:
        delete_query = 'DELETE FROM combo WHERE alpha_id = \'{}\''.format(alpha_id)
        select_theme_query = 'SELECT theme FROM combo WHERE alpha_id = \'{}\''.format(alpha_id)
        alpha_info = utils.get_alpha_info(alpha_id, sess)
        alpha_info["self_corr"] = selfcorr
        alpha_info["prod_corr"] = prodcorr
        #print(alpha_info)
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(select_theme_query)
        alpha_info["theme"] = cursor.fetchall()[0][0]
        utils.db_insert_submitted(alpha_info)
        cursor.execute(delete_query)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": MOVE COMBO :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

def db_delete_combo(alpha_id):
    # This function will record all exception of below functions into database (For LOGIN only, testing for a while and delete it after)
    # It's need to create database first, following the init.sql file.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        delete_query = 'DELETE FROM combo WHERE alpha_id = \'{}\''.format(alpha_id)
        cursor.execute(delete_query)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": DELETE COMBO :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

def auto_submit(mode, num_today, sess):
    try:
        max_num_alpha = 5
        num_alpha = num_today
        select_query = 'SELECT alpha_id FROM combo WHERE self_corr > 0 AND prod_corr > 0 ORDER BY {} DESC LIMIT {}'
        if mode == "1":
            while num_alpha < max_num_alpha:
                alpha_id = str(input("Alpha ID: "))
                result, selfcorr, prodcorr, tried_time = submit_alpha(alpha_id, sess)
                if result == True and tried_time < max_tried_time:
                    num_alpha = num_alpha + 1
                    db_move_combo(alpha_id, selfcorr, prodcorr, sess)
                    utils.change_name(alpha_id, sess, name = 'submitted')
                    print("Alpha {} submitted successfully. ({}/5)".format(alpha_id, num_alpha))
                elif result == False and tried_time < max_tried_time:
                    db_delete_combo(alpha_id)
                    print("Can not submit alpha {}.".format(alpha_id))
                elif result == False and tried_time == max_tried_time:
                    print("Time-out")
                else:
                    print("There was an exception!!!")
        elif mode == "2":
            db = mysql.connect(**config.config_db)
            cursor = db.cursor()
            cursor.execute(select_query.format(config.combo_criteria, 5))
            records = cursor.fetchall()
            db.close()
            for alpha_id in records:
                if num_alpha == 5:
                    break
                result, selfcorr, prodcorr, tried_time = submit_alpha(alpha_id[0], sess)
                if result == True and tried_time < max_tried_time:
                    num_alpha = num_alpha + 1
                    db_move_combo(alpha_id[0], selfcorr, prodcorr, sess)
                    utils.change_name(alpha_id[0], sess, name = 'submitted')
                    print("Alpha {} submitted successfully. ({}/5)".format(alpha_id[0], num_alpha))
                elif result == False and tried_time < max_tried_time:
                    db_delete_combo(alpha_id[0])
                    print("Can not submit alpha {}.".format(alpha_id[0]))
                elif result == False and tried_time == max_tried_time:
                    print("Time-out")
                else:
                    print("There was an exception!!!")
        elif mode == "3":
            print("WARNING: Pause the combo simulation!")
            # Recheck 15 alphas >> Submit 1 >> Increase index >> Loop.
            # If an alpha get stucks, cannot submit and show "Time-out" forever, the function will be stucked. But I'm too lazy for it, so well :v.
            while num_alpha < 5:
                stuff.re_check(sess,10)
                db = mysql.connect(**config.config_db)
                cursor = db.cursor()
                cursor.execute(select_query.format(config.combo_criteria, 1)) # Choose one alpha to submit
                alpha_id = cursor.fetchall()
                db.close()
                result, selfcorr, prodcorr, tried_time = submit_alpha(alpha_id[0][0], sess)
                if result == True and tried_time < max_tried_time:
                    num_alpha = num_alpha + 1
                    db_move_combo(alpha_id[0][0], selfcorr, prodcorr, sess)
                    utils.change_name(alpha_id[0][0], sess, name = 'submitted')
                    print("Alpha {} submitted successfully. ({}/5)".format(alpha_id[0][0], num_alpha))
                elif result == False and tried_time < max_tried_time:
                    db_delete_combo(alpha_id[0][0])
                    print("Can not submit alpha {}.".format(alpha_id[0][0]))
                elif result == False and tried_time == max_tried_time:
                    print("Time-out")
                else:
                    print("There was an exception!!!")
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("auto_submit",str(trace_msg), "")



#### EXECUTE ######

sess = requests.session()
utils.login(sess)

websim_time = datetime.now(pytz.timezone('EST5EDT'))
day_ws_time = str(websim_time).split(" ")[0]
num_today = stuff.num_alpha_submitted(day_ws_time, sess)

print("\nAUTO SUBMIT ALPHAS\n")
print("WorldQuant Time: " + str(websim_time).split(".")[0])
if num_today >= 5:
    print("\nYou have submitted {}/5 alphas today. Just relax :)\n".format(num_today))
else:
    print("Number of alpha submitted today: {}/5\n".format(num_today))
    print("Mode 1: Type alpha_id to submit")
    print("Mode 2: Auto submit 5 alphas (Fast Mode)")
    print("Mode 3: Auto submit 5 alphas (Slow Mode) - Recommended\n")
    mode = str(input("Choose mode: "))
    modes = ["1","2","3"]
    assert(mode in modes)
    print("=============================================")
    auto_submit(mode, num_today, sess)

print("=============================================")
answer = str(input("Do you want to run re-check process (Y/N): "))
answers = ["Y", "y", "N", "n"]
assert(answer in answers)
if answer == "Y" or answer == "y":
    input = input("Number of qualified alphas (Default: 15): ")
    if input == "":
        stuff.re_check(sess) # Default
    elif input == "all":
        stuff.re_check_all(sess) # Check all combos
    else:
        qual_num = int(input)
        stuff.re_check(sess, qual_num)
    print("==============================")
else:
    print("GOOD BYE!")

