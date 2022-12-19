#pragma once

#include "Game.h"
#include <random>
#include <algorithm>

class MinMax
{

public:
  Game &game;
  char player;

  MinMax(Game &game, char player) : game(game), player(player) {}

  void move()
  {

    // TODO Check for quick moves (or blocks)

    char nr_of_moves = this->game.getLegalMovesCount();

    if (nr_of_moves == 0 || this->game.state != ACTIVE)
      return;

    int score = -99999;
    Move bestMove;

    vector<Move> moves;
    game.getLegalMoves(moves);
    auto rng = std::default_random_engine {};
    std::shuffle(std::begin(moves), std::end(moves), rng);
    for (auto move : moves)
    {
      game.move(move, player);
      int s = minmax(game, player == 'X' ? 'O' : 'X', -999999, 999999, 3);
      game.board[move.x][move.y][move.z] = ' ';
      game.state = ACTIVE;

      // cout << s << '\n';
      if (s > score)
      {
        bestMove = move;
        score = s;
      }
    }

    this->game.move(bestMove, player);
    game.updateHeuristics(bestMove, player);
  }

  int minmax(Game &board, char symbol, int alpha, int beta, int iter)
  {

    // Termination
    if (board.getLegalMovesCount() == 0 || board.state != ACTIVE || iter == 0)
    {

     // cout << iter;// << "\n";

      // Calculate heuristic

      if (board.state == ACTIVE)
      {
        // int X_score = 1000 * board.X_group_count[2] + 100 * board.X_group_count[1] + 10 * board.X_group_count[0];
        // int O_score = 1000 * board.O_group_count[2] + 100 * board.O_group_count[1] + 10 * board.O_group_count[0];

        int s = board.calculateHeuristics(symbol) - board.calculateHeuristics(symbol == 'X' ? 'O' : 'X');

        // cout << s << "\n";

        return s;
      }

      // Evaluation function
      if (board.state == DRAW)
      {
        return 0;
      }
      else
      {
        if ((board.state == CROSS_WIN && this->player == 'X') || (board.state == NOUGHT_WIN && this->player == 'O'))
        {
          return 10000;
        }
        else
        {
          return -10000;
        }
      }
    }

    int cScore = player == symbol ? -99999 : 99999;

    vector<Move> moves;
    board.getLegalMoves(moves);
    for (auto move : moves)
    {

      // Do move
      board.move(move, symbol);

      // Calculate score
      int score = this->minmax(board, symbol == 'X' ? 'O' : 'X', alpha, beta, iter - 1);

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