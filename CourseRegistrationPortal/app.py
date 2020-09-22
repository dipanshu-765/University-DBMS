import hashlib

import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from CourseRegistrationPortal.models.database import Database

app = Flask(__name__)
app.secret_key = "tdu"


clashing_slots = {
    'A1': ['L1', 'A1'],
    'A2': ['L2', 'A2'],
    'B1': ['L3', 'B1'],
    'B2': ['L4', 'B2'],
    'C1': ['L5', 'C1'],
    'C2': ['L6', 'C2'],
    'D1': ['L7', 'D1'],
    'D2': ['L8', 'D2'],
    'E1': ['L9', 'E1'],
    'E2': ['L10', 'E2'],
    'F1': ['F1'],
    'F2': ['F2'],
    'L1': ['L1', 'A1'],
    'L2': ['L2', 'A2'],
    'L3': ['L3', 'B1'],
    'L4': ['L4', 'B2'],
    'L5': ['L5', 'C1'],
    'L6': ['L6', 'C2'],
    'L7': ['L7', 'D1'],
    'L8': ['L8', 'D2'],
    'L9': ['L9', 'E1'],
    'L10': ['L10', 'E2']
}


SEMESTER_ID = "SEM000001"


@app.before_first_request
def initialize():
    session['username'] = None
    URI = f"mongodb://temp-123:temp-123@127.0.0.1:27000/admin"
    try:
        client = MongoClient(URI, wtimeout=3000)
        Database.initialize(URI)
    except pymongo.errors.OperationFailure:
        return redirect("/")
    except pymongo.errors.ServerSelectionTimeoutError:
        return render_template("servers_down.html")


@app.route("/")
def home():
    return render_template("dashboard.html") if session['username'] else render_template("home.html")


@app.route("/auth/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    if Database.db["student_details"].find_one({"_id": username}) and \
            Database.db["student_details"].find_one({"_id": username})['current_password']==\
            str(hashlib.sha256(password.encode()).hexdigest()):
        session['username'] = username

    return redirect("/")


if __name__ == "__main__":
    app.run(port=4992, debug=True)