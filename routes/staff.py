import json
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.schema import StaffSchema
# from db import mongo
# from log_services.logger import logger  # Import your logger

blp = Blueprint("staff", __name__, description="Operations on staff")


@blp.route("/")
class Staff(MethodView):
    def get(self):
        return "App is running..."

@blp.route("/staff")
class Staff(MethodView):
    def get(self):
        return "staff"


@blp.route("/staff/login")
class staffRegister(MethodView):
    @blp.arguments(StaffSchema)
    def post(self,staff_data):
        store
