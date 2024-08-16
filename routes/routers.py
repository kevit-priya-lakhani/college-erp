from apps.basic_app import app

@app.route("/", methods=['GET'])
def index():
    return "App is running..."

@app.route("/health-check", methods=["GET"])
def test_route():
    return "Hello World"