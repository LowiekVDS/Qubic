#pragma once

#include "Game.h"
#include <random>

class MonteCarlo
{

public:
  Game &game;
  char player;

  MonteCarlo(Game &game, char player) : game(game), player(player) {}

  void move()
  {

    char nr_of_moves = this->game.getLegalMovesCount();

    if (nr_of_moves == 0 || this->game.state != ACTIVE)
      return;

    int score = -9999;
    Move bestMove;

    vector<Move> moves;
    game.getLegalMoves(moves);
    for (auto move : moves)
    {
      int s = minmax(game, player, -999999, 999999, 0);

      if (s > score)
      {
        bestMove = move;
        score = s;
      }
    }

    this->game.move(bestMove, player);
    game.updateHeuristics(bestMove, player);
  }

  int simulate(Game &board, char symbol, int iter)
  {

    // Termination
    if (board.getLegalMovesCount() == 0 || board.state != ACTIVE || iter == 4)
    {

     // cout << iter;// << "\n";

      // Calculate heuristic

      if (board.state == ACTIVE)
      {
        int X_score = 1000 * board.X_group_count[2] + 100 * board.X_group_count[1] + 10 * board.X_group_count[0];
        int O_score = 1000 * board.O_group_count[2] + 100 * board.O_group_count[1] + 10 * board.O_group_count[0];

        return player == 'X' ? X_score - O_score : O_score - X_score;
      }

      // Evaluation function
      if (board.state == DRAW)
      {
        return 0;
      }
      else
      {
        if (board.state == CROSS_WIN && symbol == 'X')
        {
          return 1000;
        }
        else
        {
          return -1000;
        }
      }
    }

    int cScore = player == symbol ? -9999 : 9999;

    vector<Move> moves;
    board.getLegalMoves(moves);
    for (auto move : moves)
    {

      // Do move
      board.move(move, symbol);

      // Calculate score
      int score = this->minmax(board, player == 'X' ? 'O' : 'X', alpha, beta, iter + 1);

      // Undo move
      board.board[move.x][move.y][move.z] = ' ';
      board.state = ACTIVE;

      if (player == symbol && score > cScore)
      {
        cScore = score;

        if (cScore >= beta)
        {
          break;
        }

        alpha = alpha > cScore ? alpha : cScore;
      }
      else if (player != symbol && score < cScore)
      {
        cScore = score;

        if (cScore <= alpha)
        {
          break;
        }

        beta = beta < cScore ? beta : cScore;
      }
    }

    return cScore;
  }
};