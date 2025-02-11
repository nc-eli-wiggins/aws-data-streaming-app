from unittest.mock import patch, Mock
import sys

import pytest

# sys.path.append('./lambda_app')

from lambda_app.lambda_function import lambda_handler


@pytest.fixture
def mock_setup_logger():
    with patch("lambda_app.lambda_function.setup_logger") as mock_setup_logger:
        yield mock_setup_logger

@pytest.fixture
def mock_get_api_key():
    with patch("lambda_app.lambda_function.get_api_key") as mock_get_api_key:
        yield mock_get_api_key

@pytest.fixture
def mock_request_content():
    with patch("lambda_app.lambda_function.request_content") as mock_request_content:
        yield mock_request_content

@pytest.fixture
def mock_prepare_messages():
    with patch("lambda_app.lambda_function.prepare_messages") as mock_prepare_messages:
        yield mock_prepare_messages

@pytest.fixture
def mock_post_to_sqs():
    with patch("lambda_app.lambda_function.post_to_sqs") as mock_post_to_sqs:
        yield mock_post_to_sqs

@pytest.fixture
def patch_all(mock_setup_logger, mock_get_api_key, mock_request_content, mock_prepare_messages, mock_post_to_sqs):
    yield "Woah! Sure you're doing enough patching there, Sonny Jim?"

@pytest.fixture
def test_event():
    return {"SearchTerm": "futuristic egg", "FromDate": "01-01-2025"}

def test_returns_dict(patch_all, test_event):
    output = lambda_handler(test_event, "AWS")
    assert isinstance(output, dict)

def test_dict_has_status_code_key(patch_all, test_event):
    output = lambda_handler(test_event, "AWS")
    assert "statusCode" in output