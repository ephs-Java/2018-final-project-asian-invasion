import pandas
import keras
from tkinter import *


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.make_widgets()


    def make_widgets(self):
        lbl = Label()


if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.mainloop()

else:
    print(__name__)
