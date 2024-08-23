import datetime
from email import message
import json
from os import access
from bson import json_util
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from helper import authorize
from models.schema import DepartmentSchema
from passlib.hash import pbkdf2_sha256
from db import mongo
import re
from log_services.logger import logger  # Import your logger

blp = Blueprint("department", __name__, description="Operations on department")


@blp.route("/")
class Index(MethodView):
    def get(self):
        return "App is running..."

    
@blp.route("/department/<string:department_name>")
class department(MethodView):    
    @jwt_required()
    @authorize(permission= "staff")
    @blp.response(200,DepartmentSchema)
    def get(self,department_name):
        department = mongo.db.department.find_one_or_404({"name":(department_name)})
        department = json.loads(json_util.dumps(department))
        return {**department}
    
    @jwt_required()
    @authorize(permission= "admin")
    @blp.response(200, DepartmentSchema)
    @blp.arguments(DepartmentSchema)
    def put(self,department_data,department_name):
        try:
            department_data['updated_at']= datetime.datetime.now()
            mongo.db.department.update_one({"name": (department_name)}, {'$set': department_data})
            mongo.db.staff.update_many({"dept":department_name},{'$set':{"dept":department_data['name']}})
            mongo.db.student.update_many({"dept":department_name},{'$set':{"dept":department_data['name']}})
            department = mongo.db.department.find_one_or_404({"name": (department_name)})
            department = json.loads(json_util.dumps(department))
            return {"message": "Department updated successfully ", **department}
        except Exception as e:
            abort(401, message= f"An error occurred while updating. {e}")

    @jwt_required()
    @authorize(permission= "admin")
    def delete(self, department_name):
        try:
            if mongo.db.student.find_one({'dept':department_name}) or mongo.db.student.find_one({'dept':department_name}):
                abort(403, message= f"Forbidden. Department exists in student/staff data")
            mongo.db.department.delete_one({"name":(department_name)})
            return {"message": "Department deleted"}
        except Exception as e:
            abort(401, message= f"An error occurred while deleting. {e}")



@blp.route("/department")
class DepartmentList(MethodView):
    @jwt_required()
    @authorize(permission= "staff")
    def get(self):
        # logger.info("GET method accessed for all departments")
        department_list = mongo.db.department.find()
        department_list = json.loads(json_util.dumps(department_list))
        # logger.info("All departments retrieved successfully")
        return {"department_list": list(department_list)}
    
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
            
            department_data['created_at']= datetime.datetime.now()
            print(department_data['created_at'])
            mongo.db.department.insert_one(department_data)
            logger.info("Department data added successfully.")
            return {"message": "Department data added successfully"}
        except Exception as e:
            logger.error(f"An error occurred while inserting department data: {e}")
            abort(400, message=f"An exception occurred while inserting data, {e}")



