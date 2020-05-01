from PIL import ImageTk, Image
from src.CollageItem import CollageItem
from functools import wraps


class ViewingWindowException(Exception):
    def __init__(self, message):
        self.message = message


class ViewingWindow():
    """
    Class for managing viewing window in original image
    """
    def __init__(self, original, width, height, scale_step=0.01, scale_value_min=0.2, move_step=5):
        self.original = original
        self.width = width
        self.height = height
        self.image_size = (width, height)
        self.scale_value = 1
        self.scale_step = scale_step
        self.move_step = move_step
        self.view_vector = [0, 0]
        self.scale_value_min = scale_value_min

    def _crop(self):
        """
        Crops rectangle from original image and resizes it to image size
        Returns cropped PIL Image
        """
        center = [self.original.width // 2 + self.view_vector[0], self.original.height // 2 + self.view_vector[1]]
        left = center[0] - self.width // 2
        upper = center[1] - self.height // 2
        right = center[0] + self.width // 2
        lower = center[1] + self.height // 2
        if left < 0 or right > self.original.width or upper < 0 or lower > self.original.height:
            raise ViewingWindowException("Can't crop original image")
        return self.original.crop((left, upper, right, lower)).resize(self.ImageSize)

    def _scale(self):
        self.width, self.height = int(self.ImageSize[0] * self.scale_value), int(self.ImageSize[1] * self.scale_value)
        return self._crop()

    def get(self):
        return self._crop()

    def zoom_in(self):
        self.scale_value = max(self.scale_value - self.scale_step, self.scale_value_min)
        return self._scale()

    def zoom_out(self):
        self.scale_value = self.scale_value + self.scale_step
        return self._scale()

    def move_up(self):
        self.view_vector[1] -= self.move_step
        return self._crop()

    def move_down(self):
        self.view_vector[1] += self.move_step
        return self._crop()

    def move_left(self):
        self.view_vector[0] -= self.move_step
        return self._crop()

    def move_right(self):
        self.view_vector[0] += self.move_step
        return self._crop()

    ImageSize = property()

    @ImageSize.getter
    def ImageSize(self):
        return self.image_size

    @ImageSize.setter
    def ImageSize(self, value):
        self.image_size = value
        self.width, self.height = int(value[0] * self.scale_value), int(value[1] * self.scale_value)


def add_image_to_collage(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        fn(self, *args, **kwargs)
        self.collage.itemconfig(self.Id, image=self.PhotoImage)
    return wrapper


def add_corners_to_image(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        fn(self, *args, **kwargs)
        self._update_corners()
    return wrapper


class PILCollageImage(CollageItem):
    def __init__(
        self,
        filename,
        coords,
        width,
        height,
        corner_creator,
        collage,
    ):
        self.collage = collage
        self.corners = corner_creator
        self.PIL_image = Image.open(filename)
        self.original = Image.open(filename)
        self.viewing_window = ViewingWindow(self.original, width, height)
        self.PIL_image = self.viewing_window.get()
        self._update_corners()
        id = collage.create_image(
            coords[0], coords[1], anchor="nw", image=self.PhotoImage
        )
        super().__init__(id, collage)

    def resize(self, size):
        """
        Resize the image
        size – The requested size in pixels, as a 2-tuple: (width, height).
        """
        self.viewing_window.ImageSize = size
        self.PIL_image = self.viewing_window.get()
        self.update_corners()
        self.collage.itemconfig(self.Id, image=self.PhotoImage)
        self.reset_selection()

    @add_image_to_collage
    @add_corners_to_image
    def move_view_up(self):
        self.PIL_image = self.viewing_window.move_up()

    @add_image_to_collage
    @add_corners_to_image
    def move_view_down(self):
        self.PIL_image = self.viewing_window.move_down()

    @add_image_to_collage
    @add_corners_to_image
    def move_view_left(self):
        self.PIL_image = self.viewing_window.move_left()

    @add_image_to_collage
    @add_corners_to_image
    def move_view_right(self):
        self.PIL_image = self.viewing_window.move_right()

    @add_image_to_collage
    @add_corners_to_image
    def zoom_in(self):
        self.PIL_image = self.viewing_window.zoom_in()

    @add_image_to_collage
    @add_corners_to_image
    def zoom_out(self):
        self.PIL_image = self.viewing_window.zoom_out()

    def _update_corners(self):
        img = self.PIL_image
        alpha = self.corners.get_alpha(self.PIL_image.size)
        img.putalpha(alpha)
        self.PIL_image = img

    @add_image_to_collage
    def update_corners(self):
        self._update_corners()

    PIL_image = property()
    PhotoImage = property()
    Width = property()
    Height = property()

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

    @Width.getter
    def Width(self):
        return self.photo_image.width()

    @Height.getter
    def Height(self):
        return self.photo_image.height()
