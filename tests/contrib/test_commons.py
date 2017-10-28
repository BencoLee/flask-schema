#!/usr/bin/env python
# encoding: utf-8
import pytest

from flask_schema.contrib.commons import TreeNode


@pytest.mark.parametrize(
    "chains, search, expected_search",
    [
        (
            ["test1", "<name>", "first", "<int:id>"],
            ["test1", "<name>", "first", "<int:id>"],
            True
        ),
        (
            ["test1", "<name>", "first", "<int:id>"],
            ["test2", "<name>", "first", "<int:id>"],
            False
        )
    ]
)
def test_tire_tree(chains, search, expected_search):
    root = TreeNode("begin")
    TreeNode.insert(root, chains)
    assert TreeNode.search(root, search) == expected_search
