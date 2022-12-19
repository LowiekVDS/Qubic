#pragma once

#include "Game.h"
#include <random>

class RandomPlayer
{

public:
  Game &game;
  char player;

  RandomPlayer(Game &game, char player) : game(game), player(player) {}

  void move()
  {

    // Random number
    char nr_of_moves = this->game.getLegalMovesCount();

    if (nr_of_moves == 0 || this->game.state != ACTIVE)
      return;

    std::random_device rd;                                     // obtain a random number from hardware
    std::mt19937 gen(rd());                                    // seed the generator
    std::uniform_int_distribution<> distr(0, nr_of_moves - 1); // define the range

    char move = distr(gen);

    vector<Move> moves;
    this->game.getLegalMoves(moves);

    this->game.move(moves[move], player);
    game.updateHeuristics(moves[move], player);
  }
};