import datetime
import json
from bson import ObjectId, json_util
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from passlib.hash import pbkdf2_sha256
from db import mongo
from models.schema import StudentSchema, StudentUpdateSchema
from helper import authorize
from log_services.logger import logger  # Import your logger

blp = Blueprint("student", __name__, description="Operations on students")


@blp.route("/student/<string:student_id>")
class Student(MethodView):
    """
    A resource class for handling operations on individual students.

    Methods:
        get: Retrieves a specific student by their ID.
        put: Updates a specific student's details by their ID.
        delete: Deletes a specific student by their ID.
    """

    @jwt_required()
    @blp.response(200, StudentSchema)
    def get(self, student_id):
        """
        Retrieve a specific student's details by their ID.

        Args:
            student_id (str): The ID of the student.

        Returns:
            A JSON object containing the student's details.
        """
        logger.info(f"Fetching student with ID: {student_id}")
        try:
            student = mongo.db.students.find_one_or_404({"_id": ObjectId(student_id)})
            student = json.loads(json_util.dumps(student))
            logger.info(f"Student with ID: {student_id} retrieved successfully.")
            return {**student}
        except Exception as e:
            logger.error(f"Error fetching student with ID: {student_id}: {e}")
            abort(404, message=f"Student not found: {e}")

    @jwt_required()
    @authorize(permission="staff")
    @blp.response(200, StudentSchema)
    @blp.arguments(StudentUpdateSchema)
    def put(self, student_data, student_id):
        """
        Update a specific student's details by their ID.

        Args:
            student_data (dict): The updated data for the student.
            student_id (str): The ID of the student to update.

        Returns:
            A JSON object with a success message and the updated student details.

        Raises:
            401 Unauthorized: If an error occurs during the update process.
        """
        logger.info(f"Attempting to update student with ID: {student_id}")
        try:
            if 'password' in student_data:
                student_data['password'] = pbkdf2_sha256.hash(student_data['password'])

            student_data['updated_at'] = datetime.datetime.now()
            mongo.db.students.update_one({"_id": ObjectId(student_id)}, {'$set': student_data})
            student = mongo.db.students.find_one_or_404({"_id": ObjectId(student_id)})
            student = json.loads(json_util.dumps(student))
            logger.info(f"Student with ID: {student_id} updated successfully.")
            return {"message": "Student updated successfully", **student}
        except Exception as e:
            logger.error(f"Error updating student with ID: {student_id}: {e}")
            abort(401, message=f"An error occurred while updating. {e}")

    @jwt_required()
    @authorize(permission="staff")
    def delete(self, student_id):
        """
        Delete a specific student by their ID.

        Args:
            student_id (str): The ID of the student to delete.

        Returns:
            A JSON object with a success message.

        Raises:
            401 Unauthorized: If an error occurs during the deletion process.
        """
        logger.info(f"Attempting to delete student with ID: {student_id}")
        try:
            mongo.db.students.delete_one({"_id": ObjectId(student_id)})
            logger.info(f"Student with ID: {student_id} deleted successfully.")
            return {"message": "Student deleted"}
        except Exception as e:
            logger.error(f"Error deleting student with ID: {student_id}: {e}")
            abort(401, message=f"An error occurred while deleting. {e}")


@blp.route("/student")
class StudentList(MethodView):
    """
    A resource class for handling operations on the list of students.

    Methods:
        get: Retrieves a list of all students.
    """

    @jwt_required()
    def get(self):
        """
        Retrieve a list of all students.

        Returns:
            A JSON object containing a list of all students.
        """
        logger.info("Fetching all students.")
        try:
            student_list = mongo.db.students.find()
            student_list = json.loads(json_util.dumps(student_list))
            logger.info("All students retrieved successfully.")
            return {"student_list": list(student_list)}
        except Exception as e:
            logger.error(f"Error fetching all students: {e}")
            abort(404, message=f"An error occurred while fetching students. {e}")
