import datetime
from email import message
from importlib.metadata import MetadataPathFinder
import json
from os import access
import trace
from bson import ObjectId, json_util
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from helper.authorize_helper import authorize, authorizeUpdate
from schema.attendance import AttendanceSchema
from db import mongo
import re
from services.logger import logger  # Import your logger
from helper.attendance_helper import *
blp = Blueprint("attendance", __name__, description="Operations on attendance")

@blp.route("/attendance")
class Attendance(MethodView):
    """
    A resource class for handling operations on attendance records.

    Methods:
        get: Retrieves all attendance records.
        post: Adds a new attendance record.
    """
    
    @jwt_required()
    @authorize(permission="staff")
    def get(self):
        """
        Retrieve all attendance records from the database.
        
        Returns:
            A JSON object containing a list of all attendance records.
        """
        attendance_list = get_attendance_data()
        return {"attendance": list(attendance_list)}
    
    @jwt_required()
    @authorize(permission="admin")
    # @blp.arguments(AttendanceSchema)
    def post(self):
        """
        Add a new attendance record to the database.

        Args:
            attendance_data (dict): The data for the new attendance record.

        Returns:
            A JSON object with a success message.
        
        Raises:
            400 Bad Request: If an exception occurs during the insertion.
        """
        logger.info("Attempting to add new attendance data.")
        try:
            add_attendance_data()
            logger.info("Attendance data added successfully.")
            return {"message": "Attendance data added successfully"}
        except Exception as e:
            logger.error(f"An error occurred while inserting attendance data: {e}")
            abort(400, message=f"An exception occurred while inserting data, {e}")

@blp.route("/attendance/<string:student_id>")
class AttendanceStudent(MethodView):
    """
    A resource class for handling operations on attendance records by student ID.

    Methods:
        get: Retrieves attendance records for a specific student.
    """
    
    @jwt_required()
    @authorize(permission="admin")
    def get(self, student_id):
        """
        Retrieve attendance records for a specific student.

        Args:
            student_id (str): The ID of the student.

        Returns:
            A JSON object containing a list of attendance records for the student.
        """
        attendance_list = get_student_attendance_list(student_id)
        return {"attendance": list(attendance_list)}
    

@blp.route("/attendance/<string:date>")
class AttendanceDate(MethodView):
    """
    A resource class for handling operations on attendance records by date.

    Methods:
        get: Retrieves attendance records for a specific date.
    """
    
    @jwt_required()
    @authorize(permission="admin")
    def get(self, date):
        """
        Retrieve attendance records for a specific date.

        Args:
            date (str): The date in the format 'YYYY-MM-DD'.

        Returns:
            A JSON object containing a list of attendance records for the date.
        """
        logger.info(f"Fetching attendance records for date: {date}")
        try:
            attendance_list = get_datewise_attendance_data(date)
            return {"attendance": list(attendance_list)}
        except Exception as e:
            logger.error(f"An error occurred while fetching attendance data for date {date}: {e}")
            abort(400, message=f"An error occurred while fetching attendance data for date {date}. {e}")



@jwt_required()
@blp.route("/attendance/<string:date>/<string:student_id>")
class AttendanceUpdate(MethodView):
    @blp.arguments(AttendanceSchema)
    def put(self,attendance_data,date, student_id):
        try:
            update_attendance_data(attendance_data,date,student_id)
            return {"message": "Attendance data updated successfully"}
        except Exception as e:
            logger.error(f"An error occurred while updating attendance data: {e}")
            abort(400, message=f"An exception occurred while inserting data, {e}")
