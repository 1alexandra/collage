import collage.mainwindow
import collage.textconfig
import tkinter as tk


def test_run_Application():
    app = collage.mainwindow.Application(master=tk.Tk())
    app.update()
    app.destroy()


def test_run_TextConfigureApp():
    app = collage.textconfig.TextConfigureApp(master=tk.Tk())
    app.update()
    app.destroy()
