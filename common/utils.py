import requests
import json
import time
import threading
import traceback
import random
from common import config
import mysql.connector as mysql

from datetime import datetime

login_url = "https://api.worldquantvrc.com/authentication"
sim_url = "https://api.worldquantvrc.com/simulations"
myalpha_url = "https://api.worldquantvrc.com/users/self/alphas"
alpha_url = "https://api.worldquantvrc.com/alphas/"
headers = {
    'content-type': 'application/json'
}
################## ERROR Function

def ERRORS(sess, response):
    # List all exceptions from responsed json string from server.
    # Input: Session, Response.text (from requests module)
    # Thank Ho Duc Nhan for this part.
    # 'b\'\''
    # 'b\'{}\''
    ServerErrors = ['Time-out', 'Gateway', 'Server Error', '<html>'
                    'An invalid response was received from the upstream server',
                    'The upstream server is timing out', 'Not found']
    # if any(err in str(response) for err in ServerErrors):
    #     db_insert_log("ERRORS: SERVER", "", str(response))
    #     return True

    # This following for loop is for testing only. After that, you should use the above code for faster executing time.
    for err in ServerErrors:
        if err in response:
            db_insert_log("ERRORS: SERVER",str(err), str(response))
            return True
    if 'Incorrect authentication credentials' in str(response): # You know its meaning :)
        db_insert_login("LOGIN", "", response)
        login(sess)
        return True
    elif 'API rate limit exceeded' in str(response): # Exceed maximum times for checking corrs per day.
        db_insert_log("API","",response)
        time.sleep(5 * 60)
        return True
    elif 'THROTTLED' in str(response): # Exceed concurrent check submission.
        db_insert_log("API SUBMISSION","",response)
        time.sleep(random.randint(60,180))
        return True
    elif 'maintenance downtime' in str(response): # Websim is became stupid and need fix.
        db_insert_log("MAINTAIN","",response)
        time.sleep(1800)
        return True
    return False
#SIMULATION_LIMIT_EXCEEDED
################## Database related Function

def db_insert_log(func_name, exception, response):
    # This function will record all exception of below functions into database
    # It's need to create database first, following the init.sql file.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO log (logged_time, func_name, exception, response) VALUES (%s, %s, %s, %s)"
        values = (str(datetime.now()), func_name, exception, response)
        cursor.execute(query, values)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": LOG    :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

def db_insert_login(func_name, exception, response):
    # This function will record all exception of below functions into database (For LOGIN only, testing for a while and delete it after)
    # It's need to create database first, following the init.sql file.
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO login_log (logged_time, func_name, exception, response) VALUES (%s, %s, %s, %s)"
        values = (str(datetime.now()), func_name, exception, response)
        cursor.execute(query, values)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": LOG    :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()


def db_insert_signals(alpha_info):
    # Insert signals data into signals tables.
    # alpha_info is a dictionary type get from get_alpha_info()
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO signals (alpha_id, created_at, alpha_code, region, universe, settings, sharpe, fitness, self_corr, prod_corr, longCount, shortCount, pnl, turnover, theme, last_used, count_used) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            str(alpha_info["alpha_id"]),
            str(alpha_info["create_day"]),
            str(alpha_info["alpha_code"]),
            str(alpha_info["region"]),
            str(alpha_info["universe"]),
            str(alpha_info["settings"]),
            float(alpha_info["sharpe"]),
            float(alpha_info["fitness"]),
            float(alpha_info["self_corr"]),
            float(alpha_info["prod_corr"]),
            int(alpha_info["longCount"]),
            int(alpha_info["shortCount"]), 
            int(alpha_info["pnl"]),
            float(alpha_info["turnover"])*100,
            int(alpha_info["theme"]),
            None,
            0
            )
        cursor.execute(query, values)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": SIGNAL :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()


