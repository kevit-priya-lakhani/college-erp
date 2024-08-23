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

            user = None
            if permission == "staff":
                user = mongo.db.staff.find_one({"_id": ObjectId(current_user)})
            if permission == "admin":
                user = mongo.db.staff.find_one(
                    {"_id": ObjectId(current_user), "is_admin": True}
                )
                print(user)
            if not user:
                abort(403, message="You do not have the required permission.")

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def authorizeUpdate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        staff_id = kwargs.get("staff_id")

        # Fetch the user's information from the database
        current_user = (mongo.db.staff.find_one({"_id": ObjectId(current_user_id)}))
        staff = mongo.db.staff.find_one({"_id": ObjectId(staff_id)})
        if not staff:
            abort(404, message="Staff member not found.")
        
        # Check if the user is an admin or the owner of the account
        if current_user["is_admin"] == False and staff_id != (current_user_id):
            print(staff["is_admin"])
            print("current_user", (current_user_id), "staff_id", (staff_id))
            abort(403, message="You do not have permission to update this information.")

        return f(*args, **kwargs)

    return decorated_function
