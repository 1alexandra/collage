from tkinter import filedialog
from tkinter import VERTICAL, HORIZONTAL


def int_clamp(val, min_val=None, max_val=None):
    if max_val is not None:
        val = min(val, max_val)
    if min_val is not None:
        val = max(val, min_val)
    return int(round(val))


def is_up_left(where):
    return where in ('w', 'n')


def is_up_bottom(where):
    return where in ('s', 'n')


def get_orient(where):
    return VERTICAL if is_up_bottom(where) else HORIZONTAL


def ask_open_image():
    filename = filedialog.askopenfilename(
        title="Select file",
        filetypes=(
            ("image files", ("*.jpg", "*.png", "*.gif", "*.jpeg", "*.tiff", "*.bmp")),
        )
    )

    return filename
