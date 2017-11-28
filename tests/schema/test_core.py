#!/usr/bin/env python
# encoding: utf-8
import pytest

from flask_schema.schema.core import InputSchemaBase


def methods_schema():
    return {
        "index": {
            "type": "object",
            "properties": {
                "description": {"type": "string",
                                "default": "This is index description"},
                "name": {"type": "string", "minLength": 4},
                "age": {"type": "integer", "minimum": 0},
                "id": {"type": "integer"}
            },
            "required": ["name", "age", "id"]
        }
    }


def valid_config_schema():
    return {
        "methods": methods_schema(),
    }


def invalid_config_schema():
    """Lack of resource or resources"""
    return {
        "method": methods_schema()
    }


@pytest.mark.parametrize(
    "config_schema, expected_input_valid, expected_methods_valid",
    [
        ([None], False, False),
        (invalid_config_schema(), False, False),
        (valid_config_schema(), True, True),
        (
            (lambda x: x["methods"]["index"].pop("properties") and x)(valid_config_schema()),
            True,
            True
        ),
        (
            (lambda x: x["methods"]["index"].pop("type") and x)(valid_config_schema()),
            True,
            False
        )
    ]
)
def test_raise_value_error(config_schema, expected_input_valid,
                           expected_methods_valid):
    schema_obj = InputSchemaBase(config_schema)
    schema_obj.check_schema_validation()
    assert schema_obj.is_valid_input_schema == expected_input_valid
    assert schema_obj.is_valid_methods_schema == expected_methods_valid


@pytest.mark.parametrize(
    "config_schema, validate_data, expected_value",
    [
        ([None], None, False),
        (valid_config_schema(), [None], False),
        (
            valid_config_schema(),
            {
                "methods": {
                    "index": {
                        "name": "ray",
                        "age": 18,
                        "id": 1
                    }
                },
            },
            False
        ),
        (
            valid_config_schema(),
            {
                "methods": {
                    "index": {
                        "name": "raytlty",
                        "age": 18,
                        "id": 1
                    }
                },
            },
            True
        )
    ]
)
def test_validate(config_schema, validate_data, expected_value):
    schema_obj = InputSchemaBase(config_schema)
    assert schema_obj.is_validate(validate_data) == expected_value
