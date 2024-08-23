import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from routes.staff import blp as StaffBlueprint
from routes.student import blp as StudentBlueprint
from routes.user import blp as UserBlueprint
from routes.attendance import blp as AttendanceBlueprint
from routes.department import blp as DepartmentBlueprint
from blocklist import BLOCKLIST
from db import mongo
import logging

# Initialize a logger
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()

# Application configuration
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["MONGO_URI"] = os.environ.get("MONGO_URL")

# Initialize MongoDB with the app
mongo.init_app(app)

# Initialize Flask-Smorest API
api = Api(app)

# JWT configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_KEY")
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    """
    Checks if a JWT token is in the blocklist (revoked).

    Args:
        jwt_header (dict): The JWT header.
        jwt_payload (dict): The JWT payload.

    Returns:
        bool: True if the token is in the blocklist, False otherwise.
    """
    logger.info("Checking if token is in blocklist")
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """
    Handles revoked token requests.

    Args:
        jwt_header (dict): The JWT header.
        jwt_payload (dict): The JWT payload.

    Returns:
        Response: JSON response with revoked token message and 401 status code.
    """
    logger.warning("Revoked token access attempt")
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    """
    Adds additional claims to JWT, such as admin status.

    Args:
        identity (int/str): The identity of the user.

    Returns:
        dict: Dictionary with additional claims.
    """
    logger.info("Adding claims to JWT")
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """
    Handles expired token requests.

    Args:
        jwt_header (dict): The JWT header.
        jwt_payload (dict): The JWT payload.

    Returns:
        Response: JSON response with expired token message and 401 status code.
    """
    logger.warning("Expired token access attempt")
    return(
        jsonify({"message": "The token has expired", "error":"Token expired"})
    ), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Handles invalid token requests.

    Args:
        error (str): The error message.

    Returns:
        Response: JSON response with invalid token message and 401 status code.
    """
    logger.warning("Invalid token access attempt")
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid token"}
        ), 401
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    Handles requests missing a token.

    Args:
        error (str): The error message.

    Returns:
        Response: JSON response with missing token message and 401 status code.
    """
    logger.warning("Missing token in request")
    return (
        jsonify(
            {"message": "Request does not contain an access token", "error": "Authorization required"}
        ), 401
    )

# Registering blueprints for different routes
api.register_blueprint(StaffBlueprint)
api.register_blueprint(StudentBlueprint)
api.register_blueprint(UserBlueprint)
api.register_blueprint(AttendanceBlueprint)
api.register_blueprint(DepartmentBlueprint)

# Log the successful startup of the application
logger.info("Flask application has started successfully")
