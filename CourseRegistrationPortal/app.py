import hashlib

import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from bson.objectid import ObjectId
from CourseRegistrationPortal.models.database import Database
from CourseRegistrationPortal.models.message import Message

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
    try:
        username = request.form['username']
        password = request.form['password']
        if Database.db["student_details"].find_one({"_id": username}) and \
                Database.db["student_details"].find_one({"_id": username})['current_password']==\
                str(hashlib.sha256(password.encode()).hexdigest()):
            session['username'] = username
        return redirect("/")
    except pymongo.errors.ServerSelectionTimeoutError:
        return render_template("servers_down.html")


@app.route("/register/<int:page>")
def register(page):
    if session['username'] is None:
        return redirect("/")
    else:
        limit = 10

        last_page = int(Database.db["batches"].find({"semester": SEMESTER_ID}).count()/10)
        courses = []
        for course in Database.db["batches"].find({"semester": SEMESTER_ID}).sort('_id', pymongo.ASCENDING).skip(page*10).limit(limit):
            courses.append(course)
        return render_template("register_courses.html", courses=courses, next_page=page+1,
                               last_page=last_page, prev_page=page-1, message=Message)


def is_seat_available(batch_id):
    return True if int(Database.db["batches"].find_one({"_id": ObjectId(batch_id)})["available_seats"]) > 0 else False


def get_available_seats(batch_id):
    return int(Database.db["batches"].find_one({"_id": ObjectId(batch_id)})["available_seats"])


def is_class_registered(batch_id):
    temp = [t for t in Database.db["student_sem_classes"].find({"reg_no": session["username"], "batch_id": batch_id})]
    return True if not temp else False


def is_slot_available(slot):
    clashing = clashing_slots.get(slot)
    for batch in Database.db["student_sem_classes"].find({"reg_no": session["username"], "semester": SEMESTER_ID}):
        if batch["slot"] in clashing:
            return False
    return True


@app.route("/register-course", methods=["POST"])
def register_course():
    _id = request.form["_id"]
    course_id = request.form["course_id"]
    semester = request.form["semester"]
    prof_id = request.form["prof_id"]
    slot = request.form["slot"]
    available_seats = get_available_seats(batch_id=_id)
    if is_seat_available(_id):
        if is_class_registered(batch_id=_id):
            if is_slot_available(slot):
                Database.db["batches"].update_one({"_id": ObjectId(_id)},
                                                  {"$set": {"available_seats": str(available_seats - 1)}})
                Database.db["student_sem_classes"].insert_one({
                    "reg_no": session["username"],
                    "semester": semester,
                    "batch_id": _id,
                    "course_id": course_id,
                    "prof_id": prof_id,
                    "slot": slot
                })
            else:
                Message.slot_fail()
        else:
            Message.batch_fail()
    else:
        Message.seats_fail()
    return redirect("/register/0")


@app.route("/delete")
def delete():
    courses = [course for course in Database.db["student_sem_classes"].find({"reg_no": session['username'], "semester": SEMESTER_ID})]
    return render_template("delete_courses.html", courses=courses)


if __name__ == "__main__":
    app.run(port=4992, debug=True)


#TODO: Add Logout Button