from random import randint
import board
import numpy as np

class RandomPlayer:

  # Cross starts
  def __init__(self, game : board.Board, symbol=board.CROSS) -> None:
    self.board = game
    self.symbol = symbol

  def move(self):
    legal_moves = self.board.get_legal_moves()
    
    N = len(legal_moves[0])

    if N == 0:
      return

    move = randint(0, N-1)

    self.board.move(legal_moves[0][move], legal_moves[1][move], legal_moves[2][move], self.symbol)