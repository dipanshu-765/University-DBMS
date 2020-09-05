class Message(object):
    addStudentRecordFail = False
    addTeacherRecordFail = False
    addCourseFail = False
    courseFoundFail = False
    updateStudentRecordFail = False
    updateTeacherRecordFail = False
    updateCourseFail = False
    deleteStudentRecordFail = False
    deleteTeacherRecordFail = False
    deleteCourseFail = False
    addSemesterFail = False
    updateSemesterFail = False
    deleteSemesterFail = False
    addBatchFail = False
    validFileUpload = True

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

    @staticmethod
    def add_course_success():
        Message.addCourseFail = False

    @staticmethod
    def add_course_fail():
        Message.addCourseFail = True

    @staticmethod
    def update_course_success():
        Message.updateCourseFail = False

    @staticmethod
    def update_course_fail():
        Message.updateCourseFail = True

    @staticmethod
    def delete_course_success():
        Message.deleteCourseFail = False

    @staticmethod
    def delete_course_fail():
        Message.deleteCourseFail = True

    @staticmethod
    def course_found_fail():
        Message.courseFoundFail = True

    @staticmethod
    def course_found_success():
        Message.courseFoundFail = False

    @staticmethod
    def add_batch_success():
        Message.addBatchFail = False

    @staticmethod
    def add_batch_fail():
        Message.addBatchFail = True

    @staticmethod
    def valid_file_upload_success():
        Message.validFileUpload = True

    @staticmethod
    def valid_file_upload_fail():
        Message.validFileUpload = False

    @staticmethod
    def add_semester_fail():
        Message.addSemesterFail = True

    @staticmethod
    def add_semester_success():
        Message.addSemesterFail = False

    @staticmethod
    def update_semester_fail():
        Message.updateSemesterFail = True

    @staticmethod
    def update_semester_success():
        Message.updateSemesterFail = False

    @staticmethod
    def delete_semester_fail():
        Message.deleteSemesterFail = True

    @staticmethod
    def delete_semester_success():
        Message.deleteSemesterFail = False
