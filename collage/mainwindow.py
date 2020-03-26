import tkinter as tk
from collage.textconfig import TextConfigureApp
from collage.grid import grid_frame


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        grid_frame(self.master, [0], [0], None, None, None)
        grid_frame(self, [0], [1])
        left_frame = tk.LabelFrame(self, text='Menu', padx=10, pady=10)
        grid_frame(left_frame, [0, 1, 2], [0], 0, 0, 'nw')
        right_frame = tk.Frame(self, padx=10, pady=10)
        grid_frame(right_frame, [1], [1], 0, 1, 'news')

        self.create_buttons(left_frame)
        self.create_entries(left_frame)
        self.create_add_text_button(left_frame)
        self.create_canvas_frame(right_frame)

    def create_buttons(self, frame):
        # TODO: bind command functions
        # TODO: add icons
        buttons_frame = tk.Frame(frame, bd=10)
        grid_frame(buttons_frame, [0, 1, 2], [0, 1], 0, 0, 'news')
        bw = 10
        self.undo_button = tk.Button(buttons_frame, text='Undo', width=bw)
        self.redo_button = tk.Button(buttons_frame, text='Redo', width=bw)
        self.load_button = tk.Button(buttons_frame, text='Load model', width=bw)
        self.save_button = tk.Button(buttons_frame, text='Save model', width=bw)
        self.save2_button = tk.Button(buttons_frame, text='Save as...', width=bw)
        self.print_button = tk.Button(buttons_frame, text='Print', width=bw)
        buttons = [
            self.undo_button,
            self.redo_button,
            self.load_button,
            self.save_button,
            self.save2_button,
            self.print_button
        ]
        for i, button in enumerate(buttons):
            button.grid(row=i // 2, column=i % 2, sticky='new')

    def create_entries(self, frame):
        # TODO: add validation functions
        entries_frame = tk.Frame(frame, bd=10)
        grid_frame(entries_frame, [0, 1, 2, 3], [0, 1], 1, 0, 'news')
        px = 5

        bw = 10
        self.width_label = tk.Label(entries_frame, text="Width in pixels", padx=px)
        self.width_entry = tk.Entry(entries_frame, width=bw)
        self.width_entry.insert(0, '300')

        self.height_label = tk.Label(entries_frame, text="Height in pixels", padx=px)
        self.height_entry = tk.Entry(entries_frame, width=bw)
        self.height_entry.insert(0, '300')

        self.margin_label = tk.Label(entries_frame, text="Margin in pixels", padx=px)
        self.margin_entry = tk.Entry(entries_frame, width=bw)
        self.margin_entry.insert(0, '3')

        self.corner_label = tk.Label(entries_frame, text="Corner curvature (0-1)", padx=px)
        self.corner_entry = tk.Entry(entries_frame, width=bw)
        self.corner_entry.insert(0, '0')

        labels_entries = [
            (self.width_label, self.width_entry),
            (self.height_label, self.height_entry),
            (self.margin_label, self.margin_entry),
            (self.corner_label, self.corner_entry)
        ]
        for i, (label, entry) in enumerate(labels_entries):
            label.grid(row=i, column=0, sticky='e')
            entry.grid(row=i, column=1, sticky='w')

        self.get_entry_button = tk.Button(entries_frame, text="Change parameters")
        self.get_entry_button.grid(row=4, column=0, columnspan=2, sticky='new')
        self.get_entry_button.bind('<Button-1>', self.change_canvas_parameters)

    def create_add_text_button(self, frame):
        text_button_frame = tk.Frame(frame, bd=10)
        grid_frame(text_button_frame, [0], [0], 2, 0, 'news')
        self.text_button = tk.Button(text_button_frame, text="Add text...", padx=5, pady=5)
        self.text_button.grid()
        self.text_button.bind('<Button-1>', self.open_text_window)

    def create_canvas_frame(self, frame):
        # TODO: bind commands
        self.add_left = tk.Button(frame, text='+')
        self.add_right = tk.Button(frame, text='+')
        self.add_up = tk.Button(frame, text='+')
        self.add_down = tk.Button(frame, text='+')

        self.add_left.grid(row=1, column=0, sticky='nws')
        self.add_right.grid(row=1, column=2, sticky='nes')
        self.add_up.grid(row=0, column=1, sticky='ews')
        self.add_down.grid(row=2, column=1, sticky='new')

        self.collage = tk.Canvas(frame, bg='white')
        self.collage.grid(row=1, column=1)
        self.change_canvas_parameters(None)

    def change_canvas_parameters(self, event):
        self.collage['width'] = int(self.width_entry.get())
        self.collage['height'] = int(self.height_entry.get())
        # TODO: get margin and corner

    def open_text_window(self, event):
        # Output: tk.canvas object
        root = tk.Tk()
        window = TextConfigureApp(master=root)
        window.mainloop()
        return window.get_return()
