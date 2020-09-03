import uuid


class Batch(object):
    def __init__(self, prof_name, prof_id, available_seats, course_title, course_id, slot, semester, batch_id=uuid.uuid4().hex):
        self.batch_id = batch_id
        self.prof_name = prof_name
        self.prof_id = prof_id
        self.available_seats = available_seats
        self.course_title = course_title
        self.course_id = course_id
        self.semester = semester
        self.slot = slot

    def save_to_mongo(self, database):
        database["batches"].insert_one({
            "batch_id": self.batch_id,
            "course_id": self.course_id,
            "course_title": self.course_title,
            "prof_id": self.prof_id,
            "prof_name": self.prof_name,
            "available_seats": self.available_seats,
            "slot": self.slot,
            "semester": self.semester
        })
