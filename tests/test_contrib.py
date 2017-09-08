#!/usr/bin/env python
# encoding: utf-8
import pytest
import json
from flask import Blueprint, Flask

from contrib.base import FlaskAPIClass, Jar


flask_app = Flask(__name__)
jar = Jar(flask_app, __name__)
test_bp = Blueprint("api_v1_test", __name__, url_prefix="/api/v1/test")
return_value = "<h1>Hello, World</h1>"


@jar.register(blueprint=test_bp, resource="first")
class TestAPI(FlaskAPIClass):

    def show(self, web_request, data, **kwargs):
        return return_value


@pytest.fixture
def client():
    return flask_app.test_client()


def test_api_show(client):
    url_path = "/api/v1/test/first"
    r1 = client.get("/first")
    assert json.loads(r1.data) == return_value
