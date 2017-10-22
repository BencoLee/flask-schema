#!/usr/bin/env python
# encoding: utf-8
import logging
from jsonschema.exceptions import SchemaError, ValidationError


class SchemaBase(object):

    @staticmethod
    def _is_valid_schema(validator, schema_rule, validate_schema):
        try:
            validator.check_schema(validate_schema)
            validator_executor = validator(schema_rule)
            validator_executor.validate(validate_schema)
        except (SchemaError, ValidationError) as e:
            logging.warning(e)
            return False
        else:
            return True

    @staticmethod
    def _is_valid_data(validator, validate_schema, validate_data):
        try:
            validator_executor = validator(validate_schema)
            validator_executor.validate(validate_data)
        except ValidationError as e:
            logging.warning(e)
            return False
        else:
            return True

    def is_validate(self, validate_data):
        raise NotImplementedError

    def get_method_from_schema(self, selection):
        raise NotImplementedError

    def check_schema_validation(self):
        raise NotImplementedError
