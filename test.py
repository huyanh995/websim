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
from concurrent.futures import ProcessPoolExecutor as Executor

start_time = time.time()
# Checking status including number of alphas, payout, and announcements.

sess = requests.session()
utils.login(sess)
websim_time = datetime.now(pytz.timezone('EST5EDT'))
day_ws_time = str(websim_time).split(" ")[0]
try:
    with Executor() as executor:
        result1 = executor.submit(stuff.get_payout, sess)
        result2 = executor.submit(stuff.get_summary, sess)
        result3 = executor.submit(stuff.num_alpha_submitted, day_ws_time, sess)
        result4 = executor.submit(stuff.get_ann, sess)
        result5 = executor.submit(stuff.get_db_stat, day_ws_time)
        result6 = executor.submit(stuff.get_failed_status, sess)
        result7 = executor.submit(stuff.get_system_info, day_ws_time)

        yesterday, this_month, total = result1.result()
        is_sum, os_sum, prod_sum = result2.result()
        num_today = result3.result()
        messages = result4.result()
        num_signal, num_combo, diff_signal, diff_combo = result5.result()
        num_failed_combo, num_failed_signal = result6.result()
        total_log_count, today_log_count, today_log_in_count = result7.result()
except Exception as ex:
    trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
    utils.db_insert_log("MULTI STAT ", str(trace_msg), "")   

num_days = int(day_ws_time.split("-")[-1])
if num_days == 1:
    average = 0
elif num_days == 2:
    average = yesterday
else:
    if yesterday == 0:
        average = round(this_month / (num_days-2),2)
    else:
        average = round(this_month / (num_days-1), 2)

print("\nTODAY STATUS")
print("\nWorldQuant Time: " + str(websim_time).split(".")[0])

print("\nPAYOUT       $"+str(yesterday))
print("----------------------------------")
print("Average      " + "$"+str(average))
print("This month   " + "$"+str(this_month))
print("Total        " + "$"+str(total))


print("\nALPHAS       {}/5".format(num_today))
print("----------------------------------")
print("Combo        " + str(num_combo).ljust(9," ") + "+{}".format(diff_combo).ljust(5," ") + str(num_failed_combo))
print("Signal       " + str(num_signal).ljust(9," ") + "+{}".format(diff_signal).ljust(5," ") + str(num_failed_signal))
print("IS           " + str(is_sum))
print("OS           " + str(os_sum-config.num_alphathon))


if today_log_count > 500 or today_log_in_count > 500:
    message = "WARNING"
    print("\nSYSTEM       {}".format(message))
    print("----------------------------------")
    print("Today log    " + str(today_log_count))
    print("Today login  " + str(today_log_in_count))
    print("Total log    " + str(total_log_count))
else:
    message = "GOOD"
    print("\nSYSTEM       {}".format(message))
    print("----------------------------------")

print("\nANNOUNCEMENTS")
print("----------------------------------")
for mess in messages:
    print(str(mess["dateCreated"]).split("T")[0] + "   " + mess["title"])
#print("\n")


if yesterday != 0 and num_today == 0:
    date_yesterday = str(datetime.now() - timedelta(hours = 24)).split(" ")[0]
    update_payout_query = "UPDATE submitted SET payout = {} WHERE submitted_at = \'{}\' AND alpha_id != \'\'"
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(update_payout_query.format(yesterday, date_yesterday))
    db.commit()
    db.close()


print("--- %s seconds ---" % (time.time() - start_time))