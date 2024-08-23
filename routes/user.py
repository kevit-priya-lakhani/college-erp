import datetime
import json
from os import access
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
)
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import jwt
from helper import authorize
from models.schema import PlainStudentSchema, LoginSchema, PlainStaffSchema
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST
from db import mongo
import re
from log_services.logger import logger  # Import your logger


blp = Blueprint("login", __name__, description="Login/logout operations")


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        if re.match(".*@.*staff.*", login_data["email"]):
            print("enter try block")
            staff = mongo.db.staff.find_one({"email": login_data["email"]})
            if staff and pbkdf2_sha256.verify(
                login_data["password"], staff["password"]
            ):
                print("logged in")
                staff_id = str(staff["_id"])
                access_token = create_access_token(identity=staff_id, fresh=True)
                refresh_token = create_refresh_token(identity=staff_id)
                return {
                    "message": "Staff logged in successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            else:
                abort(401, message="Invalid credentials")

        elif re.match(".*@.*student.*", login_data["email"]):

            student = mongo.db.students.find_one({"email": login_data["email"]})
            if student and pbkdf2_sha256.verify(
                login_data["password"], student["password"]
            ):
                student_id = str(student["_id"])
                access_token = create_access_token(identity=student_id, fresh=True)
                refresh_token = create_refresh_token(identity=student_id)
                return {
                    "message": "Student logged in successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            else:
                abort(401, message="Invalid credentials")
        return {"message": "Invalid email"}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        # logger.info("Logout POST method accessed")
        try:
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            # logger.info("User logged out successfully")
            return {"message": "Successfully logged out"}, 200
        except Exception as e:
            # logger.error(f"Error during logout: {str(e)}")
            abort(500, message="An error occurred during logout")


@blp.route("/register/student")
class StudentRegister(MethodView):
    def get(self):
        return "running"

    @jwt_required()
    @authorize(permission="staff")
    @blp.arguments(PlainStudentSchema)
    def post(self, mem_data):
        if not mongo.db.students.find_one({"email": mem_data["email"]}):
            if not mongo.db.department.find_one({"name": mem_data["dept"]}):
                abort(403, message="Forbidden, department doesn't exist")
            mem_data["created_at"] = datetime.datetime.now()
            mem_data["password"] = pbkdf2_sha256.hash(mem_data["password"])
            student_id = mongo.db.students.insert_one(mem_data).inserted_id
            student_id = json.loads(json_util.dumps(student_id))
            return {"message": "Member registered", "id": student_id}
        return {"message": "email already exists"}


@blp.route("/register/staff")
class StaffRegister(MethodView):
    def get(self):
        return "running"

    @jwt_required()
    @authorize(permission="admin")
    @blp.arguments(PlainStaffSchema)
    def post(self, mem_data):
        if re.match(".*@.*staff.*", mem_data["email"]):
            if not mongo.db.staff.find_one({"email": mem_data["email"]}):
                if not mongo.db.department.find_one({"name": mem_data["dept"]}):
                    abort(403, message="Forbidden, department doesn't exist")
                mem_data["created_at"] = datetime.datetime.now()
                mem_data["password"] = pbkdf2_sha256.hash(mem_data["password"])
                staff_id = mongo.db.staff.insert_one(mem_data).inserted_id
                staff_id = json.loads(json_util.dumps(staff_id))
                return {"message": "Member registered", "id": staff_id}
            return {"message": "email already exists"}
        return {"message": "Invalid email"}
