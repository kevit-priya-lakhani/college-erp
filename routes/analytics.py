import datetime
import json
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import jwt_required
from helper.authorize_helper import authorize
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import mongo
from services.logger import logger  # Import your logger
from helper.analysis_helper import *


blp = Blueprint("analytics", __name__, description="Analytics")

@blp.route("/analytics/q1")
class AnalysisTask1(MethodView):
    """
    Endpoint to retrieve year-wise student count analytics.
    
    This endpoint returns the total number of students for each batch year,
    along with the student count in each department.
    """
    @jwt_required()
    @authorize(permission="staff")
    def get(self):
        logger.info("Fetching year-wise student count analytics")
        try:
            yearly_student_analytics = analysis_task_1()
            return {"yearly student analytics": list(yearly_student_analytics)}
        except Exception as e:
            logger.error(f"Error fetching year-wise student count analytics: {e}")
            abort(500, message="Internal Server Error")

@blp.route("/analytics/q2")
class AnalysisTask2(MethodView):
    """
    Endpoint to retrieve absentee students analytics.
    
    This endpoint returns the list of students who were absent on a given date,
    filtered by optional batch, department, and semester criteria.
    """
    @jwt_required()
    @authorize(permission="staff")
    def post(self):
        logger.info("Fetching absentee student analytics")
        data = request.json
        try:
            absent_student_analytics = analysis_task_2(data)
            return {"absent student analytics": list(absent_student_analytics)}
        except Exception as e:
            logger.error(f"Error fetching absentee student analytics: {e}")
            abort(500, message="Internal Server Error")

@blp.route("/analytics/q3")
class AnalysisTask3(MethodView):
    """
    Endpoint to retrieve low attendance student analytics.
    
    This endpoint returns the list of students with attendance below 75% up to a specified date,
    filtered by optional batch, department, and semester criteria.
    """
    @jwt_required()
    @authorize(permission="staff")
    def post(self):
        logger.info("Fetching low attendance student analytics")
        data = request.json
        try:
            low_attendance_analytics = analysis_task_3(data)
            return {"low attendance analytics": list(low_attendance_analytics)}
        except Exception as e:
            logger.error(f"Error fetching low attendance student analytics: {e}")
            abort(500, message="Internal Server Error")

@blp.route("/analytics/q4")
class AnalysisTask4(MethodView):
    """
    Endpoint to retrieve batch and department-wise student count analytics.
    
    This endpoint returns the student count per batch and department,
    including the available intake and total students intake.
    """
    @jwt_required()
    @authorize(permission="staff")
    def post(self):
        logger.info("Fetching batch and department-wise student count analytics")
        data = request.json
        try:
            student_count_analytics= analysis_task_4(data)
            return {"student count analytics": list(student_count_analytics)}
        except Exception as e:
            logger.error(f"Error fetching batch and department-wise student count analytics: {e}",exc_info=True)
            abort(500, message="Internal Server Error")
