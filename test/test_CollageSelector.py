from collage.Collage import Collage
from collage.CollageItem import CollageItem
from collage.CollageSelector import CollageSelector
import pytest


@pytest.fixture()
def selector():
    collage = Collage(0, 1, 1, [], {})
    item = CollageItem(collage.create_rectangle(1, 1, 3, 3), collage)
    selector = CollageSelector(item)
    return selector


def test_init(selector):
    assert not selector.is_selected
    assert selector.collage.coords(selector.collage.selection_rectangle_id) == [0.0, 0.0, 0.0, 0.0]


def test_set_selection(selector):
    selector.set_selection()
    assert selector.is_selected
    # borders of item is rectangle with width and height greater by 1 px than item's width and height
    assert selector.collage.coords(selector.collage.selection_rectangle_id) == [0.0, 0.0, 4.0, 4.0]


def test_unset_selection(selector):
    selector.set_selection()
    selector.unset_selection()
    assert not selector.is_selected
    assert selector.collage.coords(selector.collage.selection_rectangle_id) == [0.0, 0.0, 0.0, 0.0]


def apply_selection(selector):
    selector.apply_selection()
    assert selector.is_selected
    selector.apply_selection()
    assert not selector.is_selected


def reset_selection(selector):
    selector.reset_selection()
    assert not selector.is_selected

    selector.set_selection()
    selector.reset_selection()
    assert not selector.is_selected
