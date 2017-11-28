#!/usr/bin/env python
# encoding: utf-8
import os
from setuptools import setup, find_packages


# FLASK_SCHEMA_DIR = os.path.join(
    # os.path.abspath(os.path.dirname(__file__)),
    # "flask_schema"
# )


setup(
    name="flask_schema",
    version="0.0.1",
    packages=["flask_schema", "cli", "sdk", "tests"],
    # packages=find_packages(FLASK_SCHEMA_DIR),
    url="https://github.com/BencoLee/flask_schema",
    description="Flask Schema Tools",
)
