import tkinter as tk
from src.utils import is_up_left, is_up_bottom, ask_open_image, safe_open_image


def get_orient(where):
    return tk.VERTICAL if is_up_bottom(where) else tk.HORIZONTAL


class CollageRoot(tk.Frame):
    def __init__(self, master, corner_creator, width, height, margin=0, bg='white', **master_kwargs):
        super().__init__(master=master, width=width, height=height, bg=bg, **master_kwargs)

        self.root = None
        self.margin = margin
        self.corner_creator = corner_creator

    def _create_root_node(self, orient):
        old_root = self.root
        if old_root is not None:
            old_root.grid_forget()
        self.root = CollageNode(
            master=self, orient=orient, height=self['height'], width=self['width'], bg=self['bg'])
        self.root.grid(row=0, column=0)

        return old_root

    def _create_root_leaf(self, image):
        old_root = self.root
        if old_root is not None:
            old_root.grid_forget()
        self.root = CollageLeaf(
            image, master=self, corner_creator=self.corner_creator,
            height=self['height'], width=self['width'], bg=self['bg'], margin=self.margin)
        self.root.grid(row=0, column=0)

        return old_root

    def add_image(self, image, where):
        assert where in ('w', 's', 'n', 'e')

        if self.root is None:
            self._create_root_leaf(image)
        else:
            old_root = self._create_root_node(orient=get_orient(where))

            if is_up_left(where):
                self.root.add_child_leaf(image=image, margin=self.margin, corner_creator=self.corner_creator)
                # rebuild an old part
                self.root.add_child_node(node=old_root)
            else:
                # rebuild an old part
                self.root.add_child_node(node=old_root)
                self.root.add_child_leaf(image=image, margin=self.margin, corner_creator=self.corner_creator)

    def update_corners(self, new_width, new_height, new_margin):
        old_width, old_height = self['width'], self['height']
        self['width'], self['height'] = new_width, new_height
        if self.root is not None:
            # update images
            self.root.update_corners()

            # rebuild the tree if it is necessary
            if new_width != old_width or new_height != old_height or self.margin != new_margin:
                self.root.grid_forget()
                self.root = self.root.change_parent(
                    self, width_multiplier=new_width / old_width, height_multiplier=new_height / old_height,
                    new_margin=new_margin
                )
                self.root.grid(row=0, column=0)
        self.margin = new_margin


class CollageNode(tk.PanedWindow):
    def __init__(self, master, width, height, orient, bg='white', **master_kwargs):
        super().__init__(
            master=master, width=width, height=height, orient=orient, bg=bg,
            bd=0, sashwidth=2, **master_kwargs)
        self._orient = orient
        self._children = []

    def add_child_leaf(self, image, margin, corner_creator):
        # split canvas into two equal parts depending on chosen side
        width = self['width'] // 2 if self._orient == tk.HORIZONTAL else self['width']
        height = self['height'] // 2 if self._orient == tk.VERTICAL else self['height']
        leaf = CollageLeaf(
            image, master=self, corner_creator=corner_creator, width=width, height=height, margin=margin, bg=self['bg'])
        self.add(leaf)

    def add_child_node(self, node):
        # split canvas into two equal parts depending on chosen side
        width_multiplier = 0.5 if self._orient == tk.HORIZONTAL else 1
        height_multiplier = 0.5 if self._orient == tk.VERTICAL else 1

        node = node.change_parent(self, width_multiplier=width_multiplier, height_multiplier=height_multiplier)
        self.add(node)

    def add(self, child, **kw):
        # the tree is binary
        assert len(self.panes()) < 2
        super().add(child, **kw)
        self._children.append(child)

    def change_parent(self, parent, width_multiplier=1, height_multiplier=1, new_margin=None):
        sep_x, sep_y = self.sash_coord(0)
        sep_x = int(sep_x * width_multiplier)
        sep_y = int(sep_y * height_multiplier)

        width = int(self['width'] * width_multiplier)
        height = int(self['height'] * height_multiplier)

        # rebuild the node
        new_node = CollageNode(
            master=parent, width=width, height=height, bg=self['bg'], orient=self._orient)
        for child in self._children:
            new_node.add(child.change_parent(
                new_node, width_multiplier=width_multiplier, height_multiplier=height_multiplier, new_margin=new_margin))
        # update the borders
        # here we use binary property: each node should process only one border.
        new_node.sash_place(0, sep_x, sep_y)

        return new_node

    def replace_child(self, old_child, new_child):
        if old_child is self._children[1]:
            self._children = [self._children[0]]
            self.forget(self.panes()[1])
            self.add(new_child)
        else:
            for child in self.panes():
                self.forget(child)

            children = [new_child]
            if len(self._children) > 1:
                children.append(self._children[1])
            self._children = []

            for child in children:
                self.add(child)

    def update_corners(self):
        for child in self._children:
            child.update_corners()


class CollageLeaf(tk.Canvas):
    def __init__(self, image, master, width, height, corner_creator, margin=0, bg='white', **master_kwargs):
        super().__init__(master=master, width=width, height=height, bg=bg, bd=-2 + margin, **master_kwargs)

        self.width = width
        self.height = height
        self.margin = margin

        self.corner_creator = corner_creator

        self.image = image
        self.image.resize((width, height))

        self.id = self.create_image(0, 0, anchor="nw", image=self.image.PhotoImage)

        self.popup = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Add image to the left", command=self._add_image('w'))
        self.popup.add_command(label="Add image to the right", command=self._add_image('e'))
        self.popup.add_command(label="Add image on top", command=self._add_image('n'))
        self.popup.add_command(label="Add image below", command=self._add_image('s'))

        self.bind("<Button-3>", self.selection_area_handler)
        self.bind("<Configure>", self.resize_event_handler)

    def change_parent(self, parent, width_multiplier=1, height_multiplier=1, new_margin=None):
        width = int(self.width * width_multiplier)
        height = int(self.height * height_multiplier)
        margin = new_margin if new_margin is not None else self.margin
        # rebuild the leaf
        return CollageLeaf(
            self.image, master=parent, width=width, height=height, margin=margin, bg=self['bg'],
            corner_creator=self.corner_creator
        )

    def resize_event_handler(self, event):
        if self.image is not None:
            self.image.resize((event.width, event.height))

            self.width = event.width
            self.height = event.height
            self.itemconfig(self.id, image=self.image.PhotoImage)

    def selection_area_handler(self, event):
        try:
            # display the popup menu
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    def update_corners(self):
        if self.image is not None:
            self.image.update_corners()
            # update image on canvas
            self.itemconfig(self.id, image=self.image.PhotoImage)

    def _add_image(self, where):
        def func():
            filename = ask_open_image()
            image = safe_open_image(filename, corner_creator=self.corner_creator)
            if image:
                if type(self.master) == CollageRoot:
                    self.master.add_image(image=image, where=where)
                else:
                    new_parent = CollageNode(
                        master=self.master, orient=get_orient(where), height=self.height, width=self.width, bg=self['bg'])

                    if is_up_left(where):
                        new_parent.add_child_leaf(image=image, margin=self.margin, corner_creator=self.corner_creator)
                        new_parent.add_child_node(self)
                    else:
                        new_parent.add_child_node(self)
                        new_parent.add_child_leaf(image=image, margin=self.margin, corner_creator=self.corner_creator)
                    self.master.replace_child(old_child=self, new_child=new_parent)
        return func
