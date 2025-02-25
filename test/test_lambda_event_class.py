import sys, os

# Remove the Lambda layer path from sys.path
lambda_layer_path = os.path.join(os.getcwd(), 'layer', 'python')
if lambda_layer_path in sys.path:
    sys.path.remove(lambda_layer_path)

from pydantic import ValidationError

import pytest

from lambda_app.lambda_classes import LambdaEvent


@pytest.mark.it("Validates when event contains valid SearchTerm and queue and no FromDate")
def test_valid_request():
    event = {'SearchTerm': "blob", "queue": "guardian_content"}
    LambdaEvent(**event)


@pytest.mark.it("Validates when event contains valid SearchTerm, queue and FromDate")
def test_valid_request_no_from():
    event = {'SearchTerm': "blob", "FromDate": "2016-09-10", "queue": "guardian_content"}
    LambdaEvent(**event)


@pytest.mark.it("Raises validation error when SearchTerm missing")
def test_missing_search():
    with pytest.raises(ValidationError):
        event = {"FromDate": "2016-09-10", "queue": "guardian_content"}
        LambdaEvent(**event)


@pytest.mark.it("Raises validation error when queue missing")
def test_missing_queue():
    with pytest.raises(ValidationError):
        event = {'SearchTerm': "blob", "FromDate": "2016-09-10"}
        LambdaEvent(**event)


@pytest.mark.it("Raises validation error when SearchTerm isn't string")
def test_raises_err_search():
    for x in [{}, [], (), 1, True]:
        event = {'SearchTerm': x, "FromDate": "2016-09-10", "queue": "guardian_content"}
        with pytest.raises(ValidationError):
            LambdaEvent(**event)


@pytest.mark.it("Raises validation error when from date doesn't match yyyy-mm-dd format")
def test_raises_err_date():
    event = {'SearchTerm': "egg", "queue": "guardian_content", "FromDate": "20-02-1608"}
    with pytest.raises(ValidationError):
        LambdaEvent(**event)


@pytest.mark.it("Raises validation error if queue not 'guardian_content'")
def test_queue_not_guardian():
    event = {'SearchTerm': "egg", "queue": "guardian_content", "FromDate": "20-02-1608"}
    with pytest.raises(ValidationError):
        LambdaEvent(**event)


@pytest.mark.it("Raises validation error if SearchFrom < 2 chars")
def test_search_from_chars():
    event = {'SearchTerm': "e", "queue": "guardian_content", "FromDate": "2016-09-10"}
    with pytest.raises(ValidationError):
        LambdaEvent(**event)