import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    pass


def get_api_key():
    
    region_name = "eu-west-2"
    secret_name = "Guardian-API-Key"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    return get_secret_value_response["SecretString"]


def request_content():
    pass


def post_to_sqs():
    pass