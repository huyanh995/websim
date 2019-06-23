import requests
import json
import traceback
from common import utils, config, stuff
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

# response = sess.get('https://api.worldquantvrc.com/users/self/alphas?limit=30&offset=0&stage=IS&name~potential&order=-is.fitness&hidden=false')
# info_res_json = json.loads(response.content)
# results = info_res_json["results"]
# for result in results:
#     if result["grade"] == 'SPECTACULAR' or result["grade"] == 'EXCELLENT':
#         alpha_id = result["id"]
#         alpha_info = utils.get_alpha_info(alpha_id, sess)
#         test, selfcorr, prodcorr, _ = utils.check_submission(alpha_id, sess)
#         print(str(test)+" : "+str(selfcorr)+" : "+str(prodcorr))
#         if test == True:
#             alpha_info["self_corr"] = selfcorr
#             alpha_info["prod_corr"] = prodcorr
#             utils.db_insert_combo(alpha_info)
#             utils.change_name(alpha_id, sess, name = "can_submit")
#         else:
#             utils.change_name(alpha_id, sess, name = "failed")
#     else:
#         utils.change_name(alpha_id, sess, name = "anonymous")


# print(url)
# response = sess.get(url)
# print(response.content)

print(utils.get_alpha_info("XwXeOgz", sess))