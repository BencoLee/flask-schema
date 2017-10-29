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


@pytest.mark.parametrize(
    "chains1, chains2, expected_search, expected_num",
    [
        (
            ["test1", "<name>", "first", "<int:id>"],
            ["test1", "<name>", "second"],
            "test1/<name>",
            2
        )
    ]
)
def test_tree_node(chains1, chains2, expected_search, expected_num):
    root = TreeNode("begin")
    TreeNode.insert(root, chains1)
    TreeNode.insert(root, chains2)
    node = root
    for item in expected_search.split("/"):
        node = getattr(node.children, item)
    assert len(node.children) == expected_num
