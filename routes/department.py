import datetime
from email import message
import json
from os import access
from bson import json_util
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from helper.helper import authorize
from schema import DepartmentSchema
from passlib.hash import pbkdf2_sha256
from db import mongo
import re
from services.logger import logger  # Import your logger

blp = Blueprint("department", __name__, description="Operations on department")

@blp.route("/")
class Index(MethodView):
    """
    A simple index route to check if the application is running.
    
    Methods:
        get: Returns a string indicating that the application is running.
    """

    def get(self):
        """
        Return a message indicating that the application is running.
        
        Returns:
            A string message.
        """
        logger.info("Index route accessed - App is running.")
        return "App is running..."

    
@blp.route("/department/<string:department_name>")
class Department(MethodView):
    """
    A resource class for handling operations on individual departments.

    Methods:
        get: Retrieves a specific department by its name.
        put: Updates a specific department's details by its name.
        delete: Deletes a specific department by its name.
    """

    @jwt_required()
    @authorize(permission="staff")
    @blp.response(200, DepartmentSchema)
    def get(self, department_name):
        """
        Retrieve a specific department's details by its name.

        Args:
            department_name (str): The name of the department.

        Returns:
            A JSON object containing the department's details.
        """
        logger.info(f"Fetching department with name: {department_name}")
        try:
            department = mongo.db.department.find_one_or_404({"name": department_name})
            department = json.loads(json_util.dumps(department))
            logger.info(f"Department with name: {department_name} retrieved successfully.")
            return {**department}
        except Exception as e:
            logger.error(f"Error fetching department with name: {department_name}: {e}")
            abort(404, message=f"Department not found: {e}")
    
    @jwt_required()
    @authorize(permission="admin")
    @blp.response(200, DepartmentSchema)
    @blp.arguments(DepartmentSchema)
    def put(self, department_data, department_name):
        """
        Update a specific department's details by its name.

        Args:
            department_data (dict): The updated data for the department.
            department_name (str): The name of the department to update.

        Returns:
            A JSON object with a success message and the updated department details.

        Raises:
            401 Unauthorized: If an error occurs during the update process.
        """
        logger.info(f"Attempting to update department with name: {department_name}")
        try:
            department_data['updated_at'] = datetime.datetime.now()
            mongo.db.department.update_one({"name": department_name}, {'$set': department_data})
            mongo.db.staff.update_many({"dept": department_name}, {'$set': {"dept": department_data['name']}})
            mongo.db.student.update_many({"dept": department_name}, {'$set': {"dept": department_data['name']}})
            department = mongo.db.department.find_one_or_404({"name": department_name})
            department = json.loads(json_util.dumps(department))
            logger.info(f"Department with name: {department_name} updated successfully.")
            return {"message": "Department updated successfully", **department}
        except Exception as e:
            logger.error(f"Error updating department with name: {department_name}: {e}")
            abort(401, message=f"An error occurred while updating. {e}")

    @jwt_required()
    @authorize(permission="admin")
    def delete(self, department_name):
        """
        Delete a specific department by its name.

        Args:
            department_name (str): The name of the department to delete.

        Returns:
            A JSON object with a success message.

        Raises:
            401 Unauthorized: If an error occurs during the deletion process.
            403 Forbidden: If the department is associated with existing student or staff data.
        """
        logger.info(f"Attempting to delete department with name: {department_name}")
        try:
            if mongo.db.student.find_one({'dept': department_name}) or mongo.db.staff.find_one({'dept': department_name}):
                logger.warning(f"Deletion forbidden. Department {department_name} exists in student/staff data.")
                abort(403, message=f"Forbidden. Department exists in student/staff data")
            mongo.db.department.delete_one({"name": department_name})
            logger.info(f"Department with name: {department_name} deleted successfully.")
            return {"message": "Department deleted"}
        except Exception as e:
            logger.error(f"Error deleting department with name: {department_name}: {e}")
            abort(401, message=f"An error occurred while deleting. {e}")


@blp.route("/department")
class DepartmentList(MethodView):
    """
    A resource class for handling operations on the list of departments.

    Methods:
        get: Retrieves a list of all departments.
        post: Adds a new department to the database.
    """

    @jwt_required()
    @authorize(permission="staff")
    def get(self):
        """
        Retrieve a list of all departments.

        Returns:
            A JSON object containing a list of all departments.
        """
        logger.info("Fetching all departments.")
        try:
            department_list = mongo.db.department.find()
            department_list = json.loads(json_util.dumps(department_list))
            logger.info("All departments retrieved successfully.")
            return {"department_list": list(department_list)}
        except Exception as e:
            logger.error(f"Error fetching all departments: {e}")
            abort(404, message=f"An error occurred while fetching departments. {e}")

    @jwt_required()
    @authorize(permission="admin")
    @blp.arguments(DepartmentSchema)
    def post(self, department_data):
        """
        Add a new department record to the database.

        Args:
            department_data (dict): The data for the new department record.

        Returns:
            A JSON object with a success message.

        Raises:
            400 Bad Request: If an exception occurs during the insertion.
        """
        logger.info("Attempting to add new department data.")
        try:
            department_data['created_at'] = datetime.datetime.now()
            print(department_data['created_at'])
            mongo.db.department.insert_one(department_data)
            logger.info("Department data added successfully.")
            return {"message": "Department data added successfully"}
        except Exception as e:
            logger.error(f"An error occurred while inserting department data: {e}")
            abort(400, message=f"An exception occurred while inserting data, {e}")
