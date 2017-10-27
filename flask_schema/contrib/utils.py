#!/usr/bin/env python
# encoding: utf-8
import requests


class Singleton(type):

    def __init__(self, name, bases, attrs):
        super(Singleton, self).__init__(name, bases, attrs)
        self._registers = {}

    def __call__(self, *args, **kwargs):
        if self not in self._registers:
            obj = super(Singleton, self).__call__(*args, **kwargs)
            self._registers[self] = obj
        return self._registers[self]


class SimpleClient(object):

    __metaclass__ = Singleton

    session = None

    def __new__(cls, *args, **kwargs):
        obj = super(SimpleClient, cls).__new__(cls, *args, **kwargs)
        if cls.session is None:
            cls.session = requests.Session()
        return obj

    def get_site_maps(self):
        url = "http://localhost:5000/site_maps"
        resp = self.session.get(url)
        return resp.json()


def extra_action(action_name, action_method):
    def wrapper(func):
        func.__is_action__ = True
        func.__action_name = action_name
        func.__action_method = action_method
        return func
    return wrapper
