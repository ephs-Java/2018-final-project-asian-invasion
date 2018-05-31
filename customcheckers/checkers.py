import random

import numpy as np


def sgn(x):
    return abs(x) / x


def sum_tuple(a, b):
    return tuple(sum(c) for c in zip(a, b))


class CheckerBoard:

    KING_VAL = 3

    def __init__(self, board_to_use=None, current_turn=1):
        # 0, 0 is at top left.
        # 7, 0 is at bottom left

        if board_to_use is None:
            self.board = np.zeros((8, 8))
            self._init_board()
        else:
            self.board = board_to_use
        self.current_turn = current_turn  # positive team goes first

    def _init_board(self):
        # Each player starts with 8 pieces (should be 12)

        # Fill top row with team positive
        for i in range(8):
            self.board[i % 2, i] = 1

        # Fill bottom row with team negative
        for i in range(8):
            self.board[6 + i % 2, i] = -1

    def _move_to_capture(self, r, c):
        team = sgn(self.board[r, c])
        opposing_team = -1 * team
        capturables = []
        is_king = abs(self.board[r, c]) == CheckerBoard.KING_VAL
        can_go_south = is_king or sgn(self.board[r, c]) == 1
        can_go_north = is_king or sgn(self.board[r, c]) == -1
        if r > 1 and can_go_north:  # check r - 1
            if c > 1:  # check c - 1
                if self.board[r - 1, c - 1] != 0 and sgn(
                        self.board[r - 1, c - 1]) == opposing_team:  # there is an enemy northwest to us
                    if self.board[r - 2, c - 2] == 0:  # if there is an empty space beyond northwest
                        capturables.append((r - 2, c - 2, True))
            if c < 6:  # check c + 1
                if self.board[r - 1, c + 1] != 0 and sgn(
                        self.board[r - 1, c + 1]) == opposing_team:  # there is an enemy northeast to us
                    if self.board[r - 2, c + 2] == 0:  # if there is an empty space beyond northeast
                        capturables.append((r - 2, c + 2, True))
        if r < 6 and can_go_south:  # check r + 1
            if c > 1:  # check c - 1
                if self.board[r + 1, c - 1] != 0 and sgn(
                        self.board[r + 1, c - 1]) == opposing_team:  # there is an enemy southwest to us
                    if self.board[r + 2, c - 2] == 0:  # if there is an empty space beyond southwest
                        capturables.append((r + 2, c - 2, True))
            if c < 6:  # check c + 1
                if self.board[r + 1, c + 1] != 0 and sgn(
                        self.board[r + 1, c + 1]) == opposing_team:  # there is an enemy southeast to us
                    if self.board[r + 2, c + 2] == 0:  # if there is an empty space beyond southeast
                        capturables.append((r + 2, c + 2, True))
        return capturables

    def get_all_possible_moves(self, team=None):
        if team is None:
            team = self.current_turn
        possible_moves = {}
        for piece in self.get_team_locs(team):
            possible_moves[piece] = self.get_possible_moves(piece[0], piece[1])

        return possible_moves

    def get_possible_moves(self, r, c):
        locs_to_check = []
        possible_moves = []
        is_king = abs(self.board[r, c]) == CheckerBoard.KING_VAL
        can_go_south = is_king or sgn(self.board[r, c]) == 1
        can_go_north = is_king or sgn(self.board[r, c]) == -1
        if r > 0 and can_go_north:
            if c > 0:
                locs_to_check.append((r - 1, c - 1))
            if c < 7:
                locs_to_check.append((r - 1, c + 1))
        if r < 7 and can_go_south:
            if c > 0:
                locs_to_check.append((r + 1, c - 1))
            if c < 7:
                locs_to_check.append((r + 1, c + 1))

        for loc in locs_to_check:
            if self.board[loc] == 0:
                possible_moves.append(loc + (False,))

        return self._move_to_capture(r, c) + possible_moves

    def move_piece(self, old_loc, new_loc):
        r, c = old_loc
        new_r, new_c, capture = new_loc
        piece_val = self.board[r, c]
        if sgn(piece_val) != self.current_turn:
            raise Exception("You are playing out of turn")
        if new_loc not in self.get_possible_moves(r, c):
            raise Exception("Moving the piece at " + str(old_loc) + " to " + str(new_loc) + " is an illegal move.")
        self.board[r, c] = 0
        self.board[new_r, new_c] = piece_val
        if capture:
            captured_r = int((r + new_r) / 2)
            captured_c = int((c + new_c) / 2)
            self.board[captured_r, captured_c] = 0
        if sgn(piece_val) == 1 and new_r == 7:
            self.board[new_r, new_c] = CheckerBoard.KING_VAL
        elif sgn(piece_val) == -1 and new_r == 0:
            self.board[new_r, new_c] = -CheckerBoard.KING_VAL
        self.current_turn *= -1


    def pretend_to_move_piece(self, old_loc, new_loc):
        board_copy = self.board.copy()
        r, c = old_loc
        new_r, new_c, capture = new_loc
        piece_val = board_copy[r, c]
        board_copy[r, c] = 0
        board_copy[new_r, new_c] = piece_val
        if capture:
            captured_r = int((r + new_r) / 2)
            captured_c = int((c + new_c) / 2)
            board_copy[captured_r, captured_c] = 0
        return CheckerBoard(board_to_use=board_copy, current_turn=self.current_turn)

    def flip_board(self):
        board_copy = np.flipud(self.board.copy())
        return CheckerBoard(-board_copy, self.current_turn)

    def flip_board_nocopy(self):
        self.board = -np.flipud(self.board)
        self.current_turn *= -1

    def count_team_pieces(self, team):
        return self._count(lambda x: x != 0 and sgn(x) == team)

    def count_team_kings(self, team):
        return self._count(lambda x: x == team * CheckerBoard.KING_VAL)

    def get_team_locs(self, team):
        return self._get_locs(lambda x: x != 0 and sgn(x) == team)

    def _get_locs(self, categorizer):
        locs = []
        for r, row in enumerate(self.board):
            for c, entry in enumerate(row):
                if categorizer(entry):
                    locs.append((r, c))

        return locs

    def _count(self, categorizer):
        count = 0
        for row in self.board:
            for entry in row:
                if categorizer(entry):
                    count += 1
        return count

    def __str__(self):
        rows = []
        for r, row in enumerate(self.board):
            rows.append("| ")
            for c, entry in enumerate(row):
                if entry == 0:
                    rows[2 * r] += " "
                elif entry == 1:
                    rows[2 * r] += "x"
                elif entry == CheckerBoard.KING_VAL:
                    rows[2 * r] += "X"
                elif entry == -1:
                    rows[2 * r] += "o"
                elif entry == -CheckerBoard.KING_VAL:
                    rows[2 * r] += "0"
                rows[2 * r] += " | "
            rows.append("".join("-" for _ in range(34)))

        return "\n".join(rows)

    def copy(self):
        return CheckerBoard(self.board.copy, self.current_turn)

    def get_endangered_pieces(self, team):
        locs = set()
        enemys_possible_moves = self.get_all_possible_moves(-team)
        for piece, possible_moves in enemys_possible_moves.items():
            for possible_move in possible_moves:
                if possible_move[2]:  # if can capture
                    locs.add(((piece[0] + possible_move[0]) / 2, (piece[1] + possible_move[1]) / 2))
        return list(locs)

    def is_game_over(self):
        if self.count_team_pieces(1) == 0:
            return True, -1  # negative team won
        elif self.count_team_pieces(-1) == 0:
            return True, 1  # positive team won
        else:
            current_players_pieces = self.get_team_locs(self.current_turn)
            for r, c in current_players_pieces:
                if len(self.get_possible_moves(r, c)) != 0:
                    return False, 0  # pieces can still move
            return True, -self.current_turn  # drawn

    def get_state_vec(self):
        vec = np.zeros((1, 8))  # 6 rows, 1 column
        # assume computer is playing team positive
        vec[0, 0] = self.count_team_pieces(1) / 8  # our pieces
        vec[0, 1] = self.count_team_pieces(-1) / 8  # enemy pieces
        vec[0, 2] = self.count_team_kings(1) / 8  # our kings
        vec[0, 3] = self.count_team_kings(-1) / 8  # enemy kings
        vec[0, 4] = len(self.get_endangered_pieces(1)) / 8  # our pieces in danger
        vec[0, 5] = len(self.get_endangered_pieces(-1)) / 8  # enemy pieces in danger
        vec[0, 6] = self.get_vertical_com(1) / 7
        vec[0, 7] = self.get_vertical_com(-1) / 7

        return vec

    def get_alt_state_vec(self):
        vec = np.zeros((1, 32))
        vec_i = 0
        for r, row in enumerate(self.board):
            for c, entry in enumerate(row):
                if (r + c) % 2 == 0:
                    vec[0, vec_i] = entry
        return vec


    def scramble(self):
        for _ in range(random.randint(8, 25)):
            all_allowed_moves = self.get_all_possible_moves()
            capturing_moves = []
            for piece, potential_moves in all_allowed_moves.items():
                if len(potential_moves) > 0:
                    # pass
                    for move in potential_moves:
                        if move[2]:  # if capture
                            capturing_moves.append((piece, move))
                            break
                if len(capturing_moves) > 0:
                    break
            if len(capturing_moves) > 0:
                move_choice = random.choice(capturing_moves)
                self.move_piece(move_choice[0], move_choice[1])
            else:
                allowed_moves_lst = list(all_allowed_moves.items())
                random.shuffle(allowed_moves_lst)
                for piece, potential_moves in allowed_moves_lst:
                    if len(potential_moves) > 0:
                        self.move_piece(piece, potential_moves[0])
                        break

    def get_vertical_com(self, team):
        pieces = self.get_team_locs(team)
        sum_vert = sum(piece[0] for piece in pieces)
        if len(pieces) > 0:
            return sum_vert / len(pieces)
        else:
            return 3.5

    def __getitem__(self, item):
        return self.board[item]

    def __setitem__(self, key, value):
        self.board[key] = value



iteration = 0
if __name__ == '__main__':
    board = CheckerBoard()

    # print(board)
    # possible_moves_a = board.get_possible_moves(1, 1)
    # while not board.is_game_over():
    #     all_allowed_moves = board.get_all_possible_moves()
    #     capturing_move = None
    #     for piece, potential_moves in all_allowed_moves.items():
    #         if len(potential_moves) > 0:
    #             # pass
    #             for move in potential_moves:
    #                 if move[2]:  # if capture
    #                     capturing_move = (piece, move)
    #                     break
    #         if capturing_move is not None:
    #             break
    #     if capturing_move is not None:
    #         board.move_piece(capturing_move[0], capturing_move[1])
    #     else:
    #         for piece, potential_moves in all_allowed_moves.items():
    #             if len(potential_moves) > 0:
    #                 board.move_piece(piece, potential_moves[0])
    #                 break
    #     print("\n\n####################################################\n\n")
    #     print(board)
    #     iteration += 1
    #
    #     print("\n\n----------------------------------------------------\n\n")
    # print(board.flip_board())
    #
    #
    print(board)
    board.scramble()
    print(board.get_state_vec())
