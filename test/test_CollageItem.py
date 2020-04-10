from collage.CollageItem import CollageItem
from collage.Collage import Collage
import pytest


@pytest.fixture()
def collage_item():
    collage = Collage(1, [], {})
    return CollageItem(collage.create_rectangle(0, 0, 0, 0), collage)


def test_Id():
    collage = Collage(1, [], {})
    id = collage.create_rectangle(0, 0, 0, 0)
    item = CollageItem(id, collage)
    assert item.Id == id


def test_Pos(collage_item):
    assert collage_item.Pos == [0.0, 0.0, 0.0, 0.0]


def test_move(collage_item):
    assert collage_item.move(0, 0) is None


def test_IsSelected(collage_item):
    assert not collage_item.IsSelected
    collage_item.set_selection()
    assert collage_item.IsSelected


def test_apply_selection(collage_item):
    collage_item.apply_selection()
    assert collage_item.IsSelected
    collage_item.apply_selection()
    assert not collage_item.IsSelected


def test_reset_selection(collage_item):
    collage_item.reset_selection()
    assert not collage_item.IsSelected

    collage_item.set_selection()
    collage_item.reset_selection()
    assert collage_item.IsSelected


def test_set_selection(collage_item):
    collage_item.set_selection()
    assert collage_item.IsSelected

    collage_item.set_selection()
    assert collage_item.IsSelected


def unset_selection(collage_item):
    collage_item.set_selection()
    collage_item.unset_selection()
    assert not collage_item.IsSelected

    collage_item.unset_selection()
    assert not collage_item.IsSelected
