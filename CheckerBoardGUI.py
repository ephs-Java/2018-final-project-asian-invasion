import collections
from tkinter import *

from checkers import CheckerBoard

SelectedPiece = collections.namedtuple("SelectedPiece", ['loc', 'team'])


class CheckerBoardGUI():
    def __init__(self, board: CheckerBoard):
        self.turnCounter = 1
        self.board = board
        self.selected = None

    def can_selected_piece_capture(self, target_row, target_col):
        return (target_row, target_col, True) in self.board.get_possible_moves(self.selected.loc[0],
                                                                               self.selected.loc[1])

    def can_selected_piece_move(self, target_row, target_col):
        return (target_row, target_col, False) in self.board.get_possible_moves(self.selected.loc[0],
                                                                                self.selected.loc[1])

    def click_piece(self, event):
        selected_row, selected_col = event.x // 50, event.y // 50
        print("Clicking piece at:", selected_row, ",", selected_col)
        print(self.board.current_turn)
        print(self.board[selected_row, selected_col])
        if self.board.current_turn == 1 and self.board[selected_row, selected_col] > 0:
            self.selected = SelectedPiece((selected_row, selected_col), 1)
        elif self.board.current_turn == -1 and self.board[selected_row, selected_col] < 0:
            self.selected = SelectedPiece((selected_row, selected_col), -1)

        self.repaint_board()

    def repaint_board(self):
        self.draw_checkerboard()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    canvas.create_oval(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='red')
                elif self.board[i][j] == 0:
                    if (i + j) % 2 == 0:
                        canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill="black")
                    else:
                        canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill="gray85")
                elif self.board[i][j] == -1:
                    canvas.create_oval(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='blue2')
                elif self.board[i][j] == CheckerBoard.KING_VAL:
                    canvas.create_oval(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='DarkOrange3')
                elif self.board[i][j] == -CheckerBoard.KING_VAL:
                    canvas.create_oval(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='SkyBlue1')

        if self.selected is not None:
            row, col = self.selected.loc
            if self.selected.team == 1:
                canvas.create_oval(row * 50, col * 50, (row + 1) * 50, (col + 1) * 50, fill='green')
            elif self.selected.team == -1:
                canvas.create_oval(row * 50, col * 50, (row + 1) * 50, (col + 1) * 50, fill='purple1')

    def draw_checkerboard(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    canvas.create_rectangle(row * 50, col * 50, (row + 1) * 50, (col + 1) * 50, fill="black")
                else:
                    canvas.create_rectangle(row * 50, col * 50, (row + 1) * 50, (col + 1) * 50, fill="gray85")

    def move_selected_piece(self, event):
        target_row, target_col = event.x // 50, event.y // 50
        print("Moving selected piece to:", target_row, ",", target_col)
        if self.selected is not None:
            if self.can_selected_piece_capture(target_row, target_col):
                self.board.move_piece(self.selected.loc, (target_row, target_col, True))
            elif self.can_selected_piece_move(target_row, target_col):
                self.board.move_piece(self.selected.loc, (target_row, target_col, False))
        self.selected = None
        self.repaint_board()

    def deselect_piece(self):
        self.selected = None
        self.repaint_board()


matrixChecker = CheckerBoard()
c = CheckerBoardGUI(matrixChecker)
root = Tk()
b = Button(root, text="Deselect Piece", command=c.deselect_piece)
b.pack()
canvas = Canvas(root, width=400, height=400)
canvas.pack()
c.draw_checkerboard()
canvas.bind("<Button-1>", c.click_piece)
canvas.pack()
canvas.bind("<Button-2>", c.move_selected_piece)
canvas.pack()
c.repaint_board()
root.mainloop()
