import logging

import pytest

from lambda_app.lambda_utils import validate_event


@pytest.mark.it("Return none when event contains valid SearchTerm and no FromDate")
def test_return_none_search():
    event = {'SearchTerm': "egg"}
    output = validate_event(event)
    assert output is None


@pytest.mark.it("Return none when event contains valid SearchTerm and valid FromDate")
def test_return_none_date():
    event = {'SearchTerm': "egg", "FromDate": "2014-02-16"}
    output = validate_event(event)
    assert output is None


@pytest.mark.it("Raises assertion error when search term isn't string")
def test_raises_err_search():
    for x in [{}, [], (), 1, True]:
        with pytest.raises(AssertionError, match="SearchTerm must be a string."):
            validate_event({'SearchTerm': x})


@pytest.mark.it("Raises assertion error when from date doesn't match yyyy-mm-dd format")
def test_raises_err_date():
    event = {'SearchTerm': "egg", "FromDate": "20-02-1608"}
    with pytest.raises(AssertionError, match="FromDate must match the format yyyy-mm-dd, e.g. 2014-02-16."):
        validate_event(event)