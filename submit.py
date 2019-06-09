import requests
import json
import time
import threading
import traceback
import random
from common import config, utils
import mysql.connector as mysql

from datetime import datetime

# Submit file. It is not the necessary part of the project. But I wrote it when my code is not ready to use (in beta test)

headers = {
    'content-type': 'application/json'
}

def submit_alpha(alpha_id, sess):
    # Submit alpha, using alpha_id as input.
    # Return ...
    max_tried_time = 1000
    tried_time = 1
    submit_url = 'https://api.worldquantvrc.com/alphas/{}/submit'.format(alpha_id)
    print(submit_url)
    try:
        while tried_time < max_tried_time:
            response = requests.request("POST", submit_url, headers=headers)
            print("RESPONSE: " + str(response))
            if utils.ERRORS(sess, response.text):
                time.sleep(1)
            elif 'checks' in response.text:
                if 'FAIL' in response.text:
                    print("SUBMIT FAIL")
                else:
                    print("SUBMIT SUCCESS")
            tried_time = tried_time + 1
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("submit",str(trace_msg), response.text)

sess = requests.session()
utils.login(sess)
#submit_alpha('jNpqjYQ', sess)

# WARNING: Haven't tested yet.

