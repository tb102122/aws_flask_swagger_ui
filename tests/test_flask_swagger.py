import os
import json
import logging
from flask import Flask
from aws_flask_swagger_ui import get_swaggerui_blueprint

logger = logging.getLogger(__name__)


def test_with_api_url(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.set_level(logging.DEBUG, logger="aw_flask_swagger")

    flask_app = Flask(__name__)
    SWAGGER_URL = "/api/docs"
    API_URL = "http://petstore.swagger.io/v2/swagger.json"

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={"app_name": "Test application"},  # Swagger UI config overrides
    )
    flask_app.register_blueprint(swaggerui_blueprint)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        response = testing_client.get("/api/docs/")
        assert response.status_code == 200
        assert b"Test application" in response.data
        assert b"http://petstore.swagger.io/v2/swagger.json" in response.data


def test_with_json(caplog):
    caplog.set_level(logging.DEBUG)
    caplog.set_level(logging.DEBUG, logger="aw_flask_swagger")
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(SCRIPT_DIR, "data/swagger.json")
    with open(os.path.join(SCRIPT_DIR, input_filename)) as input_fp:
        api_def = json.load(input_fp)

    flask_app = Flask(__name__)
    SWAGGER_URL = "/api/docs"

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, config={"app_name": "JSON Test application", "spec": api_def}
    )
    flask_app.register_blueprint(swaggerui_blueprint)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        response = testing_client.get("/api/docs/")
        assert response.status_code == 200
        assert b"JSON Test application" in response.data
        assert b"Swagger Petstore" in response.data
