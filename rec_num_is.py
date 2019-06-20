import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff
import mysql.connector as mysql
from datetime import datetime

summary_url = 'https://api.worldquantvrc.com/users/self/alphas/summary'


sess = requests.session()
utils.login(sess)
num_is = []
start = 0
while True:
    f = open('record.txt','a+')
    is_sum, _, _ = stuff.get_summary(sess)
    num_is.append(is_sum)
    current_time = datetime.now()
    if len(num_is) <= 1:
        f.write(str(current_time)+ "     " + str(is_sum)+'\n')
        print("RECORDED")       
    else:
        diff = is_sum - num_is[start - 1]
        f.write(str(current_time)+ "     " + str(is_sum)+ "     " + str(diff) + '\n')
        print("RECORDED")
    start = start + 1
    time.sleep(5 * 60)
 
