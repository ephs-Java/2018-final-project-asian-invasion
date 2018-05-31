import random
from collections import namedtuple

import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

from checkers import CheckerBoard

FILE_NAME = 'alternate_state_vec.h5'

Move = namedtuple('Move', ['oldLoc', 'newLoc'])
TrainingData = namedtuple('TrainingData', ['stateVec', 'whoWins'])

thing_1 = Sequential()

# Adding the input layerthing_1.add(Dense(units=1, kernel_initializer='uniform', activation='tanh', input_dim=16))

thing_1.add(Dense(units=64, kernel_initializer='uniform', activation='relu', input_dim=32))
thing_1.add(Dense(units=64, kernel_initializer='uniform', activation='relu', input_dim=64))
thing_1.add(Dense(units=1, kernel_initializer='uniform', activation='tanh', input_dim=64))

# output 0 for not win, 1 for win
thing_1.compile(optimizer="adadelta", loss="mse", metrics=['accuracy'])

thing_2 = Sequential()

# Adding the input layer
thing_2.add(Dense(units=64, kernel_initializer='uniform', activation='relu', input_dim=32))
thing_2.add(Dense(units=64, kernel_initializer='uniform', activation='relu', input_dim=64))
thing_2.add(Dense(units=1, kernel_initializer='uniform', activation='tanh', input_dim=64))

# output 0 for not win, 1 for win
thing_2.compile(optimizer="adadelta", loss="mse", metrics=['accuracy'])


try:
    thing_1.load_weights("customcheckers/thing1___" + FILE_NAME)
except Exception:
    print("WARN: model thing1 has not been saved previously")
else:
    print("Loaded thing 1 a-ok")

try:
    thing_2.load_weights("customcheckers/thing2___" + FILE_NAME)
except Exception as e:
    print("WARN: model thing2 has not been saved previously")
else:
    print("loaded thing2 a-ok")

def max_index(iterable):
    max_val = iterable[0]
    i = 0
    for i, n in enumerate(iterable):
        if n > max_val:
            max_val = n
            i = i
    return i

games_per_itr = 50
if __name__ == '__main__':
    try:
        for super_itr in range(100):

            print("Iteration:", super_itr)
            thing1_data = []
            thing2_data = []

            for i in range(games_per_itr):  # play multiple games
                should_display_game_results = i == games_per_itr - 1
                game = CheckerBoard()
                game.scramble()
                thing1_state_vecs = []
                thing2_state_vecs = []

                # by flippping the board we switch teams but actually stay on team 1 according to the game object
                team_for_real = 1
                moves_taken = 0
                while not game.is_game_over()[0]:  # play 1 game

                    moves = game.get_all_possible_moves()

                    possible_moves_lst = []

                    for piece, possible_piece_moves in moves.items():
                        for possible_piece_move in possible_piece_moves:
                            possible_moves_lst.append(Move(piece, possible_piece_move))
                    random.shuffle(possible_moves_lst)

                    possible_board_states = [game.pretend_to_move_piece(move.oldLoc, move.newLoc) for move in
                                             possible_moves_lst]

                    possible_state_vecs = [state.get_alt_state_vec() for state in possible_board_states]

                    if team_for_real == 1:
                        scores = [thing_1.predict(vec)[0, 0] for vec in possible_state_vecs]
                    else:
                        scores = [thing_2.predict(vec)[0, 0] for vec in possible_state_vecs]

                    best_move = possible_moves_lst[max_index(scores)]

                    game.move_piece(best_move.oldLoc, best_move.newLoc)

                    if team_for_real == 1:
                        thing1_state_vecs.append(game.get_alt_state_vec())
                    else:
                        thing2_state_vecs.append(game.get_alt_state_vec())

                    if should_display_game_results and team_for_real == 1:
                        print(game)
                    game.flip_board_nocopy()
                    if should_display_game_results and team_for_real == -1:
                        print(game)

                    if should_display_game_results:
                        print("#############################################################################")
                    team_for_real *= -1
                    moves_taken += 1


                did_we_win = game.is_game_over()
                print("Played", i, "of", games_per_itr, "games")
                # post game memory
                who_actually_won = team_for_real * did_we_win[1]

                thing1_score = ((who_actually_won + 1) / 2) * 6 / moves_taken
                thing2_score = (-who_actually_won + 1) / 2

                thing1_data.extend(
                    TrainingData(state_vec, thing1_score) for state_vec in thing1_state_vecs)
                thing2_data.extend(
                    TrainingData(state_vec, thing2_score) for state_vec in thing2_state_vecs)

            thing1_state_vecs = np.concatenate(tuple(training_data.stateVec for training_data in thing1_data), axis=0)
            thing1_who_wins = np.matrix([[training_data.whoWins] for training_data in thing1_data])

            thing2_state_vecs = np.concatenate(tuple(training_data.stateVec for training_data in thing1_data), axis=0)
            thing2_who_wins = np.matrix([[training_data.whoWins] for training_data in thing1_data])

            print("Fitting thing 1")
            thing_1.fit(thing1_state_vecs, thing1_who_wins, epochs=10, batch_size=10)

            print("Fitting thing 2")
            thing_2.fit(thing2_state_vecs, thing2_who_wins, epochs=10, batch_size=10)

        thing_1.save_weights(FILE_NAME)

    except KeyboardInterrupt as e:
        thing_1.save_weights('thing1___' + FILE_NAME)
        thing_2.save_weights('thing2___' + FILE_NAME)
        print("WARN: Crashed")
        print(e)
