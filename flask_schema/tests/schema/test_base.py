#!/usr/bin/env python
# encoding: utf-8
import pytest
from flask_schema.schema.base import SchemaBase


@pytest.fixture
def schema_base():
    return SchemaBase()


def test_without_config_and_data(schema_base):
    schema_base.check_schema()
    assert schema_base.check_config_schema is False


def test_raise_value_error(schema_base):
    schema_base.config_schema = list()
    with pytest.raises(ValueError):
        schema_base.check_schema()


def test_validate_false(schema_base):
    # One
    schema_base.config_schema = list()
    assert schema_base.is_validate() == False

    # Two
    config_schema = {
        "type": "object",
        "properties": {
            "index": {
                "type": "object",
                "properties": {
                    "description": "This is index description",
                    "name": {"type": "string", "minLength": 4},
                    "age": {"type": "integer", "minimum": 0},
                    "id": {"type": "integer"}
                }
            }
        }
    }
    schema_base.config_schema = config_schema
    assert schema_base.is_validate() == False


