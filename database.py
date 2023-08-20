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

queries = []
TABLES = {}

TABLES["heartdisease"] = [
    ("age", "number"),
    ("sex", "string"),
    ("cp", "number"),
    ("trestbps", "number"),
    ("chol", "number"),
    ("fbs", "number"),
    ("restecg", "number"),
    ("thalach", "number"),
    ("exang", "number"),
    ("oldpeak", "number"),
    ("slope", "number"),
    ("ca", "number"),
    ("thal", "number"),
    ("target", "number"),
]


for key in TABLES.keys():
    query = "CREATE TABLE `{}` (".format(key)
    for index, item in enumerate(TABLES[key]):
        if index == len(TABLES[key]) - 1:
            temp = (
                " {} FLOAT )".format(item[0])
                if item[1] == "number"
                else "{} varchar(25) )".format(item[0])
            )
        else:
            temp = (
                " {} FLOAT ,".format(item[0])
                if item[1] == "number"
                else "{} varchar(25) ,".format(item[0])
            )
        query += temp
    queries.append(query)

cursor = connection.cursor()
for query in queries:
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(error.msg)


connection.close()
