import tkinter as tk

from src.CollageTree import CollageRoot
from src.CornerCreator import CornerCreator
from src.CollageImage import safe_open_image


class Collage(tk.Frame):
    def __init__(
        self,
        margin,
        corner_width,
        corner_curve,
        master_args,
        master_kwargs
    ):
        super().__init__(*master_args, **master_kwargs)
        self.margin = margin
        self.corner_creator = CornerCreator(corner_width, corner_curve)

        self.collage_root = CollageRoot(
            tk_master=self, corner_creator=self.corner_creator, margin=self.margin, **master_kwargs)
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
            new_width=self.winfo_reqwidth(), new_height=self.winfo_reqheight(), new_margin=self.margin)

    def save_collage(self, filename):
        self.collage_root.save_collage(filename)
