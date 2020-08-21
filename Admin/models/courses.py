class Courses(object):
    def __init__(self, db, course_id, course_title):
        self.course_id = course_id
        self.course_title = course_title
        self.is_success = Courses.check_course_id(database=db, course_id=course_id)

    @staticmethod
    def check_course_id(database, course_id):
        temp = database["courses"].find_one({"course_id": course_id})
        if temp is None:
            return True
        else:
            return False

    def save_to_mongo(self, database):
        database["courses"].insert_one({
            "course_id": self.course_id,
            "course_title": self.course_title
        })

    @staticmethod
    def update_course(database, course_id, course_title):
        return database["courses"].update_one(
            {
                "course_id": course_id},
            {
                "$set": {
                    "course_title": course_title
                }
            }
        )

    @staticmethod
    def delete_course(database, course_id):
        return database["courses"].delete_one({"course_id": course_id})

    @staticmethod
    def check_courses(database, courses):
        for course in courses:
            temp = database["courses"].find_one({"course_id": course})
            if temp is None:
                return False
        return True
