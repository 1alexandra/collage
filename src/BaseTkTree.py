from src.utils import int_clamp
from src.constants import WINDOW_SEP_WIDTH


class BaseTkTreeNode:
    def __init__(self, obj_class, parent, width, height, tk_master=None, bg='white', **special_kwargs):
        self._root = None

        self._obj_class = obj_class
        self._parent = parent

        self._bg = bg
        self._width = width
        self._height = height

        self._special_kwargs = special_kwargs

        self._left = None
        self._right = None
        self._proportion = None

        self._create_tk_object(tk_master=tk_master)

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_tk_object(self):
        return self._root

    def update_leaf_vars(self, **kwargs):
        """Calls function recursively"""
        if self._left is not None:
            self._left.update_leaf_vars(**kwargs)
        if self._right is not None:
            self._right.update_leaf_vars(**kwargs)

    def _resize_handler(self, event):
        pass

    def _create_tk_object(self, tk_master=None):
        """
        If tk_master is passed, creates TkObject with tk_master as master,
        otherwise - gets master from "parent" field.
        """
        if self._root is not None:
            del self._root
        master = self._parent.get_tk_object() if tk_master is None else tk_master
        self._root = self._obj_class(
            master=master, width=self._width, height=self._height, bg=self._bg, **self._special_kwargs)
        self._root.bind('<Configure>', self._resize_handler)


class BreedingTkNode(BaseTkTreeNode):
    def replace_child(self, old_child, new_child):
        """Replaces child "old_child" by "new_child"."""
        if self._left is old_child:
            if self._left is not None:
                self._root.forget(self._get_left_child_internal())

            self._left = new_child
            if new_child is not None:
                self._root.add(self._left.get_tk_object())

                if self._right is not None:
                    self._root.paneconfigure(self._get_right_child_internal(), before=self._get_left_child_internal())
            else:
                self._left = self._right
                self._right = None
        elif self._right is old_child:
            if self._right is not None:
                self._root.forget(self._get_right_child_internal())
            self._right = new_child
            if new_child is not None:
                self._root.add(self._right.get_tk_object())
        else:
            assert False

        if self._right is not None:
            self._align_children()

    def add_child(self, child, begin=False):
        self._proportion = 0.5
        self.replace_child(old_child=None, new_child=child)
        if begin and self._right is not None:
            self._root.paneconfigure(self._get_right_child_internal(), before=self._get_left_child_internal())
            self._left, self._right = self._right, self._left
        self._align_children()

    def remove_child(self, child):
        self.replace_child(old_child=child, new_child=None)

    def collapse(self):
        assert self._right is None

        if self._left is not None:
            self._left.update_tk_object(new_parent=self._parent, instead=self)

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
        """Updates the border between windows according to self._proportion"""
        if self._right is not None:
            new_width = int_clamp(self._proportion * (self._width - WINDOW_SEP_WIDTH), min_val=0)
            new_height = int_clamp(self._proportion * (self._height - WINDOW_SEP_WIDTH), min_val=0)

            child_internal = self._get_left_child_internal()
            assert child_internal is not None
            self._root.paneconfig(child_internal, width=new_width, height=new_height)

    def _get_left_child_internal(self):
        """Get tkinter object of the left child"""
        if len(self._root.panes()) > 0:
            return self._root.panes()[0]

    def _get_right_child_internal(self):
        """Get tkinter object of the right child"""
        if len(self._root.panes()) > 1:
            return self._root.panes()[1]

    def get_children_number(self):
        if self._right is not None:
            return 2
        elif self._left is not None:
            return 1
        return 0

    def update_proportion(self, child):
        """Updates the proportion of children's windows' sizes"""
        if child is self._left:
            if not hasattr(self, '_left_unresized'):
                self._left_unresized = False
            if self._left is not None and self._right is not None and not self._left_unresized:
                self._proportion = min(self._left.get_width() / int_clamp(self._width - WINDOW_SEP_WIDTH, min_val=1),
                                       self._left.get_height() / int_clamp(self._height - WINDOW_SEP_WIDTH, min_val=1))
            elif self._left_unresized:
                self._left_unresized = False

    def _resize_handler(self, event):
        if event.width != self._width or event.height != self._height:
            self._width = event.width
            self._height = event.height

            if self._parent is not None:
                self._parent.update_proportion(self)

            self._left_unresized = self._left is not None
            if self._right is not None:
                self._align_children()


class UpdatableTkNode(BaseTkTreeNode):
    def update_tk_object(self, new_parent=None, instead=None):
        if new_parent is not None:
            self._parent = new_parent
        self._create_tk_object()
        if new_parent is not None:
            self._parent.replace_child(old_child=instead, new_child=self)

        if self._left is not None:
            self._forget_children()
            self._left.update_tk_object()
            if self._right is not None:
                self._right.update_tk_object()
            self._display_children()

    def wrap_into_paned(self, internal_node_class, orient):
        new_parent = internal_node_class(
            parent=self._parent, orient=orient,
            width=self._width, height=self._height,
            bg=self._bg
        )
        self._parent.replace_child(old_child=self, new_child=new_parent)
        self.update_tk_object(new_parent=new_parent)
