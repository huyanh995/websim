import requests
import json
from common import config, utils, stuff
from datetime import datetime
import mysql.connector as mysql
from data import alldata
import traceback
import time
import math

## Transfer
def get_submitted_alpha(sess):
    offset = 0
    while True:
        collect_url = 'https://api.worldquantvrc.com/users/self/alphas?limit=100&offset={}&stage=OS%1fPROD&order=-dateSubmitted&hidden=false'.format(offset*100)
        response = sess.get(collect_url)
        res_json = json.loads(response.content)
        results = res_json["results"]
        if len(results) != 0:
            for result in results:
                alpha_id = result["id"]
                print("TRANSFER Alpha ID: {}".format(alpha_id))
                alpha_info = utils.get_alpha_info(alpha_id, sess)
                utils.db_insert_submitted(alpha_info)
                utils.change_name(alpha_id, sess, name = 'submitted')
            offset = offset + 1
        else:
            print("FINISHED!")
            break
       
## Theme check
update_query = 'UPDATE combo SET theme = {} WHERE alpha_id = \'{}\''
select_query = 'SELECT alpha_id, alpha_code, settings FROM combo WHERE self_corr > 0 and theme = 0'
select_sub_query = 'SELECT alpha_id, alpha_code, settings FROM submitted WHERE self_corr > 0'
update_sub_query = 'UPDATE submitted SET theme = {} WHERE alpha_id = \'{}\''

def theme_check(alpha_id, alpha_code, settings, data, query):
    # Checking if any combo is satisfied current multi-theme
    try:
        multiplier = 0
        if "ASI" in settings or "EUR" in settings:
            multiplier = multiplier + 2
        if any(err in alpha_code for err in data):
            if multiplier > 0:
                multiplier = multiplier + 1
            else:
                multiplier = multiplier + 2
        if multiplier > 0:
            print(str(alpha_id) + ": THEME x{}".format(multiplier))
        else:
            print(str(alpha_id) + ": NOT THEME")
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(query.format(multiplier, alpha_id))
        #cursor.execute(update_query.format(multiplier, alpha_id))
        #cursor.execute(update_sub_query.format(multiplier, alpha_id))
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("theme_check", str(trace_msg),"")

### EXECUTE ###
print("\nTOOLS")
while True:
    print("\n[1]: Import submitted alphas to MySQL DB")
    print("[2]: Update theme for existed combo/submitted alphas")
    print("[3]: Test MySQL connection")
    print("[4]: Import payout data to submitted table")
    print("[5]: Record number of generated alpha")
    print("[6]: Update signals list for combo (Developing)")
    print("\n[x]: Exit")
    mode = str(input("\nChoose mode: "))
    modes = ["1","2","3","4","5","x","X"]
    assert(mode in modes)
    print("----------------------------------")    
    sess = requests.session()
    utils.login(sess)
    if mode == "1":
        ## Transfer
        print("\nTRANSFER SUBMITTED ALPHAS TO MySQL DB\n")        
        get_submitted_alpha(sess)
        print("\nDONE")
        print("\n----------------------------------")  
    elif mode == "2":
        print("\nUPDATE THEME FOR EXISTED COMBO/SUBMITTED ALPHAS\n")  
        data_theme = alldata.data["Theme"]
        print("[1]: Combo")
        print("[2]: Submitted Alphas")
        theme_mode = str(input("\nChoose mode: "))
        theme_modes = ["1", "2"]
        assert(theme_mode in theme_modes)
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        if theme_mode == "1":
            cursor.execute(select_query)
            records = cursor.fetchall()
            db.close()
            for record in records:
                theme_check(record[0], record[1], record[2], data_theme, update_query)
        else:
            cursor.execute(select_sub_query)
            records = cursor.fetchall()
            db.close()
            for record in records:
                theme_check(record[0], record[1], record[2], data_theme, update_sub_query)
        print("\nDONE")
        print("\n----------------------------------")  
    elif mode == "3":
        print("\nTEST MySQL CONNECTION\n") 
        db = mysql.connect(**config.config_db)
        print("Connection: " + str(db.is_connected())+ "\nUser:       " + str(db._user))
        db.close()
        print("\n----------------------------------")  
    elif mode == "4":
        ## Payout
        print("\nIMPORT PAYOUT DATA TO DATABASE\n")
        stuff.get_payout_all(sess)
        print("\nDONE")
        print("\n----------------------------------")  
    elif mode == "5":
        print("\nRECORD NUMBER OF GENERATED ALPHA\n")
        num_is = []
        start = 0
        while True:
            f = open('record.txt','a+')
            is_sum, _, _ = stuff.get_summary(sess)
            num_is.append(is_sum)
            current_time = datetime.now()
            if len(num_is) <= 1:
                f.write(str(current_time)+ "     " + str(is_sum)+'\n')
                print("RECORDED")       
            else:
                diff = is_sum - num_is[start - 1]
                f.write(str(current_time)+ "     " + str(is_sum)+ "     " + str(diff) + '\n')
                print("RECORDED")
            start = start + 1
            time.sleep(5 * 60)
    else:
        break





