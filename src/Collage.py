import tkinter as tk
import tkinter.messagebox as messagebox
import PIL
from src.CollageImage import PILCollageImage
from src.CornerCreator import CornerCreator


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

        # TODO class to manage images
        self.images = dict()
        self.image = None
        self.selection_rectangle_id = self.create_rectangle(
            0, 0, 0, 0, dash=(2, 2), fill='', outline='white', tag="image"
        )
        self.bind("<Configure>", self.resize_event_handler)
        self.bind("<Double-Button-1>", self.selection_area_handler)

    def add_image(self, filename, where):
        """
        Add image in collage to specified side
        filename: image file name
        where: 'n', 'w', 'e', 's'
        """
        try:
            self.image = PILCollageImage(
                filename,
                [
                    self.margin,
                    self.margin,
                ],
                self.winfo_width() - self.margin,
                self.winfo_height() - self.margin,
                self.corner_creator,
                self
            )
        except PIL.UnidentifiedImageError:
            messagebox.showerror("Error", "Failed open file {0}".format(filename))
            return

        self.images[self.image.id] = self.image
        # to show selection
        self.tag_lower(self.image.Id)

    def selection_area_handler(self, event):
        image_id = self.find_closest(event.x, event.y)[0]
        self.images[image_id].apply_selection()

    def resize_event_handler(self, event):
        if self.image is not None:
            self.image.resize((event.width, event.height))

    def update_corners(self):
        if self.image is not None:
            self.image.update_corners()
