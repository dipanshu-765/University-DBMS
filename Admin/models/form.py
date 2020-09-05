from flask_wtf import FlaskForm
from wtforms import SelectField


class AddBatchForm(FlaskForm):
    semester = SelectField(label="Semester", choices=[])
    course = SelectField(label="Course", choices=[])
    teacher = SelectField(label="Teacher", choices=[])
    slot = SelectField(label="Slot",
                       choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2'),
                                ('D1', 'D1'), ('D2', 'D2'), ('E1', 'E1'),
                                ('E2', 'E2'), ('F1', 'F1'), ('F2', 'F2'), ('L1', 'L1'), ('L2', 'L2'),
                                ('L3', 'L3'), ('L4', 'L4'), ('L5', 'L5'), ('L6', 'L6'),
                                ('L7', 'L7'), ('L8', 'L8'), ('L9', 'L9'), ('L10', 'L10')])


class StudentsAccessForm(FlaskForm):
    semester = SelectField(label="Semester", choices=[])
