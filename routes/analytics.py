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
                            "$push": {
                                "k": "$_id.dept",
                                "v": {"studentCount": "$students_count"},
                            }
                        },
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "batch": "$_id.year",
                        "totalStudents": 1,
                        "branches": {"$arrayToObject": "$branches"},
                    }
                },
            ]
        )
        yearly_student_analytics = json.loads(json_util.dumps(yearly_student_analytics))
        return {"yearly student analytics": list(yearly_student_analytics)}


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
            {"$unwind": {"path": "$result"}},
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
        pipeline.append(
            {
                "$project": {
                    "date": 1,
                    "name": "$result.name",
                    "sem": "$result.sem",
                    "branch": "$result.dept",
                    "batch": "$result.batch",
                    "email": "$result.email",
                    "student_id": 1,
                    "present": 1,
                    "_id": 0,
                }
            }
        )
        print(pipeline)

        absent_student_analytics = mongo.db.attendance.aggregate(pipeline)
        absent_student_analytics = json.loads(json_util.dumps(absent_student_analytics))
        return {"absent student analytics": list(absent_student_analytics)}


@blp.route("/analytics/q3")
class AnalysisTask3(MethodView):
    @jwt_required()
    @authorize(permission="staff")
    def post(self):
        # low attendance students
        data = request.json
        data["date"] = datetime.datetime.strptime(data["date"], f"%d-%m-%Y")
        pipeline = [
            {"$match": {"date": {"$lte": data["date"]}}},
            {
                "$lookup": {
                    "from": "students",
                    "localField": "student_id",
                    "foreignField": "_id",
                    "as": "result",
                }
            },
            {"$unwind": {"path": "$result"}},
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

        pipeline = pipeline + [
            {
                "$group": {
                    "_id": {"student_id": "$student_id", "name": "$result.name"},
                    "total_count": {"$sum": 1},
                    "present_count": {"$sum": "$present"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "student_details": "$_id",
                    "attendance": {"$divide": ["$present_count", "$total_count"]},
                }
            },
            {"$match": {"attendance": {"$lte": 0.75}}},
        ]
        print(pipeline)
        low_attendance_analytics = mongo.db.attendance.aggregate(pipeline)
        low_attendance_analytics = json.loads(json_util.dumps(low_attendance_analytics))
        return {"low attendance analytics": list(low_attendance_analytics)}


@blp.route("/analytics/q4")
class AnalysisTask4(MethodView):
    @jwt_required()
    @authorize(permission="staff")
    def post(self):
        # batch and dept wise student count
        data = request.json
        pipeline = [
            {
                "$group": {
                    "_id": {"batch": "$batch", "branch": "$dept"},
                    "studentCount": {"$sum": 1},
                }
            },
            {
                "$lookup": {
                    "from": "batches",
                    "localField": "_id.batch",
                    "foreignField": "year",
                    "as": "result",
                }
            },
            {"$unwind": {"path": "$result"}},
            {"$unwind": {"path": "$result.branches"}},
            {"$match": {"$expr": {"$eq": ["$_id.branch", "$result.branches.name"]}}},
            {
                "$group": {
                    "_id": "$_id.batch",
                    "branches": {
                        "$push": {
                            "k": "$_id.branch",
                            "v": {
                                "totalStudents": "$studentCount",
                                "totalStudentsIntake": "$result.branches.totalStudentsIntake",
                                "availableIntake": {
                                    "$subtract": [
                                        "$result.branches.totalStudentsIntake",
                                        "$studentCount",
                                    ]
                                },
                            },
                        }
                    },
                    "totalStudents": {"$sum": "$studentCount"},
                    "totalStudentsIntake": {
                        "$sum": "$result.branches.totalStudentsIntake"
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "batch": "$_id",
                    "totalStudents": 1,
                    "totalStudentsIntake": 1,
                    "availableIntake": {
                        "$subtract": ["$totalStudentsIntake", "$totalStudents"]
                    },
                    "branches": {"$arrayToObject": "$branches"},
                }
            },
        ]

        batch = data.get("batch", None)
        dept = data.get("dept", None)

        if batch:
            pipeline.append({"$match": {"batch": batch}})
        # if dept:
        #     pipeline.append({"$match": {"result.dept": dept}})

        print("pipeline", pipeline)
        student_count_analytics = mongo.db.students.aggregate(pipeline)
        # explanation = student_count_analytics.explain()
        # print('explain:',explanation)
        student_count_analytics = json.loads(json_util.dumps(student_count_analytics))
        return {"student count analytics": list(student_count_analytics)}
