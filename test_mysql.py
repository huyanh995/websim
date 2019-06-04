import mysql.connector as mysql
from common import config

# Test current connection and user used.
db = mysql.connect(**config.config_db)
print("===========================")
print("Connection: " + str(db.is_connected())+ "\nUser: " + str(db._user))
