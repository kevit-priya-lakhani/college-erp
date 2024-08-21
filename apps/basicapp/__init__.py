from flask import Flask,jsonify
from flask.cli import load_dotenv
from flask_smorest import Api
from resources.books import blp as BooksBlueprint 
from resources.users import blp as UsersBlueprint 
from resources.reviews import blp as ReviewsBlueprint 
from db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
import os

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"]="Book Reviews API"
    app.config["API_VERSION"] = "v1"
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    print(app.config["SQLALCHEMY_DATABASE_URI"] )
    db.init_app(app)

    migrate = Migrate(app,db)
    

    # with app.app_context():
    #     db.create_all() 


    api = Api(app)

    app.config["JWT_SECRET_KEY"]= "340002295594837289408925169365897159961"
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


    api.register_blueprint(BooksBlueprint)
    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(ReviewsBlueprint)

    return app






