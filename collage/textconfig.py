import tkinter as tk
from tkinter.colorchooser import askcolor
from collage.fonts import get_system_fonts
from collage.grid import grid_frame
from datetime import datetime


class TextConfigureApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.rgb = (0, 0, 0)
        self.create_widgets()

    def create_widgets(self):
        grid_frame(self.master, is_root=True)
        grid_frame(self, [0], [0], 0, 0, 'news')
        frame = tk.Frame(self, padx=10, pady=10)
        grid_frame(frame, [0, 1], [0, 1], 0, 0, 'news')
        self.create_text_redactor(frame, 0, 0)
        self.create_font_chooser(frame, 0, 1)
        self.create_canvas(frame, 1, 0)
        self.create_buttons(frame, 1, 1)

    def create_canvas(self, frame, row, col):
        self.canvas = tk.Canvas(frame, width=300, height=100, bg='white', bd=10)
        self.canvas.grid(row=row, column=col)

    def create_text_redactor(self, frame, row, col):
        text_frame = tk.Frame(frame, bd=10)
        grid_frame(text_frame, [1], [0], row, col, 'news')
        label_text = tk.Label(text_frame, text="Type text here: ", padx=10, pady=10)
        label_text.grid(row=0, column=0, sticky='s')
        self.text_redactor = tk.Text(text_frame, width=45, height=15)
        self.text_redactor.grid(row=1, column=0, sticky='news')
        self.text_redactor.insert(tk.END, datetime.now().date().strftime("%B %Y"))

    def create_font_chooser(self, frame, row, col):
        font_frame = tk.Frame(frame, bd=10)
        grid_frame(font_frame, [1], [0], row, col, 'news')
        label_font = tk.Label(font_frame, text="Select font: ", padx=10, pady=10)
        label_font.grid(row=0, column=0, sticky='s')
        self.font_box = tk.Listbox(font_frame, selectmode='SINGLE')
        self.font_box.grid(row=1, column=0, sticky='news')
        self.system_fonts = get_system_fonts()
        for item in self.system_fonts:
            self.font_box.insert(tk.END, item)
        self.font_box.selection_set(0)
        self.font_box.bind('<Double-Button-1>', self.choose_font)

    def create_buttons(self, frame, row, col):
        buttons = tk.Frame(frame, bd=10)
        grid_frame(buttons, [1], [0, 1, 2], row, col, 'news')

        px = 5
        w = 15
        self.italic_var = tk.BooleanVar()
        italic_check = tk.Checkbutton(buttons, text='italic', variable=self.italic_var, onvalue=1, offvalue=0, bd=px)
        italic_check.grid(row=0, column=0, sticky='ne')

        self.bold_var = tk.BooleanVar()
        bold_check = tk.Checkbutton(buttons, text='bold', variable=self.bold_var, onvalue=1, offvalue=0, bd=px)
        bold_check.grid(row=0, column=1, sticky='ne')

        self.lined_var = tk.BooleanVar()
        lined_check = tk.Checkbutton(buttons, text='underlined', variable=self.lined_var, onvalue=1, offvalue=0, bd=px)
        lined_check.grid(row=0, column=2, sticky='ne')

        fontsize_label = tk.Label(buttons, text="Font size:", padx=px)
        fontsize_label.grid(row=1, column=0, sticky='ne')
        self.fontsize_entry = tk.Entry(buttons, width=w * 2)
        self.fontsize_entry.insert(0, '12')
        self.fontsize_entry.grid(row=1, column=1, sticky='new', columnspan=2)

        self.color_button = tk.Button(buttons, text="Change color...", padx=px, pady=px, width=w)
        self.color_button.grid(row=2, column=0, sticky='ews')
        self.color_button.bind('<Button-1>', self.choose_color)

        self.try_button = tk.Button(buttons, text="Try font", padx=px, pady=px, width=w)
        self.try_button.grid(row=2, column=1, sticky='ews')
        self.try_button.bind('<Button-1>', self.choose_font)

        self.ok_button = tk.Button(buttons, text="OK", padx=px, pady=px, width=w)
        self.ok_button.grid(row=2, column=2, sticky='ews')
        self.ok_button.bind('<Button-1>', self.quit)

    def choose_color(self, event):
        self.rgb, self.color_name = askcolor(parent=self, title="Choose color:")
        self.draw()

    def choose_font(self, event):
        self.font = self.system_fonts[self.font_box.curselection()[0]]
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
