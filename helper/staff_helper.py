from services.logger import logger
from db import mongo
import json
from bson import ObjectId, json_util
import datetime
from passlib.hash import pbkdf2_sha256

def get_staff_data(staff_id):
    staff = mongo.db.staff.find_one_or_404({"_id": ObjectId(staff_id)})
    staff = json.loads(json_util.dumps(staff))
    logger.info(f"Staff member with ID: {staff_id} retrieved successfully.")
    return staff

def update_staff_data(staff_id,staff_data):
    if 'password' in staff_data:
        staff_data['password'] = pbkdf2_sha256.hash(staff_data['password'])
    staff_data['updated_at'] = datetime.datetime.now()
    mongo.db.staff.update_one({"_id": ObjectId(staff_id)}, {'$set': staff_data})
    staff = mongo.db.staff.find_one_or_404({"_id": ObjectId(staff_id)})
    staff = json.loads(json_util.dumps(staff))
    logger.info(f"Staff member with ID: {staff_id} updated successfully.")
    return {"message": "Member updated successfully", **staff}

def delete_staff_data(staff_id):
    mongo.db.staff.delete_one({"_id": ObjectId(staff_id)})
    logger.info(f"Staff member with ID: {staff_id} deleted successfully.")
    return {"message": "Staff deleted"}

def get_staff_list():
    staff_list = mongo.db.staff.find()
    staff_list = json.loads(json_util.dumps(staff_list))
    logger.info("All staff members retrieved successfully.")
    return staff_list