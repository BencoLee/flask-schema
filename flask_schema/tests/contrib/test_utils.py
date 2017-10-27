#!/usr/bin/env python
# encoding: utf-8

from flask_schema.contrib.utils import Singleton, SimpleClient


def test_singleton():

    class TestClass(object):
        __metaclass__ = Singleton

    obj1 = TestClass()
    obj2 = TestClass()

    assert obj1 == obj2


def test_simple_client():

    c1 = SimpleClient()
    c2 = SimpleClient()

    assert id(c1) == id(c2)
    assert c1 == c2
    assert c1 is c2
    assert c1.session == c2.session
    assert id(c1.session) == id(c2.session)
