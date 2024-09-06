from bson import json_util, ObjectId
import json
import datetime
from db import mongo
from services.logger import logger
from flask import request
from flask_smorest import abort


def get_attendance_data():
    logger.info("Fetching all attendance records.")
    attendance_list = mongo.db.attendance.find()
    attendance_list = json.loads(json_util.dumps(attendance_list))
    logger.info("Attendance records retrieved successfully.")


def add_attendance_data():
    attendance_data = request.json
    for data in attendance_data["data"]:
        data["date"] = datetime.datetime.strptime(data["date"], f"%d-%m-%Y")
        data["student_id"] = ObjectId(data["student_id"])
        if data["date"].weekday() in (5, 6):
            logger.info("Entry not allowed on weekends.")
            abort(400, message="Entry not allowed on weekends.")
    mongo.db.attendance.insert_many(attendance_data["data"])


def get_student_attendance_list(student_id):
    logger.info(f"Fetching attendance records for student ID: {student_id}")
    attendance_list = mongo.db.attendance.find({"student_id": student_id})
    attendance_list = json.loads(json_util.dumps(attendance_list))
    logger.info(f"Attendance records retrieved for student ID: {student_id}")
    return attendance_list

def get_datewise_attendance_data(date):
    date = datetime.datetime.strptime(date, f"%Y-%m-%d").datetime()
    attendance_list = mongo.db.attendance.find(
        {"date": date}
        )
    attendance_list = json.loads(
        json_util.dumps(attendance_list)
        )
    logger.info(f"Attendance records retrieved for date: {date}")

def update_attendance_data(attendance_data,date, student_id):
    date = datetime.datetime.strptime(date, f"%d-%m-%Y")
    mongo.db.attendance.update_one({"date":date,"student_id":student_id},{'$set':{"present":attendance_data['present']}})
    logger.info("Attendance data updated successfully.")
    