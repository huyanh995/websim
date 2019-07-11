import requests
import json
import time
import threading
import traceback
import random
from common import config, utils
import mysql.connector as mysql

from datetime import datetime

# This file contains some functions to make additional features. 

ann_url = 'https://api.worldquantvrc.com/users/self/messages?order=-dateCreated&limit=5&type=ANNOUNCEMENT'
summary_url = 'https://api.worldquantvrc.com/users/self/alphas/summary'

def get_payout(sess):
    try:
        while True:
            response = sess.get('https://api.worldquantvrc.com/users/self/activities/base-payment')
            payout_res = json.loads(response.content)
            if "yesterday" in response.text:
                yesterday = payout_res["yesterday"]["value"]
                this_month = payout_res["current"]["value"]
                total = payout_res["total"]["value"]
                return yesterday, this_month, total
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        if response.text:
            utils.db_insert_log("get_payout", str(trace_msg), response.text)
        else:
            utils.db_insert_log("get_payout", str(trace_msg), "")

def get_ann(sess):
    try:
        response = sess.get(ann_url)
        messages = json.loads(response.content)["results"]
        return messages
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_ann",str(trace_msg), "")

def get_summary(sess):
    try:
        while True:
            response = sess.get(summary_url)
            if "is" in response.text:
                res_summary = json.loads(response.content)
                is_sum = res_summary["is"]
                os_sum = res_summary["os"]
                prod_sum = res_summary["prod"]
                return is_sum, os_sum, prod_sum 
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_summary",str(trace_msg), "")

def num_alpha_submitted(day, sess):
    try:
        os_url = 'https://api.worldquantvrc.com/users/self/alphas?limit=15&offset=0&stage=OS%1fPROD&order=-dateSubmitted&hidden=false'
        response = sess.get(os_url)
        res_os = json.loads(response.content)["results"]
        num_alpha_submitted = 0
        for alpha in res_os:
            if day in alpha["dateSubmitted"]:
                num_alpha_submitted = num_alpha_submitted + 1
        return num_alpha_submitted
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("num_alpha_submitted",str(trace_msg), response.text)


update_query = 'UPDATE combo SET self_corr = {}, prod_corr = {} WHERE alpha_id = \'{}\''
select_query = 'SELECT alpha_id FROM combo WHERE self_corr > 0 and prod_corr < 0.7 ORDER BY {} DESC'.format(config.combo_criteria)
delete_query = 'DELETE FROM combo WHERE alpha_id = \'{}\''
count_query = 'SELECT count(*) FROM combo WHERE self_corr > 0 and prod_corr < 0.7'
update_combo_query = 'UPDATE combo SET flag = -1 WHERE alpha_id = \'{}\''
def re_check(sess, num = 15):
    start = 0
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(select_query)
        records = cursor.fetchall()
        for alpha_id in records:
            if start == num:
                break
            result, selfcorr, prodcorr = utils.check_submission(alpha_id[0], sess)
            if result == True and selfcorr > 0:
                print("RESULT: Pass : " + str(selfcorr) + " : " +str(prodcorr))
                cursor.execute(update_query.format(selfcorr, prodcorr, alpha_id[0]))
                db.commit()
                start = start + 1
                print("Number of qualified alpha: {}/{}".format(start, num))
            elif result == False:
                print("RESULT: Fail : " + str(selfcorr) + " : " +str(prodcorr))
                cursor.execute(update_combo_query.format(alpha_id[0]))
                db.commit()
                utils.change_name(alpha_id[0], sess, name = 'FAILED')
            else:
                print("Timed-out or Exception")
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("re_check",str(trace_msg), "")

def re_check_all(sess):
    start = 0
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(count_query)
        num = cursor.fetchall()[0][0]
        cursor.execute(select_query)
        records = cursor.fetchall()
        for alpha_id in records:
            if start == num:
                break
            result, selfcorr, prodcorr = utils.check_submission(alpha_id[0], sess)
            if result == True and selfcorr > 0:
                print("RESULT: Pass : " + str(selfcorr) + " : " +str(prodcorr))
                cursor.execute(update_query.format(selfcorr, prodcorr, alpha_id[0]))
                db.commit()
            elif result == False:
                print("RESULT: Fail : " + str(selfcorr) + " : " +str(prodcorr))
                #print(delete_query.format(alpha_id[0]))
                cursor.execute(update_combo_query.format(alpha_id[0]))
                db.commit()
                utils.change_name(alpha_id[0], sess, name = 'FAILED')
            else:
                print("Timed-out or Exception")
            start = start + 1
            print("Number of checked alpha: {}/{}".format(start, num))
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("re_check_all",str(trace_msg), "")

def get_db_stat(day_ws_time):
    try:
        num_signal_query = 'SELECT COUNT(*) FROM signals WHERE self_corr > 0 OR prod_corr > 0'
        num_combo_query = 'SELECT COUNT(*) FROM combo WHERE self_corr > 0 OR prod_corr > 0'
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(num_signal_query)
        num_signal = cursor.fetchall()[0][0]
        cursor.execute(num_combo_query)
        num_combo = cursor.fetchall()[0][0]
        diff_signal_query = 'SELECT COUNT(*) FROM signals WHERE created_at = \'{}\''.format(day_ws_time)
        cursor.execute(diff_signal_query)
        diff_signal = cursor.fetchall()[0][0]
        diff_combo_query = 'SELECT COUNT(*) FROM combo WHERE created_at = \'{}\''.format(day_ws_time)
        cursor.execute(diff_combo_query)
        diff_combo = cursor.fetchall()[0][0]
        db.close()
        return num_signal, num_combo, diff_signal, diff_combo
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("STAT: ", str(trace_msg), "")
    
def get_payout_all(sess):
    try:
        update_payout_query = "UPDATE submitted SET payout = {} WHERE submitted_at = \'{}\' AND alpha_id != \'\'"
        response = sess.get('https://api.worldquantvrc.com/users/self/activities/base-payment')
        payout_res = json.loads(response.content)
        records = payout_res["records"]["records"]
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        for record in records:
            print("UPDATE: DAY: {} - PAYOUT: {}".format(record[0], record[1]))
            cursor.execute(update_payout_query.format(record[1], record[0]))
            db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        if response.text:
            utils.db_insert_log("get_payout", str(trace_msg), response.text)
        else:
            utils.db_insert_log("get_payout", str(trace_msg), "")

def get_failed_status(sess):
    try:
        select_failed_combo_query = "SELECT COUNT(*) FROM combo WHERE self_corr < 0 or prod_corr < 0 and flag > 0"
        select_failed_signal_query = "SELECT COUNT(*) FROM signals WHERE self_corr < 0 or prod_corr < 0"
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(select_failed_combo_query)
        num_failed_combo = cursor.fetchall()[0][0]
        cursor.execute(select_failed_signal_query)
        num_failed_signal = cursor.fetchall()[0][0]
        db.close()
        return num_failed_combo, num_failed_signal
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("FAILED ALPHAS: ", str(trace_msg), "")

def get_system_info(day):
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM log")
        total_log_count = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(*) FROM log WHERE logged_time LIKE \'%{}%\'".format(day))
        today_log_count = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(*) FROM login_log WHERE logged_time LIKE \'%{}%\'".format(day))
        today_login_count = cursor.fetchall()[0][0]
        return total_log_count, today_log_count, today_login_count
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("SYS STAT: ", str(trace_msg), "")
