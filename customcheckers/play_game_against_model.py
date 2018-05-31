import random
from collections import namedtuple

from checkers import CheckerBoard
from neuralnet import max_index, thing_1, thing_2

Move = namedtuple('Move', ['oldLoc', 'newLoc'])
TrainingData = namedtuple('TrainingData', ['stateVec', 'whoWins'])

game = CheckerBoard()

HUMAN_PLAYING = True


def get_moves_human():
    print("Your pieces are", game.get_team_locs(-1))
    piece_index = int(input("Select an index"))
    piece = game.get_team_locs(-1)[piece_index]

    possible_moves = game.get_possible_moves(piece[0], piece[1])
    if len(possible_moves) == 0:
        print("No moves possible. Try again. ")
        return get_moves_human()
    print("You can move that piece to", possible_moves)
    if len(possible_moves) == 1:
        move = game.get_possible_moves(piece[0], piece[1])[0]
    else:
        move_index = int(input("Select an index"))
        try:
            move = game.get_possible_moves(piece[0], piece[1])[move_index]
        except (IndexError, KeyError):
            print("Invalid index. Try again.")
            return get_moves_human()

    return piece, move


def get_moves_computer(board, model=thing_2):
    moves = board.get_all_possible_moves()

    possible_moves_lst = []
    random.shuffle(possible_moves_lst)
    for piece, possible_piece_moves in moves.items():
        for possible_piece_move in possible_piece_moves:
            possible_moves_lst.append(Move(piece, possible_piece_move))

    possible_board_states = [game.pretend_to_move_piece(move.oldLoc, move.newLoc) for move in
                             possible_moves_lst]

    possible_state_vecs = [state.get_alt_state_vec() for state in possible_board_states]

    scores = [model.predict(vec)[0, 0] for vec in possible_state_vecs]

    return possible_moves_lst[max_index(scores)]


if __name__ == "__main__":
    while not game.is_game_over()[0]:
        if game.current_turn == 1:
            best_move = get_moves_computer(thing_1)

            game.move_piece(best_move.oldLoc, best_move.newLoc)
        else:

            if HUMAN_PLAYING:
                piece, move = get_moves_human()
                game.move_piece(piece, move)

            else:
                game.flip_board_nocopy()  # flip it for use

                best_move = get_moves_computer(thing_2)

                game.move_piece(best_move.oldLoc, best_move.newLoc)

                game.flip_board_nocopy()  # flip it back

        print(game)
        print("############################################################################")
        # time.sleep(2)
