import tkinter as tk
from src.utils import ask_open_image, safe_open_image, get_orient, is_up_bottom, is_up_left
from src.BaseTkTree import BaseTkTreeNode, BreedingTkNode, UpdatableTkNode


class CollageBreedingNode(BreedingTkNode):
    def add_image_child(self, image, where, corner_creator, margin=0):
        width = self._width
        height = self._height
        if self._left is not None:
            if is_up_bottom(where):
                height //= 2
            else:
                width //= 2
        leaf_node = CollageLeafNode(
            image=image, corner_creator=corner_creator, parent=self,
            width=width, height=height, bg=self._bg, bd=-2, margin=margin
        )
        self.add_child(leaf_node, begin=is_up_left(where), align=True)


class InternalTkNode(CollageBreedingNode, UpdatableTkNode):
    def __init__(self, parent, orient, **init_kwargs):
        BaseTkTreeNode.__init__(
            self, tk.PanedWindow, parent=parent, orient=orient,
            sashwidth=2, sashpad=0, bd=0,
            **init_kwargs
        )


class CollageRoot(CollageBreedingNode):
    def __init__(self, tk_master, corner_creator, margin=0, **init_kwargs):
        super().__init__(obj_class=tk.PanedWindow, parent=None, bd=0, tk_master=tk_master, **init_kwargs)

        self._margin = margin
        self._corner_creator = corner_creator

    def add_image(self, image, where):
        assert where in ('w', 's', 'n', 'e')
        if self._left is not None:
            orient = get_orient(where)
            self._left.wrap_into_paned(internal_node_class=InternalTkNode, orient=orient)
            self._left.add_image_child(
                image=image, where=where, margin=self._margin,
                corner_creator=self._corner_creator)
        else:
            self.add_image_child(
                image=image, where=where, margin=self._margin,
                corner_creator=self._corner_creator)

    def update_corners(self, new_width, new_height, new_margin):
        self._root.config(width=new_width, height=new_height)
        if new_margin != self._margin:
            self._margin = new_margin
            self.update_leaf_vars(margin=self._margin)


class CollageLeafNode(UpdatableTkNode):
    def __init__(self, image, corner_creator, parent, margin=0, **init_kwargs):
        self._margin = margin
        self._image = image
        self._image_id = None
        self._corner_creator = corner_creator

        super().__init__(obj_class=tk.Canvas, parent=parent, **init_kwargs)

        self._image.resize((self.get_real_width(), self.get_real_height()))

    def get_real_width(self):
        return self._width - 2 * self._margin

    def get_real_height(self):
        return self._height - 2 * self._margin

    def update_leaf_vars(self, margin=None, **kwargs):
        if margin is not None:
            self._margin = margin
            self._set_image()

    def _set_image(self):
        self._image_id = self._root.create_image(self._margin, self._margin, anchor="nw", image=self._image.PhotoImage)

    def _resize_handler(self, event):
        if self._image is not None:
            self._width = event.width
            self._height = event.height

            self._image.resize((self.get_real_width(), self.get_real_height()))

            self._root.itemconfig(self._image_id, image=self._image.PhotoImage)

    def _create_tk_object(self, tk_master=None):
        super()._create_tk_object(tk_master)
        self._set_image()

        self._context_menu = tk.Menu(self._root, tearoff=0)
        self._context_menu.add_command(label="Add image to the left", command=self._add_image('w'))
        self._context_menu.add_command(label="Add image to the right", command=self._add_image('e'))
        self._context_menu.add_command(label="Add image on top", command=self._add_image('n'))
        self._context_menu.add_command(label="Add image below", command=self._add_image('s'))

        self._root.bind("<Button-3>", self._context_menu_handler)
        self._root.bind("<Button-1>", lambda event: self._root.focus_set())

    def _context_menu_handler(self, event):
        self._root.focus_set()
        try:
            # display the context menu
            self._context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self._context_menu.grab_release()

    def _add_image(self, where):
        def func():
            filename = ask_open_image()
            image = safe_open_image(filename, corner_creator=self._corner_creator)

            if image:
                self.wrap_into_paned(internal_node_class=InternalTkNode, orient=get_orient(where))
                self._parent.add_image_child(
                    image=image, margin=self._margin, where=where,
                    corner_creator=self._corner_creator
                )
        return func
