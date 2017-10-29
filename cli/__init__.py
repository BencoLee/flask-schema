#!/usr/bin/env python
# encoding: utf-8

from flask_schema.contrib.commons import TreeNode


class CommandLineTool(TreeNode):

    def __init__(self, name, *args, **kwargs):

