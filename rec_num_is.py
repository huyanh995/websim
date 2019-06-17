import requests
import json
import time
import threading
import traceback
import random
from common import config, utils
import mysql.connector as mysql
from datetime import datetime

summary_url = 'https://api.worldquantvrc.com/users/self/alphas/summary'
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
while True:
    f = open('record.txt','a+')
    is_sum, _, _ = get_summary(sess)
    current_time = datetime.now()
    f.write(str(current_time)+ "     " + str(is_sum)+'\n')
    print("RECORDED")
    time.sleep(5 * 60)
 
