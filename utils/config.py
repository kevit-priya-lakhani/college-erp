import os, dotenv

dotenv.load_dotenv(".env", override=True)

PORT = int(os.getenv("PORT"))

FLASK_HEADERS = os.getenv('FLASK_HEADERS')

TEAMS_ERROR_WEBHOOK = os.getenv("TEAMS_ERROR_WEBHOOK")