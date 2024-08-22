import datetime
from email import message
import json
from os import access
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.schema import  StaffSchema,StaffUpdateSchema
from passlib.hash import pbkdf2_sha256
from db import mongo
import re
# from log_services.logger import logger  # Import your logger

blp = Blueprint("staff", __name__, description="Operations on staff")


@blp.route("/")
class Index(MethodView):
    def get(self):
        return "App is running..."

@blp.route("/staff")
class StaffList(MethodView):
    def get(self):
        return "staff"
    
@jwt_required()
@blp.route("/staff/<string:staff_id>")
class Staff(MethodView):
    @blp.response(200,StaffSchema)
    def get(self,staff_id):
        staff = mongo.db.staff.find_one_or_404({"_id":ObjectId(staff_id)})
        staff = json.loads(json_util.dumps(staff))
        return {**staff}
    
    @blp.arguments(StaffUpdateSchema)
    def put(self,staff_data,staff_id):
        try:
            # if staff_data['password']:
            #     staff_data['password']=pbkdf2_sha256.hash(staff_data)
            # mongo.db.staff.update_one({"_id": ObjectId(staff_id)}, {'$set': staff_data})
            staff = mongo.db.staff.find_one_or_404({"_id": ObjectId(staff_id)})
            staff = json.loads(json_util.dumps(staff))
            return {"message": "Member updated successfully ", **staff}
        except Exception as e:
            abort(401, message= f"An error occurred while updating. {e}")
    
    def delete(self, staff_id):
        try:
            mongo.db.staff.delete_one({"_id":ObjectId(staff_id)})
            return {"message": "Staff deleted"}
        except Exception as e:
            abort(401, message= f"An error occurred while updating. {e}")








