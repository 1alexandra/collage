from src.CollageTree import ResizableLeaf
from src.Collage import Collage
from src.CollageImage import safe_open_image
from PIL import Image
from PIL import ImageChops

import pytest
import os


BORDER_WIDTH = 2


@pytest.fixture
def filename():
    return os.path.join('test', 'files', 'kotya.jpg')


@pytest.fixture
def collage_filename():
    return os.path.join('test', 'files', 'collage.png')


@pytest.fixture
def collage():
    collage = Collage(2, BORDER_WIDTH, 1, 1, None, [], {'width': 99, 'height': 99})
    collage.grid(row=0, column=0)
    return collage


@pytest.fixture
def collage_root(collage):
    return collage.get_collage_root()


@pytest.fixture
def collage_image(filename, collage):
    return safe_open_image(filename, collage.get_corners())


@pytest.fixture
def collage_images(filename, collage):
    return [safe_open_image(filename, collage.get_corners()) for _ in range(12)]


def test_init(collage_root):
    assert collage_root.get_width() == 99
    assert collage_root.get_height() == 99


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


def check_window_sizes(tree):
    if tree.get_left() is not None:
        left = tree.get_left()
        right = tree.get_right()
        assert abs(left.get_width() - right.get_width()) <= 1
        assert abs(left.get_height() - right.get_height()) <= 1
        total_width = left.get_width() + right.get_width() + BORDER_WIDTH
        total_height = left.get_height() + right.get_height() + BORDER_WIDTH
        assert total_width == tree.get_width() or total_height == tree.get_height()
        check_window_sizes(left)
        check_window_sizes(right)


def test_windows_size(collage_root, collage_images):
    sides = ['n', 'e', 'w', 's']
    for i in range(1, 6):
        cur_side = sides[i % len(sides)]
        collage_root.add_image(image=collage_images[i - 1], where=cur_side)
    collage_root.get_tk_object().update()
    check_window_sizes(collage_root.get_left())


def test_save_collage(collage_root, collage_images, collage_filename):
    sides = ['n', 'e', 'w', 's']
    for i in range(1, 6):
        cur_side = sides[i % len(sides)]
        collage_root.add_image(image=collage_images[i - 1], where=cur_side)
    collage_root.get_tk_object().update()
    save_path = os.path.join('test', 'files', 'collage_new.png')

    collage_root.save_collage(save_path)
    true_collage = Image.open(collage_filename)
    test_collage = Image.open(save_path)
    diff = ImageChops.difference(true_collage, test_collage)
    assert not diff.getbbox()


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
