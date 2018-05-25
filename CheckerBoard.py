from tkinter import *

def Matrix():
    n = 6
    m = 6
    a = [0] * n
    for i in range(n):
        a[i] = [0] * m
    for row in range(6):
        for col in range(6):
            if row<2 and (row+col)%2==1:
                a[row][col]=1
            elif row>3 and (row+col)%2==1:
                a[row][col]=-1
    return a
def clickPieceRed(event):
    if matrixchecker[event.x//100][event.y//100]==1:
        matrixchecker[event.x // 100][event.y // 100] = 2
    paintBoard()
def nextButton(event):
    matrixchecker[event.x//100][event.y//100]=1
def isMovable():

def paintBoard():
    for i in range(6):
        for j in range(6):
            if matrixchecker[i][j] == 1:
                canvas.create_oval(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill='red')
            elif matrixchecker[i][j] == -1:
                canvas.create_oval(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill='blue2')
            elif matrixchecker[i][j] == 2:
                canvas.create_oval(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill='green')

def createBoard():
    for row in range(0, 7):
        for col in range(0, 7):
            if (row + col) % 2 == 0:
                canvas.create_rectangle(row * 100, col * 100, (row + 1) * 100, (col + 1) * 100, fill="black")
            else:
                canvas.create_rectangle(row * 100, col * 100, (row + 1) * 100, (col + 1) * 100, fill="gray85")
def GameOverRed(matrix):
    for row in range(0,7):
        for col in range(0,7):
            if matrix[row][col]==1:
                return True
    return False
def GameOverBlue(matrix):
    for row in range(0,6):
        for col in range(0,6):
            if matrix[row][col]== -1:
                return True
    return False

matrixchecker=Matrix()
root = Tk()
canvas = Canvas(root, width=600, height=600)
canvas.pack()
createBoard()
paintBoard()
canvas.bind("<Button-1>", clickPieceRed)
canvas.pack()
root.mainloop()
