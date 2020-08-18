import hashlib

import pymongo


class Student(object):
    def __init__(self, reg_no, name, password, phone_no, address, father_name, mother_name, db):
        self.reg_no = reg_no
        self.name = name
        self.password = password
        self.phone_no = phone_no
        self.address = address
        self.father_name = father_name
        self.mother_name = mother_name
        self.is_success = Student.check_regno(reg_no=reg_no, database=db)

    @staticmethod
    def check_regno(database, reg_no):
        temp = database["student_details"].find_one({"registration_number": reg_no})
        if temp is None:
            return True
        else:
            return False

    def save_to_mongo(self, database):
        print(f"Added Record to {database}")
        database["student_details"].insert_one({
            "name": self.name,
            "registration_number": self.reg_no,
            "initial_password": self.password,
            "phone_number": self.phone_no,
            "address": self.address,
            "father_name": self.father_name,
            "mother_name": self.mother_name,
            "current_password": str(hashlib.sha256(self.password.encode()).hexdigest())
        })

    @staticmethod
    def update_details(database, reg_no, name, phone_no, address, father_name, mother_name):
        return database["student_details"].update_one({
            "registration_number": reg_no
        },
            {
                "$set": {
                    "name": name,
                    "phone_number": phone_no,
                    "address": address,
                    "father_name": father_name,
                    "mother_name": mother_name
                }
            })

    @staticmethod
    def delete_student(database, reg_no):
        return database["student_details"].delete_one({"registration_number": reg_no})
