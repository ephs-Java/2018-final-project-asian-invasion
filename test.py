from tkinter import *


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.make_widgets()

    def make_widgets(self):
        lbl = Label(root, text="Username")
        lbl.pack()
        ent = Entry(root)
        ent.pack()
        lbl2 = Label(root, text="Password")
        lbl2.pack()
        ent2 = Entry(root)
        ent2.pack()
        btn = Button(root, text="Log In")
        btn.pack()
        lbl3 = Label(root, text="Ritik is the GOAT")
        lbl3.pack()
        btn2 = Button(root, text="Confirm")
        btn2.pack()


root = Tk()
app = Window(root)
root.mainloop()