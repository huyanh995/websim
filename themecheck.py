import mysql.connector as mysql

from common import config, utils
from data import alldata
import traceback

update_query = 'UPDATE combo SET theme = {} WHERE alpha_id = \'{}\''
select_query = 'SELECT alpha_id, alpha_code, settings FROM combo WHERE self_corr > 0 and theme = 0'
select_sub_query = 'SELECT alpha_id, alpha_code, settings FROM submitted WHERE self_corr > 0'
update_sub_query = 'UPDATE submitted SET theme = {} WHERE alpha_id = \'{}\''

def theme_check(alpha_id, alpha_code, settings, data):
    # Checking if any combo is satisfied current multi-theme
    try:
        multiplier = 0
        if "ASI" in settings or "EUR" in settings:
            multiplier = multiplier + 2
        if any(err in alpha_code for err in data):
            if multiplier > 0:
                multiplier = multiplier + 1
            else:
                multiplier = multiplier + 2
        if multiplier > 0:
            print(str(alpha_id) + ": THEME x{}".format(multiplier))
        else:
            print(str(alpha_id) + ": NOT THEME")
        db = mysql.connect(**config.config_db)
        cursor = db.cursor()
        cursor.execute(update_query.format(multiplier, alpha_id))
        #cursor.execute(update_sub_query.format(multiplier, alpha_id))
        db.commit()
        db.close()
    except Exception as ex:
        trace_msg = traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        utils.db_insert_log("theme_check", str(trace_msg),"")

data_theme = alldata.data["Theme"]

db = mysql.connect(**config.config_db)
cursor = db.cursor()
cursor.execute(select_query)
#cursor.execute(select_sub_query)
records = cursor.fetchall()
db.close()
for record in records:
    theme_check(record[0], record[1], record[2], data_theme)



