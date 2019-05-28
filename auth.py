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

def get_myalpha(sess, region, top="", min_sharpe=0.7, min_fitness=0.7, offset=0):
    # For checking alpha in my alpha page. 
    # Return response content in json format.
    querystring = {"limit": "100", "offset": offset*100, "stage": "IS", "is.sharpe>": min_sharpe,
                   "hidden": "false", "is.fitness>": min_fitness, "order": "-is.fitness", "settings.language": "FASTEXPR", "settings.region": region, "settings.universe": top}
    response = sess.get(myalpha_url, data="",
                        headers=headers, params=querystring)
    return json.loads(response.content)["results"]
    # For further use, get alpha id in ["id"] of each alpha in results

def get_alpha(sess, page):
    response = get_myalpha(sess, offset=page)
    my_alpha_res_obj = json.loads(response.content)["results"]
    for alpha in my_alpha_res_obj:
        alpha_id = alpha['id']
        submit(alpha_id, sess)
    if "Incorrect authentication credentials" in response.text:
        login(login_url, sess)

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

sess = requests.session()
login(login_url, sess)

check_submission("Qmv2kVK",sess)
print("=====")
for x in range(101):
    for y in get_myalpha(sess, region = "EUR", min_sharpe=1.25, min_fitness=2, offset=x):
        alpha_id = y["id"]
        can_submit, self_corr, prod_corr = check_submission(alpha_id,sess)
        if can_submit == True:
            if self_corr < 0.7 and prod_corr < 0.7:
                 change_name(alpha_id, sess, name = "flag")
            





