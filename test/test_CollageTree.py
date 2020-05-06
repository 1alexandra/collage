from src.CollageTree import CollageRoot, ResizableLeaf
from src.Collage import Collage
from src.CollageImage import safe_open_image
from src.scroll import ScrolledFrame

import pytest
import os
import tkinter as tk


@pytest.fixture
def filename():
    return os.path.join('test', 'files', 'kotya.jpg')


@pytest.fixture
def collage():
    collage = Collage(0, 1, 1, None, [], {'width': 30, 'height': 30})
    return collage


@pytest.fixture
def collage_root(collage):
    return collage.get_collage_root()


@pytest.fixture
def collage_image(filename, collage):
    return safe_open_image(filename, collage.get_corners())


def test_init(collage_root):
    assert collage_root.get_width() == 30
    assert collage_root.get_height() == 30


def count_vertices(root):
    res = 1
    if root.get_left() is not None:
        res += count_vertices(root.get_left())
    if root.get_right() is not None:
        res += count_vertices(root.get_right())
    return res


def count_leafs(root):
    res = int(type(root) == ResizableLeaf)
    if root.get_left() is not None:
        res += count_leafs(root.get_left())
    if root.get_right() is not None:
        res += count_leafs(root.get_right())
    return res


def test_vertices_count_add(collage_root, collage_image):
    sides = ['n', 'e', 'w', 's']
    for i in range(1, 3 * len(sides) + 1):
        cur_side = sides[i % len(sides)]
        collage_root.add_image(image=collage_image, where=cur_side)
        vertices = count_vertices(collage_root)
        leafs = count_leafs(collage_root)
        assert vertices == 2 * i
        assert leafs == i


def test_vertices_count_remove(collage_root, collage_image):
    def get_some_leaf(root):
        if type(root) == ResizableLeaf:
            return root
        return get_some_leaf(root.get_left())

    sides = ['n', 'e', 'w', 's']
    for i in range(1, 3 * len(sides) + 1):
        cur_side = sides[i % len(sides)]
        collage_root.add_image(image=collage_image, where=cur_side)

    for i in range(3 * len(sides) - 1, 0, -1):
        leaf = get_some_leaf(collage_root)
        leaf.destroy()

        vertices = count_vertices(collage_root)
        leafs = count_leafs(collage_root)

        assert vertices == 2 * i
        assert leafs == i
