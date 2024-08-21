from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# uncomment the following lines of code to create db
# replace with database and collection name

db= client['college-ERP']