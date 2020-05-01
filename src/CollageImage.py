from PIL import ImageTk, Image
from functools import wraps


class ViewingWindowException(Exception):
    def __init__(self, message):
        self.message = message


class ViewingWindow:
    """
    Class for managing viewing window in original image
    """
    def __init__(self, original, width, height, scale_step=0.01, scale_value_min=0.2, move_step=5):
        self.original = original
        width = min(width, original.width)
        height = min(height, original.height)
        self.image_size = (width, height)
        self.scale_value = 1
        self.scale_step = scale_step
        self.move_step = move_step
        self.view_vector = [0, 0]
        self.scale_value_min = scale_value_min

    def get_width(self, scale_value=None):
        if scale_value is None:
            return int(self.ImageSize[0] * self.scale_value)
        return int(self.ImageSize[0] * scale_value)

    def get_height(self, scale_value=None):
        if scale_value is None:
            return int(self.ImageSize[1] * self.scale_value)
        return int(self.ImageSize[1] * scale_value)

    def get_borders(self, scale_value=None, view_vector=None):
        if scale_value is None:
            scale_value = self.scale_value
        if view_vector is None:
            view_vector = self.view_vector
        center = [self.original.width // 2 + view_vector[0], self.original.height // 2 + view_vector[1]]
        width, height = self.get_width(scale_value), self.get_height(scale_value)

        left = center[0] - width // 2
        upper = center[1] - height // 2
        right = center[0] + width // 2
        lower = center[1] + height // 2

        if left < 0 or right > self.original.width or upper < 0 or lower > self.original.height:
            # raise ViewingWindowException("Can't crop original image")
            return None
        return left, upper, right, lower

    def _crop(self, new_scale_value=None, new_view_vector=None):
        """
        Crops rectangle from original image and resizes it to image size
        Returns cropped PIL Image
        """
        borders = self.get_borders(scale_value=new_scale_value, view_vector=new_view_vector)
        if borders is not None:
            if new_scale_value is not None:
                self.scale_value = new_scale_value
            if new_view_vector is not None:
                self.view_vector = new_view_vector
        else:
            borders = self.get_borders()
        return self.original.crop(borders).resize(self.ImageSize)

    def _scale(self, new_scale_value):
        return self._crop(new_scale_value=new_scale_value)

    def get(self):
        return self._crop()

    def zoom_in(self):
        return self._scale(max(self.scale_value - self.scale_step, self.scale_value_min))

    def zoom_out(self):
        return self._scale(self.scale_value + self.scale_step)

    def move(self, dx, dy):
        return self._crop(new_view_vector=[self.view_vector[0] + dx, self.view_vector[1] + dy])

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
        value = (min(value[0], self.original.width), min(value[1], self.original.height))
        self.image_size = value


def add_corners_to_image(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        fn(self, *args, **kwargs)
        self._update_corners()
    return wrapper


class PILCollageImage:
    def __init__(
        self,
        filename,
        corner_creator
    ):
        self.corners = corner_creator
        self.PIL_image = Image.open(filename)
        self.original = Image.open(filename)
        self.viewing_window = None

    @add_corners_to_image
    def resize(self, size):
        """
        Resize the image
        size – The requested size in pixels, as a 2-tuple: (width, height).
        """
        if self.viewing_window is None:
            self.viewing_window = ViewingWindow(self.original, *size)
        else:
            self.viewing_window.ImageSize = size
        self.PIL_image = self.viewing_window.get()

    @add_corners_to_image
    def move_view_up(self):
        self.PIL_image = self.viewing_window.move_up()

    @add_corners_to_image
    def move_view(self, dx, dy):
        self.PIL_image = self.viewing_window.move(dx=dx, dy=dy)

    @add_corners_to_image
    def move_view_down(self):
        self.PIL_image = self.viewing_window.move_down()

    @add_corners_to_image
    def move_view_left(self):
        self.PIL_image = self.viewing_window.move_left()

    @add_corners_to_image
    def move_view_right(self):
        self.PIL_image = self.viewing_window.move_right()

    @add_corners_to_image
    def zoom_in(self):
        self.PIL_image = self.viewing_window.zoom_in()

    @add_corners_to_image
    def zoom_out(self):
        self.PIL_image = self.viewing_window.zoom_out()

    def _update_corners(self):
        img = self.PIL_image
        alpha = self.corners.get_alpha(self.PIL_image.size)
        img.putalpha(alpha)
        self.PIL_image = img

    PIL_image = property()
    PhotoImage = property()

    @PIL_image.setter
    def PIL_image(self, value):
        self.pil_image = value
        self.photo_image = ImageTk.PhotoImage(self.pil_image)

    @PIL_image.getter
    def PIL_image(self):
        return self.pil_image

    @PhotoImage.getter
    def PhotoImage(self):
        return self.photo_image
