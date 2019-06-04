import requests
import json
import time
import threading
import random

from common import config
from common import utils
from data import alldata
import mysql.connector as mysql

from datetime import datetime

alpha_codes = ["group_neutralize(rank( depre / star_ebitda_surprise_prediction_fy2 ), market)",
"group_neutralize(rank( (star_rev_surprise_prediction_fq1 - star_val_implied10_eps_cagr) / star_arm_revenue_score ), subindustry)",
"group_neutralize(rank( (cap - star_arm_global_rank) / star_eps_surprise_prediction_12m ), subindustry)",
"group_neutralize(rank( ppent / star_ebitda_surprise_prediction_fy1 ), sector)",
"group_neutralize(rank( (star_rev_smart_estimate_fq2 - cap) / cash_st ), subindustry)",
"group_neutralize(rank( (star_rev_surprise_prediction_fq1 - star_val_implied10_eps_cagr) / star_arm_revenue_score ), industry)",
"group_neutralize(rank( depre / star_ebitda_surprise_prediction_fy2 ), sector)",
"group_neutralize(rank( (EBITDA - eps) / star_val_earnings_measure_type ), sector)",
"group_neutralize(rank( (EBITDA - eps) / star_val_earnings_measure_type ), market)",
"group_neutralize(rank( ppent / star_ebitda_surprise_prediction_fy1 ), market)"]
