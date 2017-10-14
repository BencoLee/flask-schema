#!/usr/bin/env python
# encoding: utf-8
import os
from setuptools import setup, find_packages


setup(
    name="flask_schema",
    version="0.0.1",
    packages=find_packages(
        os.path.abspath(os.path.dirname(__file__))),
    url="https://github.com/BencoLee/flask_schema",
    description="Flask Schema Tools",
)
