import datetime
from email import message
import json
from os import access
from bson import ObjectId, json_util
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from helper.helper import authorize, authorizeUpdate
from schema import StaffUpdateSchema, StaffSchema
from passlib.hash import pbkdf2_sha256
from db import mongo
import re
from services.logger import logger  # Import your logger

blp = Blueprint("staff", __name__, description="Operations on staff")


@blp.route("/")
class Index(MethodView):
    """
    A simple index route to check if the application is running.
    
    Methods:
        get: Returns a string indicating that the application is running.
    """

    def get(self):
        """
        Return a message indicating that the application is running.
        
        Returns:
            A string message.
        """
        logger.info("Index route accessed - App is running.")
        return "App is running..."


@blp.route("/staff/<string:staff_id>")
class Staff(MethodView):
    """
    A resource class for handling operations on individual staff members.

    Methods:
        get: Retrieves a specific staff member by their ID.
        put: Updates a specific staff member's details by their ID.
        delete: Deletes a specific staff member by their ID.
    """

    @jwt_required()
    @authorize(permission="staff")
    @blp.response(200, StaffSchema)
    def get(self, staff_id):
        """
        Retrieve a specific staff member's details by their ID.

        Args:
            staff_id (str): The ID of the staff member.

        Returns:
            A JSON object containing the staff member's details.
        """
        logger.info(f"Fetching staff member with ID: {staff_id}")
        try:
            staff = mongo.db.staff.find_one_or_404({"_id": ObjectId(staff_id)})
            staff = json.loads(json_util.dumps(staff))
            logger.info(f"Staff member with ID: {staff_id} retrieved successfully.")
            return {**staff}
        except Exception as e:
            logger.error(f"Error fetching staff member with ID: {staff_id}: {e}")
            abort(404, message=f"Staff member not found: {e}")
    
    @jwt_required()
    @authorize(permission="staff")
    @blp.response(200, StaffSchema)
    @blp.arguments(StaffUpdateSchema)
    @authorizeUpdate
    def put(self, staff_data, staff_id):
        """
        Update a specific staff member's details by their ID.

        Args:
            staff_data (dict): The updated data for the staff member.
            staff_id (str): The ID of the staff member to update.

        Returns:
            A JSON object with a success message and the updated staff member details.

        Raises:
            401 Unauthorized: If an error occurs during the update process.
        """
        logger.info(f"Attempting to update staff member with ID: {staff_id}")
        try:
            if 'password' in staff_data:
                staff_data['password'] = pbkdf2_sha256.hash(staff_data['password'])
            staff_data['updated_at'] = datetime.datetime.now()
            mongo.db.staff.update_one({"_id": ObjectId(staff_id)}, {'$set': staff_data})
            staff = mongo.db.staff.find_one_or_404({"_id": ObjectId(staff_id)})
            staff = json.loads(json_util.dumps(staff))
            logger.info(f"Staff member with ID: {staff_id} updated successfully.")
            return {"message": "Member updated successfully", **staff}
        except Exception as e:
            logger.error(f"Error updating staff member with ID: {staff_id}: {e}")
            abort(401, message=f"An error occurred while updating. {e}")

    @jwt_required()
    @authorize(permission="admin")
    def delete(self, staff_id):
        """
        Delete a specific staff member by their ID.

        Args:
            staff_id (str): The ID of the staff member to delete.

        Returns:
            A JSON object with a success message.

        Raises:
            401 Unauthorized: If an error occurs during the deletion process.
        """
        logger.info(f"Attempting to delete staff member with ID: {staff_id}")
        try:
            mongo.db.staff.delete_one({"_id": ObjectId(staff_id)})
            logger.info(f"Staff member with ID: {staff_id} deleted successfully.")
            return {"message": "Staff deleted"}
        except Exception as e:
            logger.error(f"Error deleting staff member with ID: {staff_id}: {e}")
            abort(401, message=f"An error occurred while deleting. {e}")


@blp.route("/staff")
class StaffList(MethodView):
    """
    A resource class for handling operations on the list of staff members.

    Methods:
        get: Retrieves a list of all staff members.
    """

    @jwt_required()
    @authorize(permission="staff")
    def get(self):
        """
        Retrieve a list of all staff members.

        Returns:
            A JSON object containing a list of all staff members.
        """
        logger.info("Fetching all staff members.")
        try:
            staff_list = mongo.db.staff.find()
            staff_list = json.loads(json_util.dumps(staff_list))
            logger.info("All staff members retrieved successfully.")
            return {"staff_list": list(staff_list)}
        except Exception as e:
            logger.error(f"Error fetching all staff members: {e}")
            abort(404, message=f"An error occurred while fetching staff members. {e}")
