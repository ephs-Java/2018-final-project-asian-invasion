from tkinter import *
class CheckerBoard():
    def __init__(self, Matrix):
        self.turnCounter=0
        self.matrixchecker= Matrix

    def onlyOneGreenPiece(self):
        counter=0
        for row in range(6):
            for col in range(6):
                if(self.matrixchecker[row][col]==2):
                    counter= counter+1
        if(counter>1):
            return False
        return True
    def onlyOnePurplePiece(self):
        counter=0
        for row in range(6):
            for col in range(6):
                if(self.matrixchecker[row][col]==-2):
                    counter= counter+1
        if(counter>1):
            return False
        return True
    def canMoveGreenPiece(self,row, col, eventx, eventy):
        if (row+1==eventx//100 and col+1==eventy//100) and self.matrixchecker[row+1][col+1]==0:
            return True
        elif (row - 1 == eventx // 100 and col + 1 == eventy // 100) and self.matrixchecker[row - 1][col + 1] == 0:
            return True
        elif (row - 1 == eventx // 100 and col - 1 == eventy // 100) and self.matrixchecker[row - 1][col - 1] == 0:
            return True
        elif (row + 1 == eventx // 100 and col - 1 == eventy // 100) and self.matrixchecker[row + 1][col - 1] == 0:
            return True
    def canSkipGreenPiece(self, row, col, eventx, eventy):
        if (row+2==eventx//100 and col+2==eventy//100) and self.matrixchecker[row+1][col+1]==-1 and self.matrixchecker[row+2][col+2]==0:
            return True
        elif (row-2==eventx//100 and col+2==eventy//100) and self.matrixchecker[row-1][col+1]==-1 and self.matrixchecker[row-2][col+2]==0:
            return True
        elif (row+2==eventx//100 and col-2==eventy//100) and self.matrixchecker[row+1][col-1]==-1 and self.matrixchecker[row+2][col-2]==0:
            return True
        elif (row-2==eventx//100 and col-2==eventy//100) and self.matrixchecker[row-1][col-1]==-1 and self.matrixchecker[row-2][col-2]==0:
            return True
    def canMovePurplePiece(self,row, col, eventx, eventy):
        if (row+1==eventx//100 and col+1==eventy//100) and self.matrixchecker[row+1][col+1]==0:
            return True
        elif (row - 1 == eventx // 100 and col + 1 == eventy // 100) and self.matrixchecker[row - 1][col + 1] == 0:
            return True
        elif (row - 1 == eventx // 100 and col - 1 == eventy // 100) and self.matrixchecker[row - 1][col - 1] == 0:
            return True
        elif (row + 1 == eventx // 100 and col - 1 == eventy // 100) and self.matrixchecker[row + 1][col - 1] == 0:
            return True
    def canSkipPurplePiece(self, row, col, eventx, eventy):
        if (row+2==eventx//100 and col+2==eventy//100) and self.matrixchecker[row+1][col+1]==1 and self.matrixchecker[row+2][col+2]==0:
            return True
        elif (row-2==eventx//100 and col+2==eventy//100) and self.matrixchecker[row-1][col+1]==1 and self.matrixchecker[row-2][col+2]==0:
            return True
        elif (row+2==eventx//100 and col-2==eventy//100) and self.matrixchecker[row+1][col-1]==1 and self.matrixchecker[row+2][col-2]==0:
            return True
        elif (row-2==eventx//100 and col-2==eventy//100) and self.matrixchecker[row-1][col-1]==1 and self.matrixchecker[row-2][col-2]==0:
            return True
    def clickPieceRed(self, eventx, eventy):
        if self.turnCounter%2==0:
            arr=[]
            arr.extend([eventx//100,eventy//100])
            if self.matrixchecker[eventx//100][eventy//100]==1:
                self.matrixchecker[eventx // 100][eventy // 100] = 2
                if self.onlyOneGreenPiece()==False:
                    self.matrixchecker[arr[0]][arr[1]] = 1
                    del arr[0]
                    del arr[0]

            self.paintBoard()
    def clickGreenPiece(self, eventx, eventy):
        for row in range(6):
            for col in range(6):
                if self.matrixchecker[row][col]==2:
                    if self.canMoveGreenPiece(row, col, eventx, eventy):
                        self.matrixchecker[row][col] = 0
                        self.matrixchecker[eventx//100][eventy//100]=1
                    elif self.canSkipGreenPiece(row, col, eventx, eventy):
                        self.matrixchecker[row][col] = 0
                        self.matrixchecker[eventx//100][eventy//100]= 1
                        self.matrixchecker[(row+(eventx//100))//2][(col+(eventy//100))//2]=0
                        self.turnCounter-=1
        self.turnCounter+=1
        self.paintBoard()
    def clickBluePiece(self, eventx, eventy):
            arr2 = []
            arr2.extend([eventx // 100, eventy // 100])
            if self.matrixchecker[eventx // 100][eventy // 100] == -1:
                self.matrixchecker[eventx // 100][eventy // 100] = -2
                if self.onlyOnePurplePiece() == False:
                    self.matrixchecker[arr2[0]][arr2[1]] = -1
                    del arr2[0]
                    del arr2[0]

            self.paintBoard()
    def clickPurplePiece(self, eventx, eventy):
        for row in range(6):
            for col in range(6):
                if self.matrixchecker[row][col]==-2:
                    if self.canMovePurplePiece(row, col, eventx, eventy):
                        self.matrixchecker[row][col] = 0
                        self.matrixchecker[eventx//100][eventy//100]= -1
                    elif self.canSkipPurplePiece(row, col, eventx, eventy):
                        self.matrixchecker[row][col] = 0
                        self.matrixchecker[eventx//100][eventy//100]= -1
                        self.matrixchecker[(row+(eventx//100))//2][(col+(eventy//100))//2]=0
                        self.turnCounter-=1
        self.turnCounter+=1
        self.paintBoard()
    def isMovable(self, x, y):
        if self.matrixchecker[x][y]==0:
            return True
        return False
    def paintBoard(self):
        for i in range(6):
            for j in range(6):
                if self.matrixchecker[i][j] == 1:
                    canvas.create_oval(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill='red')
                elif self.matrixchecker[i][j]== 0:
                    if (i + j) % 2 == 0:
                        canvas.create_rectangle(i * 100, j * 100, (i+ 1) * 100, (j + 1) * 100, fill="black")
                    else:
                        canvas.create_rectangle(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill="gray85")
                elif self.matrixchecker[i][j] == -1:
                    canvas.create_oval(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill='blue2')
                elif self.matrixchecker[i][j] == 2:
                    canvas.create_oval(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill='green')
                elif self.matrixchecker[i][j]== -2:
                    canvas.create_oval(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill='purple3')

    def createBoard(self):
        for row in range(0, 7):
            for col in range(0, 7):
                if (row + col) % 2 == 0:
                    canvas.create_rectangle(row * 100, col * 100, (row + 1) * 100, (col + 1) * 100, fill="black")
                else:
                    canvas.create_rectangle(row * 100, col * 100, (row + 1) * 100, (col + 1) * 100, fill="gray85")
    def GameOverRed(self, matrix):
        for row in range(0,7):
            for col in range(0,7):
                if matrix[row][col]== 1:
                    return True
        return False
    def GameOverBlue(self, matrix):
        for row in range(0,6):
            for col in range(0,6):
                if matrix[row][col]== -1:
                    return True
        return False
    def updateTurnCounter(self):
        self.turnCounter+=1
    def clickRedandBlue(self, event):
            if self.turnCounter%2==0:
                self.clickPieceRed(event.x, event.y)
            elif self.turnCounter%2==1:
                self.clickBluePiece(event.x, event.y)
    def clickGreenandPurple(self, event):
        if self.turnCounter%2==1:
            self.clickPurplePiece(event.x, event.y)
        elif self.turnCounter%2==0:
            self.clickGreenPiece(event.x, event.y)
    def deselectPawn(self):
        for row in range(6):
            for col in range(6):
                if self.matrixchecker[row][col]==2:
                    self.matrixchecker[row][col]=1
                elif self.matrixchecker[row][col]==-2:
                   self.matrixchecker[row][col]=-1
        self.paintBoard()
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
matrixChecker= Matrix()
c=CheckerBoard(matrixChecker)
root = Tk()
b= Button(root, text= "Deselect Piece", command=c.deselectPawn)
b.pack()
canvas = Canvas(root, width=600, height=600)
canvas.pack()
c.createBoard()
canvas.bind("<Button-1>", c.clickRedandBlue)
canvas.pack()
canvas.bind("<Double-Button-1>", c.clickGreenandPurple)
canvas.pack()
c.paintBoard()
root.mainloop()
