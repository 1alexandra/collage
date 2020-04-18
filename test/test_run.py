from src.mainwindow import Application
from src.textconfig import TextConfigureApp
import tkinter as tk


def test_run_Application():
    app = Application(master=tk.Tk())
    app.update()
    app.destroy()


def test_run_TextConfigureApp():
    app = TextConfigureApp(master=tk.Tk())
    app.update()
    app.destroy()
