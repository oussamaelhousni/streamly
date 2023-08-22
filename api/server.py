# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import mysql.connector

DBNAME = "privacydatabase"
try:
    connection = mysql.connector.connect(
        user="root", password="root", host="127.0.0.1", database=DBNAME
    )
    print("connected")
except:
    print("error in connection")

cursor = connection.cursor()

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)


class HeartDisease(Resource):
    def get(self):
        cursor.execute("SELECT * FROM heartdisease")
        result = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
        return jsonify(result)


class Diabetes(Resource):
    def get(self):
        cursor.execute("SELECT * FROM diabetes")
        result = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
        return jsonify(result)


# adding the defined resources along with their corresponding urls
api.add_resource(HeartDisease, "/heartdisease")
api.add_resource(Diabetes, "/diabetes")

# driver function
if __name__ == "__main__":
    app.run(debug=False)
