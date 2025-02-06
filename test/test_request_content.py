from unittest.mock import patch, Mock

import pytest

from lambda_function import request_content


@pytest.fixture
def mock_200_response():
    mock_200_response = Mock()
    mock_200_response.status_code = 200
    mock_200_response.json.return_value = {}
    return mock_200_response


@pytest.fixture
def mock_500_response():
    mock_500_response = Mock()
    mock_500_response.status_code = 500
    return mock_500_response


@patch("lambda_function.get_request")
def test_uses_parameters_in_request(mock_get_request, mock_200_response):
    mock_get_request.return_value = mock_200_response
    request_content("test-API-key", "test-search-term", "2023-03-28")
    mock_get_request.assert_called_with(
        "https://content.guardianapis.com/search?q=test-search-term&from-date=2023-03-28&api-key=test-API-key"
    )


@patch("lambda_function.get_request")
def test_returns_dict_for_200_response(mock_get_request, mock_200_response):
    mock_get_request.return_value = mock_200_response
    output = request_content("test-API-key", "test-search-term", "2023-03-28")
    assert isinstance(output, dict)


@patch("lambda_function.get_request")
def test_returns_none_for_500_response(mock_get_request, mock_500_response):
    mock_get_request.return_value = mock_500_response
    output = request_content("test-API-key", "test-search-term", "2023-03-28")
    assert output is None