def db_insert_combo(alpha_info):
    # Insert alpha informations into combo tables.
    # Using alpha_info dictionary get from get_my_info()
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO combo (alpha_id, created_at, alpha_code, settings, sharpe, fitness, grade, self_corr, prod_corr, longCount, shortCount, pnl, returns_, turnover, margin, drawdown, theme) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            str(alpha_info["alpha_id"]),
            str(alpha_info["create_day"]),
            str(alpha_info["alpha_code"]),
            str(alpha_info["settings"]),
            float(alpha_info["sharpe"]),
            float(alpha_info["fitness"]),
            str(alpha_info["grade"]),
            float(alpha_info["self_corr"]),
            float(alpha_info["prod_corr"]),
            int(alpha_info["longCount"]),
            int(alpha_info["shortCount"]), 
            int(alpha_info["pnl"]),
            float(alpha_info["returns"]*100),
            float(alpha_info["turnover"])*100,
            alpha_info["margin"]*10000,
            alpha_info["drawdown"],
            int(alpha_info["theme"])
            )
        cursor.execute(query, values)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": COMBO  :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

def db_insert_submitted(alpha_info):
    # Insert alpha informations into combo tables.
    # Using alpha_info dictionary get from get_my_info()
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO submitted (alpha_id, created_at, submitted_at, alpha_code, settings, sharpe, fitness, grade, self_corr, prod_corr, longCount, shortCount, pnl, returns_, turnover, margin, drawdown, theme) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            str(alpha_info["alpha_id"]),
            str(alpha_info["create_day"]),
            str(alpha_info["submit_day"]),
            str(alpha_info["alpha_code"]),
            str(alpha_info["settings"]),
            float(alpha_info["sharpe"]),
            float(alpha_info["fitness"]),
            str(alpha_info["grade"]),
            float(alpha_info["self_corr"]),
            float(alpha_info["prod_corr"]),
            int(alpha_info["longCount"]),
            int(alpha_info["shortCount"]), 
            int(alpha_info["pnl"]),
            float(alpha_info["returns"]*100),
            float(alpha_info["turnover"])*100,
            alpha_info["margin"]*10000,
            alpha_info["drawdown"],
            int(alpha_info["theme"])
            )
        cursor.execute(query, values)
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+":SUBMITTED:  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

def db_insert_count(func_name, no1=-1, no2=-1, no3=-1):
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO count_use (func_name, no1, no2, no3) VALUES (%s, %s, %s, %s)"
        values = (func_name, no1, no2, no3)
        cursor.execute(query, values)
        db.commit()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": TEST   :  "+str(trace_msg)+"\n"
        db_exception.write(log_mess)
        db_exception.close()
################## LOGIN Function

def login(sess):
    # Login function: A session expires after 4 hours, function returns responsed json content and status
    # Add exception from Nhan in the future (Added)
    response = sess.post(login_url, auth=(
        config.username, config.password), headers=headers)
    db_insert_login("LOGIN", "STATUS: "+str(response.status_code), response.text)

################## CHECK TESTS Function

def check_prodcorr(alpha_id, sess):
    # Check prod corr function, input: alpha_id, output: prod corr.
    # Call api continuously until reached max tried time (pre-defined) or get result.
    #max_tried_times = 150
    max_tried_times = 1000 # For checking max valuable.
    tried_times = 1
    # print("Check product correlation alpha id: "+str(alpha_id)) # For testing only
    while tried_times < max_tried_times:
        try:
            check_prodcorr_url = "https://api.worldquantvrc.com/alphas/" + \
                str(alpha_id) + "/correlations/prod"
            response = sess.get(check_prodcorr_url, data="", headers=headers)
            if ERRORS(sess, response.text):
                time.sleep(1)
            elif "prodCorrelation" in response.text:
                print("Tried times: "+str(tried_times))
                prod_corr_res_obj = json.loads(response.content)["records"]
                for x in range(1, len(prod_corr_res_obj)-1):
                    if prod_corr_res_obj[len(prod_corr_res_obj)-x][2] != 0:
                        prod_corr = prod_corr_res_obj[len(
                            prod_corr_res_obj)-x][1]
                        db_insert_count("check_prod", tried_times, -1, -1)
                        return prod_corr
            time.sleep(0.5) # Delayed time between requests.
            tried_times = tried_times + 1
        # except ConnectionError:
        #     print('CONNECTION LOST!')
        #     time.sleep(20)
        except Exception as ex:
            trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
            db_insert_log("check_prodcorr",str(trace_msg), response.text)
            return -2
    # If reaching max tried time and still can not calculate prod corr, return -1
    # it means this alpha id failed to check prod corr
    return -1


