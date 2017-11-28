#!/usr/bin/env python
# encoding: utf-8
import re
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


def parser_rule(rule):
    _rule_re = re.complie(r'''
        (?P<static>[^<]*)
        <
        (?:
            (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)
            (?:\((?P<args>.*?)\))?
        )?
        (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)
    ''', re.VERBOSE)

    pos, end = 0, len(rule)
    do_match = _rule_re.match
    user_names = set()
    while pos < end:
        m = do_match(rule, pos)
        if m is None:
            break
        data = m.groupdict()
        if data['static']:
            yield None, None, data['static']
        variable = data['variable']
        converter = data.get('converter') or 'default'
        if variable in user_names:
            raise ValueError('variable name %r used twice' % variable)
        user_names.add(variable)
        yield converter, data.get('args'), variable
        pos = m.end()
    if pos < end:
        remaining = rule[pos:]
        if '<' in remaining or '>' in remaining:
            raise ValueError('malformed url rule: %r' % rule)
        yield None, None, remaining
