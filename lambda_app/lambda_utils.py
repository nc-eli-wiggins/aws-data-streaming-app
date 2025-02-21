import logging
import re
from json import dumps

import boto3
from requests import get as get_request


def setup_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    json_handler = logging.StreamHandler()
    formatter = JSONFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s " + "%(filename)s %(funcName)s"
    )
    json_handler.setFormatter(formatter)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(json_handler)

    return logger


def get_api_key() -> str:
    secret_name = "Guardian-API-Key"
    client = boto3.client("secretsmanager")
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    return get_secret_value_response["SecretString"]


def request_content(api_key: str, search_term: str, from_date: str, to_date: str = "") -> dict | None:

    url = f"https://content.guardianapis.com/search?q={search_term}"

    if from_date:
        url += f"&from-date={from_date}"

    if to_date:
        url += f"&to-date={to_date}"

    options = "&show-fields=wordcount&show-blocks=body"

    response = get_request(url + options + f"&api-key={api_key}")

    if response.status_code == 200:
        return response.json()
    else:
        return None


def prepare_messages(raw_response):
    articles = raw_response["response"]["results"]

    id_range = range(1, len(articles)+1) 
    id_gen = iter(id_range)
    shorten = lambda x: x[:1001].rsplit('.', 1)[0] + '.'
    
    prepared_messages = [
        {
            "Id": str(next(id_gen)),
            "MessageBody": dumps(
                {
                    "Title": x["webTitle"],
                    "Section": x["sectionName"],
                    "PublicationDate": x["webPublicationDate"],
                    "WordCount": x['fields']["wordcount"],
                    "Url": x["webUrl"],
                    "Preview": shorten(x["blocks"]["body"][0]["bodyTextSummary"])
                }
            ),
        }
        for x in articles
    ]

    return prepared_messages


def post_to_sqs(messages: list):
    sqs_client = boto3.client("sqs")
    queue_url = sqs_client.get_queue_url(QueueName="guardian_content")["QueueUrl"]
    response = sqs_client.send_message_batch(QueueUrl=queue_url, Entries=messages)
    return response


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "asctime": self.formatTime(record, self.datefmt),
            "levelname": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "filename": record.filename,
            "funcName": record.funcName,
        }
        return dumps(log_obj)
