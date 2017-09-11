#!/usr/bin/env python
# encoding: utf-8
import jsonschema
import logging
from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidatError, SchemaError


class Configuration(object):

    _schema = {
        "type": "object",
        "properties": {
            "methods": {"type": "object"},
            "resource": {"type": "string"},
            "resources": {"type": "string"}
        },
        "oneOf": [
            {"required": ["resource", ]},
            {"required": ["resources", ]}
        ],
        "required": ["methods"],
        "additionalProperties": "true"
    }

    def __init__(self, config_schema=None, validate_data=None, validator=None, **kwargs):
        if validator is None:
            self.validator = Draft4Validator
        else:
            self.validator = validator
        self.config_schema = config_schema
        self.validate_data = validate_data
        self.check_config_schema = True

    def check_schema(self):
        if self.config_schema is None:
            self.check_config_schema = False
        schema_rule = self.config_schema
        if not self.check_config_schema:
            schema_rule = self._schema
        if not schema_rule or not isinstance(schema_rule, dict):
            raise ValueError("{} should be an instance of type dict".format(schema_rule))

        # May raise SchemaError if check illegal schema
        self.validator.check_schema(self._schema)

    @property
    def schema_form_checked(self):
        return self._schema_form_checked

    @schema_form_checked.setattr
    def schema_form_checked(self, checked_sign=False):
        self._schema_form_checked = checked_sign

    def validate(self):
        """
        First step: check schema is legal or not
        Second step: if check_config_schema is True, should check the validate_data
                     otherwise should raise ValidatError
        Third step: validator_executor = Draft4Validator(self.config_schema) and use executor
                    validate data
        """
        try:
            self.check_schema()
        except (ValueError, SchemaError) as e:
            logging.exception(e)
            return False
        else:
            if self.check_config_schema is False and self.validate_data:
                raise ValidatError("")
            validator_executor = Draft4Validator(self.config_schema)
            try:
                validator_executor.validate(self)
