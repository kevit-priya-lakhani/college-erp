import datetime
import json
import re
import redis
import jwt
from db import mongo
from passlib.hash import pbkdf2_sha256
from services.logger import logger
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
)
from flask_smorest import abort
from bson import json_util

def user_login(login_data):
    if re.match(".*@.*staff.*", login_data["email"]):
        staff = mongo.db.staff.find_one({"email": login_data["email"]})
        if staff and pbkdf2_sha256.verify(login_data["password"], staff["password"]):
            logger.info("Staff login successful for email: %s", login_data["email"])
            staff_id = str(staff["_id"])
            access_token = create_access_token(identity=staff_id, fresh=True)
            refresh_token = create_refresh_token(identity=staff_id)
            return {
                "message": "Staff logged in successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        else:
            logger.warning("Invalid credentials for staff with email: %s", login_data["email"])
            abort(401, message="Invalid credentials")

    elif re.match(".*@.*student.*", login_data["email"]):
        student = mongo.db.students.find_one({"email": login_data["email"]})
        if student and pbkdf2_sha256.verify(login_data["password"], student["password"]):
            logger.info("Student login successful for email: %s", login_data["email"])
            student_id = str(student["_id"])
            access_token = create_access_token(identity=student_id, fresh=True)
            refresh_token = create_refresh_token(identity=student_id)
            return {
                "message": "Student logged in successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        else:
            logger.warning("Invalid credentials for student with email: %s", login_data["email"])
            abort(401, message="Invalid credentials")


def user_logout():
    jti = get_jwt()["jti"]
    mongo.db.blacklist.insert_one({"jti":jti,"created_at":datetime.datetime.now()})
    logger.info("User logged out successfully")
    return {"msg":"Access token revoked"}
    


def register_student_data(mem_data):
    logger.info("Attempting to register student with email: %s", mem_data["email"])

    if not mongo.db.students.find_one({"email": mem_data["email"]}):
        if not mongo.db.department.find_one({"name": mem_data["dept"]}):
            logger.warning("Department does not exist: %s", mem_data["dept"])
            abort(403, message="Forbidden, department doesn't exist")

        mem_data["created_at"] = datetime.datetime.now()
        mem_data["password"] = pbkdf2_sha256.hash(mem_data["password"])
        student_id = mongo.db.students.insert_one(mem_data).inserted_id
        student_id = json.loads(json_util.dumps(student_id))
        logger.info("Student registered successfully with ID: %s", student_id)
        return {"message": "Member registered", "id": student_id}
    
    logger.warning("Email already exists: %s", mem_data["email"])
    return {"message": "email already exists"}


def register_staff_data(mem_data):
    logger.info("Attempting to register staff with email: %s", mem_data["email"])

    if re.match(".*@.*staff.*", mem_data["email"]):
        if not mongo.db.staff.find_one({"email": mem_data["email"]}):
            if not mongo.db.department.find_one({"name": mem_data["dept"]}):
                logger.warning("Department does not exist: %s", mem_data["dept"])
                abort(403, message="Forbidden, department doesn't exist")

            mem_data["created_at"] = datetime.datetime.now()
            mem_data["password"] = pbkdf2_sha256.hash(mem_data["password"])
            staff_id = mongo.db.staff.insert_one(mem_data).inserted_id
            staff_id = json.loads(json_util.dumps(staff_id))
            logger.info("Staff registered successfully with ID: %s", staff_id)
            return {"message": "Member registered", "id": staff_id}
        
        logger.warning("Email already exists: %s", mem_data["email"])
        return {"message": "email already exists"}
    
    logger.error("Invalid email format: %s", mem_data["email"])
    return {"message": "Invalid email"}

