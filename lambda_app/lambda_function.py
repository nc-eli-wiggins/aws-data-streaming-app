from pydantic import ValidationError

from lambda_utils import (setup_logger, get_api_key, request_content, prepare_messages, post_to_sqs)
from lambda_classes import LambdaEvent


def lambda_handler(event, context):
    logger = setup_logger("Guardian Data Streaming Lambda")
    logger.info("Guardian data streaming lambda invoked")

    # Validate event
    try:
        logger.info("Validating event")
        event = LambdaEvent(**event)
        logger.info("Event validated")
    except ValidationError as e:
        logger.error(f"Invalid event. Event = {event}")
        return {"statusCode": 400, "body": f"{str(e)}"}
    
    # Capture values from event
    search_term = event.SearchTerm
    from_date = event.FromDate

    # Get API key from Secrets Manager
    try:
        logger.info("get_api_key invoked")
        api_key = get_api_key()
        logger.info("get_api_key executed successfully")
    except Exception as e:
        logger.critical(f"Critical error during get_api_key execution: {repr(e)}")
        return {"statusCode": 500, "body": "Critical error experienced while processing request."}
    
    # Make get request using search terms and API key
    try:
        logger.info(f"request_content invoked, search_term = {search_term}")
        raw_response = request_content(api_key, search_term, from_date)
        logger.info(f"request_content executed successfully, search_term = {search_term}")
    except Exception as e:
        logger.critical(f"Critical error during request_content execution: {repr(e)}")
        return {"statusCode": 500, "body": "Critical error experienced while processing request."}

    # Prepare content into messages
    try:
        logger.info("prepare_messages invoked")
        prepared_messages = prepare_messages(raw_response)
        logger.info("prepare_messages executed successfully")
    except Exception as e:
        logger.critical(f"Critical error during perpare_messages execution: {repr(e)}")
        return {"statusCode": 500, "body": "Critical error experienced while processing request."}

    if prepared_messages == []:
        return {"statusCode": 200, "body": "0 articles retrieved"}
    
    # Post messages to SQS
    try:
        logger.info("post_to_sqs invoked")
        sqs_response = post_to_sqs(prepared_messages)
        logger.info("post_to_sqs executed successfully")
    except Exception as e:
        logger.critical(f"Critical error during post_to_sqs execution: {repr(e)}")
        return {"statusCode": 500, "body": "Critical error experienced while processing request."}

    return {"statusCode": 200, "body": f"{len(prepared_messages)} messages uploaded to SQS"}
