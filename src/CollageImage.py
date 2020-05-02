from PIL import ImageTk, Image
from functools import wraps


class ViewingWindow:
    """
    Class for managing viewing window in original image
    """
    def __init__(self, original, width, height, scale_step=0.1, scale_value_min=0.2, move_step=5):
        self.original = original
        self.image_size = (width, height)
        self.scale_value = 1
        self.scale_step = scale_step
        self.move_step = move_step
        self.view_vector = (0, 0)
        self.scale_value_min = scale_value_min

    width = property()
    height = property()

    @width.getter
    def width(self):
        return self.ImageSize[0] * self.scale_value

    @height.getter
    def height(self):
        return self.ImageSize[1] * self.scale_value

    def _crop(self):
        """
        Crops rectangle from original image and resizes it to image size
        Returns cropped PIL Image
        """
        center = (self.original.width / 2 + self.view_vector[0], self.original.height / 2 + self.view_vector[1])

        left = center[0] - self.width / 2
        upper = center[1] - self.height / 2
        right = center[0] + self.width / 2
        lower = center[1] + self.height / 2

        new_borders = (
            int(round(max(left, 0))),
            int(round(max(upper, 0))),
            int(round(min(right, self.original.width))),
            int(round(min(lower, self.original.height)))
        )
        new_width = max(min(int(round((new_borders[2] - new_borders[0]) / self.scale_value)), self.ImageSize[0]), 1)
        new_height = max(min(int(round((new_borders[3] - new_borders[1]) / self.scale_value)), self.ImageSize[1]), 1)

        corner_x = int(min(max(round(-left / self.scale_value), 0), self.ImageSize[0] - 1))
        corner_y = int(min(max(round(-upper / self.scale_value), 0), self.ImageSize[1] - 1))

        return self.original.crop(new_borders).resize((new_width, new_height)), (corner_x, corner_y)

    def _scale(self, new_scale_value):
        self.scale_value = new_scale_value
        return self._crop()

    def get(self):
        return self._crop()

    def zoom_in(self):
        return self._scale(max(self.scale_value - self.scale_step, self.scale_value_min))

    def zoom_out(self):
        return self._scale(self.scale_value + self.scale_step)

    def move(self, dx, dy):
        self.view_vector = (self.view_vector[0] + dx, self.view_vector[1] + dy)
        return self._crop()

    def move_up(self):
        return self.move(dx=0, dy=-self.move_step)

    def move_down(self):
        return self.move(dx=0, dy=self.move_step)

    def move_left(self):
        return self.move(dx=-self.move_step, dy=0)

    def move_right(self):
        return self.move(dx=self.move_step, dy=0)

    ImageSize = property()

    @ImageSize.getter
    def ImageSize(self):
        return self.image_size

    @ImageSize.setter
    def ImageSize(self, value):
        self.image_size = value


def update_image(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        img, corner = fn(self, *args, **kwargs)
        img = self._update_corners(img)
        self._corner = corner
        self._photo_image = ImageTk.PhotoImage(img)
    return wrapper


class PILCollageImage:
    def __init__(
        self,
        filename,
        corner_creator
    ):
        self.corners = corner_creator
        self.original = Image.open(filename)
        self.viewing_window = None
        self._photo_image = None
        self._corner = None

    @update_image
    def resize(self, size):
        """
        Resize the image
        size – The requested size in pixels, as a 2-tuple: (width, height).
        """
        if self.viewing_window is None:
            self.viewing_window = ViewingWindow(self.original, *size)
        else:
            self.viewing_window.ImageSize = size
        return self.viewing_window.get()

    @update_image
    def move_view_up(self):
        return self.viewing_window.move_up()

    @update_image
    def move_view(self, dx, dy):
        return self.viewing_window.move(dx=dx, dy=dy)

    @update_image
    def move_view_down(self):
        return self.viewing_window.move_down()

    @update_image
    def move_view_left(self):
        return self.viewing_window.move_left()

    @update_image
    def move_view_right(self):
        return self.viewing_window.move_right()

    @update_image
    def zoom_in(self):
        return self.viewing_window.zoom_in()

    @update_image
    def zoom_out(self):
        return self.viewing_window.zoom_out()

    def _update_corners(self, img):
        alpha = self.corners.get_alpha(img.size)
        img.putalpha(alpha)
        return img

    PhotoImage = property()
    corner = property()

    @PhotoImage.getter
    def PhotoImage(self):
        return self._photo_image

    @corner.getter
    def corner(self):
        return self._corner
