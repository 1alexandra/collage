import tkinter as tk


class CollageRoot(tk.Frame):
    def __init__(self, master, width, height, margin=0, bg='white', **master_kwargs):
        super().__init__(master=master, width=width, height=height, bg=bg, **master_kwargs)

        self.root = None
        self.height = height
        self.width = width
        self.bg = bg
        self.margin = margin

    def add_image(self, image, where):
        assert where in ('w', 's', 'n', 'e')
        # the first image
        if self.root is None:
            leaf = CollageLeaf(image, master=self, height=self.height, width=self.width, bg=self.bg, margin=self.margin)
            self.root = leaf
            self.root.grid(row=0, column=0)
        else:
            self.root.grid_forget()
            old_root = self.root
            # if up_bottom == True, then frames are stacked vertically
            up_bottom = where in ('n', 's')
            orient = tk.VERTICAL if up_bottom else tk.HORIZONTAL
            self.root = CollageNode(
                master=self, orient=orient, height=self.height, width=self.width, bg=self.bg)
            self.root.grid(row=0, column=0)

            # split canvas into two equal parts depending on chosen side
            width = self.width // 2 if not up_bottom else self.width
            height = self.height // 2 if up_bottom else self.height
            width_multiplier = 0.5 if not up_bottom else 1
            height_multiplier = 0.5 if up_bottom else 1

            leaf = CollageLeaf(image, self.root, width=width, height=height, margin=self.margin)

            # up-left case
            if where in ('n', 'w'):
                self.root.add(leaf)
                # rebuild an old part
                self.root.add(old_root.change_parent(
                    self.root, width_multiplier=width_multiplier, height_multiplier=height_multiplier))
            else:
                # rebuild an old part
                self.root.add(old_root.change_parent(
                    self.root, width_multiplier=width_multiplier, height_multiplier=height_multiplier))
                self.root.add(leaf)

    def update_corners(self, new_width, new_height, new_margin):
        # update the base frame
        self['width'] = new_width
        self['height'] = new_height
        if self.root is not None:
            # update images
            self.root.update_corners()

            # rebuild the tree if it is necessary
            if new_width != self.width or new_height != self.height or self.margin != new_margin:
                self.root.grid_forget()
                self.root = self.root.change_parent(
                    self, width_multiplier=new_width / self.width, height_multiplier=new_height / self.height,
                    new_margin=new_margin
                )
                self.root.grid(row=0, column=0)
        self.width, self.height,self.margin = new_width, new_height, new_margin


class CollageNode(tk.PanedWindow):
    def __init__(self, master, width, height, orient, bg='white', **master_kwargs):
        super().__init__(
            master=master, width=width, height=height, orient=orient, bg=bg,
            bd=0, sashwidth=0, **master_kwargs)
        self.width = width
        self.height = height
        self.bg = bg
        self.orient = orient
        self.childs = []

    def add(self, child, **kw):
        # the tree is binary
        assert len(self.panes()) < 2
        super().add(child, **kw)
        self.childs.append(child)

    def change_parent(self, parent, width_multiplier=1, height_multiplier=1, new_margin=None):
        sep_x, sep_y = self.sash_coord(0)
        sep_x = int(sep_x * width_multiplier)
        sep_y = int(sep_y * height_multiplier)

        width = int(self.width * width_multiplier)
        height = int(self.height * height_multiplier)

        # rebuild the node
        new_node = CollageNode(
            master=parent, width=width, height=height, bg=self.bg, orient=self.orient)
        for child in self.childs:
            new_node.add(child.change_parent(
                new_node, width_multiplier=width_multiplier, height_multiplier=height_multiplier, new_margin=new_margin))
        # update separators
        # here we use binary property: each node should process only one border.
        new_node.sash_place(0, sep_x, sep_y)

        return new_node

    def update_corners(self):
        for child in self.childs:
            child.update_corners()


class CollageLeaf(tk.Canvas):
    def __init__(self, image, master, width, height, margin=0, bg='white', **master_kwargs):
        super().__init__(master=master, width=width, height=height, bg=bg, bd=-2 + margin, **master_kwargs)

        self.width = width
        self.height = height
        self.margin = margin
        self.bg = bg

        self.image = image
        self.image.resize((width, height))

        self.id = self.create_image(0, 0, anchor="nw", image=self.image.PhotoImage)

        self.bind("<Configure>", self.resize_event_handler)

    def change_parent(self, parent, width_multiplier=1, height_multiplier=1, new_margin=None):
        width = int(self.width * width_multiplier)
        height = int(self.height * height_multiplier)
        margin = new_margin if new_margin is not None else self.margin
        # rebuild the leaf
        return CollageLeaf(self.image, master=parent, width=width, height=height, margin=margin, bg=self.bg)

    def resize_event_handler(self, event):
        if self.image is not None:
            self.image.resize((event.width, event.height))

            self.width = event.width
            self.height = event.height
            self.itemconfig(self.id, image=self.image.PhotoImage)

    def update_corners(self):
        if self.image is not None:
            self.image.update_corners()
            # update image on canvas
            self.itemconfig(self.id, image=self.image.PhotoImage)
