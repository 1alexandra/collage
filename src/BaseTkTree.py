import tkinter as tk
from src.utils import is_up_left, is_up_bottom, ask_open_image, safe_open_image


def get_orient(where):
    return tk.VERTICAL if is_up_bottom(where) else tk.HORIZONTAL


class BaseTkTreeNode:
    def __init__(self, obj_class, parent, width, height, corner_creator, tk_master=None, bg='white', **special_kwargs):
        self._root = None

        self._obj_class = obj_class
        self._parent = parent

        self._bg = bg
        self._width = width
        self._height = height

        self._corner_creator = corner_creator
        self._special_kwargs = special_kwargs

        self._left = None
        self._right = None

        self._create_tk_object(tk_master=tk_master)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def _resize_handler(self, event):
        pass

    def _create_tk_object(self, tk_master=None):
        if self._root is not None:
            del self._root
        master = self._parent.get_tk_object() if tk_master is None else tk_master
        self._root = self._obj_class(
            master=master, width=self._width, height=self._height, bg=self._bg, **self._special_kwargs)
        self._root.bind('<Configure>', self._resize_handler)

    def get_tk_object(self):
        return self._root


class BreedingTkNode(BaseTkTreeNode):
    def replace_child(self, old_child, new_child):
        if self._left is old_child:
            if self._left is not None:
                self._root.forget(self._get_left_child_internal())

            self._left = new_child
            self._root.add(self._left.get_tk_object())

            if self._right is not None:
                self._root.paneconfigure(self._get_right_child_internal(), before=self._get_left_child_internal())
        elif self._right is old_child:
            if self._right is not None:
                self._root.forget(self._get_right_child_internal())
            self._right = new_child
            self._root.add(self._right.get_tk_object())
        else:
            assert False

    def add_child(self, child, begin=False):
        self.replace_child(old_child=None, new_child=child)
        if begin and self._right is not None:
            self._root.paneconfigure(self._get_right_child_internal(), before=self._get_left_child_internal())
            self._left, self._right = self._right, self._left

    def add_image_child(self, image_node_class, image, where):
        width = self._width
        height = self._height
        if self._left is not None:
            if is_up_bottom(where):
                height //= 2
            else:
                width //= 2
        leaf_node = image_node_class(
            image, self._corner_creator, parent=self, width=width, height=height, bg=self._bg, bd=-2
        )
        self.add_child(leaf_node, begin=is_up_left(where))
        if self._right is not None:
            self._align_children()

    def _forget_children(self):
        if self._left is not None:
            self._root.forget(self._left.get_tk_object())
        if self._right is not None:
            self._root.forget(self._right.get_tk_object())

    def _display_children(self):
        if self._left is not None:
            self._root.add(self._left.get_tk_object())
        if self._right is not None:
            self._root.add(self._right.get_tk_object())

    def _align_children(self):
        if self._right is not None:
            sep_width = self._root['sashwidth']
            self._root.update()
            self._set_child_window_size(
                self._left,
                width=(self._width - sep_width) // 2,
                height=(self._height - sep_width) // 2
            )
            self._root.update()

    def _get_left_child_internal(self):
        if len(self._root.panes()) > 0:
            return self._root.panes()[0]

    def _get_right_child_internal(self):
        if len(self._root.panes()) > 1:
            return self._root.panes()[1]

    def _set_child_window_size(self, child, width, height):
        child_internal = None
        if self._left is child:
            child_internal = self._get_left_child_internal()
        elif self._right is child:
            child_internal = self._get_left_child_internal()

        if child_internal is not None:
            self._root.paneconfig(child_internal, width=width, height=height)

    def _resize_handler(self, event):
        if self._right is not None:
            width_scale = event.width / self._width
            height_scale = event.height / self._height

            new_width = int(self._left.get_width() * width_scale)
            new_height = int(self._left.get_height() * height_scale)
            self._set_child_window_size(self._left, width=new_width, height=new_height)

        self._width = event.width
        self._height = event.height


class UpdatableTkNode(BaseTkTreeNode):
    def update_tk_object(self, new_parent=None):
        if new_parent is not None:
            self._parent = new_parent
        self._create_tk_object()
        if new_parent is not None:
            self._parent.add_child(child=self)

        if self._left is not None:
            self._forget_children()
            self._left.update_tk_object()
            if self._right is not None:
                self._right.update_tk_object()
            self._display_children()

    def wrap_into_paned(self, orient):
        new_parent = InternalTkNode(
            corner_creator=self._corner_creator,
            parent=self._parent, orient=orient,
            width=self._width, height=self._height,
            bg=self._bg
        )
        self._parent.replace_child(old_child=self, new_child=new_parent)

        self._parent = new_parent
        self.update_tk_object(new_parent=new_parent)


class InternalTkNode(BreedingTkNode, UpdatableTkNode):
    def __init__(self, parent, orient, **init_kwargs):
        BaseTkTreeNode.__init__(
            self, tk.PanedWindow, parent=parent, orient=orient,
            sashwidth=2, sashpad=0, bd=0,
            **init_kwargs
        )
