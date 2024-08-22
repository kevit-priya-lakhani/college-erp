import datetime
import json
from os import access
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.schema import  StudentSchema,StudentUpdateSchema
from passlib.hash import pbkdf2_sha256
from db import mongo
import re


blp = Blueprint("student", __name__, description="Operations on students")


@blp.route("/student/<string:student_id>")
class Student(MethodView):
    @jwt_required()
    @blp.response(200,StudentSchema)
    def get(self,student_id):
        student = mongo.db.students.find_one_or_404({"_id":ObjectId(student_id)})
        student = json.loads(json_util.dumps(student))
        return {**student}
    
    @jwt_required()
    @blp.response(200, StudentSchema)
    @blp.arguments(StudentUpdateSchema)
    def put(self,student_data,student_id):
        try:
            student_data['password']= pbkdf2_sha256.hash(student_data['password'])

        except:
            pass

        finally:
            try:
                student_data['updated_at']= datetime.datetime.now()
                mongo.db.students.update_one({"_id": ObjectId(student_id)}, {'$set': student_data})
                student = mongo.db.students.find_one_or_404({"_id": ObjectId(student_id)})
                student = json.loads(json_util.dumps(student))
                return {"message": "Student updated successfully ", **student}
            except Exception as e:
                abort(401, message= f"An error occurred while updating. {e}")

    @jwt_required()
    def delete(self, student_id):
        try:
            mongo.db.students.delete_one({"_id":ObjectId(student_id)})
            return {"message": "student deleted"}
        except Exception as e:
            abort(401, message= f"An error occurred while updating. {e}")



@blp.route("/student")
class StudentList(MethodView):
    @jwt_required()
    def get(self):
        # logger.info("GET method accessed for all students")
        student_list = mongo.db.students.find()
        student_list = json.loads(json_util.dumps(student_list))
        # logger.info("All students retrieved successfully")
        return {"student_list": list(student_list)}
    



