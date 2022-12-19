#include <iostream>
#include "Game.h"
#include "RandomPlayer.h"
#include "MinMax.h"
#include <vector>

using namespace std;

int main()
{

int wildcards[64] = {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

  // Choose wildcards randomly


  Game board = Game(16);
  board.resetBoard();

  

  // Generate random playrs
  MinMax *p1 = new MinMax(board, 'X');
  RandomPlayer *p2 = new RandomPlayer(board, 'O');

  int nr_of_games = 10;
  int winners[4] = {0};

  for (int i = 0; i < nr_of_games; i++)
  {

    board.resetBoard();
    board.print();
    while (board.state == ACTIVE)
    {
      p1->move();
      // board.print();
       p2->move();
      // board.print();
      
      
     
    }
    winners[board.state] += 1;

  }

  cout << float(winners[1]) / float(nr_of_games) << '\n';
  cout << float(winners[2]) / float(nr_of_games) << '\n';
  cout << float(winners[3]) / float(nr_of_games) << '\n';

  return 0;
}