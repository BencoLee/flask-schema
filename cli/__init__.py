#!/usr/bin/env python
# encoding: utf-8

import argparse
import logging
import re

from flask_schema.cli.constants import (
    CONVERT_VARIABLE_PATTERN
)
from flask_schema.contrib.commons import ProxyNode, ResClient

"""
/api/v1/test1/resource1
/api/v1/test1/<int:id>/resource2
"""


template_argument = {
    "positional": None,
    "optional": None,
    "help": "",
    "type": ""
}

convert_value_re = re.complie(CONVERT_VARIABLE_PATTERN, re.VERBOSE)


def get_send_requests():
    def _wrapper()


def split_paths(url, urlprefix_ignore="/api/v1"):
    url = url.split(urlprefix_ignore)[-1]
    return [path for path in url.split("/") if path]


def convert_type_to_value(matched):
    convert, value = matched.groupdict().values()
    if convert not in ("str", "int", "float", "bool"):
        logging.warning("Convert type maybe dangerous: %s" % convert)

    try:
        value = eval("{}({})".format(convert, value))
    except TypeError as e:
        logging.warning("TypeError {}".format(e))

    return convert, value


class CommandLineTool(object):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.is_last = False
        self.children = ProxyNode()
        self.parser = argparse.ArgumentParser()

    @property
    def subparser(self):
        if hasattr(self, "_subparser"):
            return self._subparser
        else:
            return self.parser.add_subparsers()

    @subparser.setter
    def subparser(self, parser):
        self._subparser = parser

    @staticmethod
    def insert(root, url, support_methods):
        node, paths = root, split_paths(url)
        extra_keyword = []
        for path in paths:
            if path not in node.children:
                res = CommandLineTool.insert_to_node(node, path)
                if isinstance(res, tuple):
                    extra_keyword.append({
                        "positional": path,
                        "type": res[0],
                        "help": "{} resource need {}".format(node.name, path),
                        "value": res[1]
                    })
                    continue
            node = getattr(node.children, path)
        for method, properties in support_methods:
            CommandLineTool.insert_into_node(node, method)
            method_node = getattr(node.children, method)
            CommandLineTool.add_arguments(method_node, properties, extra_keyword)

        node.is_last = True

    @staticmethod
    def insert_into_node(node, path):
        if path.startswith("<") and path.endswith(">"):
            matched = convert_value_re.match(path)
            if matched:
                convert, value = convert_type_to_value(matched)
            else:
                raise ValueError("Checkout {} not a"
                                 "legal string".format(path))
            return (convert, value)

        parser = node.subparser.add_parser(path)
        sub_node = CommandLineTool(path)
        sub_node.subparser = parser
        setattr(node.children, path, sub_node)

    @staticmethod
    def add_arguments(node, properties, extra_keyword):
        positional = properties["positional"]
        optional = properties["optional"]

        parser = node.subparser
        parser.set_default(__function=get_send_requests())
        for name, help in optional:
            if not name.startswith("--"):
                name = "--{}".format(name)
            parser.add_argument(name, help=help)

        for name, help in positional:
            parser.add_argument(name, help=help)

        for keyword in extra_keyword:
            positional = keyword.pop("positional")
            optional = keyword.get("optional")
            if optional:
                kwargs = {
                    name: "--{}".format(optional)
                    if not optional.startswith("--") else optional,
                    help: keyword.get("help", "optional argument")
                }
                if keyword.get("type"):
                    kwargs["type"] = keyword.get("type")
            elif positional:
                kwargs = {
                    name: positional,
                    help: keyword.get("help", "positional argument")
                }
                if keyword.get("type"):
                    kwargs["type"] = keyword.get("type")
            parser.add_argument(**kwargs)

    @staticmethod
    def execute(root):
        args = root.parser.parse_args()
        if hasattr(args, "__function"):
            return args.__function(**vars(args))
        else:
            return args
