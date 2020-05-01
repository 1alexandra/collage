import tkinter as tk
import tkinter.messagebox as messagebox
import PIL
from src.CollageImage import PILCollageImage, ViewingWindowException
from src.CornerCreator import CornerCreator
from functools import wraps


def image_update_event_wrapper(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.selected_image is not None:
            try:
                fn(self, *args, **kwargs)
            except ViewingWindowException as ex:
                messagebox.showinfo("Info", ex.message)
    return wrapper


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
        self.selected_image = None
        self.selection_rectangle_id = self.create_rectangle(
            0, 0, 0, 0, dash=(2, 2), fill='', outline='white', tag="image"
        )
        self.bind("<Configure>", self.resize_event_handler)
        self.bind("<Double-Button-1>", self.selection_area_handler)
        self.bind("<1>", lambda event: self.focus_set())
        self.bind("<Key>", self.scale_image_handler)
        self.bind("<Up>", self.move_image_view_up_handler)
        self.bind("<Down>", self.move_image_view_down_handler)
        self.bind("<Left>", self.move_image_view_left_handler)
        self.bind("<Right>", self.move_image_view_right_handler)

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
        if self.selected_image is not None:
            if image_id != self.selected_image.Id:
                self.selected_image.Id.apply_selection()

        self.images[image_id].apply_selection()
        if self.images[image_id].IsSelected:
            self.selected_image = self.images[image_id]
        else:
            self.selected_image = None

    @image_update_event_wrapper
    def scale_image_handler(self, event):
        if event.char in ['[', ']']:
            if event.char == '[':
                self.selected_image.zoom_in()
            elif event.char == ']':
                self.selected_image.zoom_out()

    @image_update_event_wrapper
    def move_image_view_up_handler(self, event):
        self.selected_image.move_view_up()

    @image_update_event_wrapper
    def move_image_view_down_handler(self, event):
        self.selected_image.move_view_down()

    @image_update_event_wrapper
    def move_image_view_left_handler(self, event):
        self.selected_image.move_view_left()

    @image_update_event_wrapper
    def move_image_view_right_handler(self, event):
        self.selected_image.move_view_right()

    def resize_event_handler(self, event):
        if self.image is not None:
            self.image.resize((event.width, event.height))

    def update_corners(self):
        if self.image is not None:
            self.image.update_corners()
