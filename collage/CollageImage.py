from PIL import ImageTk, Image
from collage.CollageItem import CollageItem


class PILCollageImage(CollageItem):
    def __init__(
        self,
        filename,
        coords,
        width,
        height,
        collage,
    ):
        self.PIL_image = Image.open(filename)
        self.original = Image.open(filename)
        id = collage.create_image(
            coords[0], coords[1], anchor="nw", image=self.PhotoImage
        )
        CollageItem.__init__(self, id, collage)
        self.resize((width, height))

    def resize(self, size):
        """
        Resize the image
        size – The requested size in pixels, as a 2-tuple: (width, height).
        """
        self.PIL_image = self.original.resize(size)
        self.collage.itemconfig(self.Id, image=self.PhotoImage)
        self.reset_selection()

    PIL_image = property()
    PhotoImage = property()
    Width = property()
    Height = property()

    @PIL_image.setter
    def PIL_image(self, value):
        self.pil_image = value
        self.photo_image = ImageTk.PhotoImage(self.pil_image)

    @PhotoImage.getter
    def PhotoImage(self):
        return self.photo_image

    @Width.getter
    def Width(self):
        return self.photo_image.width()

    @Height.getter
    def Height(self):
        return self.photo_image.height()
