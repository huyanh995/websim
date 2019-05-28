#from . import config
import requests
import json
import time
import threading
from common import config

# max_retried_times = 10

# headers = {
#     'user-agent': 'Mozilla/5.0'
# }

# login_data = {
#     'EmailAddress': "huyanhkstntt@gmail.com",
#     'Password': "Dangquang1995",    
#     'next': '',
#     'g-recaptcha-response': ''
# }



login_url = "https://api.worldquantvrc.com/authentication"
sim_url = "https://api.worldquantvrc.com/simulations"
myalpha_url = "https://api.worldquantvrc.com/users/self/alphas"
alpha_url = "https://api.worldquantvrc.com/alphas/"

#sim_url = "https://www.worldquantvrc.com/simulate"
#login_url = "https://www.worldquantvrc.com/login/process"
# def login(sess):
#     r = sess.post(login_url, data=login_data, headers=headers)
#     print(r.content)


# def simulate_for_submission(sess, alpha_code, region, top):
#     tried_times = 1

#     print('simulating \'' + alpha_code + '\', tried times = {}:'.format(tried_times))
#     while tried_times < max_retried_times:
#         args = []
#         args.append({'nanhandling': 'off', 'delay': '1', 'unitcheck': 'off', 'pasteurize': 'on', 'univid': top,
#                      'opcodetype': 'FLOWSEXPR', 'opassetclass': 'EQUITY', 'unithandling': 'verify',
#                      'optrunc': '0.1',
#                      'code': alpha_code, 'region': region, 'opneut': 'none', 'IntradayType': None,
#                      'tags': 'equity',
#                      'decay': '0', 'DataViz': '0', 'backdays': '256', 'simtime': 'Y10'})
#         sim_data_obj = {
#             'args': args
#         }
#         sim_data_json = json.dumps(sim_data_obj)
#         response = sess.post(sim_url, data=sim_data_json)
#         sim_res_json = response.content
#         print(str(tried_times))
#         try:
#             sim_res_obj = json.loads(sim_res_json)
#             if sim_res_obj['error'] is None:
#                 print("DONE, job id = {}".format(sim_res_obj['result']))
#                 return sim_res_obj['result'][0]
#             elif "You have reached the limit of concurrent simulations" in sim_res_obj['error']['all']:
#                 print("You have reached the limit of concurrent simulations, wait for 3s and retry!")
#                 time.sleep(1)
#         except Exception as ex:
#             tried_times = tried_times + 1
#             print('-------EXCEPTION---------')
#             print(ex)
#             print(sim_res_json)
#             print('-------------------------')
#             pass

#     return 0


# def progress(sess, job_id):
#     loop_count = 0
#     while (True):
#         loop_count = loop_count + 1
#         print("Simulation Loop: " + str(loop_count))
#         progress_url = "https://www.worldquantvrc.com/job/progress/" + str(job_id)
#         prog_res_json = sess.post(progress_url).content
#         print(prog_res_json)
#         prog_res_obj = json.loads(prog_res_json)
#         if prog_res_obj == "DONE":
#             sum_url = "https://www.worldquantvrc.com/job/simsummary/" + str(job_id)
#             sum_res_json = sess.post(sum_url).content
#             sum_res_obj = json.loads(sum_res_json)
#             results = sum_res_obj['result']
#             return sum_res_obj
#         time.sleep(4)


# def req_job_detail(sess, job_id):
#     job_detail_url = "https://www.worldquantvrc.com/job/details/" + str(job_id)
#     jd_res_json = sess.post(job_detail_url).content
#     jd_res_obj = json.loads(jd_res_json)

#     client_alpha_id = jd_res_obj['result']['clientAlphaId']
#     return client_alpha_id


# def req_job_simsummary(sess, job_id):
#     job_simsum_url = "https://www.worldquantvrc.com/job/simsummary/" + str(job_id)
#     job_simsum_json = sess.post(job_simsum_url).content
#     job_simsum_obj = json.loads(job_simsum_json)

#     sharpe = job_simsum_obj['result'][-1]['Sharpe']
#     fitness = job_simsum_obj['result'][-1]['Fitness']
#     long_count = job_simsum_obj['result'][-1]['LongCount']
#     short_count = job_simsum_obj['result'][-1]['ShortCount']
#     return sharpe, fitness, long_count, short_count

# max_simulation_times = 100
# def submit(sess, alpha_id):
#     try:
#         sub_start_url = "https://www.worldquantvrc.com/submission/start"
#         sub_start_data = {
#             "args": json.dumps({"alpha_list": [alpha_id]})
#         }
#         sub_start_res_json = sess.post(sub_start_url, data=sub_start_data).content
#         sub_start_res_obj = json.loads(sub_start_res_json)

#         request_id = sub_start_res_obj['result']['RequestId']
#         print(request_id)
#         loop_count = 0
#         while (True):
#             loop_count = loop_count + 1
#             print("Submission Loop: " + str(loop_count))
#             sub_result_url = "https://www.worldquantvrc.com/submission/result/" + str(request_id)
#             sub_result_json = sess.post(sub_result_url).content
#             sub_result_obj = json.loads(sub_result_json)
#             print(sub_result_obj)
#             if sub_result_obj['error'] is None:
#                 return True, sub_result_obj
#             else:
#                 if ('Cannot submit alpha' in sub_result_obj['error']):
#                     hide_alpha(sess, alpha_id)
#                 return False, sub_result_obj['error']
#             time.sleep(4)
#             if loop_count >= max_simulation_times:
#                 hide_alpha(sess, alpha_id)
#                 return False, sub_result_obj['error']
#     except Exception as ex:
#         print('EXCEPTION: {}'.format(ex))
#         print(sub_start_res_json)
#         pass


