import requests
import json
import time
import threading
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

def ERRORS(s, response):
    # List all exceptions from responsed json string from server.
    # Thank Ho Duc Nhan for this part.
    ServerErrors = ['Time-out', 'Gateway', 'b\'\'', 'b\'{}\'', 'Server Error',
                    'An invalid response was received from the upstream server', 'THROTTLED',
                    'The upstream server is timing out', 'Not found']
    if any(s in str(response) for s in ServerErrors):
        return True
    elif 'Incorrect authentication credentials' in str(response):
        print('LOG IN!!!')
        login(login_url, s)
        return True
    elif 'API rate limit exceeded' in str(response):
        print('API rate limit exceeded!!')
        time.sleep(5 * 60)
        return True
    elif 'maintenance downtime' in str(response):
        print("MAINTENANCE DOWNTIME!")
        time.sleep(1800)
        return True
    return False

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
    except Exception as ex:
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": LOG    :  "+str(ex)+"\n"
        db_exception.write(log_mess)
        db_exception.close()


def db_insert_signals(alpha_info, self_corr =0, prod_corr =0):
    # Insert signals data into signals tables.
    # alpha_info is a dictionary type get from get_alpha_info()
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO signals (alpha_id, created_at, alpha_code, settings, sharpe, fitness, self_corr, prod_corr, longCount, shortCount, pnl, turnover, count_used) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            str(alpha_info["alpha_id"]),
            str(alpha_info["create_day"]),
            str(alpha_info["alpha_code"]),
            str(alpha_info["settings"]),
            float(alpha_info["sharpe"]),
            float(alpha_info["fitness"]),
            self_corr,
            prod_corr,
            int(alpha_info["longCount"]),
            int(alpha_info["shortCount"]), 
            int(alpha_info["pnl"]),
            float(alpha_info["turnover"])*100,
            1
            )
        cursor.execute(query, values)
        db.commit()
    except Exception as ex:
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": SIGNAL :  "+str(ex)+"\n"
        db_exception.write(log_mess)
        db_exception.close()


def db_insert_combo(alpha_info, self_corr =0, prod_corr =0):
    # Insert alpha informations into combo tables.
    # Using alpha_info dictionary get from get_my_info()
    try:
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        query = "INSERT INTO combo (alpha_id, created_at, alpha_code, settings, sharpe, fitness, grade, self_corr, prod_corr, longCount, shortCount, pnl, returns_, turnover, margin, drawdown, submitted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            str(alpha_info["alpha_id"]),
            str(alpha_info["create_day"]),
            str(alpha_info["alpha_code"]),
            str(alpha_info["settings"]),
            float(alpha_info["sharpe"]),
            float(alpha_info["fitness"]),
            str(alpha_info["grade"]),
            self_corr,
            prod_corr,
            int(alpha_info["longCount"]),
            int(alpha_info["shortCount"]), 
            int(alpha_info["pnl"]),
            float(alpha_info["returns"]*100),
            float(alpha_info["turnover"])*100,
            alpha_info["margin"]*10000,
            alpha_info["drawdown"],
            str(alpha_info["status"])
            )
        cursor.execute(query, values)
        db.commit()
    except Exception as ex:
        db_exception = open("db_exception.txt", "a+")
        log_mess = str(datetime.now())+": COMBO  :  "+str(ex)+"\n"
        db_exception.write(log_mess)
        db_exception.close()

################## LOGIN Function

def login(url, sess):
    # Login function: A session expires after 4 hours, function returns responsed json content and status
    # Add exception from Nhan in the future (Added)
    response = sess.post(url, auth=(
        config.username, config.password), headers=headers)
    db_insert_log("LOGIN", "STATUS: "+str(response.status_code), response.text)

################## CHECK TESTS Function

def check_prodcorr(alpha_id, sess):
    # Check prod corr function, input: alpha_id, output: prod corr.
    # Call api continuously until reached max tried time (pre-defined) or get result.
    max_tried_times = 100
    tried_times = 1
    # print("Check product correlation alpha id: "+str(alpha_id)) # For testing only
    while tried_times < max_tried_times:
        try:
            check_prodcorr_url = "https://api.worldquantvrc.com/alphas/" + \
                str(alpha_id) + "/correlations/prod"
            response = sess.get(check_prodcorr_url, data="", headers=headers)
            if ERRORS(sess, response.content):
                time.sleep(5)
            elif "prodCorrelation" in response.text:
                print("Tried times: "+str(tried_times))
                prod_corr_res_obj = json.loads(response.content)["records"]
                for x in range(1, len(prod_corr_res_obj)-1):
                    if prod_corr_res_obj[len(prod_corr_res_obj)-x][2] != 0:
                        prod_corr = prod_corr_res_obj[len(
                            prod_corr_res_obj)-x][1]
                        return prod_corr
            time.sleep(0.5)
            tried_times = tried_times + 1
        except ConnectionError:
            print('CONNECTION LOST!')
            time.sleep(20)
        except:
            print('EXCEPTION {}'.format(response.content))
            return -1
    # If reaching max tried time and still can not calculate prod corr, return -1
    # it means this alpha id failed to check prod corr
    return -1


