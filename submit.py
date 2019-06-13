import requests
import json
import time
import threading
import traceback
import random
from common import config, utils
from recheck import re_check
import mysql.connector as mysql

from datetime import datetime, timedelta
import pytz

# Submit file. It is not the necessary part of the project. But I wrote it when my code is not ready to use (in beta test)

headers = {
    'content-type': 'application/json'
}
max_tried_time = 1000

def submit_alpha(alpha_id, sess):
    # Submit alpha, using alpha_id as input.
    # Return ... 
    tried_time = 1
    submit_url = 'https://api.worldquantvrc.com/alphas/{}/submit'.format(alpha_id)
    print(submit_url)
    print("SUBMITTING Alpha ID: {}".format(alpha_id))
    try:
        initial = sess.post(submit_url)
        print("INITIAL: " + str(initial.text))
        while tried_time < max_tried_time:
            response = sess.get(submit_url) # POST lan 1, cac lan sau GET.
            print("RESPONSE {}: ".format(tried_time) + str(response.text))
            if utils.ERRORS(sess, response.text):
                time.sleep(1)
            elif 'checks' in response.text:
                if 'FAIL' in response.text:
                    return False, tried_time
                else:
                    return True, tried_time
            time.sleep(0.5)
            tried_time = tried_time + 1
        return False, tried_time
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("submit",str(trace_msg), response.text)
        return False, -1

def db_update_combo(alpha_id, status):
    # This function will record all exception of below functions into database (For LOGIN only, testing for a while and delete it after)
    # It's need to create database first, following the init.sql file.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        update_query = 'UPDATE combo SET submitted = \'{}\' WHERE alpha_id = \'{}\''.format(status, alpha_id)
        print(update_query)
        cursor.execute(update_query)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": UPDATE COMBO :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

def db_delete_combo(alpha_id):
    # This function will record all exception of below functions into database (For LOGIN only, testing for a while and delete it after)
    # It's need to create database first, following the init.sql file.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        delete_query = 'delete from combo where alpha_id = \'{}\''.format(alpha_id)
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
    max_num_alpha = 5
    num_alpha = num_today
    select_query = 'select alpha_id from combo where self_corr > 0 and prod_corr > 0 and submitted = \'UNSUBMITTED\' order by fitness/(self_corr * exp(2*prod_corr)) desc'
    if mode == "1":
        while num_alpha < max_num_alpha:
            alpha_id = str(input("Alpha ID: "))
            result, tried_time = submit_alpha(alpha_id, sess)
            if result == True and tried_time < max_tried_time:
                num_alpha = num_alpha + 1
                db_update_combo(alpha_id, status = 'SUBMITTED')
                utils.change_name(alpha_id, sess, name = 'submitted')
                print("Alpha {} submitted successfully. ({}/5)".format(alpha_id, num_alpha))
            elif result == False and tried_time < max_tried_time:
                db_delete_combo(alpha_id)
                print("Can not submit alpha {}.".format(alpha_id))
            elif result == False and tried_time == max_tried_time:
                db_update_combo(alpha_id, status = "PENDING")
                print("Time-out")
            else:
                print("There was an exception!!!")
    elif mode == "2":
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(select_query)
        records = cursor.fetchall()
        db.close()
        for alpha_id in records:
            if num_alpha == 5:
                break
            result, tried_time = submit_alpha(alpha_id[0], sess)
            if result == True and tried_time < max_tried_time:
                num_alpha = num_alpha + 1
                db_update_combo(alpha_id[0], status = 'SUBMITTED')
                utils.change_name(alpha_id[0], sess, name = 'submitted')
                print("Alpha {} submitted successfully. ({}/5)".format(alpha_id[0], num_alpha))
            elif result == False and tried_time < max_tried_time:
                db_delete_combo(alpha_id[0])
                print("Can not submit alpha {}.".format(alpha_id[0]))
            elif result == False and tried_time == max_tried_time:
                db_update_combo(alpha_id[0], status = "PENDING")
                print("Time-out")
            else:
                print("There was an exception!!!")
                

def num_alpha_submitted(day, sess):
    os_url = 'https://api.worldquantvrc.com/users/self/alphas?limit=15&offset=0&stage=OS%1fPROD&order=-dateSubmitted&hidden=false'
    response = sess.get(os_url)
    res_os = json.loads(response.content)["results"]
    num_alpha_submitted = 0
    for alpha in res_os:
        if day in alpha["dateSubmitted"]:
            num_alpha_submitted = num_alpha_submitted + 1
    return num_alpha_submitted




sess = requests.session()
utils.login(sess)

websim_time = datetime.now(pytz.timezone('EST5EDT'))
day_ws_time = str(websim_time).split(" ")[0]
num_today = num_alpha_submitted(day_ws_time, sess)

print("\nAUTO SUBMIT ALPHAS\n")
print("WQ Time: " + str(websim_time))
print("Number of alpha submitted today: {}/5\n".format(num_today))
print("Mode 1: Type alpha_id to submit")
print("Mode 2: Auto submit 5 alphas\n")
mode = str(input("Choose mode: "))
modes = ["1","2"]
assert(mode in modes)
print("=============================================")
auto_submit(mode, num_today, sess)

print("=============================================")
answer = str(input("Do you want to run re-check process (Y/N): "))
answers = ["Y", "y", "N", "n"]
assert(answer in answers)
if answer == "Y" or answer == "y":
    re_check(sess)
else:
    print("GOOD BYE!")
