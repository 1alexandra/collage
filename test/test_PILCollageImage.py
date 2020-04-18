from src.Collage import Collage
from src.CollageImage import PILCollageImage
from src.CornerCreator import CornerCreator

import pytest
import os


@pytest.fixture
def filename():
    return os.path.join('test', 'files', 'kotya.jpg')


@pytest.fixture
def collage_image(filename):
    collage = Collage(1, 1, 1, [], {})
    corners = CornerCreator(1, 1)
    return PILCollageImage(os.path.join(filename), [0, 0], 10, 10,
                           corners, collage)


def test_init(collage_image):
    assert collage_image.PhotoImage is not None
    assert collage_image.Width == 10
    assert collage_image.Height == 10


def test_resize(collage_image):
    collage_image.resize((100, 150))
    assert collage_image.Width == 100
    assert collage_image.Height == 150
