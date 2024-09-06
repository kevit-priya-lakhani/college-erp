from email import message
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from helper.authorize_helper import authorize
from schema.student import PlainStudentSchema
from schema.user import LoginSchema
from schema.staff import PlainStaffSchema
from services.logger import logger 
from helper.user_helper import *


blp = Blueprint("login", __name__, description="Login/logout operations")

@blp.route("/login")
class Login(MethodView):
    """
    Handles user login operations for both staff and students.
    """

    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """
        Log in a user by verifying their credentials.

        Args:
            login_data (dict): The login data containing email and password.

        Returns:
            JSON response with a success message and tokens if login is successful,
            or an error message if credentials are invalid.
        """
        logger.info("Login attempt with email: %s", login_data["email"])

        message = user_login(login_data)
        if not message:
            logger.error("Invalid email format: %s", login_data["email"])
            return {"message": "Invalid email"}
        return message


@blp.route("/logout")
class UserLogout(MethodView):
    """
    Handles user logout by invalidating the JWT token.
    """

    @jwt_required()
    def post(self):
        """
        Log out a user by adding their JWT ID to the blocklist.

        Returns:
            JSON response with a success message if logout is successful,
            or an error message if an exception occurs.
        """
        logger.info("Logout attempt")

        try:
            user_logout()           
            return {"message": "Successfully logged out"}, 200
        except Exception as e:
            logger.error("Error during logout: %s", str(e))
            abort(500, message="An error occurred during logout")


@blp.route("/register/student")
class StudentRegister(MethodView):
    """
    Handles student registration operations.
    """

    def get(self):
        """
        Health check for the registration endpoint.

        Returns:
            A message indicating that the endpoint is running.
        """
        return "running"

    @jwt_required()
    @authorize(permission="staff")
    @blp.arguments(PlainStudentSchema)
    def post(self, mem_data):
        """
        Register a new student.

        Args:
            mem_data (dict): The student data for registration.

        Returns:
            JSON response with a success message and student ID if registration is successful,
            or an error message if email already exists or department is invalid.
        """
        register_student_data(mem_data)


@blp.route("/register/staff")
class StaffRegister(MethodView):
    """
    Handles staff registration operations.
    """

    @jwt_required()
    @authorize(permission="admin")
    @blp.arguments(PlainStaffSchema)
    def post(self, mem_data):
        """
        Register a new staff member.

        Args:
            mem_data (dict): The staff data for registration.

        Returns:
            JSON response with a success message and staff ID if registration is successful,
            or an error message if email already exists or department is invalid.
        """
        register_staff_data(mem_data)