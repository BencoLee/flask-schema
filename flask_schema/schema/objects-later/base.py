#!/usr/bin/env python
# encoding: utf-8
"""
TODO will be provide later
"""


class MetaType(type):

    def __new__(cls, name, bases, attrs):
        return super(cls, MetaType).__new__(cls, name, bases, attrs)


class BaseType(object):
    __metaclass__ = MetaType
