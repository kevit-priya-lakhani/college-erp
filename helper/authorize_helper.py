from functools import wraps
from bson import ObjectId
from flask_smorest import abort
from flask import request, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from db import mongo
from services.logger import logger  # Import your logger

# Initialize a logger

def authorize(permission):
    """
    Decorator to authorize user based on permission levels.

    Args:
        permission (str): The required permission level for the user ("staff" or "admin").

    Returns:
        function: The decorated function if authorization is successful.

    Raises:
        403 Forbidden: If the user does not have the required permission.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()  # Ensure JWT is valid
                current_user = get_jwt_identity()

                user = None
                if permission == "staff":
                    user = mongo.db.staff.find_one({"_id": ObjectId(current_user)})
                if permission == "admin":
                    user = mongo.db.staff.find_one(
                        {"_id": ObjectId(current_user), "is_admin": True}
                    )
                    logger.info(f"User details: {user}")

                if not user:
                    logger.warning(f"Authorization failed for user {current_user}. Required permission: {permission}")
                    abort(403, message="You do not have the required permission.")
                return fn(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error during authorization: {str(e)}")
                abort(403, message="Authorization error.")
        return wrapper
    return decorator


def authorizeUpdate(f):
    """
    Decorator to authorize updates based on user role and ownership.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function if authorization is successful.

    Raises:
        403 Forbidden: If the user is not an admin and does not own the account.
        404 Not Found: If the staff member to be updated is not found.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            staff_id = kwargs.get("staff_id")

            # Fetch the user's information from the database
            current_user = mongo.db.staff.find_one({"_id": ObjectId(current_user_id)})
            staff = mongo.db.staff.find_one({"_id": ObjectId(staff_id)})

            if not staff:
                logger.warning(f"Staff member with ID {staff_id} not found.")
                abort(404, message="Staff member not found.")
            
            # Check if the user is an admin or the owner of the account
            if not current_user["is_admin"] and staff_id != current_user_id:
                logger.info(f"User {current_user_id} attempted to update staff ID {staff_id}.")
                abort(403, message="You do not have permission to update this information.")

            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error during update authorization: {str(e)}")
            abort(403, message="Authorization error.")
    return decorated_function
