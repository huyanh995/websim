import requests
import json
from common import utils, config
from datetime import datetime
import mysql.connector as mysql

alpha_ids = ['168q6nm', 'PjRJjX7', 'lJnLJR5', 'EojZogJ', 'AKB']


sess = requests.session()
utils.login(sess)

# def check_again(sess):
#     try:
#         db = mysql.connect(**config.config_db)
#         cursor = db.cursor()
#         query_select = "SELECT alpha_id FROM signals where self_corr = 0"
#         print(query_select)
#         cursor.execute(query_select)
#         alpha_ids = cursor.fetchall()
#         for alpha_id in alpha_ids:
#             print("CHECKING Alpha ID {}:".format(alpha_id[0]))
#             selfcorr = utils.check_selfcorr(alpha_id[0], sess)
#             #prodcorr = utils.check_prodcorr(alpha_id[0], sess)
#             print("RESULT: "+str(selfcorr))
#             query_update = "UPDATE signals SET self_corr = {} WHERE alpha_id = \'{}\'".format(selfcorr, alpha_id[0])
#             print(query_update)       
#             cursor.execute(query_update)
#             db.commit()
#     except Exception as ex:
#         print(ex)


# check_again(sess)


# url = "https://api.worldquantvrc.com/users/self/alphas"

# querystring = {"limit":"30","offset":"0","stage":"IS","name~potential":"","order":"-is.fitness","hidden":"false"}

# headers = {
#     'content-type': 'application/json'
# }

# response = requests.request("GET", url, headers=headers, params=querystring)
# print(response.url)
# print(response.text)
# for i in range(0,13):
#     offset = i*100
#     response = sess.get('https://api.worldquantvrc.com/users/self/alphas?limit=100&offset={}&stage=IS&name~potential&order=-is.fitness&hidden=false'.format(offset))
#     res_json = json.loads(response.content)
#     for j in range(0,100):
#         alpha_id = res_json["results"][j]["id"]
#         result, selfcorr, prodcorr, _ = utils.check_submission(alpha_id, sess)
#         print("RESULTS: "+ str(result) + str(selfcorr) + str(prodcorr))
#         if result == True:
#             alpha_info = utils.get_alpha_info(alpha_id, sess)
#             alpha_info['self_corr'] = float(selfcorr)
#             alpha_info['prod_corr'] = float(prodcorr)
#             utils.db_insert_combo(alpha_info)
#             utils.change_name(alpha_id, sess, "can_submit")
#         else:
#             utils.change_name(alpha_id, sess, "checkagain")

db = mysql.connect(**config.config_db)
cursor = db.cursor()
select_query = 'SELECT alpha_id FROM combo where self_corr = 0'
cursor.execute(select_query)
records = cursor.fetchall()
print(records)
for alpha_id in records:
    _, selfcorr, prodcorr, times = utils.check_submission(alpha_id[0], sess)
    print("RESULTS: " + str(selfcorr) + ": " + str(prodcorr))
    update_query = "UPDATE combo SET self_corr = {}, prod_corr = {} WHERE alpha_id = \'{}\'".format(selfcorr, prodcorr, alpha_id[0])
    if selfcorr < 0 or prodcorr < 0:
        print("TRIED TIMES: "+str(times))
    cursor.execute(update_query)
    db.commit()


