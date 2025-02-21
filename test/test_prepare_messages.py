from json import load, loads
from string import ascii_letters, digits

import pytest

from lambda_app.lambda_utils import prepare_messages


### Fixtures ###

@pytest.fixture()
def raw_response():
    with open("test/test_data/raw_response.json", "r") as jsizzle:
        raw_response = load(jsizzle)
    return raw_response


@pytest.fixture()
def raw_response_empty():
    with open("test/test_data/raw_response_empty.json", "r") as jsizzle:
        raw_response_empty = load(jsizzle)
    return raw_response_empty


### Tests ###

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
    required_keys = ("Title", "Section", "PublicationDate",  "WordCount", "Url", "Preview")
    output = prepare_messages(raw_response) 
    assert all(
        tuple(loads(x['MessageBody']).keys()) == required_keys for x in output
    )


@pytest.mark.it("Returns empty list when response contains no results")
def test_handles_empty_response(raw_response_empty):
    output = prepare_messages(raw_response_empty) 
    assert output == []


@pytest.mark.it("Message Ids are unique")
def test_message_ids_unique(raw_response):
    output = prepare_messages(raw_response)
    message_ids = [x["Id"] for x in output]
    assert len(message_ids) == len(set(message_ids))


@pytest.mark.it("Message Ids meet char stipulations")
def test_message_ids_stipulations(raw_response):
    '''
    An id can only contain alphanumeric characters, hyphens and underscores. 
    It can be at most 80 letters long."
    '''
    valid_chars = ascii_letters + digits + '-_'
    output = prepare_messages(raw_response)
    message_ids = [x["Id"] for x in output]
    for id in message_ids:
        assert len(id) < 81
        assert all(char in valid_chars for char in id)


@pytest.mark.it("Previews are > 1001 chars ")
def test_summary_limit(raw_response):
    '''
    An id can only contain alphanumeric characters, hyphens and underscores. 
    It can be at most 80 letters long."
    '''
    output = prepare_messages(raw_response)
    previews = [loads(x["MessageBody"])["Preview"] for x in output]
    for preview in previews:
        assert len(preview) < 1001


