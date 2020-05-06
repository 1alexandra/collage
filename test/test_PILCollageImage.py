from src.Collage import Collage
from src.CollageImage import PILCollageImage
from src.CornerCreator import CornerCreator
from src.CollageImage import safe_open_image

import pytest
import os


@pytest.fixture
def filename():
    return os.path.join('test', 'files', 'kotya.jpg')


@pytest.fixture
def collage():
    collage = Collage(0, 1, 1, [], {'width': 30, 'height': 30})
    return collage


@pytest.fixture
def collage_image(filename, collage):
    img = safe_open_image(filename, collage.get_corners())
    img.resize((10, 10))
    return img


def test_init(collage_image):
    assert collage_image.PhotoImage is not None
    assert collage_image.PhotoImage.width() == 10
    assert collage_image.PhotoImage.height() == 10


def test_resize(collage_image):
    collage_image.resize((100, 150))
    assert collage_image.PhotoImage.width() == 100
    assert collage_image.PhotoImage.height() == 150


def test_big_resize(collage_image):
    collage_image.resize((1000, 800))
    assert collage_image.PhotoImage.width() == 960
    assert collage_image.PhotoImage.height() == 768
    assert 2 * collage_image.corner[0] + collage_image.PhotoImage.width() == 1000
    assert 2 * collage_image.corner[1] + collage_image.PhotoImage.height() == 800
