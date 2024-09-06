from db import mongo
from services.logger import logger
import json
from bson import json_util
import datetime
from flask_smorest import abort

def get_department_data(department_name):
    department = mongo.db.department.find_one_or_404({"name": department_name})
    department = json.loads(json_util.dumps(department))
    logger.info(f"Department with name: {department_name} retrieved successfully.")

def update_department_data(department_name,department_data):
    department_data['updated_at'] = datetime.datetime.now() 
    mongo.db.department.update_one({"name": department_name}, {'$set': department_data})
    mongo.db.staff.update_many({"dept": department_name}, {'$set': {"dept": department_data['name']}})
    mongo.db.student.update_many({"dept": department_name}, {'$set': {"dept": department_data['name']}})
    department = mongo.db.department.find_one_or_404({"name": department_name})
    department = json.loads(json_util.dumps(department))
    logger.info(f"Department with name: {department_name} updated successfully.")
    return department_data

def delete_department_data(department_name):
    if mongo.db.student.find_one({'dept': department_name}) or mongo.db.staff.find_one({'dept': department_name}):
        logger.warning(f"Deletion forbidden. Department {department_name} exists in student/staff data.")
        abort(403, message=f"Forbidden. Department exists in student/staff data")
    mongo.db.department.delete_one({"name": department_name})
    logger.info(f"Department with name: {department_name} deleted successfully.")
    
def get_department_list():
    department_list = mongo.db.department.find()
    department_list = json.loads(json_util.dumps(department_list))
    logger.info("All departments retrieved successfully.")
    return department_list

def create_department(department_data):
    department_data['created_at'] = datetime.datetime.now()
    print(department_data['created_at'])
    mongo.db.department.insert_one(department_data)
    logger.info("Department data added successfully.")
        