def check_selfcorr(alpha_id, sess):
    # Same functionality as prod corr check.
    max_tried_time = 100
    tried_times = 1
    print("Check self correlation alpha id: "+str(alpha_id))
    while tried_times < max_tried_time:
        try:
            check_selfcorr_url = "https://api.worldquantvrc.com/alphas/" + \
                alpha_id + "/correlations/self"
            response = sess.get(check_selfcorr_url, data="", headers=headers)
            if ERRORS(sess, response.content):
                time.sleep(5)
            elif "selfCorrelation" in response.text:
                print("Tried times: "+str(tried_times))
                self_corr = json.loads(response.content)["records"][0][5]
                return self_corr
            time.sleep(0.2)
            tried_times = tried_times + 1
        except ConnectionError:
            print('CONNECTION LOST!')
        except:
            print('EXCEPTION {}'.format(response.content))
            return -1
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
    max_tried_times = 15
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
            elif 'PENDING' in response.text or ERRORS(sess, response.content):
                time.sleep(3)
            else:
                list_test = json.loads(response.content)["is"]["checks"]
                for check in list_test:
                    if check['name'] == 'SELF_CORRELATION':
                        self_corr = check['value']
                    if check['name'] == 'PROD_CORRELATION':
                        prod_corr = check['value']
                return True, self_corr, prod_corr, tried_times
            tried_times = tried_times + 1
        except ConnectionError:
            time.sleep(20)
        except:
            f = open("log.txt", "a+")
            f.write('EXCEPTION: {}' .format(response.content))
            f.close()
            return True, -1, -1, tried_times
    return True, -1, -1, tried_times

################## SIMULATE and SUBMIT Function

def simulate_alpha(sess, alpha_code, top, region):  # Need to check again.
    # Simulate alpha (mostly use for signals). Input alpha, universe and region.
    # For signals simulation, alphas have fitness > 0.7, sharpe > 0.7 and corr < determined values are called signals.
    max_tried_times = 10
    # First step: POST request to get Job ID, if there're 10 simulteneously thread, wait 3 seconds and re-send.
    tried_sim_time = 1  # For 1st step
    # Second step: After get Job ID, GET request to get Alpha ID
    tried_res_time = 1  # For 2nd step
    while tried_sim_time < max_tried_times:
        payload = {"type": "SIMULATE", "settings": {"nanHandling": "OFF", "instrumentType": "EQUITY", "delay": 1, "universe": top, "truncation": 0.08, "unitHandling": "VERIFY",
                                                    "pasteurization": "ON", "region": region, "language": "FASTEXPR", "decay": 0, "neutralization": "NONE", "visualization": False}, "code": alpha_code}
        # POST request to server to get Job ID (It's different ID, to get Alpha ID in futher)
        job_response = sess.post(
            sim_url, data=json.dumps(payload), headers=headers)
        print(job_response.text)
        # Get JSON string from server
        if 'SIMULATION_LIMIT_EXCEED' in job_response.text:
            print(str(tried_sim_time))
            time.sleep(3)
        if job_response.status_code == 201:
            job_id = job_response.headers["Location"].split("/")[-1]
            print("DONE... :"+str(job_id))
            while tried_res_time < 5*max_tried_times:
                sim_alpha_url = sim_url + "/" + str(job_id)
                alpha_res_json = sess.get(
                    sim_alpha_url, data="", headers=headers)
                print(alpha_res_json.text)
                if ("COMPLETE" in alpha_res_json.text) or ("WARNING" in alpha_res_json.text):
                    alpha_id = json.loads(alpha_res_json.content)["alpha"]
                    return alpha_id
                time.sleep(0.5)
                tried_res_time = tried_res_time + 1
        time.sleep(0.5)
        tried_sim_time = tried_sim_time + 1
    return None


