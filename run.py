import tkinter as tk
import collage.mainwindow

if __name__ == "__main__":
    root = tk.Tk()
    app = collage.mainwindow.Application(master=root)
    app.mainloop()
