import tkinter as tk

from src.grid import grid_frame


class ScrolledFrame(tk.Frame):
    """Frame with scrollbars.

    parent -- parent frame,
    vertical -- do you need vertical scrollbar,
    horisontal -- do you need horisontal scrollbar.
    """
    def __init__(self, parent, vertical, horizontal):
        self.parent = parent

        super().__init__(parent)
        grid_frame(self, [], [])

        self._canvas = tk.Canvas(self)
        self._canvas.grid(row=0, column=0)

        self._vertical_bar = tk.Scrollbar(self, orient='vertical', command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._vertical_bar.set)
        self._vertical_bar.activate()

        self._horizontal_bar = tk.Scrollbar(self, orient='horizontal', command=self._canvas.xview)
        self._canvas.configure(xscrollcommand=self._horizontal_bar.set)
        self._horizontal_bar.activate()

        if vertical:
            self._vertical_bar.grid(row=0, column=1, sticky='wns')

        if horizontal:
            self._horizontal_bar.grid(row=1, column=0, sticky='nwe')

        self.inner = tk.Frame(self._canvas)
        self.inner.grid()

        self._window = self._canvas.create_window((0, 0), window=self.inner, anchor='nw')
        self.bind('<Configure>', self.frame_config)
        self._canvas.bind('<Configure>', self.canvas_config)
        self.inner.bind('<Configure>', self.resize_handler)

    def frame_config(self, event):
        """Self frame resize event handler."""
        w = min(event.width - self._vertical_bar.winfo_width(), self.inner.winfo_width())
        h = min(event.height - self._horizontal_bar.winfo_height(), self.inner.winfo_height())
        self._canvas.configure(width=w, height=h)

    def canvas_config(self, event):
        """Canvas resize event handler"""
        if self._horizontal_bar.get()[1] * self._horizontal_bar.winfo_width() > event.width:
            self._canvas.xview_moveto(0)
        if self._vertical_bar.get()[1] * self._vertical_bar.winfo_height() > event.height:
            self._canvas.yview_moveto(0)

    def resize_handler(self, event=None, width=None, height=None):
        """self.inner frame resize event handler. Use <Configure> event or width and height of result frame."""
        if event is not None:
            width = event.width
            height = event.height
        canvas_w = min(width, self.winfo_width() - self._vertical_bar.winfo_width())
        canvas_h = min(height, self.winfo_height() - self._horizontal_bar.winfo_height())
        self._canvas.configure(width=canvas_w, height=canvas_h, scrollregion=(0, 0, width, height))
