# reference from: https://www.yiibai.com/mongodb/mongodb_python.html

from pymongo import MongoClient
client = MongoClient("mongodb+srv://mengjq:OXDueFslVZNWtiqT@assignmentsubmmsion.nttaj.mongodb.net/?retryWrites=true&w=majority")
db = client.assignment
collection = db.submissions
print(collection['1909'])
print(client['assignmentInfo']['1909'].name)
