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
import sqlite3

sess = requests.session()
utils.login(sess)


conn = sqlite3.connect('USA.db')
cursor = conn.cursor()
cursor.execute('SELECT alpha_code FROM TOP3000')
results = cursor.fetchall()
for result in results:
    alpha_code = result[0].replace(" ","")
    alpha_id = simulator.simulate_alpha(sess, alpha_code, "TOP3000", "USA", 0)
    alpha_info = utils.get_alpha_info(alpha_id, sess)
    if alpha_info["sharpe"] >= config.min_signal[0] and alpha_info["fitness"] >= config.min_signal[1]:
        alpha_info["self_corr"] = utils.check_selfcorr(alpha_id, sess)
        alpha_info["prod_corr"] = utils.check_prodcorr(alpha_id, sess)
        print(alpha_info)
        utils.db_insert_signals(alpha_info)
conn.commit()
conn.close()
