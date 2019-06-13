import requests
import json
import time
import threading
import traceback
import random
from common import config, utils
import mysql.connector as mysql

from datetime import datetime

# Re-checking submission all combo from combo DB to get the precise self and prod correlation.
# Recommend using after a day. 

update_query = 'UPDATE combo SET self_corr = {}, prod_corr = {} WHERE alpha_id = \'{}\''
select_query = 'SELECT alpha_id FROM combo WHERE self_corr > 0 and prod_corr < 0.7 and submitted = \'UNSUBMITTED\' ORDER BY fitness/(self_corr * exp(2*prod_corr)) DESC'
delete_query = 'DELETE FROM combo WHERE alpha_id = \'{}\''
def re_check(sess, num = 15):
    start = 0
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()
    for alpha_id in records:
        if start == num:
            break
        result, selfcorr, prodcorr, _ = utils.check_submission(alpha_id[0], sess)
        if result == True and selfcorr > 0:
            print(str(selfcorr)+": "+str(prodcorr))
            print(update_query.format(selfcorr, prodcorr, alpha_id[0]))
            cursor.execute(update_query.format(selfcorr, prodcorr, alpha_id[0]))
            db.commit()
            start = start + 1
        elif result == False:
            print(str(selfcorr)+": "+str(prodcorr))
            print(delete_query.format(alpha_id[0]))
            cursor.execute(delete_query.format(alpha_id[0]))
            db.commit()
            utils.change_name(alpha_id[0], sess, name = 'FAILED')
        else:
            print("Timed-out or Exception")
    db.close()


print("\nRE-CHECKING ALPHAS IN COMBO DB\n")
qual_num = int(input("Number of qualified alphas (Default: 15): "))
print("==============================")
sess = requests.session()
utils.login(sess)
re_check(sess, qual_num)
