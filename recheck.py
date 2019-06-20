import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff
import mysql.connector as mysql

from datetime import datetime

# Re-checking submission all combo from combo DB to get the precise self and prod correlation.
# Recommend using after a day. 

print("\nRE-CHECKING ALPHAS IN COMBO DB\n")
print("Mode 1: Recheck the combo(es) after submitting.")
print("Mode 2: Recheck failed combo after checking submission.")

mode = str(input("\nChoose mode: "))
sess = requests.session()
utils.login(sess)
if mode == "1":
    input = input("Number of qualified alphas (Default: 15): ")
    if input == "":
        stuff.re_check(sess) # Default
    elif input == "all":
        stuff.re_check_all(sess) # Check all combos
    else:
        qual_num = int(input)
        stuff.re_check(sess, qual_num)
    print("==============================")
elif mode == "2":
    select_query = 'SELECT alpha_id FROM combo WHERE self_corr < 0 OR prod_corr <0;'
    db = mysql.connect(**config.config_db)
    cursor = db.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()
    for alpha_id in records:
        result, selfcorr, prodcorr, _ = utils.check_submission(alpha_id[0], sess)
        if result == True:
            print("RESULT: Pass : " + str(selfcorr) + " : " +str(prodcorr))
            cursor.execute(stuff.update_query.format(selfcorr, prodcorr, alpha_id[0]))
            db.commit()
        elif result == False:
            print("RESULT: Fail : " + str(selfcorr) + " : " +str(prodcorr))
            cursor.execute(stuff.delete_query.format(alpha_id[0]))
            db.commit()
            utils.change_name(alpha_id[0], sess, name = 'FAILED')


