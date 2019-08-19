import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff, simulator
from data import alldata, operators
import mysql.connector as mysql
from datetime import datetime, timedelta
import pytz


sess = requests.session()
utils.login(sess)

# db = mysql.connect(**config.config_db)
# cursor = db.cursor()
# delete_query = "DELETE FROM signals WHERE alpha_code = \'{}\' and alpha_id != \'\'"
# select_query = "SELECT alpha_code FROM alpha_error WHERE message = \'Grouping data used outside of group operator.\'"
# cursor.execute(select_query)
# records = cursor.fetchall()
# for record in records:
#     alpha_code = record[0].replace(" ","")
#     cursor.execute(delete_query.format(alpha_code))
#     db.commit()
# db.close()

print(len(alldata.data["ASI"]))
print(len(operators.operators()))

