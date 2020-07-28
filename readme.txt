Run the Following Commands in different shell windows before running any of the flask apps otherwise
database servers won't be running.

mongod --config node1.conf (Window 1)
mongod --config node2.conf (Window 2)
mongod --config node3.conf (Window 3)

mongo --port 27000 (Window 4)
mongo --port 27001 (Window 5)
mongo --port 27002 (Window 6)

Now, go to Window 4 and enter the following commands:

rs.initiate()
use admin
db.createUser({
    user: 'temp-123',
    pwd: 'temp-123',
    roles: [{
        role:"root", db:"admin"
    }]
})

exit
mongo --host "DBMS/127.0.0.1:27000" -u "temp-123" -p "temp-123" --authenticationDatabase "admin"
rs.initiate()
rs.add("127.0.0.1:27001")
rs.add("127.0.0.1:27002")
