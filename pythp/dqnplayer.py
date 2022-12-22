from random import randint
import board
import numpy as np
import json
import tensorflow as tf
import keras
from keras.layers import Dense
from collections import deque
import random

MIN_REPLAY_SIZE = 1000

def agent():
    learning_rate = 0.001
    init = tf.keras.initializers.HeUniform()
    model = keras.Sequential()
    model.add(keras.layers.Dense(10, input_shape=(76,), activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(10, activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(64, activation='softmax', kernel_initializer=init))
    model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])
    return model

class DQNPlayer:

    # Cross starts
    def __init__(self, game: board.Board, symbol=board.CROSS) -> None:
        self.board = game
        self.symbol = symbol

        self.learning_rate = 0.7 # Learning rate
        self.discount_factor = 0.618
        self.batch_size = 128
        self.steps_to_update_target_model = 0

        self.epsilon = 1 # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start
        self.max_epsilon = 1 # You can't explore more than 100% of the time
        self.min_epsilon = 0.01 # At a minimum, we'll always explore 1% of the time
        self.decay = 0.01

        self.episode = 0

        self.replay_memory = deque(maxlen=100000)

        self.model = agent()
        self.target_model = agent()
        self.target_model.set_weights(self.model.get_weights())

        print(self.model.summary())

    def new_episode(self):
        self.episode += 1
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay * self.episode)

    def to_int(self, i, j, k):
        return i * 16 + j * 4 + k

    def int_to_move(self, move_id):
        i = move_id // 16
        j = (move_id - i * 16) // 4
        k = (move_id - i * 16 - j * 4)

        return i,j,k

    def train(self, done):
        return

        if len(self.replay_memory) < MIN_REPLAY_SIZE:
            return

        mini_batch = random.sample(self.replay_memory, self.batch_size)
        current_states = np.array([transition[0] for transition in mini_batch])
        current_qs_list = self.model.predict(current_states)
        new_current_states = np.array([transition[3] for transition in mini_batch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        Y = []
        for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
            if not done:
                max_future_q = reward + self.discount_factor * np.max(future_qs_list[index])
            else:
                max_future_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = (1 - self.learning_rate) * current_qs[action] + self.learning_rate * max_future_q

            X.append(observation)
            Y.append(current_qs)

        self.model.fit(np.array(X), np.array(Y), batch_size=self.batch_size, verbose=0, shuffle=True)

    def move(self):

        if self.board.state != board.ACTIVE:
            return [0, 0, 0], False, False

        other_symbol = board.Board.other_side(self.symbol)

        summary = self.board.summary(self.symbol)
        other_summary = self.board.summary(other_symbol)
        csum = self.board.compact_summary(self.symbol)

        # If 3 in a row, do that move
        if 3 in summary:
            # print("Forced WIN: 3 in a row")
            line = board.WINNING_LINES[list(summary).index(3)]
            for move in line:
                if self.board.is_move_legal(move[0], move[1], move[2]):
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    return move, True, False
        if 3 in other_summary:
            # print("Forced BLOCK: 3 in a row")
            line = board.WINNING_LINES[list(other_summary).index(3)]
            for move in line:
                if self.board.is_move_legal(move[0], move[1], move[2]):
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    return move, True, False
        
        # Check if there are moves that transform at least 2 lines from 2 to 3 (guaranteed win)
        for line in self.board.get_candidate_moves_from_summary(summary):
            for move in line:
                trans = self.board.get_move_transitions(summary, move)

                if trans[2] > 1:
                    # print("Forced WIN SEQUENCE: 2x 2-->3")
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    return move, True, False

        # Check if there are moves that transform at least 2 lines from 2 to 3 in opponent (guaranteed loss prevention)
        for line in self.board.get_candidate_moves_from_summary(other_summary):
            for move in line:
                trans = self.board.get_move_transitions(other_summary, move)

                if trans[2] > 1:
                    # print("Forced BLOCK SEQUENCE: 2x 2-->3")
                    self.board.move(move[0], move[1], move[2], self.symbol)
                    return move, True, False

        # If nothing works, run evaluation model to get best action
        # print("DQN/random move")
        # if np.random.rand() < self.epsilon:
        # Random move
        legal_moves = self.board.get_legal_moves()
        N = len(legal_moves[0])
        if N == 0:
            return [0, 0, 0], False, False
        move = randint(0, N-1)
        action = [legal_moves[0][move], legal_moves[1][move], legal_moves[2][move]]
            
        # else:
        #     # Exploit best known action
        #     # model dims are (batch, env.observation_space.n)
        #     encoded = np.array(csum)
        #     encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
        #     predicted = self.model.predict(encoded_reshaped).flatten()

        #     action = np.argmax(predicted)
        #     action = self.int_to_move(action) 

        wasLegal = self.board.is_move_legal(action[0], action[1], action[2])

        self.board.move(action[0], action[1], action[2], self.symbol)

        return action, wasLegal, True