import datetime
import json
from os import access
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.schema import  PlainStudentSchema
from passlib.hash import pbkdf2_sha256
from db import mongo
import re


blp = Blueprint("student", __name__, description="Operations on students")

