import tkinter as tk
from collage.textconfig import TextConfigureApp
from collage.grid import grid_frame


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.collage_width = tk.StringVar(master, '300')
        self.collage_height = tk.StringVar(master, '300')
        self.collage_margin = tk.StringVar(master, '3')
        self.collage_corner = tk.StringVar(master, '0')

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
        # TODO: add validation functions to entries
        entries_frame = tk.Frame(frame, bd=10)
        grid_frame(entries_frame, [0, 1, 2, 3], [0, 1], row, col, 'news')
        variables = {
            'Width in pixels': self.collage_width,
            'Height in pixels': self.collage_height,
            'Margin in pixels': self.collage_margin,
            'Corner curvature (0-1)': self.collage_corner
        }
        for i, (text, variable) in enumerate(variables.items()):
            label = tk.Label(entries_frame, text=text, padx=5)
            entry = tk.Entry(entries_frame, textvariable=variable, width=10)
            label.grid(row=i, column=0, sticky='e')
            entry.grid(row=i, column=1, sticky='w')

    def create_change_buttons(self, frame, row, col):
        button_frame = tk.Frame(frame, bd=10)
        grid_frame(button_frame, [], [0, 1], row, col, 'news')
        commands = {
            'Change parameters': self.change_canvas_parameters,
            'Add text...': self.open_text_window
        }
        for i, (text, command) in enumerate(commands.items()):
            button = tk.Button(button_frame, text=text, command=command, padx=5, pady=5)
            button.grid(row=0, column=i, sticky='new')

    def create_canvas_frame(self, frame, row, col):
        # TODO: add two scrolling bars to canvas_frame
        # TODO: bind commands
        canvas_frame = tk.Frame(frame, bd=10)
        grid_frame(canvas_frame, [0, 2], [0, 2], row, col, 'news')

        self.add_left = tk.Button(canvas_frame, text='+')
        self.add_right = tk.Button(canvas_frame, text='+')
        self.add_up = tk.Button(canvas_frame, text='+')
        self.add_down = tk.Button(canvas_frame, text='+')

        self.add_left.grid(row=1, column=0, sticky='nes')
        self.add_right.grid(row=1, column=2, sticky='nws')
        self.add_up.grid(row=0, column=1, sticky='ews')
        self.add_down.grid(row=2, column=1, sticky='new')

        self.collage = tk.Canvas(canvas_frame, bg='white')
        self.collage.grid(row=1, column=1)
        self.change_canvas_parameters()

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
        self.collage['width'] = int(self.collage_width.get())
        self.collage['height'] = int(self.collage_height.get())
        # TODO: get margin and corner

    def open_text_window(self):
        # Output: tk.canvas object
        root = tk.Tk()
        window = TextConfigureApp(master=root)
        window.mainloop()
        return window.get_return()
