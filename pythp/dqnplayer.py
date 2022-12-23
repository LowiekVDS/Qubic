from random import randint
import board
import numpy as np
import json
import tensorflow as tf
import keras
from keras.layers import Dense
from collections import deque
import random

from dict import dic

MIN_REPLAY_SIZE = 1000

def agent():
    learning_rate = 0.001
    init = tf.keras.initializers.HeUniform()
    model = keras.Sequential()
    #model.add(Conv3D(2, kernel_size=2, activation='relu', input_shape=(4,4,4,2)))
    
   # model.add(Conv2D(1, kernel_size=4, activation='relu'))
    #model.add(Flatten())
    model.add(keras.layers.Dense(64, input_shape=(128,), activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(64, activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(64, activation='softmax', kernel_initializer=init))
    model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), metrics=['accuracy'])

    model.load_weights("weights")

    return model

class DQNPlayer:

    # Cross starts
    def __init__(self, game: board.Board, A, B, symbol=board.CROSS) -> None:
        self.board = game
        self.symbol = symbol

        self.A = A
        self.B = B

        # Stores game information for random moves
        # Used to determine policy in choosing moves
        self.temp_game_buffer = []

        self.model = agent()

        self.ok = False

    def to_int(self, i, j, k):
        return i * 16 + j * 4 + k

    def int_to_move(self, move_id):
        i = move_id // 16
        j = (move_id - i * 16) // 4
        k = (move_id - i * 16 - j * 4)

        return i,j,k

    def move(self):

        if self.board.state != board.ACTIVE:
            return

        other_symbol = board.Board.other_side(self.symbol)

        summary = self.board.summary(self.symbol)
        other_summary = self.board.summary(other_symbol)
        csum = self.board.compact_summary(self.symbol)

        # If 3 in a row, do that move
        if 3 in summary:
            #print("Forced WIN: 3 in a row")
            line = board.WINNING_LINES[list(summary).index(3)]
            for move in line:
                if self.board.is_move_legal(move[0], move[1], move[2]):
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    # self.ok = True
                    return
        if 3 in other_summary:
            #print("Forced BLOCK: 3 in a row")
            line = board.WINNING_LINES[list(other_summary).index(3)]
            for move in line:
                if self.board.is_move_legal(move[0], move[1], move[2]):
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    return
        
        # Check if there are moves that transform at least 2 lines from 2 to 3 (guaranteed win)
        for line in self.board.get_candidate_moves_from_summary(summary):
            for move in line:
                trans = self.board.get_move_transitions(summary, move)

                if trans[2] > 1:
                    #print("Forced WIN SEQUENCE: 2x 2-->3")
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    self.ok = True
                    return

        # Check if there are moves that transform at least 2 lines from 2 to 3 in opponent (guaranteed loss prevention)
        for line in self.board.get_candidate_moves_from_summary(other_summary):
            for move in line:
                trans = self.board.get_move_transitions(other_summary, move)

                if trans[2] > 1:
                    #print("Forced BLOCK SEQUENCE: 2x 2-->3")
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    return

        # Choose the move with most 1 --> 2 transitions, both in his own field and in oponn
        max_move = None
        max_score = 0
        for line in self.board.get_candidate_moves_from_summary(summary):
            for move in line:

                trans = self.board.get_move_transitions(summary, move)
                other_trans = [0, 0, 0, 0]

                # Search for other trans
                done = False
                for other_line in self.board.get_candidate_moves_from_summary(other_summary):
                    for other_move in other_line:

                        if move == other_move:
                            other_trans = self.board.get_move_transitions(other_summary, move)
                            # print("NICE")
                            done = True
                            break
                    if done:
                        break

                score = np.dot(trans, self.A) + np.dot(other_trans, self.B)
                # print(score)

                if score > max_score:
                    max_score = score
                    max_move = list(move)

        # Calculate 
        
        if max_move is not None:
            self.board.move(max_move[0], max_move[1], max_move[2], self.symbol)
            return
        # Choose the

        # h = hash(tuple(list(self.board.to_tensor(self.symbol)[64:])))
        # # print(len(dic))
        # if h in dic:
        #     move = dic[h]
        #     print("fff")
        #     if self.board.is_move_legal(move[0], move[1], move[2]):
        #         self.board.move(move[0], move[1], move[2], self.symbol)
        #         print("OK")
        #         return

        # print(self.board.to_tensor(self.symbol))
        # X = self.board.to_tensor(self.symbol)
        # Y = self.model.predict(np.asarray(X).reshape((1,128)))
        # moveid = np.argmax(Y)
        # # print(moveid, X)
        # action = self.int_to_move(moveid)
        # if self.board.is_move_legal(action[0], action[1], action[2]):
        #     print("Fdsfds")
        #     self.board.move(action[0], action[1], action[2], self.symbol)
        # else:
        # Take move based on score
        scores = []

        # Random move
        legal_moves = self.board.get_legal_moves()
        N = len(legal_moves[0])
        if N == 0:
            return
        move = randint(0, N-1)
        action = [legal_moves[0][move], legal_moves[1][move], legal_moves[2][move]]
        
        trans = self.board.get_move_transitions(summary, action)

        self.board.move(action[0], action[1], action[2], self.symbol)

        # Store action into temp buffer
        self.temp_game_buffer.append((action, self.board.to_tensor(self.symbol), trans))