import pymongo
from flask import Flask, render_template, request, session, make_response, redirect, url_for
from pymongo import MongoClient
from Admin.models.student import Student
from Admin.models.teacher import Teacher
from Admin.models.database import Database
from Admin.models.courses import Courses
from Admin.models.message import Message

app = Flask(__name__)
app.secret_key = "tdu"


@app.before_first_request
def clear_session():
    session['username'] = None


@app.before_first_request
def initialize_message():
    Message.add_student_record_success()
    Message.add_teacher_record_success()
    Message.add_course_success()
    Message.update_student_success()
    Message.update_teacher_record_success()
    Message.update_course_success()
    Message.delete_student_record_success()
    Message.delete_teacher_record_success()
    Message.delete_course_success()
    Message.course_found_success()


@app.route('/')
def home_template():
    if session['username'] is None:
        return render_template("home.html")
    else:
        return redirect("/home")


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.form['admin-username']
    password = request.form['admin-pwd']
    URI = f"mongodb://127.0.0.1:27000/admin"
    try:
        client = MongoClient(URI, wtimeout=3000)
        admin_db = client['admin']
        if admin_db.authenticate(name=username, password=password, source="admin"):
            session['username'] = username
            Database.initialize(f"mongodb://{username}:{password}@127.0.0.1:27000/admin")
            return redirect("/home")
        else:
            session['username'] = None
            return render_template("home.html")
    except pymongo.errors.OperationFailure:
        return redirect("/")
    except pymongo.errors.ConfigurationError:
        return redirect("/")
    except pymongo.errors.ServerSelectionTimeoutError:
        return redirect("/error")
    except ValueError:
        return redirect("/")


@app.route('/home')
def admin_dashboard():
    if session['username'] is None:
        print(session)
        return redirect("/")
    else:
        print(session)
        return render_template("dashboard.html", message=Message)


@app.route('/add/student-details', methods=['POST'])
def add_student():
    student = Student(db=Database.db,
                      reg_no=request.form["student-reg-no"],
                      name=request.form["student-name"],
                      password=request.form["student-initial-password"],
                      phone_no=request.form["student-phone-number"],
                      address=request.form["student-address"],
                      mother_name=request.form["student-mother-name"],
                      father_name=request.form["student-father-name"]
                      )
    if student.is_success:
        Message.add_student_record_success()
        student.save_to_mongo(Database.db)
        return redirect("/")
    else:
        Message.add_student_record_fail()
        return redirect("/")


@app.route('/update/student-details', methods=['POST'])
def update_student():
    if Student.update_details(database=Database.db,
                              reg_no=request.form["student-reg-no"],
                              name=request.form["student-name"],
                              phone_no=request.form["student-phone-number"],
                              address=request.form["student-address"],
                              mother_name=request.form["student-mother-name"],
                              father_name=request.form["student-father-name"]
                              ).matched_count == 1:
        Message.update_student_success()
    else:
        Message.update_student_fail()
    return redirect("/")


@app.route('/delete/student-details', methods=['POST'])
def delete_student():
    if Student.delete_student(database=Database.db, reg_no=request.form["student-reg-no"]).deleted_count == 1:
        Message.delete_student_record_success()
    else:
        Message.delete_student_record_fail()
    return redirect("/")


@app.route('/add/teacher-details', methods=['POST'])
def add_teacher():
    teacher = Teacher(
        db=Database.db,
        prof_id=request.form["prof-id"],
        name=request.form["teacher-name"],
        phone_no=request.form["teacher-phone-no"],
        address=request.form["teacher-address"],
        password=request.form["teacher-password"],
        courses=request.form["teacher-courses"]
    )
    if teacher.is_success and teacher.is_course:
        Message.add_teacher_record_success()
        Message.course_found_success()
        teacher.save_to_mongo(database=Database.db)
    elif not teacher.is_course and teacher.is_success:
        Message.course_found_fail()
    elif not teacher.is_success and teacher.is_course:
        Message.add_teacher_record_fail()
    elif not teacher.is_success and not teacher.is_course:
        Message.add_teacher_record_fail()
        Message.course_found_fail()
    return redirect("/")


@app.route('/update/teacher-details', methods=['POST'])
def update_teacher():
    courses = request.form["teacher-courses"]
    if Courses.check_courses(database=Database.db, courses=courses):
        Message.course_found_success()
    else:
        Message.course_found_fail()
    temp = Teacher.update_teacher(
        database=Database.db,
        prof_id=request.form["prof-id"],
        name=request.form["teacher-name"],
        phone_no=request.form["teacher-phone-no"],
        address=request.form["teacher-address"],
        courses=courses
    )
    if temp.matched_count == 1:
        Message.update_teacher_record_success()
    else:
        Message.update_teacher_record_fail()
    return redirect("/")


@app.route('/delete/teacher-details', methods=['POST'])
def delete_teacher():
    if Teacher.delete_teacher(database=Database.db, prof_id=request.form["prof-id"]).deleted_count == 1:
        Message.delete_teacher_record_success()
    else:
        Message.delete_teacher_record_fail()
    return redirect("/")


@app.route('/add/course', methods=['POST'])
def add_course():
    course = Courses(db=Database.db,
                     course_id=request.form["course-id"],
                     course_title=request.form["course-title"]
                     )
    if course.is_success:
        Message.add_course_success()
        course.save_to_mongo(database=Database.db)
    else:
        Message.add_course_fail()
        print(Message.addCourseFail)
    return redirect("/")


@app.route('/update/course', methods=['POST'])
def update_course():
    if Courses.update_course(database=Database.db,
                             course_id=request.form["course-id"],
                             course_title=request.form["course-title"]).matched_count == 1:
        Message.update_course_success()
    else:
        Message.update_course_fail()
    return redirect("/")


@app.route('/delete/course', methods=['POST'])
def delete_course():
    if Courses.delete_course(database=Database.db,
                             course_id=request.form["course-id"]).deleted_count == 1:
        Message.delete_course_success()
    else:
        Message.delete_course_fail()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=4990, debug=True)