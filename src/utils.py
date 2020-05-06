from tkinter import filedialog
from tkinter import VERTICAL, HORIZONTAL
import numpy as np
from PIL.Image import fromarray
import tkinter as tk


def mix_image_with_bg(im, bg_color):
    im_np = np.array(im)
    rgb, alpha = im_np[:, :, :3], im_np[:, :, -1]
    alpha = (alpha / 255.0)[:, :, None]
    color = (np.array(tk.Frame().winfo_rgb(bg_color))[None, None] / 256.0).astype(int)
    rgb = (alpha * rgb + (1 - alpha) * color).round().astype(np.uint8)
    return fromarray(rgb, mode='RGB')


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


def is_vertical(orient):
    return orient == VERTICAL


def ask_open_image():
    filename = filedialog.askopenfilename(
        title="Select file",
        filetypes=(
            ("image files", ("*.jpg", "*.png", "*.gif", "*.jpeg", "*.tiff", "*.bmp")),
        )
    )

    return filename
