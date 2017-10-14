#!/usr/bin/env python
# encoding: utf-8
import json
import pytest
import urllib
from flask import Blueprint, Flask, render_template, url_for

from flask_schema.contrib.base import FlaskAPIClass, Jar


flask_app = Flask(__name__)
jar = Jar(flask_app, __name__)
test1_bp = Blueprint("api_v1_test1", __name__, url_prefix="/api/v1/test1")
test2_bp = Blueprint("api_v1_test2", __name__, url_prefix="/api/v1/test2")
test3_bp = Blueprint("api_v1_test3", __name__, url_prefix="/api/v1/test3")
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

    def show(self, web_request, data, id, **kwargs):
        return id


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
    # return jsonify(links)


@pytest.fixture
def client():
    return flask_app.test_client()


def test_api_show_1(client):
    url_path = "/api/v1/test1/first"
    r = client.get(url_path)
    assert json.loads(r.data) == return_value


def test_api_show_2(client):
    url_path = "api/v1/test2/second"
    r = client.get(url_path)
    assert r.status_code == 200


def test_api_show_3(client):
    _id = 3
    url_path = "api/v1/test3/third/{}".format(_id)
    r = client.get(url_path)
    r = json.loads(r.data)
    assert int(r) == _id


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
    @jar.register(blueprint=test1_bp, resource="first")
    class Test4API(FlaskAPIClass):
        pass

    assert isinstance(Test4API(), FlaskAPIClass) == True
