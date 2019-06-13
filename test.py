import requests
import json
import traceback
from common import utils, config
from datetime import datetime, timedelta
import mysql.connector as mysql
import pytz

alpha_ids = ['168q6nm', 'PjRJjX7', 'lJnLJR5', 'EojZogJ', 'AKB']

def db_update_combo(alpha_id, status):
    # This function will record all exception of below functions into database (For LOGIN only, testing for a while and delete it after)
    # It's need to create database first, following the init.sql file.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        update_query = 'UPDATE combo SET submitted = \'{}\' WHERE alpha_id = \'{}\''.format(status, alpha_id)
        print(update_query)
        cursor.execute(update_query)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": UPDATE COMBO :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

sess = requests.session()
utils.login(sess)
alpha_ids = ['kkEnGLl', 'l6p3g8x', '9PZbwM9', '1Vkapwm', '0kOeJXk']
for alpha_id in alpha_ids:
    db_update_combo(alpha_id, "SUBMITTED")

