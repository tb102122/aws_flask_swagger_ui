import boto3
import json


def get_api_gateway_documentation(
    profile_name: str = None,
    region: str = "eu-central-1",
    restApiId: str = None,
    stageName: str = None,
    exportType: str = "oas30",
    parameters: dict = {},
) -> dict:
    #
    """
    Get Documentation from AWS API Gateway and prefer for usage with Swagger UI.

    Args:
        profile_name (str, optional): Profile name for AWS credentials. Defaults to None.
        region (str, optional): AWS Region of API Gateway Endpoint. Defaults to "eu-central-1".
        restApiId (str, optional): The string identifier of the associated RestApi. Defaults to None.
        stageName (str, optional): The name of the Stage that will be exported. Defaults to None.
        exportType (str, optional): The type of export. Acceptable values are 'oas30' for OpenAPI 3.0.x and 'swagger' for Swagger/OpenAPI 2.0. Defaults to "oas30".
        parameters (dict, optional): Check for details existing Boto3 documentation https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_export. Defaults to {}.
        accepts (str, optional): The content-type of the export, for example  . Currently application/json and application/yaml are supported for exportType of``oas30`` and swagger . This should be specified in the Accept header for direct API requests. Defaults to None.
    Returns:
        dict: Dictionary of API gateway definition
    """
    if not restApiId:
        raise ValueError("restApiId needs to be defined!")
    if not stageName:
        raise ValueError("stageName needs to be defined!")
    if not exportType:
        raise ValueError("exportType needs to be defined!")

    if profile_name:
        ag_client = boto3.session.Session(profile_name=profile_name).client(
            "apigateway", region
        )
    else:
        ag_client = boto3.client("apigateway")

    response = ag_client.get_export(
        restApiId=restApiId,
        stageName=stageName,
        exportType=exportType,
        parameters=parameters,
        accepts="application/json",
    )

    api_def = json.loads(response["body"].read())

    for server in api_def["servers"]:
        path = server["variables"]["basePath"]["default"]
        if path.startswith("/"):
            server["variables"]["basePath"]["default"] = path[1:]

    api_def["paths"].pop("/api-doc/{proxy+}", None)
    api_def["paths"].pop("/api-doc", None)
    return api_def
