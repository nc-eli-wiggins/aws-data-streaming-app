from main import get_api_key

from moto import mock_aws
import boto3
from botocore.exceptions import ClientError
import pytest
import os


@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEAFULT_REGION"] = "eu-west-2"


secret_string = "Fake API code"


@pytest.fixture(scope="function")
def secrets_client(aws_creds):
    with mock_aws():
        secrets_client = boto3.client("secretsmanager")
        secrets_client.create_secret(
            Name="Guardian-API-Key", SecretString=secret_string
        )
        yield secrets_client


@pytest.fixture(scope="function")
def invalid_secrets_client(aws_creds):
    with mock_aws():
        secrets_client = boto3.client("secretsmanager")
        secret_string = "Fake API code"
        secrets_client.create_secret(
            Name="Other-API-Key", SecretString=secret_string
        )
        yield invalid_secrets_client


def test_returns_secret_string(secrets_client):
    result = get_api_key()
    assert type(result) == str
    assert result == secret_string


def test_raises_client_error_if_client_error_occurs(invalid_secrets_client):
    with pytest.raises(ClientError):
        get_api_key()