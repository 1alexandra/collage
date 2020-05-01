import tkinter as tk

from src.CollageTree import CollageRoot
from src.CornerCreator import CornerCreator
from src.utils import safe_open_image


# from functools import wraps
# import tkinter.messagebox as messagebox
#
# from src.CollageImage import ViewingWindowException
#
#
# def image_update_event_wrapper(fn):
#     @wraps(fn)
#     def wrapper(self, *args, **kwargs):
#         if self.selected_image is not None:
#             try:
#                 fn(self, *args, **kwargs)
#             except ViewingWindowException as ex:
#                 messagebox.showinfo("Info", ex.message)
#     return wrapper


class Collage(tk.Canvas):
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

        self.selected_image = None
        self.selection_rectangle_id = self.create_rectangle(
            0, 0, 0, 0, dash=(2, 2), fill='', outline='white', tag="image"
        )

        self.collage_root = CollageRoot(
            tk_master=self, corner_creator=self.corner_creator, margin=self.margin, **master_kwargs)
        self.collage_root.get_tk_object().grid(row=0, column=0)

    def add_image(self, filename, where):
        """
        Add image in collage to specified side
        filename: image file name
        where: 'n', 'w', 'e', 's'
        """
        image = safe_open_image(filename, self.corner_creator)
        if image is not None:
            self.collage_root.add_image(image=image, where=where)

    def update_corners(self):
        if self.collage_root is not None:
            self.collage_root.update_corners(
                new_width=self['width'], new_height=self['height'], new_margin=self.margin)
