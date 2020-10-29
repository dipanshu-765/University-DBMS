Run the Following Commands in different shell windows before running any of the flask apps otherwise
database servers won't be running.

mongod --config node1.conf (Window 1)
mongo --port 27000 (Window 2)

Now, from the window 2 enter the following commands:

use admin
db.createUser({
    user: 'temp-123',
    pwd: 'temp-123',
    roles: [{
        role:"root", db:"admin"
    }]
})

use tdu
db.createCollection("student_details")
db.createCollection("teacher_details")
db.createCollection("courses")
db.createCollection("course_registration_access")
db.createCollection("batches")
db.createCollection("teacher_slots")
db.createCollection("semester")
db.createCollection("students_semester_classes")
db.createCollection("grades")