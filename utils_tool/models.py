#!/usr/bin/env python
# encoding: utf-8

import pymongo


class Transactions(object):

    def __init__(self, conn=None, method=None):
        if conn is None:
            self.conn = pymongo.MongoClient()
        else:
            self.conn = conn
        self.method = method

    def __getattr__(self, key):
        attr = getattr(self.conn, key)
        if callable(attr):
            if isinstance(attr, pymongo.database.Database):
                return Transactions(conn=attr)
            elif isinstance(attr, pymongo.collection.Collection):
                return Transactions(conn=attr)
            else:
                return Transactions(conn=self.conn, method=attr)
        return attr

    def __call__(self, *args, **kwargs):
        if self.method is None:
            return self.conn(*args, **kwargs)
        else:
            return self.method(*args, **kwargs)

    @property
    def collection(self):
        return self.conn.Transactions.transactions

    def insert_one(self, *args, **kwargs):
        doc = self.collection.insert_one(*args, **kwargs)
        return doc

    def fine_one_and_update(self, *args, **kwargs):
        doc = self.collection.find_one_and_update(*args, **kwargs)
        return doc
