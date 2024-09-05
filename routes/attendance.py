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
from helper.helper import authorize, authorizeUpdate
from schema import AttendanceSchema
from db import mongo
import re
from services.logger import logger  # Import your logger

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
        logger.info("Fetching all attendance records.")
        attendance_list = mongo.db.attendance.find()
        attendance_list = json.loads(json_util.dumps(attendance_list))
        logger.info("Attendance records retrieved successfully.")
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
            attendance_data = request.json
            for data in attendance_data['data']:
                data['date'] = datetime.datetime.strptime(data['date'], f"%d-%m-%Y")
                data['student_id']= ObjectId(data['student_id'])
                if data['date'].weekday() in (5, 6):
                    logger.info("Entry not allowed on weekends.")
                    abort(400, message="Entry not allowed on weekends.")
            # print(attendance_data['date'])
            mongo.db.attendance.insert_many(attendance_data['data'])
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
        logger.info(f"Fetching attendance records for student ID: {student_id}")
        attendance_list = mongo.db.attendance.find({"student_id": student_id})
        attendance_list = json.loads(json_util.dumps(attendance_list))
        logger.info(f"Attendance records retrieved for student ID: {student_id}")
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
            date = datetime.datetime.strptime(date, f"%Y-%m-%d").datetime()
            attendance_list = mongo.db.attendance.find(
                {"date": date}
                )
            attendance_list = json.loads(
                json_util.dumps(attendance_list)
                )
            logger.info(f"Attendance records retrieved for date: {date}")
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
            date = datetime.datetime.strptime(date, f"%d-%m-%Y")
            mongo.db.attendance.update_one({"date":date,"student_id":student_id},{'$set':{"present":attendance_data['present']}})
            logger.info("Attendance data updated successfully.")
            return {"message": "Attendance data updated successfully"}
        except Exception as e:
            logger.error(f"An error occurred while updating attendance data: {e}")
            abort(400, message=f"An exception occurred while inserting data, {e}")
