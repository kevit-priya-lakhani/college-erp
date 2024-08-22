from functools import wraps
from bson import ObjectId
from flask_smorest import abort
from flask import request, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from db import mongo

def authorize(permission):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Ensure JWT is valid
            current_user = get_jwt_identity()
            print(current_user)

            user= None
            if permission =="staff":
                user = mongo.db.staff.find_one({"_id": ObjectId(current_user)})
            if permission =="admin":
                user = mongo.db.staff.find_one({"_id": ObjectId(current_user),"is_admin":1})

            if not user:
                abort(403, message="You do not have the required permission.")

            return fn(*args, **kwargs)
        return wrapper
    return decorator

