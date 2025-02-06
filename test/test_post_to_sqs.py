import os

from moto import mock_aws
import boto3
from botocore.exceptions import ClientError
import pytest

from lambda_function import post_to_sqs
from test_data.prepared_messages import prepared_messages


@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEAFULT_REGION"] = "eu-west-2"


queue_url = None

@pytest.fixture(scope="function")
def sqs_client(aws_creds):
    with mock_aws():
        sqs_client = boto3.client("sqs")
        sqs_client.create_queue(
            QueueName='guardian_content',
            Attributes={
                'MessageRetentionPeriod': '259200'
            }
        )

        global queue_url
        queue_url = sqs_client.get_queue_url(
            QueueName='guardian_content'
        )['QueueUrl']
        
        yield sqs_client


def test_adds_single_message(sqs_client):
    single_message = [prepared_messages[0]]
    output = post_to_sqs(single_message)
    assert list(output.keys())[0] == 'Successful'
    response = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    assert len(response['Messages']) == 1