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


# Checking status including number of alphas, payout, and announcements.

sess = requests.session()
utils.login(sess)
websim_time = datetime.now(pytz.timezone('EST5EDT'))
day_ws_time = str(websim_time).split(" ")[0]
yesterday, this_month, total = stuff.get_payout(sess)
num_days = int(day_ws_time.split("-")[-1])
if num_days > 1:
    if yesterday != 0:
        average = round(this_month / num_days,2)
    else:
        average = round(this_month / (num_days-1), 2)
else:
    average = yesterday
is_sum, os_sum, prod_sum = stuff.get_summary(sess)
num_today = stuff.num_alpha_submitted(day_ws_time, sess)
messages = stuff.get_ann(sess)
num_signal, num_combo, diff_signal, diff_combo = stuff.get_db_stat(day_ws_time)

print("\nTODAY STATUS")
print("\nWorldQuant Time: " + str(websim_time).split(".")[0])

print("\nPAYOUT       $"+str(yesterday))
print("----------------------------------")
print("Average      " + "$"+str(average))
print("This month   " + "$"+str(this_month))
print("Total        " + "$"+str(total))


print("\nALPHAS       {}/5".format(num_today))
print("----------------------------------")
print("Combo        " + str(num_combo) + " (+{})".format(diff_combo))
print("Signal       " + str(num_signal)+ " (+{})".format(diff_signal))
print("IS           " + str(is_sum))
print("OS           " + str(os_sum))


print("\nANNOUNCEMENTS")
print("----------------------------------")
for mess in messages:
    print(str(mess["dateCreated"]).split("T")[0] + "   " + mess["title"])
print("\n")