#!/usr/bin/env python
# encoding: utf-8

from flask_schema.contrib.utils import Singleton


def test_singleton():

    class TestClass(object):
        __metaclass__ = Singleton

    obj1 = TestClass()
    obj2 = TestClass()

    assert obj1 == obj2
