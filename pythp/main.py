import numpy as np
from board import *
from randomplayer import RandomPlayer
from minmaxplayer import MinMaxPlayer
from strategicplayer import StrategicPlayer
from collections import deque
from dqnplayer import DQNPlayer, agent
import random

# Setup of board
b = Board()

p1 = DQNPlayer(b, [], [],  CROSS)
p2 = StrategicPlayer(b, NOUGHT)

nr_of_games = 100

steps_to_update_target_model = 0

winners = deque([], maxlen=10000)

game_buffer = []

bestA = None
bestB = None

bestRatio = 0

for j in range(100):

    scaleA = [random.randint(0, 10) for i in range(2)]
    scaleB = [random.randint(0, 10) for i in range(2)]

    A = [random.uniform(-scaleA[0] * (i+1), scaleA[1] * (i+1)) for i in range(4)]
    B = [random.uniform(-scaleB[0] * (i+1), scaleB[1]  * (i+1)) for i in range(4)]
    # A = [5.427628436846672, 7.544349900985335, 23.964134330037293, 21.79992859580046]
    # B = [0.7273519014046617, 0.23613172861757192, -6.747686136903879, 8.069420932370463]

    p1.A = A
    p1.B = B

    for i in range(nr_of_games):

        # Reset board        
        b.clear()
        nr_of_wildcards = np.random.randint(0,10)
        b.add_wildcards(nr_of_wildcards)
        p1.ok = False
        
        total_reward = 0

        if i % 10 == 0:
            print(f"Iteration {i}/{nr_of_games}")
            for i in range(1, 4):
                print(f"Wins {i}: {winners.count(i) / max(len(winners),1)}")


        while b.state == ACTIVE:
            steps_to_update_target_model += 1

            # Make moves
            # print(b)
            p2.move()
            # print(b)
            p1.move()
            # print(b)
        #print(b)

        # Store game
        # if p1.ok:
        #     game_buffer.append(p1.temp_game_buffer)
        p1.temp_game_buffer = []

        winners.append(b.state)

    ratio = winners.count(2) / max(len(winners),1) + winners.count(3) / max(len(winners),1)

    if ratio > bestRatio:
        bestRatio = ratio
        bestA = A
        bestB = B

        f = open("result.txt", 'w')
        f.write(str(A) + "\n")
        f.write(str(B) + "\n")
        f.write(str(bestRatio) + "\n")
        f.close()

    print(f"Best: {bestRatio}")

    for i in range(1, 4):
        print(f"Wins {i}: {winners.count(i) / max(len(winners),1)}")

# Do some analysis