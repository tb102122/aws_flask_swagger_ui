import json
import os
import secrets

from flask import (
    Blueprint,
    Response,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

from .aws_api_gateway_docu import get_api_gateway_documentation


def get_swaggerui_blueprint(
    base_url: str,
    api_url: str = None,
    config: dict = {},
    aws_gw_config: dict = None,
    oauth_config: dict = None,
    blueprint_name: str = "swagger_ui",
    icons: list = None,
    basic_auth_credentials: tuple = None,
) -> Blueprint:
    """
    Get Flask App with Swagger UI as BluePrint and option to get Swagger definition directly from AWS Gateway.

    Args:
        base_url (str): URL for exposing Swagger UI (without trailing '/')
        api_url (str, optional): Our API url (can of course be a local resource). Defaults to None.
        config (dict, optional): Swagger UI config overrides. Defaults to {}.
        aws_gw_config (dict, optional): AWS API Gateway Configuration for details see get_api_gateway_documentation. Defaults to None.

        oauth_config (dict, optional): OAuth config for details see https://github.com/swagger-api/swagger-ui#oauth2-configuration. Defaults to None.
        blueprint_name (str, optional): Name of Flask App. Defaults to "swagger_ui".
        icons (list, optional): Option to overwrite default icons in format of [{"href": "./favicon-32x32.png", "sizes": "32x32"}]. Defaults to None.
        basic_auth_credentials (tuple, optional): (username, password) to require HTTP Basic Auth before serving
            any Swagger UI route (page and static assets). Falls back to the SWAGGER_BASIC_AUTH_USER /
            SWAGGER_BASIC_AUTH_PASSWORD environment variables when not provided. Defaults to None (no auth).

    Raises:
        ValueError: in case of missing Swagger configuration.

    Returns:
        Blueprint: Flask Blueprint with Swagger UI.
    """
    if api_url is None and config.get("spec", {}) == {} and aws_gw_config is None:
        raise ValueError(
            "All Swagger specifications are empty at least one needs to be provided!"
        )

    swagger_ui = Blueprint(
        blueprint_name,
        __name__,
        static_folder="dist",
        template_folder="templates",
        url_prefix=base_url,
    )

    if basic_auth_credentials:
        basic_auth_user, basic_auth_pass = basic_auth_credentials
    else:
        basic_auth_user = os.getenv("SWAGGER_BASIC_AUTH_USER")
        basic_auth_pass = os.getenv("SWAGGER_BASIC_AUTH_PASSWORD")

    if basic_auth_user and basic_auth_pass:

        @swagger_ui.before_request
        def _require_basic_auth():
            auth = request.authorization
            authorized = (
                auth is not None
                and auth.type == "basic"
                and secrets.compare_digest(auth.username or "", basic_auth_user)
                and secrets.compare_digest(auth.password or "", basic_auth_pass)
            )
            if not authorized:
                return Response(
                    "Authentication required",
                    401,
                    {"WWW-Authenticate": 'Basic realm="Swagger UI"'},
                )

    default_config = {
        "app_name": "Swagger UI",
        "dom_id": "#swagger-ui",
        "layout": "StandaloneLayout",
        "deepLinking": True,
    }

    default_icons = [
        {"href": "./favicon-32x32.png", "sizes": "32x32"},
        {"href": "./favicon-16x16.png", "sizes": "16x16"},
    ]
    if api_url:
        default_config["url"] = api_url
    if config:
        default_config.update(config)
    if icons:
        default_icons = icons
    # print(default_config)

    fields = {
        # Some fields are used directly in template
        "base_url": base_url,
        "app_name": default_config.pop("app_name"),
        # Rest are just serialized into json string for inclusion in the .js file
        "config_json": json.dumps(default_config),
        "icons": default_icons,
    }
    if oauth_config:
        fields["oauth_config_json"] = json.dumps(oauth_config)

    @swagger_ui.route("/")
    @swagger_ui.route("/<path:path>")
    @swagger_ui.route("/<path:path>/index.html")
    def show(path=None):
        if not path or path == "index.html":
            if not default_config.get("oauth2RedirectUrl", None):
                default_config.update(
                    {
                        "oauth2RedirectUrl": os.path.join(
                            request.base_url, "oauth2-redirect.html"
                        )
                    }
                )
                fields["config_json"] = json.dumps(default_config)
            # Added password protection via query parameter.
            swagger_pass = os.getenv("SWAGGER_PASSWORD", default=None)
            if swagger_pass:
                user_pass = request.args.get("pass")
                if swagger_pass != user_pass:
                    response = jsonify({"error": "password incorrect"})
                    response.status_code = 401
                    return response
            if default_config.get("spec", {}) == {}:
                if aws_gw_config:
                    aws_gw_config["restApiId"] = (
                        request.environ.get("lambda.event", {})
                        .get("requestContext", {})
                        .get("apiId", "")
                    )
                    aws_gw_config["stageName"] = (
                        request.environ.get("lambda.event", {})
                        .get("requestContext", {})
                        .get("stage", "")
                    )
                    api_def = get_api_gateway_documentation(**aws_gw_config)
                    default_config.update({"spec": api_def})
                    fields["config_json"] = json.dumps(default_config)

            return render_template("index.template.html", **fields)
        else:
            return send_from_directory(
                # A bit of a hack to not pollute the default /static path with our files.
                os.path.join(swagger_ui.root_path, swagger_ui._static_folder),
                path,
            )

    return swagger_ui
