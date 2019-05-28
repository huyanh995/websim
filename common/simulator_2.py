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


headers = {
    'content-type': 'application/json'
}

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