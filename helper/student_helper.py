from services.logger import logger
from db import mongo
import json
from bson import ObjectId, json_util
import datetime
from passlib.hash import pbkdf2_sha256

def get_student_data(student_id):
    student = mongo.db.students.find_one_or_404({"_id": ObjectId(student_id)})
    student = json.loads(json_util.dumps(student))
    logger.info(f"Student with ID: {student_id} retrieved successfully.")
    return student

def update_student_data(student_id,student_data):
    if 'password' in student_data:
        student_data['password'] = pbkdf2_sha256.hash(student_data['password'])
    student_data['updated_at'] = datetime.datetime.now()
    mongo.db.students.update_one({"_id": ObjectId(student_id)}, {'$set': student_data})
    student = mongo.db.students.find_one_or_404({"_id": ObjectId(student_id)})
    student = json.loads(json_util.dumps(student))
    logger.info(f"Student with ID: {student_id} updated successfully.")
    return student

def delete_student_details(student_id):
    mongo.db.students.delete_one({"_id": ObjectId(student_id)})
    logger.info(f"Student with ID: {student_id} deleted successfully.")

def get_student_list():
    student_list = mongo.db.students.find()
    student_list = json.loads(json_util.dumps(student_list))
    logger.info("All students retrieved successfully.")
    return student_list