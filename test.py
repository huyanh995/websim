import requests
import json
import traceback
from common import utils, config
from datetime import datetime, timedelta
import mysql.connector as mysql
import pytz



# def db_update_submitted():
#     # This function will record all exception of below functions into database (For LOGIN only, testing for a while and delete it after)
#     # It's need to create database first, following the init.sql file.
#     try:
#         select_query = 'SELECT alpha_id, self_corr, prod_corr FROM combo WHERE submitted = \'SUBMITTED\''
#         db = mysql.connect(**config.config_db)
#         cursor = db.cursor()
#         cursor.execute(select_query)
#         records = cursor.fetchall()
#         for record in records:
#             update_query = 'UPDATE submitted SET self_corr = \'{}\', prod_corr = \'{}\' WHERE alpha_id = \'{}\''.format(record[1], record[2], record[0])
#             print(update_query)
#             cursor.execute(update_query)
#             db.commit()
#     except Exception as ex:
#         trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
#         print(trace_msg)

sess = requests.session()
utils.login(sess)

# db_update_submitted()

