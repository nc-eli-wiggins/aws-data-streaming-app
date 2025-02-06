from json import load

import pytest

from lambda_function import prepare_messages


@pytest.fixture()
def raw_response():
    with open("test/test_data/raw_response.json", "r") as jsizzle:
        raw_response = load(jsizzle)
    return raw_response


def test_returns_list(raw_response):
    output = prepare_messages(raw_response)
    assert isinstance(output, list)

