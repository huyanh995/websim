import requests
import json
import time
import threading
from common import config
import mysql.connector as mysql

from datetime import datetime

# Main part to run the whole project. It can be separated into two parts.

# 1. Simulate signals: (4 threadings)
# signal_generator() -> (alphas) -> simulate() -> (alpha_id) -> get_alpha_info()
# -> (alpha_info) -> check conditions -> db_insert_signals()



# 2. Simulate combos: (6 threadings)
# combo_generator() -> (alphas) -> simulate() -> (alpha_id) -> get_alpha_info()
# -> (alpha_info) -> check conditions -> db_insert_signals()



