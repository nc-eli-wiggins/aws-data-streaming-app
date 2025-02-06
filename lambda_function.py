from requests import get as get_request
from json import dumps

import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    if not event.get("queryStringParameters"):
        pass
    api_key = get_api_key()


def get_api_key() -> str:
    region_name = "eu-west-2"
    secret_name = "Guardian-API-Key"
    
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    
    return get_secret_value_response["SecretString"]


def request_content(api_key: str, search_term: str, from_date: str = None)  -> dict | None:
    
    url = f'https://content.guardianapis.com/search?q={search_term}'

    if from_date:
        url += f'&from-date={from_date}'
    
    response = get_request(url + f'&api-key={api_key}')

    if response.status_code == 200:
        return response.json()
    else:
        return None


def prepare_messages(raw_response):
    articles = raw_response['response']['results']
    prepared_messages = [
        {
            "Id": x["id"],
            "MessageBody": dumps({
                "webPublicationDate": x["webPublicationDate"],
                "webTitle": x["webTitle"],
                "webUrl": x["webUrl"]
            })
        } for x in articles
    ]

    return prepared_messages


def post_to_sqs(messages: list):
    
    sqs_client = boto3.client("sqs")

    queue_url = sqs_client.get_queue_url(
            QueueName='guardian_content'
        )['QueueUrl']

    response = sqs_client.send_message_batch(
        QueueUrl=queue_url,
        Entries=messages
    )
    return response