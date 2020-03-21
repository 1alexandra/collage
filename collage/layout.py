import tkinter as tk
from tkinter.colorchooser import askcolor
from matplotlib import font_manager
import numpy as np
from datetime import datetime


def get_system_fonts():
    fonts = []
    for x in font_manager.findSystemFonts():
        x = x[::-1]
        dot = x.find('.')
        slash = x.find('\\')
        x = x[slash-1:dot:-1]
        fonts += [x]
    return np.unique(fonts)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # TODO: stick to up-left bottom
        left_frame = tk.LabelFrame(self, text='Left', padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky='snwe')

        # TODO: bind command functions
        # TODO: add icons

        # Undo, redo, load, save, save as, print buttoms bar
        buttons_frame = tk.Frame(left_frame, bd=10)
        buttons_frame.grid(row=0, column=0, sticky='n')
        bc = 2
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
            button.grid(row=i // bc, column=i % bc, sticky='new')

        # TODO: add validation functions

        # Width, height, margin and corner curvature entries
        entries_frame = tk.Frame(left_frame, bd=10)
        entries_frame.grid(row=1, column=0, sticky='ns')
        px = 5

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

        # "Add text" button
        text_button_frame = tk.Frame(left_frame, bd=10)
        text_button_frame.grid(row=2, column=0, sticky='s')
        self.text_button = tk.Button(text_button_frame, text="Add text...")
        self.text_button.grid()
        self.text_button.bind('<Button-1>', self.open_text_window)

        # TODO: stick to all sides

        right_frame = tk.LabelFrame(self, text='Right', padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky='sne')

        # TODO: bind commands

        # "Add photo" buttons
        self.add_left = tk.Button(right_frame, text='+')
        self.add_right = tk.Button(right_frame, text='+')
        self.add_up = tk.Button(right_frame, text='+')
        self.add_down = tk.Button(right_frame, text='+')
        self.add_left.grid(row=1, column=0, sticky='w')
        self.add_right.grid(row=1, column=2, sticky='w')
        self.add_up.grid(row=0, column=1, sticky='n')
        self.add_down.grid(row=2, column=1, sticky='s')

        # Canvas with collage result
        self.collage = tk.Canvas(right_frame)
        self.collage.grid(row=1, column=1, sticky='nswe')

    def open_text_window(self, event):
        # Output: tk.canvas object
        root = tk.Tk()
        window = TextConfigureApp(master=root)
        window.mainloop()
        return window.get_return()


class TextConfigureApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.rgb = (0, 0, 0)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # TODO: sticky to window edges
        # Canvas with result
        self.canvas = tk.Canvas(self, width=100, height=100)
        self.canvas.grid(row=0, column=1, rowspan=2)

        # Text redactor
        text_frame = tk.Frame(self, bd=10)
        text_frame.grid(row=0, column=0)
        label_text = tk.Label(text_frame, text="Type text here: ", padx=10, pady=10)
        label_text.grid(row=0, column=0)
        self.text_redactor = tk.Text(text_frame, width=30, height=10)
        self.text_redactor.grid(row=1, column=0)
        self.text_redactor.insert(tk.END, datetime.now().date().strftime("%B %Y"))

        # Font chooser
        font_frame = tk.Frame(self, bd=10)
        font_frame.grid(row=1, column=0)
        label_font = tk.Label(font_frame, text="Select font: ", padx=10, pady=10)
        label_font.grid(row=2, column=0)
        self.font_box = tk.Listbox(font_frame, selectmode='SINGLE')
        self.font_box.grid(row=3, column=0, rowspan=3)
        self.system_fonts = get_system_fonts()
        for item in self.system_fonts:
            self.font_box.insert(tk.END, item)
        self.font_box.selection_set(0)
        self.font_box.bind('<Double-Button-1>', self.choose_font)
        buttons = tk.Frame(self, bd=10)
        buttons.grid(row=1, column=1)

        # TODO: add other text modifiers: italic, bold, underlined, font size

        # Color chooser
        self.color_button = tk.Button(buttons, text="Change color...", padx=10, pady=10, width=10)
        self.color_button.grid()
        self.color_button.bind('<Button-1>', self.choose_color)

        # Try button
        self.label_button = tk.Button(buttons, text="Try font", padx=10, pady=10, width=10)
        self.label_button.grid()
        self.label_button.bind('<Button-1>', self.choose_font)

        # Add and quit button
        self.ok_button = tk.Button(buttons, text="OK", padx=10, pady=10, width=10)
        self.ok_button.grid()
        self.ok_button.bind('<Button-1>', self.quit)

    def choose_color(self, event):
        self.rgb, self.color_name = askcolor(parent=self, title="Choose color:")
        print(self.rgb, self.color_name)
        self.draw()

    def choose_font(self, event):
        self.font = self.system_fonts[self.font_box.curselection()[0]]
        print(self.font)
        self.draw()

    def draw(self):
        # TODO: drawing text in choosen style on canvas
        pass

    def quit(self, event):
        self.master.destroy()
        return 'break'

    def get_return(self):
        # TODO: check if canvas exists after self.master.destroy
        return self.canvas
