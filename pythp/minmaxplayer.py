from random import randint
import board as game
import numpy as np
from copy import deepcopy

class MinMaxPlayer:

  # Cross starts
  def __init__(self, game : game.Board, symbol=game.CROSS) -> None:
    self.board = game
    self.symbol = symbol

  def move(self):
    legal_moves = self.board.get_legal_moves()
    
    N = len(legal_moves[0])

    if N == 0:
      return

    score, move = self.minimax(self.board, self.symbol, 0)

    self.board.move(move[0], move[1], move[2], self.symbol)
    
  def minimax(self, board: game.Board, symbol, iter):

    if iter == 2:

      counts, _ = board.count_winning_lines(symbol)
      othercounts, _ = board.count_winning_lines(game.Board.other_side(symbol))

      score = (counts[0] - othercounts[0]) + (counts[1] - othercounts[1]) * 10 + (counts[2] - othercounts[2]) * 100 + (counts[3] - othercounts[3]) * 1000

      return score, board.random_empty_spot()
      
    # Check if the game is already over
    if len(board.get_legal_moves()[0]) == 0 or board.state != game.ACTIVE:
        if board.state == game.DRAW:
          return 0, board.random_empty_spot()
        else:
          return (1, board.random_empty_spot()) if board.state == symbol else (-1, board.random_empty_spot())

    best_move = None
    best_score = -np.inf if symbol == self.symbol else np.inf

    # Loop over all possible moves
    legal_moves = board.get_legal_moves()
    # print(board.get_legal_nr_of_moves())
    for i in range(board.get_nr_of_legal_moves()):

        move = (legal_moves[0][i], legal_moves[1][i], legal_moves[2][i])
        # Apply the move to the game state
        future_board = deepcopy(board)
        # print(move)
        future_board.move(move[0], move[1], move[2], symbol)
        # print(fut)

        # Calculate the score for the future state using minimax
        score, _ = self.minimax(future_board, game.CROSS if self.symbol == symbol else game.NOUGHT, iter+1)
        # Update the best score and move if necessary
        if symbol == self.symbol:
          if score > best_score:
              best_score = score
              best_move = move
        else:
          if score < best_score:
            best_score = score
            best_move = move

    return best_score, best_move

