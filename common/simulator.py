import requests
import json
import time
import threading
import random

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

def simulate_alpha(sess, alpha_code, top, region):  # Need to check again.
    # Simulate alpha (mostly use for signals). Input alpha, universe and region.
    # For signals simulation, alphas have fitness > 0.7, sharpe > 0.7 and corr < determined values are called signals.
    max_tried_times = 10
    # First step: POST request to get Job ID, if there're 10 simulteneously thread, wait 3 seconds and re-send.
    tried_sim_time = 1  # For 1st step
    # Second step: After get Job ID, GET request to get Alpha ID
    tried_res_time = 1  # For 2nd step
    try:
        while tried_sim_time < max_tried_times:
            payload = {"type": "SIMULATE", "settings": {"nanHandling": "OFF", "instrumentType": "EQUITY", "delay": 1, "universe": top, "truncation": 0.08, "unitHandling": "VERIFY",
                                                        "pasteurization": "ON", "region": region, "language": "FASTEXPR", "decay": 0, "neutralization": "NONE", "visualization": False}, "code": alpha_code}
            # POST request to server to get Job ID (It's different ID, to get Alpha ID in futher)
            job_response = sess.post(
                sim_url, data=json.dumps(payload), headers=headers)
            # Get JSON string from server
            if 'SIMULATION_LIMIT_EXCEED' in job_response.text:
                time.sleep(3)
            # No elif ERRORS in here because while API is processing, the response is b' ' which included in ERRORs >> So it'll be stuck in there. 
            # Maybe separate blank response from server in another function (Test it later)
            else: 
                job_id = job_response.headers["Location"].split("/")[-1]
                while tried_res_time < 10*max_tried_times:
                    sim_alpha_url = sim_url + "/" + str(job_id)
                    alpha_response = sess.get(
                        sim_alpha_url, data="", headers=headers)
                    if ERRORS(sess, alpha_response.content):
                        time.sleep(3)
                    else:
                        if job_id in alpha_response.text: # Condition to know the simulation process is done. Maybe you will find a better solution.
                            alpha_id = json.loads(alpha_response.content)["alpha"]
                            return alpha_id
                    time.sleep(0.5)
                    tried_res_time = tried_res_time + 1
            time.sleep(1)
            tried_sim_time = tried_sim_time + 1
        return None
    except Exception as ex:
        db_insert_log("simulate_alpha",str(ex), "Job_ID :"+job_response.text+"\nAlpha_ID :"+alpha_response.text)



# For testing only
sess = requests.session()
login(login_url, sess)
# alpha_code = "vu0 = group_neutralize(rank( (cost_of_revenue + income) / cogs ), industry); vu1 = group_neutralize(rank( (sales + quick_ratio) / bookvalue_ps ), sector); vu2 = group_neutralize(rank( (SGA_expense + star_eps_smart_estimate_fq1) / star_ebitda_smart_estimate_fq1 ), market); vu3 = group_neutralize(rank( (star_val_dividend_projection_fy10 + SGA_expense) / retained_earnings ), sector); vu4 = group_neutralize(rank( (star_val_earnings_projection_fy10 + cashflow_op) / star_ebitda_smart_estimate_fy1 ), market); vu5 = group_neutralize(rank( (star_arm_global_rank + star_rev_smart_estimate_fy1) / inventory ), industry); vu6 = group_neutralize(rank( (sales + income) / debt ), market); vu7 = group_neutralize(rank( (income_beforeextra + star_eps_analyst_number_fy1) / ppent ), market); vu8 = group_neutralize(rank( (star_val_fwd10_eps_cagr + SGA_expense) / debt ), subindustry); vu9 = group_neutralize(rank( (star_ebitda_surprise_prediction_fq1 + star_val_earnings_projection_fy14) / star_val_earnings_projection_fy2 ), market); vu10 = group_neutralize(rank( (pretax_income + cashflow_op) / income_tax_payable ), industry); vu11 = group_neutralize(rank( (star_val_earnings_projection_fy13 + star_rev_surprise_prediction_12m) / star_val_earnings_projection_fy11 ), market); vu12 = group_neutralize(rank( (star_val_fwd10_eps_cagr + SGA_expense) / debt ), sector); vu13 = group_neutralize(rank( (star_rev_analyst_number_fq2 + cashflow_op) / star_ebitda_smart_estimate_fy2 ), industry); vu14 = group_neutralize(rank( (pretax_income + capex) / star_val_piv_region_rank ), sector); vu15 = group_neutralize(rank( (cashflow_op + star_val_earnings_projection_fy4) / liabilities_oth ), industry); alpha = group_neutralize(add(vu0, vu1, vu2, vu3, vu4, vu5, vu6, vu7, vu8, vu9, vu10, vu11, vu12, vu13, vu14, vu15, filter = true), market); alpha"
# temp = simulate_alpha(
#     sess, alpha_code, "TOP400", "EUR")
# print(check_selfcorr(temp, sess))
# print(check_prodcorr(temp, sess))
# print(check_submission(temp, sess))




