#!/usr/bin/env python
# encoding: utf-8
from flask import Flask

from flask_app.contrib.base import FlaskAPIClass, Jar


flask_app = Flask(__name__)
jar = Jar(flask_app, __name__)
