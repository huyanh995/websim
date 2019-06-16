import requests
import json
import time
import threading
import traceback
import random
from common import config, utils
import mysql.connector as mysql

from datetime import datetime, timedelta
import pytz


# Checking status including number of alphas, payout, and announcements.

ann_url = 'https://api.worldquantvrc.com/users/self/messages?order=-dateCreated&limit=5&type=ANNOUNCEMENT'
summary_url = 'https://api.worldquantvrc.com/users/self/alphas/summary'

def get_ann(sess):
    try:
        response = sess.get(ann_url)
        messages = json.loads(response.content)["results"]
        for mess in messages:
            print(str(mess["dateCreated"]).split("T")[0] + "   " + mess["title"])
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_ann",str(trace_msg), "")

def get_summary(sess):
    try:
        response = sess.get(summary_url)
        res_summary = json.loads(response.content)
        is_sum = res_summary["is"]
        os_sum = res_summary["os"]
        prod_sum = res_summary["prod"]
        return is_sum, os_sum, prod_sum 
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("get_summary",str(trace_msg), "")

sess = requests.session()
utils.login(sess)
websim_time = datetime.now(pytz.timezone('EST5EDT'))
day_ws_time = str(websim_time).split(" ")[0]
yesterday, this_month, total = utils.get_payout(sess)
is_sum, os_sum, prod_sum = get_summary(sess)
print("\nTODAY STATUS (" + str(day_ws_time)+")")

print("\nPAYOUT")
print("----------------------------------")
print("Yesterday:   " + "$"+str(yesterday))
print("This month:  " + "$"+str(this_month))
print("Total:       " + "$"+str(total))

print("\nALPHAS")
print("----------------------------------")
print("IS:          " + str(is_sum))
print("OS:          " + str(os_sum))
print("PROD:        " + str(prod_sum))

print("\nANNOUNCEMENTS")
print("----------------------------------")
get_ann(sess)
print("\n")