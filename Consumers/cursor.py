import mysql.connector
from mysql.connector import errorcode

DBNAME = "privacydatabase"
try:
    connection = mysql.connector.connect(
        user="root", password="root", host="127.0.0.1", database=DBNAME
    )
    print("connected")
except:
    print("error in connection")

cursor = connection.cursor()
