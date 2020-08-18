class Message(object):
    addStudentRecordFail = False
    updateStudentRecordFail = False
    deleteStudentRecordFail = False

    @staticmethod
    def add_student_record_fail():
        Message.addStudentRecordFail = True

    @staticmethod
    def add_student_record_success():
        Message.addStudentRecordFail = False

    @staticmethod
    def update_student_success():
        Message.updateStudentRecordFail = False

    @staticmethod
    def update_student_fail():
        Message.updateStudentRecordFail = True

    @staticmethod
    def delete_student_record_fail():
        Message.deleteStudentRecordFail = True

    @staticmethod
    def delete_student_record_success():
        Message.deleteStudentRecordFail = False