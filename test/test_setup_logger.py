import logging

import pytest

from lambda_app.lambda_utils import setup_logger, JSONFormatter


def test_returns_logger():
    output = setup_logger("test logger")
    assert isinstance(output, logging.Logger)


def test_logger_handler_has_json_formatter():
   logger = setup_logger("test logger")
   handler = logger.handlers[0]
   formatter = handler.formatter
   assert isinstance(formatter, JSONFormatter)


def test_logger_level_is_debug():
   logger = setup_logger("test logger")
   assert logger.level == 10