def check_selfcorr(alpha_id, sess):
    # Same functionality as prod corr check.
    #max_tried_time = 150
    max_tried_time = 1000 # For debugging only
    tried_times = 1
    print("Check self correlation alpha id: "+str(alpha_id))
    while tried_times < max_tried_time:
        try:
            check_selfcorr_url = "https://api.worldquantvrc.com/alphas/" + \
                alpha_id + "/correlations/self"
            response = sess.get(check_selfcorr_url, data="", headers=headers)
            if ERRORS(sess, response.text):
                time.sleep(1)
            elif "selfCorrelation" in response.text:
                print("Tried times: "+str(tried_times))
                self_corr = json.loads(response.content)["records"][0][5]
                db_insert_count("check_prod", tried_times, -1, -1)
                return self_corr
            time.sleep(0.5)
            tried_times = tried_times + 1
        # except ConnectionError:
        #     print('CONNECTION LOST!')
        except Exception as ex:
            trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
            db_insert_log("check_selfcorr",str(trace_msg), response.text)
            return -2
    return -1


def check_submission(alpha_id, sess):
    # Check submission of an alpha:
    # Criteria: There're about 8 (+1 UNIT TEST) tests. The first five tests (excluding Self/Prod Corr and IS Sharpe Ladder)
    # are tested. If any of them is failed (STATUS: FAIL), then the last three tests are cancelled (STATUS: PENDING)
    # This function return three values, the first is boolean value (TRUE: Passed tests, FAIL: failed tests)
    # second and third value are self and prod correlation, respectively.
    # If an alpha passed all the tests > Return True, self, prod
    # If an alpha failed one of the tests > Return False, -1, -1 (Self/Prod Corr are in range of 0 to 1)
    # If after 15 times, the test is not completed or have any exception > Return True, -1, -1. This values mean
    # the alpha is considered re-run the test in the future.
    #max_tried_times = 150
    max_tried_times = 1000
    tried_times = 1
    print("Check submission tests alpha id: "+str(alpha_id))
    while tried_times < max_tried_times:
        try:
            check_submision_url = "https://api.worldquantvrc.com/alphas/" + \
                str(alpha_id) + "/check"
            response = sess.get(check_submision_url, data="", headers=headers)
            # print(response.text)
            if 'FAIL' in response.text:
                # print("FAIL") # For testing only
                return False, -1, -1, tried_times
            elif 'PENDING' in response.text:
                time.sleep(3)
            elif ERRORS(sess, response.text):
                time.sleep(1)
            elif 'checks' in response.text:
                list_test = json.loads(response.content)["is"]["checks"]
                for check in list_test:
                    if check['name'] == 'SELF_CORRELATION':
                        self_corr = check['value']
                    if check['name'] == 'PROD_CORRELATION':
                        prod_corr = check['value']
                db_insert_count("check_submit", tried_times, -1, -1)
                return True, self_corr, prod_corr, tried_times
            tried_times = tried_times + 1
        # except ConnectionError:
        #     time.sleep(20)
        except Exception as ex:
            trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
            db_insert_log("check_submission",str(trace_msg), "Response: " + str(response.text) + "Alpha_ID: " +str(alpha_id))
            return True, -2, -2, tried_times
    return True, -1, -1, tried_times


################## ALPHA related Function

def get_myalpha(sess, region, top="", min_sharpe=0.7, min_fitness=0.7, offset=0):
    # For checking alpha in my alpha page.
    # Return response content in json format.
    querystring = {"limit": "100", "offset": offset*100, "stage": "IS", "is.sharpe>": min_sharpe,
                   "hidden": "false", "is.fitness>": min_fitness, "order": "-is.fitness", "settings.language": "FASTEXPR", "settings.region": region, "settings.universe": top}
    response = sess.get(myalpha_url, data="",
                        headers=headers, params=querystring)
    return json.loads(response.content)["results"]
    # For further use, get alpha id in ["id"] of each alpha in results

