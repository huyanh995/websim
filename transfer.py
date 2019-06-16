import requests
import json
from common import utils, config
from datetime import datetime
import mysql.connector as mysql


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

sess = requests.session()
utils.login(sess)
print("\nTRANSFER SUBMITTED ALPHAS TO MySQL DB\n")
print("==========================================")            
get_submitted_alpha(sess)
        