# def hide_alpha(sess, alpha_id):
#     hide_alpha_url = "https://www.worldquantvrc.com/hidealphas"
#     hide_alpha_data = {
#         "aidList": json.dumps([alpha_id])
#     }
#     hide_alpha_res_json = sess.post(hide_alpha_url, data=hide_alpha_data).content
#     hide_alpha_res_obj = json.loads(hide_alpha_res_json)

#     return hide_alpha_res_obj


# def req_set_meta(sess, alpha_id):
#     set_meta_url = "https://www.worldquantvrc.com/alphameta"
#     set_meta_data = {
#         "args": json.dumps(
#             {"category": None, "color": "acc3e2", "desc": None, "favorite": 0, "hidden": 0, "isInOS": False,
#              "name": None, "tags": [], "alphaId": alpha_id})
#     }
#     set_meta_res_json = sess.post(set_meta_url, data=set_meta_data).content

#     return set_meta_res_json

#============================================================================================================
#=========== NEW VERSION ====================================================================================
import requests
import json
import time
import threading
from common import config

login_url = "https://api.worldquantvrc.com/authentication"
sim_url = "https://api.worldquantvrc.com/simulations"
myalpha_url = "https://api.worldquantvrc.com/users/self/alphas"
alpha_url = "https://api.worldquantvrc.com/alphas/"
headers = {
    'content-type': 'application/json'
}

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

def login(url, sess):
    # Login function: A session expires after 4 hours, function returns responsed json content and status
    # Add exception from Nhan in the future (Added)
    response = sess.post(url, auth=(
        config.username, config.password), headers=headers)
    #print("\nLOGIN STATUS: " + str(response.status_code) +
    #      "\n========================================\n")

def check_prodcorr(alpha_id, sess):
    # Check prod corr function, input: alpha_id, output: prod corr.
    # Call api continuously until reached max tried time (pre-defined) or get result.
    max_tried_times = 100
    tried_times = 1
    #print("Check product correlation alpha id: "+str(alpha_id)) # For testing only
    while tried_times < max_tried_times:
        try:
            check_prodcorr_url = "https://api.worldquantvrc.com/alphas/" + \
                str(alpha_id) + "/correlations/prod"
            response = sess.get(check_prodcorr_url, data="", headers=headers)
            if ERRORS(sess, response):
                time.sleep(5)
            elif "prodCorrelation" in response.text:
                print("Tried times: "+str(tried_times))
                prod_corr_res_obj = json.loads(response.content)["records"]
                for x in range(1, len(prod_corr_res_obj)-1):
                    if prod_corr_res_obj[len(prod_corr_res_obj)-x][2] != 0:
                        prod_corr = prod_corr_res_obj[len(prod_corr_res_obj)-x][1]
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
            if ERRORS(sess, response):
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

def get_myalpha(sess, min_sharpe=0.7, min_fitness=0.7, offset=0):
    querystring = {"limit": "100", "offset": offset*100, "stage": "IS", "is.sharpe>": min_sharpe,
                   "hidden": "false", "is.fitness>": min_fitness, "order": "-is.fitness", "settings.language": "FASTEXPR", "settings.region": "ASI"}
    response = sess.get(myalpha_url, data="",
                        headers=headers, params=querystring)
    return response

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
            print(response.text)
            if 'FAIL' in response.text:
                print("FAIL") # For testing only
                return False, -1, -1
            elif 'PENDING' in response.text or ERRORS(sess, response):
                time.sleep(3)
            else:
                list_test = json.loads(response.content)["is"]["checks"]
                for check in list_test:
                    if check['name'] == 'SELF_CORRELATION':
                        self_corr = check['value']
                    if check['name'] == 'PROD_CORRELATION':
                        prod_corr = check['value'] 
                return True, self_corr, prod_corr
            tried_times = tried_times + 1
        except ConnectionError:
            time.sleep(20)
        except:
            return True, -1, -1
    return True, -1, -1

def hide_alpha(alpha_id, sess):
    # Hide alphas those are not qualified tested or not good enough to use
    # Using alpha id as determined value
    try:
        url = alpha_url + str(alpha_id)
        payload = "{ \"hidden\":true}"
        response = sess.patch(url, data=payload, headers=headers)
        #print(response.text) # For testing only
    except ConnectionError:
        time.sleep(5)
    except:
        print("THERE IS AN EXCEPTION HERE, HELPPP!")

def simulate_alpha(sess, alpha_code, top, region):
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

def change_name(alpha_id, sess, name="anonymous"):
    # Change name of an alpha. If name = None, websim automatically change it to anonymous
    meta_url = alpha_url + str(alpha_id)
    data = {"color": None, "name": name, "tags": [], "category": None, "description": None}
    try:
        sess.patch(meta_url, data=json.dumps(data), headers=headers).content
    except ConnectionError:
        time.sleep(5)
    except:
        print("EXCEPTION HERE")

#===== PENDING =======

def record_log(time_stamp, record):
    # Insert into Database exception and login event.
    return