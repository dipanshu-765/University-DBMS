import hashlib
from Admin.models.courses import Courses


class Teacher(object):
    def __init__(self, prof_id, name, phone_no, address, password, courses, db):
        self._id = prof_id
        self.name = name
        self.phone_no = phone_no
        self.address = address
        self.initial_password = password
        self.courses = courses.split(',')
        self.is_success = Teacher.check_profid(prof_id=prof_id, database=db)
        self.is_course = Courses.check_courses(database=db, courses=self.courses)

    @staticmethod
    def check_profid(database, prof_id):
        temp = database["teacher_details"].find_one({"_id": prof_id})
        if temp is None:
            return True
        else:
            return False

    def save_to_mongo(self, database):
        database["teacher_details"].insert_one({
            "_id": self._id,
            "name": self.name,
            "phone_number": self.phone_no,
            "address": self.address,
            "courses": self.courses,
            "initial_password": self.initial_password,
            "current_password": str(hashlib.sha256(self.initial_password.encode()).hexdigest())
        })

    @staticmethod
    def update_teacher(database, prof_id, name, phone_no, address, courses):
        return database["teacher_details"].update_one({"_id": prof_id}, {
            "$set": {
                "name": name,
                "phone_number": phone_no,
                "address": address,
                "courses": courses
            }
        })

    @staticmethod
    def delete_teacher(database, prof_id):
        return database["teacher_details"].delete_one({"_id": prof_id})
