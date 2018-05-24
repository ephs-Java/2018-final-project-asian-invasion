from tkinter import *

root = Tk()
canvas = Canvas(root, width=400, height=400)
canvas.pack()
for row in range(0,5):
    for col in range(0, 5):
        if (row+col)%2 == 0:
            canvas.create_rectangle(row*100, col*100, (row+1)*100, (col+1)*100, fill="black")
        else:
            canvas.create_rectangle(row*100, col*100, (row+1)*100, (col+1)*100, fill="gray85")

root.mainloop()
