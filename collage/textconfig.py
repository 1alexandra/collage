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
        self.text_redactor = None
        self.font_chooser = None
        self.system_fonts = get_system_fonts()
        self.font = self.system_fonts[0]
        self.font_size = tk.StringVar(self.master, '12')
        self.italic_var = tk.IntVar(self.master)
        self.bold_var = tk.IntVar(self.master)
        self.lined_var = tk.IntVar(self.master)
        self.create_widgets()

    def create_widgets(self):
        grid_frame(self.master, is_root=True)
        grid_frame(self, [0], [0], 0, 0, 'news')
        frame = tk.Frame(self, bd=10)
        grid_frame(frame, [0, 1, 2], [0, 1], 0, 0, 'news')
        self.create_text_redactor(frame, 0, 0)
        self.create_font_chooser(frame, 0, 1)
        self.create_canvas(frame, 1, 0)
        self.create_modifiers(frame, 1, 1)
        self.create_buttons(frame, 2, 1)
        self.draw()

    def create_canvas(self, frame, row, col):
        self.canvas = tk.Canvas(frame, width=300, height=100, bg='white')
        self.canvas.grid(row=row, column=col)

    def create_text_redactor(self, frame, row, col):
        # TODO: add scrollbar
        text_frame = tk.Frame(frame, bd=10)
        grid_frame(text_frame, [1], [0], row, col, 'news')
        label = tk.Label(text_frame, text="Type text here:", bd=10)
        label.grid(row=0, column=0, sticky='s')
        self.text_redactor = tk.Text(text_frame, width=45, height=15, wrap=tk.WORD)
        self.text_redactor.grid(row=1, column=0, sticky='news')
        self.text_redactor.insert(tk.END, datetime.now().date().strftime("%B %Y"))

    def create_font_chooser(self, frame, row, col):
        # TODO: add scrollbar
        font_frame = tk.Frame(frame, bd=10)
        grid_frame(font_frame, [1], [0], row, col, 'news')
        label = tk.Label(font_frame, text="Select font:", bd=10)
        label.grid(row=0, column=0, sticky='s')
        self.font_chooser = tk.Listbox(font_frame, selectmode='SINGLE')
        self.font_chooser.grid(row=1, column=0, sticky='news')
        for item in self.system_fonts:
            self.font_chooser.insert(tk.END, item)
        self.font_chooser.selection_set(0)

    def create_modifiers(self, frame, row, col):
        # TODO: add validation function
        buttons = tk.Frame(frame, bd=10)
        grid_frame(buttons, [1], [0, 1, 2], row, col, 'news')
        variables = {
            'italic': self.italic_var,
            'bold': self.bold_var,
            'underlined': self.lined_var
        }
        for i, (text, variable) in enumerate(variables.items()):
            check = tk.Checkbutton(buttons, text=text, variable=variable, onvalue=1, offvalue=0, bd=10)
            check.grid(row=0, column=i, sticky='ne')
        label = tk.Label(buttons, text="Font size:", padx=5)
        label.grid(row=1, column=0, sticky='ne')
        entry = tk.Entry(buttons, textvariable=self.font_size, width=30)
        entry.grid(row=1, column=1, sticky='new', columnspan=2)

    def create_buttons(self, frame, row, col):
        buttons = tk.Frame(frame, bd=10)
        grid_frame(buttons, [], [0, 1, 2], row, col, 'news')
        commands = {
            'Change color...': self.choose_color,
            'Try font': self.choose_font,
            'OK': self.ok_quit
        }
        for i, (text, command) in enumerate(commands.items()):
            button = tk.Button(buttons, text=text, command=command, padx=5, pady=5, width=15)
            button.grid(row=0, column=i, sticky='ews')

    def draw(self):
        # TODO: drawing text in choosen style on canvas
        text = self.text_redactor.get('1.0', 'end-1c')
        font = self.font
        font_size = int(self.font_size.get())
        rgb = self.rgb
        is_italic = bool(self.italic_var.get())
        is_bold = bool(self.bold_var.get())
        is_lined = bool(self.lined_var.get())
        print(text, font, font_size, rgb, is_italic, is_bold, is_lined)
        pass

    def choose_color(self):
        self.rgb, _ = askcolor(parent=self, title="Choose color:")
        self.draw()

    def choose_font(self):
        self.font = self.system_fonts[self.font_chooser.curselection()[0]]
        self.draw()

    def ok_quit(self):
        self.draw()
        self.master.destroy()
        return 'break'

    def get_return(self):
        # TODO: check if canvas exists after self.master.destroy()
        return self.canvas
