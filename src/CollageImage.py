from PIL import Image
from src.utils import int_clamp
from PIL import UnidentifiedImageError
import tkinter.messagebox as messagebox


def safe_open_image(filename, corner_creator):
    image = None
    try:
        if filename is not None and filename != "":
            image = PILCollageImage(filename, corner_creator)
    except UnidentifiedImageError:
        messagebox.showerror("Error", "Failed open file {0}".format(filename))
    return image


class ViewingWindow:
    """
    Class for managing viewing window in original image
    """
    def __init__(self, original, scale_step=0.05, scale_value_min=0.2, move_step=5):
        self.original = original
        self._image_size = None
        self.scale_value = 1
        self.scale_step = scale_step
        self.move_step = move_step
        self.view_vector = (0, 0)
        self.scale_value_min = scale_value_min

        self._borders = None
        self._corner = None
        self._actual_im_size = None

    width = property()
    height = property()

    @width.getter
    def width(self):
        return self._image_size[0] * self.scale_value

    @height.getter
    def height(self):
        return self._image_size[1] * self.scale_value

    def _update_params(self):
        center = (self.original.width / 2 + self.view_vector[0], self.original.height / 2 + self.view_vector[1])

        left = center[0] - self.width / 2
        upper = center[1] - self.height / 2
        right = center[0] + self.width / 2
        lower = center[1] + self.height / 2

        new_borders = (
            int_clamp(left, min_val=0),
            int_clamp(upper, min_val=0),
            int_clamp(right, max_val=self.original.width),
            int_clamp(lower, max_val=self.original.height)
        )
        new_width = int_clamp(
            (new_borders[2] - new_borders[0]) / self.scale_value, min_val=1, max_val=self._image_size[0])
        new_height = int_clamp(
            (new_borders[3] - new_borders[1]) / self.scale_value, min_val=1, max_val=self._image_size[1])

        corner_x = int_clamp(-left / self.scale_value, min_val=0, max_val=self._image_size[0] - 1)
        corner_y = int_clamp(-upper / self.scale_value, min_val=0, max_val=self._image_size[1] - 1)

        self._borders = new_borders
        self._actual_im_size = (new_width, new_height)
        self._corner = (corner_x, corner_y)

    def get(self):
        """
        Crops rectangle from original image and resizes it to image size
        Returns cropped PIL Image
        """
        return self.original.crop(self._borders).resize(self._actual_im_size)

    def _scale(self, new_scale_value):
        self.scale_value = new_scale_value
        self._update_params()

    def resize(self, size):
        self._image_size = int_clamp(size[0], min_val=1), int_clamp(size[1], min_val=1)
        self._update_params()

    def move(self, dx, dy):
        self.view_vector = (
            self.view_vector[0] + dx * self.scale_value,
            self.view_vector[1] + dy * self.scale_value)
        self._update_params()

    def zoom_in(self):
        self._scale(max(self.scale_value - self.scale_step, self.scale_value_min))

    def zoom_out(self):
        self._scale(self.scale_value + self.scale_step)

    def move_up(self):
        self.move(dx=0, dy=-self.move_step)

    def move_down(self):
        self.move(dx=0, dy=self.move_step)

    def move_left(self):
        self.move(dx=-self.move_step, dy=0)

    def move_right(self):
        self.move(dx=self.move_step, dy=0)

    corner = property()

    @corner.getter
    def corner(self):
        return self._corner


class PILCollageImage:
    def __init__(self, filename, corner_creator):
        self.corners = corner_creator

        original = Image.open(filename)
        self.viewing_window = ViewingWindow(original)
        self._corner = None

    def resize(self, size):
        """
        Resize the image
        size – The requested size in pixels, as a 2-tuple: (width, height).
        """
        self.viewing_window.resize(size)

    def move_view_up(self):
        self.viewing_window.move_up()

    def move_view(self, dx, dy):
        self.viewing_window.move(dx=dx, dy=dy)

    def move_view_down(self):
        self.viewing_window.move_down()

    def move_view_left(self):
        self.viewing_window.move_left()

    def move_view_right(self):
        self.viewing_window.move_right()

    def zoom_in(self):
        self.viewing_window.zoom_in()

    def zoom_out(self):
        self.viewing_window.zoom_out()

    def _update_corners(self, img):
        alpha = self.corners.get_alpha(img.size)
        img.putalpha(alpha)
        return img

    PhotoImage = property()
    corner = property()
    ViewingWindow = property()

    @PhotoImage.getter
    def PIL(self):
        return self._update_corners(self.viewing_window.get())

    @corner.getter
    def corner(self):
        return self.viewing_window.corner

    @ViewingWindow.getter
    def ViewingWindow(self):
        return self.viewing_window
