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
