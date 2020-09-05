import pymongo, re
from flask import Flask, render_template, request, session, make_response, redirect, url_for, jsonify
from pymongo import MongoClient
from Admin.models.student import Student
from Admin.models.teacher import Teacher
from Admin.models.database import Database
from Admin.models.courses import Courses
from Admin.models.semester import Semester
from Admin.models.message import Message
from Admin.models.batch import Batch
from Admin.models.form import AddBatchForm, StudentsAccessForm

app = Flask(__name__)
app.secret_key = "tdu"


def get_prof(course_id):
    print(f"get_prof called with {course_id}")
    return [teacher for teacher in Database.db["teacher_details"].find({'courses': course_id})]


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


@app.before_first_request
def clear_session():
    session['username'] = None


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
        return render_template("servers_down.html")
    except ValueError:
        return redirect("/")
    except IndexError:
        return redirect("/")


@app.route('/home')
def admin_dashboard():
    if session['username'] is None:
        print(session)
        return redirect("/")
    else:
        courses = Database.db["courses"].find({})
        return render_template("dashboard.html", message=Message, courses=courses, logout=logout)


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
    courses = [course for course in request.form["teacher-courses"].split(',')]
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


@app.route('/add/semester', methods=['POST'])
def add_semester():
    semester = Semester(sem_id=request.form['sem-id'], semester=request.form['semester'], database=Database.db)
    if semester.is_id_available:
        semester.save_to_mongo(database=Database.db)
    else:
        Message.add_semester_fail()
    return redirect("/")


@app.route('/update/semester', methods=['POST'])
def update_semester():
    if Semester.update_semester(database=Database.db, id=request.form['sem-id'],
                                semester=request.form['semester']).matched_count != 1:
        Message.update_semester_fail()
    return redirect("/")


@app.route('/delete/semester', methods=['POST'])
def delete_semester():
    if Semester.delete_semester(database=Database.db, id=request.form['sem-id']).deleted_count != 1:
        Message.delete_semester_fail()
    return redirect("/")


@app.route('/add/batch', methods=['POST', 'GET'])
def add_batch():
    courses = [course for course in Database.db["courses"].find({})]
    teachers = get_prof(course_id=courses[0]['_id'])
    semesters = [semester for semester in Database.db["semester"].find({})]
    form = AddBatchForm(courses=courses)
    form.course.choices = [(course['_id'], course['course_title']) for course in courses]
    form.teacher.choices = [(teacher['_id'], teacher['name']) for teacher in teachers]
    form.semester.choices = [(semester['_id'], semester['semester']) for semester in semesters]
    if request.method == 'GET':
        return render_template("add_batch.html", form=form)
    else:
        is_slot_available = True

        prof_id = request.form['teacher']
        prof_name = Database.db['teacher_details'].find_one({'_id': prof_id})['name']
        course_id = request.form['course']
        course_title = Database.db['courses'].find_one({'_id': course_id})['course_title']
        available_seats = request.form['seats']
        semester_id = request.form['semester']
        slot = request.form['slot']
        temp = Database.db["teacher_slots"].find({'semester_id': semester_id, 'teacher': prof_id})
        for t in temp:
            temp_slot = t['slot']
            if slot in clashing_slots.get(temp_slot, []):
                is_slot_available = False

        if is_slot_available:
            Batch(prof_id=prof_id, prof_name=prof_name, course_id=course_id, course_title=course_title,
                  available_seats=available_seats, slot=slot, semester=semester_id).save_to_mongo(database=Database.db)
            Database.db["teacher_slots"].insert_one({
                'semester_id': request.form['semester'],
                'teacher': request.form['teacher'],
                'slot': request.form['slot']
            })
        else:
            Message.add_batch_fail()

        return redirect("/")


@app.route('/teacher/<course_id>')
def teacher_state(course_id):
    if session['username'] is None:
        return redirect('/')
    teacher_array = []
    teachers = Database.db["teacher_details"].find({'courses': course_id})
    for teacher in teachers:
        temp_teacher = dict()
        temp_teacher['_id'] = teacher['_id']
        temp_teacher['name'] = teacher['name']
        teacher_array.append(temp_teacher)

    return jsonify({'teachers': teacher_array})


@app.route("/reg-portal", methods=['POST', 'GET'])
def config_reg():
    form = StudentsAccessForm()
    form.semester.choices = [(semester['_id'], semester['semester']) for semester in Database.db["semester"].find({})]
    if request.method == 'GET':
        return render_template("reg_portal.html", form=form)
    else:
        students_list = request.files['students']
        students = []
        if students_list.filename.split('.')[len(students_list.filename.split('.'))-1] != "txt":
            Message.valid_file_upload_fail()
        else:
            for line in students_list.readlines():
                reg_nums = re.search(pattern="[0-9]{2}[A-Z]{3}[0-9]{4}", string=line.decode("UTF-8"))
                if reg_nums:
                    students.append(reg_nums.group())
            semester = request.form['semester']
            Database.db["course_registration_access"].update_one(
                {
                    'semester': semester
                },
                {
                    '$set': {
                        'students_allowed': list(set(
                            students + Database.db["course_registration_access"].find_one(
                                {
                                    'semester': semester
                                }
                            )['students_allowed'] if Database.db["course_registration_access"].find_one(
                                {
                                    'semester': semester
                                }
                            ) is not None else students))
                    }
                },
                upsert=True
            )
        return redirect("/")


@app.route("/logout")
def logout():
    clear_session()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=4990, debug=True)

