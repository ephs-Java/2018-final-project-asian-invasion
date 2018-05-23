from tkinter import *

root= Tk()
canvas= Canvas(root, width=800, height=800)
canvas.pack()
for row in range(0,9):
    for col in range(0,9):
        if (row+col)%2==0:
            canvas.create_rectangle(row*100, col*100, (row+1)*100, (col+1)*100, fill="black")


root.mainloop()
