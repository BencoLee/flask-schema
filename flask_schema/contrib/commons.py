#!/usr/bin/env python
# encoding: utf-8
'''
EXAMPLES:
        {
            "/api/v1/test1/first": {
                "name": "first",
                "url_prefix": "/api/v1/test1",
                "rules": {
                    "show": {
                        "endpoint": "api_v1_test1_show",
                        "http_method": "GET",
                        "method_name": "show",
                    }
                },
                "input_schema": {
                    "show": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "id": {"type": "integer"},
                            "age": {"type": "integer"}
                        }
                    }
                }
            }
'''
import requests
from flask_schema.contrib.utils import Singleton


class ProxyNode(dict):

    """Lazy"""

    def __getattr__(self, key):
        value = self.get(key, None)
        if isinstance(value, dict):
            value = ProxyNode(value)
        if (callable(value) and
                not isinstance(value, ProxyNode)):
            value = value()
        return value

    def __setattr__(self, key, value):
        self.update({key: value})
        return self

    def __contains__(self, key):
        return key in self.keys()


class TreeNode(object):

    """Trie Tree"""

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.is_last = False
        self.children = ProxyNode()

    @staticmethod
    def search(root, chains):
        node = root
        for key in chains:
            if key in node.children:
                node = getattr(node.children, key)
        return True if node and node.is_last else False

    @staticmethod
    def insert(root, chains):
        node = root
        for key in chains:
            if key not in node.children:
                setattr(node.children, key, TreeNode(key))
            node = getattr(node.children, key)
        node.is_last = True


class URLResourceTree(object):

    __metaclass__ = Singleton

    def __init__(self, url_prefix="/api/v1"):
        self.tree_root = TreeNode(url_prefix)

    @staticmethod
    def _reduce_url_prefix(urls, url_prefix):
        return map(lambda x: x.split(url_prefix)[-1], urls)

    def build_url_tree(self, urls):
        for url in self._reduce_url_prefix(urls, self.url_prefix):
            url_list = url.split('/')
            TreeNode.insert(self.tree_root, url_list)


class ResClient(object):

    __metaclass__ = Singleton

    def __init__(self, host="localhost", port=8888):
        self.host = host
        self.port = port
        self.headers = {"Content-type": "application/json"}
        self.session = requests.Session()

    def generate_url(self, url, kwargs):
        pass

    def send_requests(self, url, method, kwargs=None, headers=None):
        pass
