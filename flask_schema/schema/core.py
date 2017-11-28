#!/usr/bin/env python
# encoding: utf-8
import logging
from functools import partial
from jsonschema import Draft4Validator

from flask_schema.schema.base import SchemaBase


class MethodNotSupportError(KeyError):
    pass


class InputSchemaBase(SchemaBase):
    _input_validation = {
        "type": "object",
        "properties": {
            "methods": {"type": "object"},
        },
        "required": ["methods", ],
        "additionalProperties": "false"
    }

    _method_validation = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "help": {"type": "string"},
            "properties": {"type": "object"},
            "required": {"type": "array"}
        },
        "required": ["type", ],
        "additionalProperties": "true"
    }

    def __init__(self, input_schema, validator=None, **kwargs):
        self.input_schema = input_schema
        if validator is None:
            self.validator = Draft4Validator
        else:
            self.validator = validator

        self.is_valid_input_schema = False
        self.is_valid_methods_schema = False
        self.check_schema_validation()

    def get_method_from_schema(self, selection):
        """
        :param selection: <str> specific method schema
        :return: <dict> schema of method dict
        """
        methods = self.input_schema["methods"]
        try:
            method_schema = methods[selection]
        except KeyError:
            raise MethodNotSupportError(
                "Input schema don't have "
                "{} method".format(selection))
        else:
            return method_schema

    def get_methods_schema(self):
        return self.input_schema.get("methods", None)

    def check_schema_validation(self):
        input_schema, validator = self.input_schema, self.validator
        validate_func = partial(self._is_valid_schema, validator)
        method_validate = partial(validate_func, self._method_validation)

        self.is_valid_input_schema = validate_func(
            self._input_validation, input_schema)

        if not (self.is_valid_input_schema and
                self.input_schema.get("methods")):
            self.is_valid_methods_schema = False
            return

        for method_schema in self.input_schema["methods"].values():
            if not method_validate(method_schema):
                self.is_valid_methods_schema = False
                break
        else:
            self.is_valid_methods_schema = True

    def is_validate(self, validate_data):

        if not isinstance(validate_data, dict):
            return False

        if not (self.is_valid_input_schema and
                self.is_valid_methods_schema):
            return False

        validator = self.validator
        method_validate = partial(self._is_valid_data, validator)
        if len(validate_data) == 1 and "methods" in validate_data:
            validate_data = validate_data.get("methods", None)
            if not validate_data:
                return False

        for key, value in validate_data.iteritems():
            try:
                method_schema = self.get_method_from_schema(key)
            except MethodNotSupportError as e:
                logging.warning(e)
                return False
            else:
                if not method_validate(method_schema, value):
                    return False
        return True


class OutputSchemaBase(SchemaBase):
    pass
