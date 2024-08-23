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


app = Flask(__name__)
load_dotenv()
# app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
# app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
# # File Logging Setup
# app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
# app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")
# app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["MONGO_URI"] =  os.environ.get("MONGO_URL")
mongo.init_app(app)


api = Api(app)

app.config["JWT_SECRET_KEY"]=  os.environ.get("JWT_KEY")
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return(
        jsonify({"message": "The token has expired", "error":"Token expired"})
    ),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed. ", "error": "invalid token"}
        ),401
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {"message": "Request does not contain and access token ", "error": "Authorization required"}
        ),401
    )

api.register_blueprint(StaffBlueprint)
api.register_blueprint(StudentBlueprint)
api.register_blueprint(UserBlueprint)
api.register_blueprint(AttendanceBlueprint)
api.register_blueprint(DepartmentBlueprint)