def get_alpha_info(alpha_id, sess):
    # Get the alpha infomation including performance and some test results.
    # Using it with simulate to complete the step
    # Note that the simulate function only return alpha ID, which have to use this fuction
    # to receive important information
    # Another purpose is to filter alphas for signals, alphas which satisfied sharpe and fitness
    # greater or equal than a determined value and passed the weight test is considered to be signal
    max_tried_time = 1000
    tried_time = 1
    try:
        while tried_time < max_tried_time:
            alpha_url_info = alpha_url + str(alpha_id)
            response = sess.get(alpha_url_info, data="", headers=headers)
            alpha_res_json = json.loads(response.content)
            if ERRORS(sess, response.text):
                time.sleep(1)
            elif alpha_id in str(alpha_res_json):
                alpha_info = {}
                alpha_info["alpha_id"] = alpha_res_json["id"]
                alpha_info["create_day"] = str(
                    alpha_res_json["dateCreated"].split("T")[0]) #YYYY-MM-DD format
                if alpha_res_json["dateSubmitted"] != None:
                    alpha_info["submit_day"] = str(
                        alpha_res_json["dateSubmitted"].split("T")[0])
                else:
                    alpha_info["submit_day"] = ""
                alpha_info["alpha_code"] = alpha_res_json["code"]
                alpha_info["settings"] = alpha_res_json["settings"]
                alpha_info["region"]= alpha_info["settings"]["region"]
                alpha_info["universe"] = alpha_info["settings"]["universe"]
                alpha_info["sharpe"] = alpha_res_json["is"]["sharpe"]
                alpha_info["fitness"] = alpha_res_json["is"]["fitness"]
                alpha_info["grade"] = alpha_res_json["grade"]
                for test in alpha_res_json["is"]["checks"]:
                    if len(alpha_res_json["is"]["details"]["records"]) < 12:
                        alpha_info["weight_test"] = "FAIL"
                        break
                    elif test["name"] == "CONCENTRATED_WEIGHT":
                        #print(test["result"])
                        alpha_info["weight_test"] = test["result"]
                        break
                alpha_info["self_corr"] = 0
                alpha_info["prod_corr"] = 0
                alpha_info["longCount"] = alpha_res_json["is"]["longCount"]
                alpha_info["shortCount"] = alpha_res_json["is"]["shortCount"]
                alpha_info["pnl"] = alpha_res_json["is"]["pnl"]
                alpha_info["returns"] = alpha_res_json["is"]["returns"]
                alpha_info["turnover"] = alpha_res_json["is"]["turnover"]
                alpha_info["theme"] = 0
                alpha_info["margin"] = alpha_res_json["is"]["margin"]
                alpha_info["drawdown"] = alpha_res_json["is"]["drawdown"]
                alpha_info["status"] = alpha_res_json["status"]
                return alpha_info
            else:
                tried_time = tried_time + 1
    # except ConnectionError:
    #     print('CONNECTION LOST!')
    #     return None
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_insert_log("get_alpha_info",str(trace_msg), response.text)
        return None



# Need to check again, exception at b' ' << Check later. THROTTLED << Check its meaning.

################## Change ALPHA PROPERTIES related Function

def hide_alpha(alpha_id, sess):
    # Hide alphas those are not qualified tested or not good enough to use
    # Using alpha id as determined value
    try:
        url = alpha_url + str(alpha_id)
        payload = "{ \"hidden\":true}"
        response = sess.patch(url, data=payload, headers=headers)
        # print(response.text) # For testing only
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_insert_log("hide_alpha",str(trace_msg), response.text)


def change_name(alpha_id, sess, name="anonymous"):
    # Change name of an alpha. If name = None, websim automatically change it to anonymous
    meta_url = alpha_url + str(alpha_id)
    data = {"color": None, "name": name, "tags": [],
            "category": None, "description": None}
    try:
        response = sess.patch(meta_url, data=json.dumps(data), headers=headers)
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        if response.text:
            db_insert_log("change_name",str(trace_msg), response.text)
        else:
            db_insert_log("change_name", str(trace_msg), str(alpha_id)+str(json.dumps(data)))


def get_payout(sess):
    try:
        response = sess.get('https://api.worldquantvrc.com/users/self/activities/base-payment')
        payout_res = json.loads(response.content)
        yesterday = payout_res["yesterday"]["value"]
        this_month = payout_res["current"]["value"]
        total = payout_res["total"]["value"]
        return yesterday, this_month, total
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        if response.text:
            db_insert_log("get_payout", str(trace_msg), response.text)
        else:
            db_insert_log("get_payout", str(trace_msg), "")

