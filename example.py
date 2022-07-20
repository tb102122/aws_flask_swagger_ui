from flask import Flask
from aws_flask_swagger_ui import get_swaggerui_blueprint, flask_ui_response
import os
import json

app = Flask(__name__)

# sample with local Swagger definition
input_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "tests/data/swagger.json"
)
with open(input_filename) as input_fp:
    api_def = json.load(input_fp)

swaggerui_blueprint = get_swaggerui_blueprint(
    "/api-doc", config={"app_name": "JSON Test application", "spec": api_def}
)

# sample with online Swagger definition
swaggerui_blueprint = get_swaggerui_blueprint(
    "/api-doc",
    "http://petstore.swagger.io/v2/swagger.json",
)

# sample with online Swagger definition from API Gateway
swaggerui_blueprint = get_swaggerui_blueprint(
    "/api-doc",
    aws_gw_config={
        "exportType": "oas30",
        "parameters": {"extensions": "integrations"},
    },
)

app.register_blueprint(swaggerui_blueprint)


def lambda_handler(event, context):
    return flask_ui_response(app, event, context, base64_content_types={"image/png"})


if __name__ == "__main__":
    app.run()
    # For local testing of the Flask App browser to localhost:5000/api-doc/
