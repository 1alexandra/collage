import tkinter as tk
from tkinter import filedialog
from src.textconfig import TextConfigureApp
from src.grid import grid_frame
from src.Collage import Collage


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.collage = None
        self.collage_width = tk.IntVar(master, 300)
        self.collage_height = tk.IntVar(master, 300)
        self.collage_margin = tk.IntVar(master, 3)
        self.corner_width = tk.IntVar(master, 30)
        self.corner_curve = tk.DoubleVar(master, 0.2)

        self.create_widgets()

    def create_widgets(self):
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
        # TODO: add icons
        buttons_frame = tk.Frame(frame, bd=10)
        grid_frame(buttons_frame, [0, 1, 2], [0, 1], row, col, 'news')
        commands = {
            'Undo': self.undo_command,
            'Redo': self.redo_command,
            'Load': self.load_command,
            'Save': self.save_command,
            'Save as...': self.save_as_command,
            'Print': self.print_command
        }
        for i, (text, command) in enumerate(commands.items()):
            button = tk.Button(buttons_frame, text=text, command=command, width=10)
            button.grid(row=i // 2, column=i % 2, sticky='new')

    def create_entries(self, frame, row, col):
        # TODO: add validation functions
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
        button_frame = tk.Frame(frame, bd=10)
        grid_frame(button_frame, [], [0], row, col, 'news')
        commands = {
            'Change parameters': self.change_canvas_parameters,
            'Add text...': self.open_text_window
        }
        for i, (text, command) in enumerate(commands.items()):
            button = tk.Button(button_frame, text=text, command=command, padx=5, pady=5)
            button.grid(row=i, column=0, sticky='new')

    def create_canvas_frame(self, frame, row, col):
        # TODO: add two scrolling bars to canvas_frame
        canvas_frame = tk.Frame(frame, bd=10)
        grid_frame(canvas_frame, [0, 2], [0, 2], row, col, 'news')
        compass = {
            'n': (-1, 0),
            'e': (0, 1),
            'w': (0, -1),
            's': (1, 0)
        }
        for key, (row, col) in compass.items():
            sticky = 'news'.replace(key, '')
            button = tk.Button(canvas_frame, text='+', command=self.get_add_photo_command(key))
            button.grid(row=row + 1, column=col + 1, sticky=sticky)
        self.collage = Collage(
            margin=self.collage_margin.get(),
            corner_width=self.corner_width.get(),
            corner_curve=self.corner_curve.get(),
            master_args=[canvas_frame],
            master_kwargs={
                "bg": "white",
                "height": self.collage_height.get(),
                "width": self.collage_width.get(),
            }
        )
        # collage will be placed on the center of the widget
        self.collage.grid(row=1, column=1)

    def undo_command(self):
        pass

    def redo_command(self):
        pass

    def load_command(self):
        pass

    def save_command(self):
        pass

    def save_as_command(self):
        pass

    def print_command(self):
        pass

    def change_canvas_parameters(self):
        self.collage['width'] = self.collage_width.get()
        self.collage['height'] = self.collage_height.get()
        self.collage.margin = self.collage_margin.get()
        self.collage.corner_creator.width = self.corner_width.get()
        self.collage.corner_creator.curve = self.corner_curve.get()
        self.collage.update_corners()

    def open_text_window(self):
        # Output: tk.canvas object
        root = tk.Tk()
        window = TextConfigureApp(master=root)
        window.mainloop()
        return window.get_return()

    def add_photo(self, where):
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=(
                ("image files", ("*.jpg", "*.png", "*.gif", "*.jpeg", "*.tiff", "*.bmp")),
            )
        )

        # file was not selected
        if filename != "":
            self.collage.add_image(filename, where)

    def get_add_photo_command(self, where):
        def add_photo_command():
            self.add_photo(where)
        return add_photo_command
