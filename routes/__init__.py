from flask import Flask
from flask_cors import CORS
import libs.utils.config as config

app = Flask(__name__)

"""  CORS handling.  """

CORS(
    app,
    resources={r"*": {"origins": "*", "methods": ["GET", "POST"]}},
    allow_headers=config.FLASK_HEADERS,
    supports_credentials=True,
)

from apps.basic_app.routes import router