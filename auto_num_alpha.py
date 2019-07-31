import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff
import mysql.connector as mysql

import datetime
import pytz

websim_time = datetime.datetime.now(pytz.timezone('EST5EDT'))
day_ws_time = str(websim_time).split(" ")[0]
sess = requests.session()
utils.login(sess)
is_sum, os_sum, prod_sum = stuff.get_summary(sess)

db = mysql.connect(**config.config_db)
cursor = db.cursor()

insert_query = "INSERT INTO num_alpha (log_at, is_num) VALUES (%s, %s)"
values = (day_ws_time, is_sum)

cursor.execute(insert_query, values)
db.commit()
db.close()
