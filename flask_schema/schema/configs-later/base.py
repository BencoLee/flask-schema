#!/usr/bin/env python
# encoding: utf-8


class Configuration(object):

    schema = {
        "type": "object",
        "properties": {
            "methods": {"type": "object"},
            "resources": {"type": "string"},
            "resource": {"type": "string"}
        },
        "oneOf": [
            {"required": ["resource", ]},
            {"required": ["resources", ]}
        ],
        "required": ["methods", ],
        "additionalProperties": "true"
    }


