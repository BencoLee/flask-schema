#!/usr/bin/env python
# encoding: utf-8


class Singleton(type):

    def __init__(self, name, bases, attrs):
        super(Singleton, self).__init__(name, bases, attrs)
        self._registers = {}

    def __call__(self, *args, **kwargs):
        if self not in self._registers:
            obj = super(Singleton, self).__call__(*args, **kwargs)
            self._registers[self] = obj
        return self._registers[self]


def action(action_name, action_method):
    def wrapper(func):
        func.__is_action__ = True
        func.__action_name = action_name
        func.__action_method = action_method
        return func
    return wrapper


if __name__ == "__name__":
    @action("foo", "bar")
    def test(*args, **kwargs):
        print args, kwargs


    print dir(test)
    print test.__dict__
    print test.__name__
