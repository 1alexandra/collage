import collage.layout
import tkinter as tk


def test_run_Application():
    app = collage.layout.Application(master=tk.Tk())
    app.update()
    app.destroy()


def test_run_TextConfigureApp():
    app = collage.layout.TextConfigureApp(master=tk.Tk())
    app.update()
    app.destroy()