def submit(alpha_id, sess):
    max_tried_times = 15
    tried_times = 1
    print("Submit alpha id: "+str(alpha_id))
    if check_submission(alpha_id, sess) is True:
        if check_selfcorr(alpha_id, sess) <= 0.7:
            if check_prodcorr(alpha_id, sess) <= 0.7:
                while tried_times < max_tried_times:
                    submit_url = "https://api.worldquantvrc.com/alphas/"+alpha_id+"/submit"
                    response = sess.post(submit_url, headers=headers)
                    if len(response.text) != 0:  # Dumb condition, only for testing
                        submit_log = open("submit_log.txt", "a+")
                        submit_log.write(
                            str(alpha_id) + "===" + str(response.text) + "\n")
                        submit_log.close()
                        break
                print("Recorded into log file")
            else:
                print("FAIL: Prod Corr")
        else:
            print("FAIL: Self Corr")
    else:
        print("FAIL: Submission Test")

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
    alpha_url_info = alpha_url + str(alpha_id)
    response = sess.get(alpha_url_info, data="", headers=headers)
    alpha_res_json = json.loads(response.content)
    try:
        if ERRORS(sess, response.content):
            time.sleep(3)
        else:
            alpha_info = {}
            alpha_info["alpha_id"] = alpha_res_json["id"]
            alpha_info["create_day"] = str(
                alpha_res_json["dateCreated"].split("T")[0]) #YYYY-MM-DD format
            alpha_info["alpha_code"] = alpha_res_json["code"]
            alpha_info["settings"] = alpha_res_json["settings"]
            alpha_info["sharpe"] = alpha_res_json["is"]["sharpe"]
            alpha_info["fitness"] = alpha_res_json["is"]["fitness"]
            alpha_info["grade"] = alpha_res_json["grade"]
            for test in alpha_res_json["is"]["checks"]:
                if test["name"] == "CONCENTRATED_WEIGHT":
                    print(test["result"])
                    alpha_info["weight_test"] = test["result"]
                    break
                elif len(alpha_res_json["is"]["details"]["records"]) < 12:
                    alpha_info["weight_test"] = "FAIL"
                    break
            alpha_info["self_corr"] = 0
            alpha_info["prod_corr"] = 0
            alpha_info["longCount"] = alpha_res_json["is"]["longCount"]
            alpha_info["shortCount"] = alpha_res_json["is"]["shortCount"]
            alpha_info["pnl"] = alpha_res_json["is"]["pnl"]
            alpha_info["returns"] = alpha_res_json["is"]["returns"]
            alpha_info["turnover"] = alpha_res_json["is"]["turnover"]
            alpha_info["margin"] = alpha_res_json["is"]["margin"]
            alpha_info["drawdown"] = alpha_res_json["is"]["drawdown"]
            alpha_info["status"] = alpha_res_json["status"]
            return alpha_info
    except ConnectionError:
        print('CONNECTION LOST!')
    except Exception as ex:
        print('EXCEPTION {}'.format(ex))
        for x in alpha_info:
            alpha_info[x] = ""
        return alpha_info



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
    except ConnectionError:
        time.sleep(5)
    except:
        print("THERE IS AN EXCEPTION HERE, HELPPP!")


def change_name(alpha_id, sess, name="anonymous"):
    # Change name of an alpha. If name = None, websim automatically change it to anonymous
    meta_url = alpha_url + str(alpha_id)
    data = {"color": None, "name": name, "tags": [],
            "category": None, "description": None}
    try:
        sess.patch(meta_url, data=json.dumps(data), headers=headers).content
    except ConnectionError:
        time.sleep(5)
    except:
        print("EXCEPTION HERE")



################## TESTING AREA - DELETE AFTER
sess = requests.session()
login(login_url, sess)

for x, y in get_alpha_info("EoQbldG",sess).items():
    print(str(x)+" : "+str(y))
db_insert_combo(get_alpha_info("EoQbldG",sess))
# for x in range(101):
#     for y in get_myalpha(sess, region = "EUR", min_sharpe=1.25, min_fitness=2, offset=x):
#         alpha_id = y["id"]
#         can_submit, self_corr, prod_corr, tried_times = check_submission(alpha_id,sess)
#         print(str(can_submit)+" : "+str(self_corr)+" : "+str(prod_corr)+" : "+str(tried_times))
#         time.sleep(20)
#         if can_submit == True:
#             if self_corr < 0.7 and prod_corr < 0.7:
#                  change_name(alpha_id, sess, name = "flag")

