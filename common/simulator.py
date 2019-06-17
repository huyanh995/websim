import requests
import json
import time
import threading
import random
import logging
import sys
import traceback

from common import config
from common.utils import *
import mysql.connector as mysql

from datetime import datetime

login_url = "https://api.worldquantvrc.com/authentication"
sim_url = "https://api.worldquantvrc.com/simulations"
myalpha_url = "https://api.worldquantvrc.com/users/self/alphas"
alpha_url = "https://api.worldquantvrc.com/alphas/"
#submit_url = "https://api.worldquantvrc.com/alphas/"+alpha_id+"/submit"

headers = {
    'content-type': 'application/json'
}
# List of universe USA > EUR > ASI
list_tops = [["TOP200", "TOP500", "TOP1000", "TOP2000", "TOP3000"], [
    "TOP100", "TOP400", "TOP600", "TOP800", "TOP1200"], ["TOP150", "TOP500", "TOP1000", "TOP1500"]]
# SIMULATE and SUBMIT Function
group = ['market', 'sector', 'industry', 'subindustry']

def simulate_alpha(sess, alpha_code, top, region, thread_num):  
    # Simulate alpha (mostly use for combos). Input alpha, universe and region.
    # For combo simulation, alphas have fitness > 1.25, sharpe > 2 and corr < determined values are called signals.
    #max_tried_times = 10
    max_tried_times = 1000
    # First step: POST request to get Job ID, if there're 10 simulteneously threads, wait 3 seconds and re-send.
    tried_sim_time = 1  # For 1st step
    # Second step: After get Job ID, GET request to get Alpha ID
    tried_res_time = 1  # For 2nd step
    try:
        while tried_sim_time < max_tried_times:
            payload = {"type": "SIMULATE", "settings": {"nanHandling": "OFF", "instrumentType": "EQUITY", "delay": 1, "universe": top, "truncation": 0.08, "unitHandling": "VERIFY",
                                                        "pasteurization": "ON", "region": region, "language": "FASTEXPR", "decay": 0, "neutralization": "NONE", "visualization": False}, "code": alpha_code}
            # POST request to server to get Job ID (It's different ID, to get Alpha ID in futher)
            print("Thread {}: SIMULATING: ".format(thread_num) + str(alpha_code))
            job_response = sess.post(
                sim_url, data=json.dumps(payload), headers=headers)
            # Get JSON string from server
            if 'SIMULATION_LIMIT_EXCEED' in job_response.text:
                time.sleep(3)
            elif ERRORS(sess, job_response.text):
                time.sleep(1)
            # No elif ERRORS in here because while API is processing, the response is b' ' which included in ERRORs >> So it'll be stuck in there. 
            # Maybe separate blank response from server in another function (Test it later)
            elif "b\'\'" in job_response.text:
                time.sleep(0.5)
            else: 
                job_id = job_response.headers["Location"].split("/")[-1]
                try:
                    while tried_res_time < 10*max_tried_times:
                        sim_alpha_url = sim_url + "/" + str(job_id)
                        alpha_response = sess.get(
                            sim_alpha_url, data="", headers=headers)
                        print("{}: ".format(tried_res_time) + str(alpha_response))
                        alpha_res_json = json.loads(alpha_response)
                        if ERRORS(sess, alpha_response.text):
                            time.sleep(1)
                        else:
                            if job_id in alpha_response.text: # Condition to know the simulation process is done. Maybe you will find a better solution.
                                if alpha_res_json["status"] == 'COMPLETE':
                                    alpha_id = json.loads(alpha_response.content)["alpha"]
                                    print("Thread {}: DONE: ".format(thread_num)+str(alpha_id))
                                    db_insert_count("simulate_alpha",tried_sim_time, tried_res_time, -1)
                                    return alpha_id
                                else:
                                    break
                        time.sleep(0.5)
                        tried_res_time = tried_res_time + 1
                except Exception as ex_alpha:
                    trace_msg_alpha = traceback.format_exception(etype=type(ex_alpha), value=ex_alpha, tb=ex_alpha.__traceback__)
                    db_insert_log("simulate_alpha",str(trace_msg_alpha), "Job_ID :"+job_response.text+"\nAlpha_ID :"+alpha_response.text)
            time.sleep(1)
            tried_sim_time = tried_sim_time + 1
        db_insert_count("simulate_alpha",tried_sim_time, tried_res_time, -1)
        return None
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_insert_log("simulate_alpha",str(trace_msg), "Job_ID :"+job_response.text) # alpha_response chua duoc khoi tao neu exception xay ra tai job_response.


