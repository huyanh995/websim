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
        query_select = "SELECT alpha_id FROM signals where self_corr = 0"
        print(query_select)
        cursor.execute(query_select)
        alpha_ids = cursor.fetchall()
        for alpha_id in alpha_ids:
            print("CHECKING Alpha ID {}:".format(alpha_id[0]))
            selfcorr = utils.check_selfcorr(alpha_id[0], sess)
            #prodcorr = utils.check_prodcorr(alpha_id[0], sess)
            print("RESULT: "+str(selfcorr))
            query_update = "UPDATE signals SET self_corr = {} WHERE alpha_id = \'{}\'".format(selfcorr, alpha_id[0])
            print(query_update)       
            cursor.execute(query_update)
            db.commit()
    except Exception as ex:
        print(ex)


check_again(sess)