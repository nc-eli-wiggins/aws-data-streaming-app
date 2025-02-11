from .lambda_utils import (setup_logger, get_api_key, request_content, prepare_messages, post_to_sqs)


def lambda_handler(event, context):
    logger = setup_logger("Guardian Data Streaming Lambda")
    logger.info("Guardian data streaming lambda invoked.")

    # Capture search_term and from_date variables
    try:
        logger.info("Accessing search terms from event.")
        if context == "local":
            search_term = event["SearchTerm"]
            from_date = event.get("FromDate", None)
        else:
            search_term = event["SearchTerm"]
            from_date = event.get("FromDate", None)
        logger.info("Search terms stored")
    except Exception as e:
        logger.critical(f"Critical error while attempting to access search terms. Event = {event}")
        raise e

    # Get API key from Secrets Manager
    try:
        logger.info("get_api_key invoked.")
        api_key = get_api_key()
        logger.info("get_api_key executed successfully.")
    except Exception as e:
        logger.critical(f"Critical error during get_api_key execution: {repr(e)}")
        raise e
    
    # Make get request using search terms and API key
    try:
        logger.info(f"request_content invoked. search_term = {search_term}")
        raw_response = request_content(api_key, search_term, from_date)
        logger.info(f"request_content invoked. search_term = {search_term}")
    except Exception as e:
        logger.critical(f"Critical error during request_content execution: {repr(e)}")
        raise e

    # Prepare content into messages
    try:
        logger.info("prepare_messages invoked.")
        prepared_messages = prepare_messages(raw_response)
        logger.info("prepare_messages executed successfully.")
    except Exception as e:
        logger.critical(f"Critical error during perpare_messages execution: {repr(e)}")
        raise e

    if prepared_messages == []:
        return {"statusCode": 200, "body": "0 articles retrieved."}
    
    # Post messages SQS
    try:
        logger.info("post_to_sqs invoked.")
        sqs_response = post_to_sqs(prepared_messages)
        logger.info("post_to_sqs executed successfully.")
    except Exception as e:
        logger.critical(f"Critical error during post_to_sqs execution: {repr(e)}")
        raise e

    return {"statusCode": 200, "body": f"{len(prepared_messages)} messages uploaded to SQS."}
