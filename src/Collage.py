import tkinter as tk
from src.CornerCreator import CornerCreator
from src.utils import safe_open_image

from src.CollageTree import CollageRoot


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

        # TODO class to manage images
        # self.images = dict()
        # self.image = None
        # self.selection_rectangle_id = self.create_rectangle(
        #     0, 0, 0, 0, dash=(2, 2), fill='', outline='white', tag="image"
        # )
        self.bind("<Configure>", self.resize_event_handler)
        self.bind("<Double-Button-1>", self.selection_area_handler)
        self.collage_root = CollageRoot(self, corner_creator=self.corner_creator, margin=self.margin, **master_kwargs)
        self.collage_root.grid(row=0, column=0)

    def add_image(self, filename, where):
        """
        Add image in collage to specified side
        filename: image file name
        where: 'n', 'w', 'e', 's'
        """
        image = safe_open_image(filename, self.corner_creator)
        if image is not None:
            self.collage_root.add_image(image=image, where=where)
        # self.images[self.image.id] = self.image
        # to show selection
        # self.tag_lower(self.image.Id)

    def selection_area_handler(self, event):
        pass
        # image_id = self.find_closest(event.x, event.y)[0]
        # self.images[image_id].apply_selection()

    def resize_event_handler(self, event):
        pass
        # if self.image is not None:
        #     self.image.resize((event.width, event.height))

    def update_corners(self):
        if self.collage_root is not None:
            self.collage_root.update_corners(new_width=self['width'], new_height=self['height'], new_margin=self.margin)
