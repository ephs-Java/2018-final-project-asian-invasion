from tkinter import *

root = Tk()
def boardSetter():
    board={}
    for row in range(0,9):
        for col in range(0,9):
            if row<4:
                if (row+col)%2==1:
                    board[row,col]=1
            elif row>5:
                if (row+col)%2==1:
                    board[row, col] = 2
    return board

canvas = Canvas(root, width=400, height=400)
canvas.pack()
board= boardSetter()
for row in range(0,9):
    for col in range(0,9):
        if (row+col)%2 == 0:
            canvas.create_rectangle(row*50, col*50, (row+1)*50, (col+1)*50, fill="black")
        else:
            canvas.create_rectangle(row*50, col*50, (row+1)*50, (col+1)*50, fill="gray85")
        if board[row, col] == 1:
            canvas.create_oval(row * 50, col * 50, (row + 1) * 50, (col + 1) * 50, fill="red")
        elif board[row, col] == 2:
            canvas.create_oval(row * 50, col * 50, (row + 1) * 50, (col + 1) * 50, fill="cyan")




root.mainloop()