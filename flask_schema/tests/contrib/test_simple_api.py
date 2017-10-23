#!/usr/bin/env python
# encoding: utf-8
import json
import pytest
import urllib
from flask import (
    jsonify, render_template, url_for,
    Blueprint, Flask
)
from flask_schema.contrib.base import FlaskAPIClass, Jar


flask_app = Flask(__name__)
jar = Jar(flask_app, __name__)
test1_bp = Blueprint("api_v1_test1", __name__, url_prefix="/api/v1/test1")
test2_bp = Blueprint("api_v1_test2", __name__, url_prefix="/api/v1/test2")
test3_bp = Blueprint("api_v1_test3", __name__, url_prefix="/api/v1/test3/<name>")
test4_bp = Blueprint("api_v1_test4", __name__, url_prefix="/api/v1/test4")
return_value = "<h1>Hello, World</h1>"


@jar.register(blueprint=test1_bp, resource="first")
class Test1API(FlaskAPIClass):

    def show(self, web_request, data, **kwargs):
        return return_value


@jar.register(blueprint=test2_bp, resource="second")
class Test2API(FlaskAPIClass):

    def show(self, web_request, data, **kwargs):
        return render_template("test.html")


@jar.register(blueprint=test3_bp, resources="third")
class Test3API(FlaskAPIClass):

    def show(self, web_request, data, id, name, **kwargs):
        return {"id": id, "name": name}


@jar.register(blueprint=test4_bp, resource="forth")
class Test4API(FlaskAPIClass):
    pass


@flask_app.route("/")
def url_map():
    links = []
    for rule in flask_app.url_map.iter_rules():
        options = {}
        for option in rule.arguments:
            options[option] = "[{0}]".format(option)
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        link = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        print link
        links.append(link)
    return jsonify(links)


@pytest.fixture
def client():
    return flask_app.test_client()


def test_api_show_first(client):
    url_path = "/api/v1/test1/first"
    r = client.get(url_path)
    assert json.loads(r.data) == return_value


def test_api_show_second(client):
    url_path = "/api/v1/test2/second"
    r = client.get(url_path)
    assert r.status_code == 200


def test_api_show_third(client):
    _id = 3
    _name = "test_name"
    url_path = "/api/v1/test3/{}/third/{}".format(_name, _id)
    r = client.get(url_path)
    r = json.loads(r.data)
    assert r == {
        "id": _id, "name": _name
    }


def test_api_raise_value_error():
    """
    same class name use different should raise ValueError
    """
    with pytest.raises(ValueError):
        @jar.register(blueprint=test1_bp, resource="first")
        class Test3API(FlaskAPIClass):
            pass


def test_jar_register_return_class():
    """
    same class name use different should raise ValueError
    """

    assert isinstance(Test4API(), FlaskAPIClass) == True
    assert issubclass(Test4API, FlaskAPIClass) == True


@pytest.mark.parametrize(
    "expect_value",
    [
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
                }
            },
            "/api/v1/test2/second": {
                "name": "second",
                "url_prefix": "/api/v1/test2",
                "rules": {
                    "show": {
                        "endpoint": "api_v1_test2_show",
                        "http_method": "GET",
                        "method_name": "show",
                    }
                }
            },
            "/api/v1/test3/<name>/third": {
                "name": "third",
                "url_prefix": "/api/v1/test3/<name>",
                "rules": {
                    "show": {
                        "endpoint": "api_v1_test3_show",
                        "http_method": "GET",
                        "method_name": "show",
                    }
                }
            },
            "/api/v1/test4/forth": {
                "name": "forth",
                "url_prefix": "/api/v1/test4",
                "rules": {}
            }
        }
    ]
)
def test_site_map(client, expect_value):
    url_path = "/site_maps"
    r = client.get(url_path)
    assert r.status_code == 200

    r = json.loads(r.data)
    assert isinstance(r, dict)
    assert r == expect_value
