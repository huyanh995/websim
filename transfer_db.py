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
cursor.execute('SELECT COUNT(*) FROM TOP3000')
total = cursor.fetchall()[0][0]
cursor.execute('SELECT alpha_code FROM TOP3000')
results = cursor.fetchall()

# db = mysql.connect(**config.config_db)
# cursor_my = db.cursor()
count = 1
for result in results:
    alpha_code = result[0].replace(" ","")
    print("Number: {}/{}".format(count, total))
    alpha_id = simulator.simulate_alpha(sess, alpha_code, "TOP3000", "USA", 0)
    alpha_info = utils.get_alpha_info(alpha_id, sess)
    if alpha_info["sharpe"] >= config.min_signal[0] and alpha_info["fitness"] >= config.min_signal[1]:
        alpha_info["self_corr"] = utils.check_selfcorr(alpha_id, sess)
        alpha_info["prod_corr"] = utils.check_prodcorr(alpha_id, sess)
        values = (
            str(alpha_info["alpha_id"]),
            str(alpha_info["create_day"]),
            str(alpha_info["alpha_code"]),
            str(alpha_info["region"]),
            str(alpha_info["universe"]),
            str(alpha_info["settings"]).replace("'","\'"),
            float(alpha_info["sharpe"]),
            float(alpha_info["fitness"]),
            float(alpha_info["self_corr"]),
            float(alpha_info["prod_corr"]),
            int(alpha_info["longCount"]),
            int(alpha_info["shortCount"]), 
            int(alpha_info["pnl"]),
            float(alpha_info["turnover"])*100,
            int(alpha_info["theme"]),
            "Null",
            0
            )
        query = "INSERT INTO signals (alpha_id, created_at, alpha_code, region, universe, settings, sharpe, fitness, self_corr, prod_corr, longCount, shortCount, pnl, turnover, theme, last_used, count_used) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, \'{}\')".format(*values) + ";\n"
        print(query)
        f = open("queries.txt", "a+")
        f.write(query)
        f.close()
    count = count + 1
conn.commit()
conn.close()
