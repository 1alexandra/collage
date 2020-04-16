from collage.Collage import Collage
from collage.CollageImage import PILCollageImage
import pytest
import os


@pytest.fixture
def filename():
    return os.path.join('test', 'files', 'kotya.jpg')


@pytest.fixture
def collage_image(filename):
    collage = Collage(1, [], {})
    return PILCollageImage(os.path.join(filename), [0, 0], 10, 10, collage)


def test_init(collage_image):
    assert collage_image.PhotoImage is not None
    assert collage_image.Width == 10
    assert collage_image.Height == 10


def test_resize(collage_image):
    collage_image.resize((100, 150))
    assert collage_image.Width == 100
    assert collage_image.Height == 150
