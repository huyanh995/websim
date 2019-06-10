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
        query_select = "SELECT alpha_id FROM signals where self_corr = -1 and prod_corr = -1"
        print(query_select)
        cursor.execute(query_select)
        alpha_ids = cursor.fetchall()
        for alpha_id in alpha_ids:
            print("CHECKING Alpha ID {}:".format(alpha_id[0]))
            selfcorr = utils.check_selfcorr(alpha_id[0], sess)
            prodcorr = utils.check_prodcorr(alpha_id[0], sess)
            print("RESULT: "+str(selfcorr)+" :"+str(prodcorr))
            query_update = "UPDATE signals SET self_corr = {} and prod_corr = {} WHERE alpha_id = \'{}\'".format(selfcorr, prodcorr, alpha_id[0])
            print(query_update)       
            cursor.execute(query_update)
            db.commit()
            db.close()
    except Exception as ex:
        print(ex)


check_again(sess)