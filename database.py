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
    ("age", "float"),
    ("sex", "int"),
    ("cp", "float"),
    ("trestbps", "float"),
    ("chol", "float"),
    ("fbs", "float"),
    ("restecg", "float"),
    ("thalach", "float"),
    ("exang", "float"),
    ("oldpeak", "float"),
    ("slope", "float"),
    ("ca", "float"),
    ("thal", "float"),
    ("target", "int"),
]

TABLES["diabetes"] = [
    ("Pregnancies", "float"),
    ("Glucose", "float"),
    ("BloodPressure", "float"),
    ("SkinThickness", "float"),
    ("Insulin", "float"),
    ("BMI", "float"),
    ("DiabetesPedigreeFunction", "float"),
    ("Age", "float"),
    ("Outcome", "int"),
]

for key in TABLES.keys():
    query = "CREATE TABLE `{}` (".format(key)
    for index, item in enumerate(TABLES[key]):
        if index == len(TABLES[key]) - 1:
            temp = (
                " {} FLOAT )".format(item[0])
                if item[1] == "float"
                else "{} VARCHAR(25) )".format(item[0])
                if item[1] == "string"
                else "{} INT )".format(item[0])
            )
        else:
            temp = (
                " {} FLOAT ,".format(item[0])
                if item[1] == "float"
                else "{} VARCHAR(25) ,".format(item[0])
                if item[1] == "string"
                else "{} INT ,".format(item[0])
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
