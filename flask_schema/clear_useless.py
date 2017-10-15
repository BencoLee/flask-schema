#!/usr/bin/env python
# encoding: utf-8
import os
import logging

DIRECTORY = os.path.abspath(os.path.dirname(__file__))
LOGGER = logging.getLogger(__name__)


def remove_pyc_file(path=None):
    if path is None:
        path = DIRECTORY

    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith("pyc"):
                    os.remove(os.path.join(dirpath, filename))
    except AttributeError as e:
        LOGGER.debug(e)


remove_pyc_file()
