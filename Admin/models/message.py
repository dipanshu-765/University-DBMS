class Message(object):
    addStudentRecordFail = False
    addTeacherRecordFail = False
    updateStudentRecordFail = False
    updateTeacherRecordFail = False
    deleteStudentRecordFail = False
    deleteTeacherRecordFail = False

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

    @staticmethod
    def add_teacher_record_fail():
        Message.addTeacherRecordFail = True

    @staticmethod
    def add_teacher_record_success():
        Message.addTeacherRecordFail = False

    @staticmethod
    def update_teacher_record_fail():
        Message.updateTeacherRecordFail = True

    @staticmethod
    def update_teacher_record_success():
        Message.updateTeacherRecordFail = False

    @staticmethod
    def delete_teacher_record_success():
        Message.deleteTeacherRecordFail = False

    @staticmethod
    def delete_teacher_record_fail():
        Message.deleteTeacherRecordFail = True
