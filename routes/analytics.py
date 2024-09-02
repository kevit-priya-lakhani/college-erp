import datetime
import json
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import jwt_required
from helper import authorize
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.schema import AttendanceSchema
from db import mongo
from log_services.logger import logger  # Import your logger

blp = Blueprint("aanlytics", __name__, description="Analytics")


@blp.route("/analytics/q1")
class AnalysisTask1(MethodView):
    @jwt_required()
    @authorize(permission="staff")
    def get(self):
        # year wise student count
        yearly_student_analytics = mongo.db.students.aggregate(
            [
                {
                    "$group": {
                        "_id": {"batch": "$batch", "dept": "$dept"},
                        "students_count": {"$count": {}},
                    }
                },
                {
                    "$group": {
                        "_id": {"year": "$_id.batch"},
                        "totalStudents": {"$sum": "$students_count"},
                        "branches": {
                            "$push": {"dept": "$_id.dept", "count": "$students_count"}
                        },
                    }
                },
            ]
        )
        yearly_student_analytics = json.loads(json_util.dumps(yearly_student_analytics))


@blp.route("/analytics/q2")
class AnalysisTask2(MethodView):
    @jwt_required()
    @authorize(permission="staff")
    def post(self):
        # absentee students
        data = request.json
        data["date"] = datetime.datetime.strptime(data["date"], f"%d-%m-%Y")
        pipeline = []
        pipeline = [
            {"$match": {"present": 0, "date": data["date"]}},
            {
                "$lookup": {
                    "from": "students",
                    "localField": "student_id",
                    "foreignField": "_id",
                    "as": "result",
                }
            },
        ]
        batch = data.get("batch", None)
        dept = data.get("dept", None)
        sem = data.get("sem", None)

        if batch:
            pipeline.append({"$match": {"result.batch": batch}})
        if dept:
            pipeline.append({"$match": {"result.dept": dept}})
        if sem:
            pipeline.append({"$match": {"result.sem": sem}})
        # print(pipeline)
        absent_student_analytics = mongo.db.attendance.aggregate(pipeline)
        absent_student_analytics = json.loads(json_util.dumps(absent_student_analytics))
        return {"yearly student analytics": list(absent_student_analytics)}


@blp.route("/analytics/q3")
class AnalysisTask1(MethodView):
    @jwt_required()
    @authorize(permission="staff")
    def post(self):
        # low attendance students
        data = request.json
        data["date"] = datetime.datetime.strptime(data["date"], f"%d-%m-%Y")
        pipeline =[
                {"$match": {"date": {"$lte": data["date"]}}},
                
                {
                "$lookup": {
                    "from": "students",
                    "localField": "student_id",
                    "foreignField": "_id",
                    "as": "result",
                }
            }
            ]
        batch = data.get("batch", None)
        dept = data.get("dept", None)
        sem = data.get("sem", None)

        if batch:
            pipeline.append({"$match": {"result.batch": batch}})
        if dept:
            pipeline.append({"$match": {"result.dept": dept}})
        if sem:
            pipeline.append({"$match": {"result.sem": sem}})
        
        pipeline= pipeline + [
            {
                    "$group": {
                        "_id": "$student_id",
                        "total_count": {"$sum": 1},
                        "present_count": {"$sum": "$present"},
                    }
                },
                {
                    "$project": {
                        "attendance": {"$divide": ["$present_count", "$total_count"]}
                    }
                },
                {"$match": {"attendance": {"$lte": 0.75}}},
                
        ]
        print(pipeline)
        low_attendance_analytics = mongo.db.attendance.aggregate(pipeline)        
        low_attendance_analytics = json.loads(json_util.dumps(low_attendance_analytics))
        return {"low attendance analytics": list(low_attendance_analytics)}
