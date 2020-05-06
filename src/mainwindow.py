import os
import tkinter as tk
from tkinter import filedialog

import pickle

from src.utils import ask_open_image
from src.textconfig import TextConfigureApp
from src.grid import grid_frame
from src.Collage import Collage
from src.scroll import ScrolledFrame
from src.utils import int_clamp
from src.constants import WINDOW_SEP_WIDTH, CANVAS_MIN_SIZE, CANVAS_MAX_SIZE


class Application(tk.Frame):
    """Simple Collage Creator application main window.

    The window consists of two frames: **menu** and **workspace**.

    The **menu** contains control buttons and fields for entering collage
    parameters:

    - ``Load``, ``Save``, ``Save as...``\
    buttons at the top,
    - ``Width``, ``Height``, ``Margin``, ``Corner width``, ``Corner Curvature`` \
    entries in the middle,
    - ``Change parameters`` button below it.

    The **workspace** contains ``Collage`` object in the middle and four buttons
    for adding photos (one on each side).
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("900x600")
        self.collage = None
        self.collage_width = tk.IntVar(master, 300)
        self.collage_height = tk.IntVar(master, 300)
        self.collage_margin = tk.IntVar(master, WINDOW_SEP_WIDTH)
        self.corner_width = tk.IntVar(master, 30)
        self.corner_curve = tk.DoubleVar(master, 0.2)

        self.create_widgets()

    def create_widgets(self):
        """Create and grid menu and workspace."""
        grid_frame(self.master, is_root=True)
        grid_frame(self, [0], [1])
        left_frame = tk.LabelFrame(self, text='Menu')
        grid_frame(left_frame, [0, 1, 2], [0], 0, 0, 'nw')
        right_frame = tk.Frame(self)
        grid_frame(right_frame, [0], [0], 0, 1, 'news')

        self.create_menu_buttons(left_frame, 0, 0)
        self.create_entries(left_frame, 1, 0)
        self.create_change_buttons(left_frame, 2, 0)
        self.create_canvas_frame(right_frame, 0, 0)

    def create_menu_buttons(self, frame, row, col):
        """Create, grid and bind menu top buttons block."""
        buttons_frame = tk.Frame(frame, bd=10)
        grid_frame(buttons_frame, [0, 1, 2], [0, 1], row, col, 'news')
        commands = {
            'Undo': None,
            'Redo': None,
            'Load project': self.load_command,
            'Dump project': self.dump_command,
            'Save as...': self.save_as_command,
            'Print...': None,
        }
        for i, (text, command) in enumerate(commands.items()):
            if command is None:
                continue
            button = tk.Button(buttons_frame, text=text, command=command)
            button.grid(row=i // 2, column=i % 2, sticky='news')

    def create_entries(self, frame, row, col):
        """Create, grid and bind menu entries block."""
        entries_frame = tk.Frame(frame, bd=10)
        grid_frame(entries_frame, [0, 1, 2, 3], [0, 1], row, col, 'news')
        variables = {
            'Width in pixels': self.collage_width,
            'Height in pixels': self.collage_height,
            'Margin in pixels': self.collage_margin,
            'Corner size in pixels': self.corner_width,
            'Corner curvature (0-1)': self.corner_curve
        }
        for i, (text, variable) in enumerate(variables.items()):
            label = tk.Label(entries_frame, text=text, padx=5)
            entry = tk.Entry(entries_frame, textvariable=variable, width=10)
            label.grid(row=i, column=0, sticky='e')
            entry.grid(row=i, column=1, sticky='w')

    def create_change_buttons(self, frame, row, col):
        """Create, bind and bind menu bottom buttons block."""
        button_frame = tk.Frame(frame, bd=10)
        grid_frame(button_frame, [], [0], row, col, 'news')
        commands = {
            'Change parameters': self.change_canvas_parameters,
            # 'Add text...': self.open_text_window
        }
        for i, (text, command) in enumerate(commands.items()):
            button = tk.Button(button_frame, text=text, command=command, padx=5, pady=5)
            button.grid(row=i, column=0, sticky='new')

    def create_canvas_frame(self, frame, row, col):
        """Create, grid and bind workspace units."""
        parent_frame = tk.Frame(frame, bd=10)
        grid_frame(parent_frame, [0], [0], row, col, 'news')
        scrolled_frame = ScrolledFrame(parent_frame, True, True)
        compass = {
            'n': (-1, 0),
            'e': (0, 1),
            'w': (0, -1),
            's': (1, 0)
        }
        self.add_buttons = {}
        for key, (row, col) in compass.items():
            sticky = 'news'.replace(key, '')
            button = tk.Button(scrolled_frame.inner, text='+', command=self.get_add_photo_command(key))
            button.grid(row=row + 1, column=col + 1, sticky=sticky)
            self.add_buttons[key] = button
        self.collage = Collage(
            margin=self.collage_margin.get(),
            corner_width=self.corner_width.get(),
            corner_curve=self.corner_curve.get(),
            scrolled_parent=scrolled_frame,
            master_args=[],
            master_kwargs={
                "bg": "white",
                "height": self.collage_height.get(),
                "width": self.collage_width.get(),
            }
        )
        self.collage.grid(row=1, column=1)

    def undo_command(self):
        raise NotImplementedError

    def redo_command(self):
        raise NotImplementedError

    def load_command(self):
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=(
                ("CLG file", "*.clg"),
            )
        )
        if filename != "":
            with open(filename, "rb") as file:
                width, height, margin, corner_width, corner_curve, collage_root = pickle.load(file)
                self.collage_width.set(width)
                self.collage_height.set(height)
                self.collage_margin.set(margin)
                self.corner_width.set(corner_width)
                self.corner_curve.set(corner_curve)
                self.change_canvas_parameters()
                self.collage.load_collage_root(collage_root)

    def dump_command(self):
        filename = filedialog.asksaveasfile(mode="w", defaultextension=".clg", filetypes=(
            ("CLG file", "*.clg"), ("All Files", "*.*")))
        if filename is not None:
            obj = (
                self.collage_width.get(), self.collage_height.get(), self.collage_margin.get(),
                self.corner_width.get(), self.corner_curve.get(),
                self.collage.get_collage_root()
            )
            with open(filename.name, "wb") as file:
                pickle.dump(obj, file)

    def save_as_command(self):
        filename = filedialog.asksaveasfile(mode="w", defaultextension=".png", filetypes=(
            ("PNG file", "*.png"), ("All Files", "*.*")))
        if filename is not None:
            self.collage.save_collage(filename.name)

    def print_command(self):
        raise NotImplementedError

    def change_canvas_parameters(self):
        """Validate and apply user input from menu entries."""
        try:
            w = int_clamp(self.collage_width.get(), CANVAS_MIN_SIZE, CANVAS_MAX_SIZE)
            self.collage_width.set(w)
            h = int_clamp(self.collage_height.get(), CANVAS_MIN_SIZE, CANVAS_MAX_SIZE)
            self.collage_height.set(h)
            m = int_clamp(self.collage_margin.get(), WINDOW_SEP_WIDTH, CANVAS_MAX_SIZE // 2)
            self.collage_margin.set(m)
            cw = int_clamp(self.corner_width.get(), 0, CANVAS_MAX_SIZE // 2)
            self.corner_width.set(cw)
            cc = min(1.0, max(0.0, self.corner_curve.get()))
            self.corner_curve.set(cc)
        except tk.TclError:
            tk.messagebox.showerror(title="Input error", message="Incorrect input. Try again.")
            return

        self.collage.configure(width=w, height=h)
        self.collage.margin = (m - WINDOW_SEP_WIDTH) // 2
        self.collage.corner_creator.Width = cw
        self.collage.corner_creator.Curve = cc
        self.collage.update_params()

        frame_width = w + self.add_buttons['e'].winfo_width() + self.add_buttons['w'].winfo_width()
        frame_height = h + self.add_buttons['s'].winfo_height() + self.add_buttons['n'].winfo_height()
        self.collage.scrolled_parent.resize_handler(width=frame_width, height=frame_height)

    def open_text_window(self):
        """Open ``TextConfigureApp`` window. Return canvas with result."""
        root = tk.Tk()
        window = TextConfigureApp(master=root)
        window.mainloop()
        return window.get_return()

    def add_photo(self, where):
        """Run file system dialog and place photo on collage.

        ``where`` values:

        - 's' is South (upper side),
        - 'n' is North (down side),
        - 'w' is West (left side),
        - 'e' is East (right side).

        Adding a photo from one side of the collage border.
        In this case, the new cell appears on this side of the collage and
        takes up half of the collage regardless of size. All previously
        existing cells are compressed to make room for a new cell.
        """
        filename = ask_open_image()

        # file was not selected
        if filename != "":
            self.collage.add_image(filename, where)

    def get_add_photo_command(self, where):
        def add_photo_command():
            self.add_photo(where)
        return add_photo_command
