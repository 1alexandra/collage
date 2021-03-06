import tkinter as tk

from src.CollageTree import CollageRoot
from src.CornerCreator import CornerCreator
from src.CollageImage import safe_open_image


class Collage(tk.Frame):
    def __init__(
        self,
        margin,
        border_width,
        corner_width,
        corner_curve,
        scrolled_parent,
        master_args,
        master_kwargs
    ):
        if scrolled_parent is not None:
            super().__init__(master=scrolled_parent.inner, *master_args, **master_kwargs)
        else:
            super().__init__(*master_args, **master_kwargs)
        self.margin = margin
        self.border_width = border_width
        self.corner_creator = CornerCreator(corner_width, corner_curve)
        self.scrolled_parent = scrolled_parent

        self.collage_root = CollageRoot(
            tk_master=self, corner_creator=self.corner_creator, margin=self.margin, border_width=self.border_width,
            **master_kwargs)
        self.collage_root.get_tk_object().grid(row=0, column=0)

    def get_collage_root(self):
        return self.collage_root

    def get_corners(self):
        return self.corner_creator

    def add_image(self, filename, where):
        """
        Add image in collage to specified side
        filename: image file name
        where: 'n', 'w', 'e', 's'
        """
        image = safe_open_image(filename, self.corner_creator)
        if image is not None:
            self.collage_root.add_image(image=image, where=where)

    def update_params(self):
        self.collage_root.update_params(
            new_width=self.winfo_reqwidth(), new_height=self.winfo_reqheight(),
            new_margin=self.margin, new_border_width=self.border_width)

    def save_collage(self, filename):
        self.collage_root.save_collage(filename)

    def load_collage_root(self, obj):
        if self.collage_root is not None:
            self.collage_root.get_tk_object().grid_remove()
        self.collage_root = obj
        self.corner_creator = obj.get_corners()
        self.collage_root.reload_object(tk_master=self)
        self.collage_root.get_tk_object().grid(row=0, column=0)