def multi_simulate(sess, alpha_codes, top, region, thread_num):
    # Simulate alpha (mostly use for signals). Input alpha, universe and region.
    # For signals simulation, alphas have fitness > 0.7, sharpe > 0.7 and corr < determined values are called signals.
    max_tried_times = 1000
    # First step: POST request to get Job ID, if there're 10 simulteneously threads, wait 3 seconds and re-send.
    # Fofr multi or batch simulate, the results will be list of Job_ID.
    tried_step1_time = 1  # For 1st step
    tried_step2_time = 1  # For 2nd step
    # Second step: After get parent Job_ID contains children Job_IDs, get Alpha_ID.
    tried_res_time = 1  # For 3rd step
    try:
        while tried_step1_time < 3*max_tried_times:
            payload = []
            for alpha_code in alpha_codes:
                payload.append({"type": "SIMULATE", "settings": {"nanHandling": "OFF", "instrumentType": "EQUITY", "delay": 1, "universe": top, "truncation": 0.08, "unitHandling": "VERIFY",
                                                            "pasteurization": "ON", "region": region, "language": "FASTEXPR", "decay": 0, "neutralization": "NONE", "visualization": False}, "code": alpha_code})
                # POST request to server to get Job ID (It's different ID, to get Alpha ID in futher)
                print("Thread {}: SIMULATING: ".format(thread_num) + str(alpha_code))
            job_response = sess.post(
                sim_url, data=json.dumps(payload), headers=headers)
            #print("1ST STEP: " + str(job_response.headers))
            # Get JSON string from server
            if 'SIMULATION_LIMIT_EXCEED' in job_response.text:
                time.sleep(3)
            elif ERRORS(sess, job_response.text):
                time.sleep(1)
            elif "b\'\'" in job_response.text:
                time.sleep(0.5)
            # No elif ERRORS in here because while API is processing, the response is b' ' which included in ERRORs >> So it'll be stuck in there. 
            # Maybe separate blank response from server in another function (Test it later) 
            else: 
                parent_job_id = job_response.headers["Location"].split("/")[-1]
                #print("PARENT ID: " + str(parent_job_id))
                while tried_step2_time < 5*max_tried_times:
                    sim_job_url = sim_url + "/" + str(parent_job_id)
                    sim_job_response = sess.get(sim_job_url, data="", headers = headers)
                    #print("2ND STEP: " + str(sim_job_response.text))
                    if 'SIMULATION_LIMIT_EXCEED' in job_response.text:
                        time.sleep(3)
                    elif "progress" in sim_job_response.text:
                        time.sleep(0.5)
                        tried_step2_time = tried_step2_time + 1
                    elif parent_job_id in sim_job_response.text: # Condition shows that the process is done.
                        children_job_ids = json.loads(sim_job_response.content)["children"]
                        #print("CHILDREN IDS: "+str(children_job_ids))
                        alpha_ids = []
                        for job_id in children_job_ids:
                            try:
                                while tried_res_time < 10*max_tried_times:
                                    sim_alpha_url = sim_url + "/" + str(job_id)
                                    alpha_response = sess.get(
                                        sim_alpha_url, data="", headers=headers)
                                    if ERRORS(sess, alpha_response.text):
                                        time.sleep(1)
                                    elif job_id in alpha_response.text: # Condition to know the simulation process is done. Maybe you will find a better solution.
                                        alpha_res_json = json.loads(alpha_response.content)
                                        if alpha_res_json["status"] == 'COMPLETE':
                                            #alpha_id = json.loads(alpha_response.content)["alpha"]
                                            alpha_id = alpha_res_json["alpha"]
                                            alpha_ids.append(alpha_id)
                                            print("Thread {}: DONE: ".format(thread_num)+str(alpha_id))
                                            break
                                        else:
                                            break
                                    else:                                          
                                        time.sleep(0.5)
                                        tried_res_time = tried_res_time + 1
                            except Exception as ex_alpha:
                                trace_msg_alpha = traceback.format_exception(etype=type(ex_alpha), value=ex_alpha, tb=ex_alpha.__traceback__)
                                db_insert_log("multi_simulate",str(trace_msg_alpha), "Job_ID :"+job_response.text+"\nAlpha_ID :"+alpha_response.text)
                        db_insert_count("multi_simulate",tried_step1_time, tried_step2_time, tried_res_time)
                        return alpha_ids, tried_step1_time, tried_step2_time, tried_res_time
            time.sleep(0.5)
            tried_step1_time = tried_step1_time + 1
        db_insert_count("multi_simulate",tried_step1_time, tried_step2_time, tried_res_time)
        return None, tried_step1_time, tried_step2_time, tried_res_time
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        db_insert_log("multi_simulate", str(trace_msg), "Job_ID :"+job_response.text)









