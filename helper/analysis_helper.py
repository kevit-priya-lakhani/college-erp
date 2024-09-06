from bson import json_util, ObjectId
import json
import datetime
from db import mongo
from services.logger import logger
from flask import request
from flask_smorest import abort

def analysis_task_1():
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
                            "v": "$students_count",
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "batch": "$_id.year",
                    "totalStudents": 1,
                    "studentCount": {"$arrayToObject": "$branches"},
                }
            },
        ]
    )
    yearly_student_analytics = json.loads(json_util.dumps(yearly_student_analytics))
    logger.info("Successfully fetched year-wise student count analytics")
    return yearly_student_analytics


def analysis_task_2(data):
    data["date"] = datetime.datetime.strptime(data["date"], f"%d-%m-%Y")
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

    absent_student_analytics = mongo.db.attendance.aggregate(pipeline)
    absent_student_analytics = json.loads(json_util.dumps(absent_student_analytics))
    logger.info("Successfully fetched absentee student analytics")
    return absent_student_analytics


def analysis_task_3(data):
    data["date"] = datetime.datetime.strptime(data["date"], f"%d-%m-%Y")
    date_year = data["date"].year
    startdate = datetime.datetime(date_year, 1, 1)
    pipeline = [
        {"$match": {"date": {"$lte": data["date"], "$gte": startdate}}},
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
                "_id": {
                    "student_id": "$student_id",
                    "name": "$result.name",
                    "batch": "$result.batch",
                    "dept": "$result.dept",
                },
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

    low_attendance_analytics = mongo.db.attendance.aggregate(pipeline)
    low_attendance_analytics = json.loads(json_util.dumps(low_attendance_analytics))
    logger.info("Successfully fetched low attendance student analytics")
    return low_attendance_analytics


def analysis_task_4(data):
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
                "totalStudentsIntake": {"$sum": "$result.branches.totalStudentsIntake"},
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

    student_count_analytics = mongo.db.students.aggregate(pipeline)
    student_count_analytics = json.loads(json_util.dumps(student_count_analytics))
    logger.info(
        "Successfully fetched batch and department-wise student count analytics"
    )
    return student_count_analytics