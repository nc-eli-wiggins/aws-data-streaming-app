from json import load, loads

import pytest

from lambda_function import prepare_messages


@pytest.fixture()
def raw_response():
    with open("test/test_data/raw_response.json", "r") as jsizzle:
        raw_response = load(jsizzle)
    return raw_response


@pytest.mark.it("Returns list of dictionaries")
def test_returns_list(raw_response):
    output = prepare_messages(raw_response)
    assert isinstance(output, list)
    assert all(isinstance(x, dict) for x in output)


@pytest.mark.it("Dicts in list have 'Id' and 'MessageBody' keys only")
def test_keys(raw_response):
    output = prepare_messages(raw_response)
    expected_keys = ("Id", "MessageBody")
    assert all(tuple(x.keys()) == expected_keys for x in output)


@pytest.mark.it("Dict values are strings")
def test_values(raw_response):
    output = prepare_messages(raw_response)   
    assert all(
        all(isinstance(v, str) for v in x.values())  for x in output
    )

@pytest.mark.it("MessageBody JSON has required keys")
def test_message_body(raw_response):
    expected_keys = ("webPublicationDate", "webTitle", "webUrl")
    output = prepare_messages(raw_response) 
    assert all(
        tuple(loads(x['MessageBody']).keys()) == expected_keys for x in output
    )