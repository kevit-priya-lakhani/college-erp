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
    """
    Handles user login operations for both staff and students.
    """

    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """
        Log in a user by verifying their credentials.

        Args:
            login_data (dict): The login data containing email and password.

        Returns:
            JSON response with a success message and tokens if login is successful,
            or an error message if credentials are invalid.
        """
        logger.info("Login attempt with email: %s", login_data["email"])

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
        
        logger.error("Invalid email format: %s", login_data["email"])
        return {"message": "Invalid email"}


@blp.route("/logout")
class UserLogout(MethodView):
    """
    Handles user logout by invalidating the JWT token.
    """

    @jwt_required()
    def post(self):
        """
        Log out a user by adding their JWT ID to the blocklist.

        Returns:
            JSON response with a success message if logout is successful,
            or an error message if an exception occurs.
        """
        logger.info("Logout attempt")

        try:
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            logger.info("User logged out successfully")
            return {"message": "Successfully logged out"}, 200
        except Exception as e:
            logger.error("Error during logout: %s", str(e))
            abort(500, message="An error occurred during logout")


@blp.route("/register/student")
class StudentRegister(MethodView):
    """
    Handles student registration operations.
    """

    def get(self):
        """
        Health check for the registration endpoint.

        Returns:
            A message indicating that the endpoint is running.
        """
        return "running"

    @jwt_required()
    @authorize(permission="staff")
    @blp.arguments(PlainStudentSchema)
    def post(self, mem_data):
        """
        Register a new student.

        Args:
            mem_data (dict): The student data for registration.

        Returns:
            JSON response with a success message and student ID if registration is successful,
            or an error message if email already exists or department is invalid.
        """
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


@blp.route("/register/staff")
class StaffRegister(MethodView):
    """
    Handles staff registration operations.
    """

    def get(self):
        """
        Health check for the registration endpoint.

        Returns:
            A message indicating that the endpoint is running.
        """
        return "running"

    @jwt_required()
    @authorize(permission="admin")
    @blp.arguments(PlainStaffSchema)
    def post(self, mem_data):
        """
        Register a new staff member.

        Args:
            mem_data (dict): The staff data for registration.

        Returns:
            JSON response with a success message and staff ID if registration is successful,
            or an error message if email already exists or department is invalid.
        """
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
