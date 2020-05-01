import tkinter as tk
from src.utils import ask_open_image, safe_open_image, get_orient
from src.BaseTkTree import BreedingTkNode, UpdatableTkNode


class CollageRoot(BreedingTkNode):
    def __init__(self, tk_master, **init_kwargs):
        super().__init__(obj_class=tk.PanedWindow, parent=None, bd=0, tk_master=tk_master, **init_kwargs)

    def add_image(self, image, where):
        assert where in ('w', 's', 'n', 'e')
        if self._left is not None:
            orient = get_orient(where)
            self._left.wrap_into_paned(orient=orient)
            self._left.add_image_child(image_node_class=CollageLeafNode, image=image, where=where)
            self._root.update()
        else:
            self.add_image_child(image_node_class=CollageLeafNode, image=image, where=where)

    def update_corners(self, new_width, new_height, new_margin):
        self._root.config(width=new_width, height=new_height)


class CollageLeafNode(UpdatableTkNode):
    def __init__(self, image, corner_creator, parent, margin=0, **init_kwargs):
        super().__init__(obj_class=tk.Canvas, corner_creator=corner_creator, parent=parent, **init_kwargs)

        self._margin = margin
        self._image = image
        self._image.resize((self._width, self._height))

        self._image_id = self._root.create_image(0, 0, anchor="nw", image=self._image.PhotoImage)

    def _resize_handler(self, event):
        if self._image is not None:
            self._image.resize((event.width, event.height))

            self._width = event.width
            self._height = event.height

            self._root.itemconfig(self._image_id, image=self._image.PhotoImage)

    def _create_tk_object(self, tk_master=None):
        super()._create_tk_object(tk_master)
        if hasattr(self, '_image'):
            self._image_id = self._root.create_image(0, 0, anchor="nw", image=self._image.PhotoImage)

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
                self.wrap_into_paned(get_orient(where))
                self._parent.add_image_child(image_node_class=CollageLeafNode, image=image, where=where)
        return func
