import numpy as np
from board import *
from randomplayer import RandomPlayer
from minmaxplayer import MinMaxPlayer
from strategicplayer import StrategicPlayer
from collections import deque
from dqnplayer import DQNPlayer, agent

# Setup of board
b = Board()

p1 = DQNPlayer(b, CROSS)
p2 = StrategicPlayer(b, NOUGHT)

nr_of_wildcards = 0
nr_of_games = 1000

steps_to_update_target_model = 0

winners = deque([], maxlen=10000)

for i in range(nr_of_games):

    # Reset board        
    b.clear()
    b.add_wildcards(nr_of_wildcards)
    
    total_reward = 0

    if i % 100 == 0 and i > 0:
        print(f"Iteration {i}/{nr_of_games}")
        for i in range(1, 4):
            print(f"Wins {i}: {winners.count(i) / len(winners)}")


    while b.state == ACTIVE:
        steps_to_update_target_model += 1

        # Make moves
        observation = b.compact_summary(p1.symbol)
        p1_action, wasLegal, remember = p1.move()
        p2.move()
        final_observation = b.compact_summary(p1.symbol)

        # Determine reward
        reward = 0
        if b.state == p1.symbol:
            reward = 1
        elif not wasLegal:
            print("ILLEGAL MOVE")
            reward = -10
        elif b.state == p2.symbol:
            reward = -1
        
        # Add experience
        if remember:
            p1.replay_memory.append([observation, p1_action, reward, final_observation, b.state != ACTIVE]) 

         # 3. Update the Main Network using the Bellman Equation
        if steps_to_update_target_model % 4 == 0 or b.state != ACTIVE:
            p1.train(b.state != ACTIVE)

    print(len(p1.replay_memory))
    # if steps_to_update_target_model >= 100:
    #     print('Copying main network weights to the target network weights')
    #     p1.target_model.set_weights(p1.model.get_weights())
    #     steps_to_update_target_model = 0

    p1.new_episode()

    winners.append(b.state)



# Should be:
#
# Straights: 48 / 76 = 63.15%
# 2ddiag: 24 / 76 = 31.58 %
# 3ddiag : 4 / 76 = 5.2%