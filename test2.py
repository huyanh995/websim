import requests
from common import utils, config
from datetime import datetime
import mysql.connector as mysql

alpha_ids = ['168q6nm', 'PjRJjX7', 'lJnLJR5', 'EojZogJ', 'AKB']


sess = requests.session()
utils.login(sess)

def check_again(sess):
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query_select = "SELECT alpha_id FROM combo ORDER BY fitness DESC"
        print(query_select)
        cursor.execute(query_select)
        alpha_ids = cursor.fetchall()
        for alpha_id in alpha_ids:
            print("CHECKING Alpha ID {}:".format(alpha_id[0]))
            selfcorr = utils.check_selfcorr(alpha_id[0], sess)
            print("RESULT: "+str(selfcorr))
            query_update = "UPDATE combo SET self_corr = {} WHERE alpha_id = \'{}\'".format(selfcorr, alpha_id[0])
            print(query_update)       
            cursor.execute(query_update)
            db.commit()
            if selfcorr < 0.7 and selfcorr > 0:
                utils.change_name(alpha_id[0], sess, name = "lasthope")
            else:
                utils.change_name(alpha_id[0], sess, name = "nohope")
    except Exception as ex:
        print(ex)


check_again(sess)