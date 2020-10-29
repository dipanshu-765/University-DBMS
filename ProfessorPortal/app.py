import datetime
import hashlib
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect
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

slots = {
    'Monday': {
        'A1': '8:00',
        'A2': '18:00',
        'B1': '10:00',
        'B2': '17:00',
        'C1': '12:00',
        'C2': '16:00',
        'D2': '14:00',
        'E2': '15:00',
        'L1': '8:30',
        'L3': '10:00'
    },
    'Tuesday': {
        'A1': '11:00',
        'B1': '12:00',
        'D1': '8:00',
        'E1': '9:00',
        'F1': '10:00',
        'A2': '14:00',
        'B2': '15:00',
        'C2': '17:00',
        'D2': '18:00',
        'F2': '16:00',
        'L2': '14:00',
        'L4': '15:30'
    },
    'Wednesday': {
        'C1': '9:00',
        'D1': '10:00',
        'E1': '11:00',
        'F1': '12:00',
        'E2': '16:00',
        'F2': '17:00',
        'L5': '8:00',
        'L7': '9:30'
    },
    'Thursday': {
        'A1': '11:00',
        'D1': '12:00',
        'E1': '10:00',
        'A2': '17:00',
        'C2': '15:00',
        'D2': '16:00',
        'L6': '14:00',
        'L8': '15:30'
    },
    'Friday': {
        'B1': '10:00',
        'C1': '8:00',
        'F1': '12:00',
        'B2': '15:00',
        'E2': '17:00',
        'F2': '18:00',
        'L9': '10:00',
        'L10': '17:30'
    }
}

SEMESTER = 'SEM000001'


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


@app.route("/auth/login", methods=["POST"])
def login():
    try:
        username = request.form['teacher-username']
        password = request.form['teacher-pwd']
        if Database.db["teacher_details"].find_one({"_id": username}) and \
                Database.db["teacher_details"].find_one({"_id": username})['current_password'] == \
                str(hashlib.sha256(password.encode()).hexdigest()):
            session['username'] = username
        return redirect("/")
    except pymongo.errors.ServerSelectionTimeoutError:
        return render_template("servers_down.html")


@app.route("/")
def home():
    teacher = Database.db["teacher_details"].find_one({'_id': session["username"]})
    all_classes = [batch for batch in Database.db["batches"].find({
        "semester": SEMESTER,
        "prof_id": session["username"]})]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day = days[datetime.date.today().weekday()]
    classes_today = []
    classes = []
    for one_class in all_classes:
        time = slots.get(day).get(one_class['slot'], None)
        course_id = Database.db["batches"].find_one({'semester': SEMESTER, 'slot': one_class['slot'], 'prof_id': session["username"]})['course_id']
        course = Database.db["courses"].find_one({'_id': course_id})['course_title']
        classes.append({'slot': one_class['slot'], 'course': course, 'id': one_class['_id']})
        if time:
            classes_today.append({'time': time, 'course': course})
    return render_template("dashboard.html", classes=classes_today, teacher=teacher, all_classes=classes) if session['username'] else render_template("home.html")


@app.route("/my-classes/<string:batch_id>")
def view_classes(batch_id):
    return render_template("classes.html", id=batch_id)


def get_students(batch_id):
    students = []
    for student in Database.db["student_sem_classes"].find({'batch_id': batch_id}):
        name = Database.db["student_details"].find_one({'_id': student['reg_no']})['name']
        students.append({
            "reg_no": student['reg_no'],
            "name": name
        })
    return students


@app.route("/my-classes/<string:batch_id>/update/da", methods=['POST', 'GET'])
def update_da(batch_id):
    students = get_students(batch_id)
    if request.method == 'GET':
        return render_template("update_grades.html", students=students)
    else:
        for student in students:
            Database.db["grades"].update_one(
                {"batch": batch_id, "reg_no": student['reg_no']},
                {"$set": {
                    "DA": request.form[student['reg_no']]
                    }
                }
                , upsert=True)
        return redirect(f"/my-classes/{batch_id}")


@app.route("/my-classes/<string:batch_id>/update/quiz1", methods=['POST', 'GET'])
def update_quiz1(batch_id):
    students = get_students(batch_id)
    if request.method == 'GET':
        return render_template("update_grades.html", students=students)
    else:
        for student in students:
            Database.db["grades"].update_one(
                {"batch": batch_id, "reg_no": student['reg_no']},
                {"$set": {
                    "Quiz 1": request.form[student['reg_no']]
                    }
                }
                , upsert=True)
        return redirect(f"/my-classes/{batch_id}")


@app.route("/my-classes/<string:batch_id>/update/quiz2", methods=['POST', 'GET'])
def update_quiz2(batch_id):
    students = get_students(batch_id)
    if request.method == 'GET':
        return render_template("update_grades.html", students=students)
    else:
        for student in students:
            Database.db["grades"].update_one(
                {"batch": batch_id, "reg_no": student['reg_no']},
                {"$set": {
                    "Quiz 2": request.form[student['reg_no']]
                    }
                }
                , upsert=True)
        return redirect(f"/my-classes/{batch_id}")


@app.route("/my-classes/<string:batch_id>/update/assessment1", methods=['POST', 'GET'])
def update_assessment1(batch_id):
    students = get_students(batch_id)
    if request.method == 'GET':
        return render_template("update_grades.html", students=students)
    else:
        for student in students:
            Database.db["grades"].update_one(
                {"batch": batch_id, "reg_no": student['reg_no']},
                {"$set": {
                    "Assessment 1": request.form[student['reg_no']]
                    }
                }
                , upsert=True)
        return redirect(f"/my-classes/{batch_id}")


@app.route("/my-classes/<string:batch_id>/update/assessment2", methods=['POST', 'GET'])
def update_assessment2(batch_id):
    students = get_students(batch_id)
    if request.method == 'GET':
        return render_template("update_grades.html", students=students)
    else:
        for student in students:
            Database.db["grades"].update_one(
                {"batch": batch_id, "reg_no": student['reg_no']},
                {"$set": {
                    "Assessment 2": request.form[student['reg_no']]
                    }
                }
                , upsert=True)
        return redirect(f"/my-classes/{batch_id}")


@app.route("/my-classes/<string:batch_id>/update/final", methods=['POST', 'GET'])
def update_finals(batch_id):
    students = get_students(batch_id)
    if request.method == 'GET':
        return render_template("update_grades.html", students=students)
    else:
        for student in students:
            Database.db["grades"].update_one(
                {"batch": batch_id, "reg_no": student['reg_no']},
                {"$set": {
                        "Finals": request.form[student['reg_no']]
                    }
                }
            , upsert=True)
        return redirect(f"/my-classes/{batch_id}")


@app.route('/logout')
def logout():
    session["username"] = None
    return redirect("/")


if __name__ == "__main__":
    app.run(port=4994, debug=True)

# TODO: Restrict access to Registration Portal
# TODO: Change schema of "Batches" collection. Keep only prof_id and course_id
# TODO: Add Logout Button
# TODO: Add Update Password and View Profile Options
# TODO: View Marks
