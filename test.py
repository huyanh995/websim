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

select_query = "SELECT alpha_code, universe, region FROM signals"
db = mysql.connect(**config.config_db)
cursor = db.cursor()
cursor.execute("SELECT count(*) FROM signals")
num_alpha = cursor.fetchall()[0]
cursor.execute(select_query)
results = cursor.fetchall()
count = 0
for result in results:
    count = count + 1
    print("{}/{}".format(count, num_alpha))
    alpha_id = simulator.simulate_alpha(sess, result[0], result[1], result[2], 1)
    if alpha_id != None:
        print(utils.get_alpha_info(alpha_id, sess))


    