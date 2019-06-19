import requests
import json
import time
import threading
import traceback
import random
from common import config, utils, stuff
import mysql.connector as mysql

from datetime import datetime

# Re-checking submission all combo from combo DB to get the precise self and prod correlation.
# Recommend using after a day. 

print("\nRE-CHECKING ALPHAS IN COMBO DB\n")
input = input("Number of qualified alphas (Default: 15): ")

sess = requests.session()
utils.login(sess)
if input == "":
    stuff.re_check(sess) # Default
elif input == "all":
    stuff.re_check_all(sess) # Check all combos
else:
    qual_num = int(input)
    stuff.re_check(sess, qual_num)
print("==============================")

