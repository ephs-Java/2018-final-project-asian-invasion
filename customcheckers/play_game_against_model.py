import random
from collections import namedtuple

import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

from checkers import CheckerBoard
from neuralnet import max_index

Move = namedtuple('Move', ['oldLoc', 'newLoc'])
TrainingData = namedtuple('TrainingData', ['stateVec', 'whoWins'])
model = Sequential()

# Adding the input layer
model.add(Dense(units=16, kernel_initializer='uniform', activation='relu', input_dim=8))
model.add(Dense(units=1, kernel_initializer='uniform', activation='tanh', input_dim=16))

# output 0 for not win, 1 for win
model.compile(optimizer="adadelta", loss="mse", metrics=['accuracy'])

try:
    model.load_weights('crashed___checkers_model_tanh_adadelta.h5')
except Exception:
    print("WARN: model has not been saved previously")



game = CheckerBoard()


while not game.is_game_over()[0]:
    if game.current_turn == 1:
        moves = game.get_all_possible_moves()

        possible_moves_lst = []

        for piece, possible_piece_moves in moves.items():
            for possible_piece_move in possible_piece_moves:
                possible_moves_lst.append(Move(piece, possible_piece_move))

        random.shuffle(possible_moves_lst)
        possible_board_states = [game.pretend_to_move_piece(move.oldLoc, move.newLoc) for move in
                                 possible_moves_lst]

        possible_state_vecs = [state.get_state_vec() for state in possible_board_states]

        scores = [model.predict(vec)[0, 0] for vec in possible_state_vecs]

        best_move = possible_moves_lst[max_index(scores)]

        game.move_piece(best_move.oldLoc, best_move.newLoc)
    else:
        def get_moves():
            print("Your pieces are", game.get_team_locs(-1))
            piece_index = int(input("Select an index"))
            piece = game.get_team_locs(-1)[piece_index]

            possible_moves = game.get_possible_moves(piece[0], piece[1])
            if len(possible_moves) == 0:
                print("No moves possible. Try again. ")
                return get_moves()
            print("You can move that piece to", possible_moves)
            if len(possible_moves) == 1:
                move = game.get_possible_moves(piece[0], piece[1])[0]
            else:
                move_index = int(input("Select an index"))
                move = game.get_possible_moves(piece[0], piece[1])[move_index]

            return piece, move

        piece,  move = get_moves()
        game.move_piece(piece, move)
        # game.flip_board_nocopy()
        # moves = game.get_all_possible_moves()






        # possible_moves_lst = []
        # random.shuffle(possible_moves_lst)
        # for piece, possible_piece_moves in moves.items():
        #     for possible_piece_move in possible_piece_moves:
        #         possible_moves_lst.append(Move(piece, possible_piece_move))
        #
        # possible_board_states = [game.pretend_to_move_piece(move.oldLoc, move.newLoc) for move in
        #                          possible_moves_lst]
        #
        # possible_state_vecs = [state.get_state_vec() for state in possible_board_states]
        #
        # scores = [model.predict(vec)[0, 0] for vec in possible_state_vecs]
        #
        # best_move = possible_moves_lst[max_index(scores)]
        #
        # game.move_piece(best_move.oldLoc, best_move.newLoc)
        # game.flip_board_nocopy()
    print(game)
    print("############################################################################")

