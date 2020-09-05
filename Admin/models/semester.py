class Semester(object):
    def __init__(self, sem_id, semester, database):
        self._id = sem_id
        self.semester = semester
        self.is_id_available = self.check_id(database)

    def save_to_mongo(self, database):
        database['semester'].insert_one({
            '_id': self._id,
            'semester': self.semester
        })

    def check_id(self, database):
        return True if database['semester'].find_one({'_id': self._id}) is None else False

    @staticmethod
    def update_semester(database, id, semester):
        return database['semester'].update_one(
            {
                '_id': id
            },
            {
                '$set': {
                    'semester': semester
                }
            }
        )

    @staticmethod
    def delete_semester(database, id):
        return database['semester'].delete_one({'_id': id})