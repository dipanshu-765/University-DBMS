import pymongo
from flask import Flask, render_template, request, session, make_response, redirect, url_for, jsonify
from pymongo import MongoClient
from Admin.models.student import Student
from Admin.models.teacher import Teacher
from Admin.models.database import Database
from Admin.models.courses import Courses
from Admin.models.message import Message
from Admin.models.batch import Batch
from Admin.models.form import AddBatchForm

app = Flask(__name__)
app.secret_key = "tdu"


def get_prof(course_id):
    return [teacher for teacher in Database.db["teacher_details"].find({'courses': course_id})]


clashing_slots = {
    'A1': 'L1',
    'A2': 'L2',
    'B1': 'L3',
    'B2': 'L4'
}


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
        return render_template("home.html", logout=logout)
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
        courses = Database.db["courses"].find({})
        return render_template("dashboard.html", message=Message, find_prof=find_prof, courses=courses, logout=logout)


def find_prof(value):
    print("onchange called")
    Batch.find_prof(database=Database.db, course=value)


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


@app.route('/add/batch', methods=['POST', 'GET'])
def add_batch():
    courses = [course for course in Database.db["courses"].find({})]
    teachers = get_prof(course_id=courses[0]['course_id'])
    form = AddBatchForm(courses=courses)
    form.course.choices = [(course['course_id'], course['course_title']) for course in courses]
    form.teacher.choices = [(teacher['prof_id'], teacher['name']) for teacher in teachers]
    if request.method == 'GET':
        return render_template("add_batch.html", form=form)
    else:
        is_slot_available = True

        prof_id = request.form['teacher']
        prof_name = Database.db['teacher_details'].find_one({'prof_id': prof_id})['name']
        course_id = request.form['course']
        course_title = Database.db['courses'].find_one({'course_id': course_id})['course_title']
        available_seats = request.form['seats']
        semester = request.form['semester']
        slot = request.form['slot']

        temp = Database.db["teacher_slots"].find({'semester': semester})
        for t in temp:
            temp_slot = t['slot']
            if clashing_slots.get(temp_slot, 0) == slot:
                is_slot_available = False

        if is_slot_available:
            Batch(prof_id=prof_id, prof_name=prof_name, course_id=course_id, course_title=course_title,
                  available_seats=available_seats, slot=slot, semester=semester).save_to_mongo(database=Database.db)
            Database.db["teacher_slots"].insert_one({
                'semester': request.form['semester'],
                'teacher': request.form['teacher'],
                'slot': request.form['slot']
            })

        return redirect("/")


@app.route('/teacher/<course_id>')
def teacher_state(course_id):
    if session['username'] is None:
        return redirect('/')
    teacher_array = []
    teachers = get_prof(course_id=course_id)
    for teacher in teachers:
        temp_teacher = dict()
        temp_teacher['prof_id'] = teacher['prof_id']
        temp_teacher['name'] = teacher['name']
        teacher_array.append(temp_teacher)

    return jsonify({'teachers': teacher_array})


@app.route("/reg-portal")
def config_reg():
    return render_template("reg_portal.html")


@app.route("/logout")
def logout():
    clear_session()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=4990, debug=True)