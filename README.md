# aws-flask-swagger-ui

![Tests Status](https://github.com/tb102122/aws_flask_swagger_ui/actions/workflows/tests.yml/badge.svg)
![Release Status](https://github.com/tb102122/aws_flask_swagger_ui/actions/workflows/py-publish.yml/badge.svg)

Simple Flask blueprint for adding [Swagger UI](https://github.com/swagger-api/swagger-ui) to your flask application.
Including a WSGI adapter for [AWS API Gateway/Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html) to allows you to use WSGI-compatible middleware and frameworks like Flask and Django with the AWS API Gateway/Lambda proxy integration for your Swagger documentation.

Included Swagger UI version: [see here](./aws_flask_swagger_ui/dist/VERSION)

## Installation

`pip install aws-flask-swagger-ui`

## Usage

Simple usage example is shown below for more options check the file [extend examples](./example.py):

```python
from flask import Flask
from aws_flask_swagger_ui import get_swaggerui_blueprint, flask_ui_response

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    "/api-doc",
    aws_gw_config={
        "exportType": "oas30",
        "parameters": {
            "extensions": "integrations",
            "extensions": "apigateway",
            "extensions": "authorizers",
        },
    },
)

app.register_blueprint(swaggerui_blueprint)


def lambda_handler(event, context):
    return flask_ui_response(app, event, context, base64_content_types={"image/png"})
```

### AWS Gateway Configuration
http://mysite.com = https://restApiId.execute-api.region.amazonaws.com/stage/

In order that the above example works correctly the Lambda function must be connected as Proxy to the endpoint http://mysite.com/api-doc/ 

Configure your API Gateway with a `{proxy+}` resource with an `ANY` method. Your "Method Response" should likely include an `application/json` "Response Body for 200" that uses the `Empty` model.

Because API Gateway doesn't match the root folder with {proxy+} definition, your default URL should contain index.html. It is suggested to create a mock integration on your path `/api-doc` to return a 301. (ex: `/api-doc => 301` => `/api-doc/index.html`) Source code based on Terraform to achieve this can be found in this [article](https://itnext.io/how-to-easily-create-a-http-301-redirection-with-aws-api-gateway-2bf2874ef3f2).

### Lambda Test Event
The Lambda function must have the permissions to export the API definition!

If you wish to use the "Test" functionality in Lambda for your function, you will need a "API Gateway AWS Proxy" event. Check the event JSON objects in the [events](events/) folder.

To update your test event, click "Actions" -> "Configure test event".

Within the Events you need to update the `"apiId"` and `"stage"` with values for your AWS account.

### Protect documentation with password
If you create an environment variable like, SWAGGER_PASSWORD=abc

Then you will need to pass a query parameter in the URL like, http://mysite.com/api-doc/?pass=abc

If you don't have the environment variable then endpoint is not password protected and you can access it as per normal http://mysite.com/api-doc/


## Configuration

The blueprint supports overloading all Swagger UI configuration options that can be JSON serialized.
See [swagger-ui configuration](https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/configuration.md#parameters) for options.

Plugins and function parameters are not supported at this time.

OAuth2 parameters can be found at [swagger-ui oauth2](https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/oauth2.md).

## License

This library is licensed under the [Apache 2.0 License](./LICENSE).

## Test
- Clone the repo and run pytest

```bash
git clone https://github.com/tb102122/aws_flask_swagger_ui.git
python -m venv virtualenv
virtualenv/bin/activate
pip install --upgrade pip, setuptools, wheel
pip install flake8 pytest boto3 pytest-cov
pip install .
flake8 .
pytest
```