import tkinter.messagebox as messagebox
from tkinter import filedialog
from src.CollageImage import PILCollageImage
from PIL import UnidentifiedImageError


def is_up_left(where):
    return where in ('w', 'n')


def is_up_bottom(where):
    return where in ('s', 'n')


def ask_open_image():
    filename = filedialog.askopenfilename(
        title="Select file",
        filetypes=(
            ("image files", ("*.jpg", "*.png", "*.gif", "*.jpeg", "*.tiff", "*.bmp")),
        )
    )

    return filename


def safe_open_image(filename, corner_creator):
    image = None
    try:
        if filename is not None and filename != "":
            image = PILCollageImage(filename, corner_creator)
    except UnidentifiedImageError:
        messagebox.showerror("Error", "Failed open file {0}".format(filename))
    return image
