import requests
import json
import time
import threading
from common import config

max_retried_times = 10

headers = {
    'user-agent': 'Mozilla/5.0'
}

login_data = {
    'EmailAddress': "huyanhkstntt@gmail.com",
    'Password': "Dangquang1995",    
    'next': '',
    'g-recaptcha-response': ''
}


sim_url = "https://www.worldquantvrc.com/simulate"
login_url = "https://www.worldquantvrc.com/login/process"
def login(sess):
    r = sess.post(login_url, data=login_data, headers=headers)
    print(r.content)


def simulate_for_submission(sess, alpha_code, region, top):
    tried_times = 1

    print('simulating \'' + alpha_code + '\', tried times = {}:'.format(tried_times))
    while tried_times < max_retried_times:
        args = []
        args.append({'nanhandling': 'off', 'delay': '1', 'unitcheck': 'off', 'pasteurize': 'on', 'univid': top,
                     'opcodetype': 'FLOWSEXPR', 'opassetclass': 'EQUITY', 'unithandling': 'verify',
                     'optrunc': '0.1',
                     'code': alpha_code, 'region': region, 'opneut': 'none', 'IntradayType': None,
                     'tags': 'equity',
                     'decay': '0', 'DataViz': '0', 'backdays': '256', 'simtime': 'Y10'})
        sim_data_obj = {
            'args': args
        }
        sim_data_json = json.dumps(sim_data_obj)
        response = sess.post(sim_url, data=sim_data_json)
        sim_res_json = response.content
        print(str(tried_times))
        try:
            sim_res_obj = json.loads(sim_res_json)
            if sim_res_obj['error'] is None:
                print("DONE, job id = {}".format(sim_res_obj['result']))
                return sim_res_obj['result'][0]
            elif "You have reached the limit of concurrent simulations" in sim_res_obj['error']['all']:
                print("You have reached the limit of concurrent simulations, wait for 3s and retry!")
                time.sleep(1)
        except Exception as ex:
            tried_times = tried_times + 1
            print('-------EXCEPTION---------')
            print(ex)
            print(sim_res_json)
            print('-------------------------')
            pass

    return 0


def progress(sess, job_id):
    loop_count = 0
    while (True):
        loop_count = loop_count + 1
        print("Simulation Loop: " + str(loop_count))
        progress_url = "https://www.worldquantvrc.com/job/progress/" + str(job_id)
        prog_res_json = sess.post(progress_url).content
        print(prog_res_json)
        prog_res_obj = json.loads(prog_res_json)
        if prog_res_obj == "DONE":
            sum_url = "https://www.worldquantvrc.com/job/simsummary/" + str(job_id)
            sum_res_json = sess.post(sum_url).content
            sum_res_obj = json.loads(sum_res_json)
            results = sum_res_obj['result']
            return sum_res_obj
        time.sleep(4)


def req_job_detail(sess, job_id):
    job_detail_url = "https://www.worldquantvrc.com/job/details/" + str(job_id)
    jd_res_json = sess.post(job_detail_url).content
    jd_res_obj = json.loads(jd_res_json)

    client_alpha_id = jd_res_obj['result']['clientAlphaId']
    return client_alpha_id


def req_job_simsummary(sess, job_id):
    job_simsum_url = "https://www.worldquantvrc.com/job/simsummary/" + str(job_id)
    job_simsum_json = sess.post(job_simsum_url).content
    job_simsum_obj = json.loads(job_simsum_json)

    sharpe = job_simsum_obj['result'][-1]['Sharpe']
    fitness = job_simsum_obj['result'][-1]['Fitness']
    long_count = job_simsum_obj['result'][-1]['LongCount']
    short_count = job_simsum_obj['result'][-1]['ShortCount']
    return sharpe, fitness, long_count, short_count

max_simulation_times = 100
def submit(sess, alpha_id):
    try:
        sub_start_url = "https://www.worldquantvrc.com/submission/start"
        sub_start_data = {
            "args": json.dumps({"alpha_list": [alpha_id]})
        }
        sub_start_res_json = sess.post(sub_start_url, data=sub_start_data).content
        sub_start_res_obj = json.loads(sub_start_res_json)

        request_id = sub_start_res_obj['result']['RequestId']
        print(request_id)
        loop_count = 0
        while (True):
            loop_count = loop_count + 1
            print("Submission Loop: " + str(loop_count))
            sub_result_url = "https://www.worldquantvrc.com/submission/result/" + str(request_id)
            sub_result_json = sess.post(sub_result_url).content
            sub_result_obj = json.loads(sub_result_json)
            print(sub_result_obj)
            if sub_result_obj['error'] is None:
                return True, sub_result_obj
            else:
                if ('Cannot submit alpha' in sub_result_obj['error']):
                    hide_alpha(sess, alpha_id)
                return False, sub_result_obj['error']
            time.sleep(4)
            if loop_count >= max_simulation_times:
                hide_alpha(sess, alpha_id)
                return False, sub_result_obj['error']
    except Exception as ex:
        print('EXCEPTION: {}'.format(ex))
        print(sub_start_res_json)
        pass


def hide_alpha(sess, alpha_id):
    hide_alpha_url = "https://www.worldquantvrc.com/hidealphas"
    hide_alpha_data = {
        "aidList": json.dumps([alpha_id])
    }
    hide_alpha_res_json = sess.post(hide_alpha_url, data=hide_alpha_data).content
    hide_alpha_res_obj = json.loads(hide_alpha_res_json)

    return hide_alpha_res_obj


def req_set_meta(sess, alpha_id):
    set_meta_url = "https://www.worldquantvrc.com/alphameta"
    set_meta_data = {
        "args": json.dumps(
            {"category": None, "color": "acc3e2", "desc": None, "favorite": 0, "hidden": 0, "isInOS": False,
             "name": None, "tags": [], "alphaId": alpha_id})
    }
    set_meta_res_json = sess.post(set_meta_url, data=set_meta_data).content

    return set_meta_res_json

