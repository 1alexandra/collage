import tkinter as tk
import collage.layout

if __name__ == "__main__":
    root = tk.Tk()
    app = collage.layout.Application(master=root)
    app.mainloop()
