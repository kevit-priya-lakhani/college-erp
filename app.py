from apps.basic_app import app as basic_app
import libs.utils.config as config
from libs.utils.log_services.logger import setup_logger

logger = setup_logger("app")

if __name__ == "__main__":
    basic_app.run(debug=True, port=config.PORT)