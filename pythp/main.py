import numpy as np
from board import *
from randomplayer import RandomPlayer
from minmaxplayer import MinMaxPlayer
from strategicplayer import StrategicPlayer

b = Board()
b.add_wildcards(5)
b.get_legal_moves()

p1 = StrategicPlayer(b, CROSS)
p2 = StrategicPlayer(b, NOUGHT)

win_reasons = []
winners = []
nr_of_games = 1000
for i in range(nr_of_games):
  
  # print(b)
  
  b.clear()
  b.add_wildcards(0)

  while b.state == ACTIVE:
    p1.move()
    # print(b)
    p2.move()
    # print(b)

  if i % 100 == 0:
    print(f"Iteration {i}/{nr_of_games}")

  winners.append(b.state)

for i in range(1, 4):
  print(f"Wins {i}: {winners.count(i) / len(winners)}")

for val in set(win_reasons):
  print(f"Reason {val}: {win_reasons.count(val) / len(win_reasons)}")

# Should be:
#
# Straights: 48 / 76 = 63.15%
# 2ddiag: 24 / 76 = 31.58 %
# 3ddiag : 4 / 76 = 5.2%