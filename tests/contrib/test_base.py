#!/usr/bin/env python
# encoding: utf-8
import pytest
from flask import Flask

from flask_schema.contrib.base import FlaskAPIClass, Jar


flask_app = Flask(__name__)


def test_singleton_jar():
    jar1 = Jar(flask_app, "jar1")
    jar2 = Jar(flask_app, "jar2")

    assert jar1 == jar2
    assert jar1 is jar2
    assert id(jar1) == id(jar2)
