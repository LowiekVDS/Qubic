#pragma once

#include "vector"
#include <random>

using namespace std;

struct Move
{
  char x;
  char y;
  char z;
};

enum GameState
{
  ACTIVE,
  DRAW,
  CROSS_WIN,
  NOUGHT_WIN
};

const char WINNING_LINES[76][4][3] = {
  // Straights 1
  {{0, 0, 0}, {0, 0, 1}, {0, 0, 2}, {0, 0, 3}},
  {{0, 1, 0}, {0, 1, 1}, {0, 1, 2}, {0, 1, 3}},
  {{0, 2, 0}, {0, 2, 1}, {0, 2, 2}, {0, 2, 3}},
  {{0, 3, 0}, {0, 3, 1}, {0, 3, 2}, {0, 3, 3}},
  {{1, 0, 0}, {1, 0, 1}, {1, 0, 2}, {1, 0, 3}},
  {{1, 1, 0}, {1, 1, 1}, {1, 1, 2}, {1, 1, 3}},
  {{1, 2, 0}, {1, 2, 1}, {1, 2, 2}, {1, 2, 3}},
  {{1, 3, 0}, {1, 3, 1}, {1, 3, 2}, {1, 3, 3}},
  {{2, 0, 0}, {2, 0, 1}, {2, 0, 2}, {2, 0, 3}},
  {{2, 1, 0}, {2, 1, 1}, {2, 1, 2}, {2, 1, 3}},
  {{2, 2, 0}, {2, 2, 1}, {2, 2, 2}, {2, 2, 3}},
  {{2, 3, 0}, {2, 3, 1}, {2, 3, 2}, {2, 3, 3}},
  {{3, 0, 0}, {3, 0, 1}, {3, 0, 2}, {3, 0, 3}},
  {{3, 1, 0}, {3, 1, 1}, {3, 1, 2}, {3, 1, 3}},
  {{3, 2, 0}, {3, 2, 1}, {3, 2, 2}, {3, 2, 3}},
  {{3, 3, 0}, {3, 3, 1}, {3, 3, 2}, {3, 3, 3}},

  // Straights 2

  {{0, 0, 0}, {0, 1, 0}, {0, 2, 0}, {0, 3, 0}},   
  {{0, 0, 1}, {0, 1, 1}, {0, 2, 1}, {0, 3, 1}},         
  {{0, 0, 2}, {0, 1, 2}, {0, 2, 2}, {0, 3, 2}},         
  {{0, 0, 3}, {0, 1, 3}, {0, 2, 3}, {0, 3, 3}},         
  {{1, 0, 0}, {1, 1, 0}, {1, 2, 0}, {1, 3, 0}},            
  {{1, 0, 1}, {1, 1, 1}, {1, 2, 1}, {1, 3, 1}},         
  {{1, 0, 2}, {1, 1, 2}, {1, 2, 2}, {1, 3, 2}},          
  {{1, 0, 3}, {1, 1, 3}, {1, 2, 3}, {1, 3, 3}},          
  {{2, 0, 0}, {2, 1, 0}, {2, 2, 0}, {2, 3, 0}},           
  {{2, 0, 1}, {2, 1, 1}, {2, 2, 1}, {2, 3, 1}},         
  {{2, 0, 2}, {2, 1, 2}, {2, 2, 2}, {2, 3, 2}},           
  {{2, 0, 3}, {2, 1, 3}, {2, 2, 3}, {2, 3, 3}},          
  {{3, 0, 0}, {3, 1, 0}, {3, 2, 0}, {3, 3, 0}},           
  {{3, 0, 1}, {3, 1, 1}, {3, 2, 1}, {3, 3, 1}},          
  {{3, 0, 2}, {3, 1, 2}, {3, 2, 2}, {3, 3, 2}},          
  {{3, 0, 3}, {3, 1, 3}, {3, 2, 3}, {3, 3, 3}},     

  // Straights 3

  {{0, 0, 0}, {1, 0, 0}, {2, 0, 0}, {3, 0, 0}},   
  {{0, 0, 1}, {1, 0, 1}, {2, 0, 1}, {3, 0, 1}},         
  {{0, 0, 2}, {1, 0, 2}, {2, 0, 2}, {3, 0, 2}},         
  {{0, 0, 3}, {1, 0, 3}, {2, 0, 3}, {3, 0, 3}},         
  {{0, 1, 0}, {1, 1, 0}, {2, 1, 0}, {3, 1, 0}},            
  {{0, 1, 1}, {1, 1, 1}, {2, 1, 1}, {3, 1, 1}},         
  {{0, 1, 2}, {1, 1, 2}, {2, 1, 2}, {3, 1, 2}},          
  {{0, 1, 3}, {1, 1, 3}, {2, 1, 3}, {3, 1, 3}},          
  {{0, 2, 0}, {1, 2, 0}, {2, 2, 0}, {3, 2, 0}},           
  {{0, 2, 1}, {1, 2, 1}, {2, 2, 1}, {3, 2, 1}},         
  {{0, 2, 2}, {1, 2, 2}, {2, 2, 2}, {3, 2, 2}},           
  {{0, 2, 3}, {1, 2, 3}, {2, 2, 3}, {3, 2, 3}},          
  {{0, 3, 0}, {1, 3, 0}, {2, 3, 0}, {3, 3, 0}},           
  {{0, 3, 1}, {1, 3, 1}, {2, 3, 1}, {3, 3, 1}},          
  {{0, 3, 2}, {1, 3, 2}, {2, 3, 2}, {3, 3, 2}},          
  {{0, 3, 3}, {1, 3, 3}, {2, 3, 3}, {3, 3, 3}},        

  // Diagonals
  
  {{0, 0, 0}, {0, 1, 1}, {0, 2, 2}, {0, 3, 3}},
  {{0, 3, 0}, {0, 2, 1}, {0, 1, 2}, {0, 0, 3}}, 

};

// const char WINNING_LINES = {
//   {0, 0, 0}, {0, 0, 1}, {0, 0, 2}, {0, 0, 3},
//   {0, 0, 0}, {0, 1, 0}, {0, 2, 0}, {0, 3, 0}
// };

class Game
{

public:
  char board[4][4][4];
  GameState state;

  int X_group_count[2]; // 0: 1 value, 1: 2 values, 3: 3 values
  int O_group_count[2];
  int nr_of_wildcards;

  // Constructor
  Game(int nr_of_wildcards) : nr_of_wildcards(nr_of_wildcards), state(ACTIVE)
  {
    this->nr_of_wildcards = nr_of_wildcards;
    cout << nr_of_wildcards;
    // resetBoard();
  }

  void print()
  {
    for (char i = 0; i < 4; i++)
    {
      cout << "---------\n";
      for (char j = 0; j < 4; j++)
      {
        for (char k = 0; k < 4; k++)
        {
          cout << "|" << board[i][j][k];
        }
        cout << "|\n";
      }
    }
    cout << "---------\n\n";
  }

  // Reset board
  void resetBoard()
  {

    X_group_count[0] = 0;
    X_group_count[1] = 0;
    X_group_count[2] = 0;
    O_group_count[0] = 0;
    O_group_count[1] = 0;
    O_group_count[2] = 0;

    state = ACTIVE;
    for (char i = 0; i < 4; i++)
    {
      for (char j = 0; j < 4; j++)
      {
        for (char k = 0; k < 4; k++)
        {

          // if (nr_of_wildcards[i * 16 + j * 4 + k] == 1)
          // {
          //   board[i][j][k] = '*';
          // }
          // else
          // {
            board[i][j][k] = ' ';
          // }
        }
      }
    }

    cout << "WRWEFSD\n";
    cout << nr_of_wildcards;
    cout << "FDS\n";

    for (int i = 0; i < 5; i++)
    {
      std::random_device rd;  // obtain a random number from hardware
      std::mt19937 gen(rd()); // seed the generator
      std::uniform_int_distribution<> distr(0, 3);

      board[distr(gen)][distr(gen)][distr(gen)] = '*';
    }
  }

  // Check for legal moves
  void getLegalMoves(std::vector<Move> &moves)
  {

    for (char i = 0; i < 4; i++)
    {
      for (char j = 0; j < 4; j++)
      {
        for (char k = 0; k < 4; k++)
        {
          if (board[i][j][k] == ' ')
          {
            moves.push_back((Move){i, j, k});
          }
        }
      }
    }
  }

  char getLegalMovesCount()
  {
    char count = 0;
    for (char i = 0; i < 4; i++)
    {
      for (char j = 0; j < 4; j++)
      {
        for (char k = 0; k < 4; k++)
        {
          if (board[i][j][k] == ' ')
          {
            count += 1;
          }
        }
      }
    }
    return count;
  }

  bool isMoveLegal(Move move)
  {
    return this->board[move.x][move.y][move.z] == ' ';
  }

  int calculateHeuristics(char symbol)
  {
    // int x = move.x;
    // int y = move.y;
    // int z = move.z;

    char b[4][4][4];
    for (char i = 0; i < 4; i++)
    {
      for (char j = 0; j < 4; j++)
      {
        for (char k = 0; k < 4; k++)
        {
          if (board[i][j][k] == '*')
          {
            b[i][j][k] = symbol; // == 'X' ? 'O' : 'X';
          }
          else if (board[i][j][k] == ' ')
          {
            b[i][j][k] = symbol;
          }
          else
          {
            b[i][j][k] = board[i][j][k];
          }
        }
      }
    }

    // Check for win
    // Straights

    int nrofavailablewinninglines = 0;

    for (char x = 0; x < 4; x++)
    {
      for (char y = 0; y < 4; y++)
      {
        if (b[x][y][0] == symbol && b[x][y][1] == symbol && b[x][y][2] == symbol && b[x][y][3] == symbol)
        {
          nrofavailablewinninglines++;
        }
        if (b[x][0][y] == symbol && b[x][1][y] == symbol && b[x][2][y] == symbol && b[x][3][y] == symbol)
        {
          nrofavailablewinninglines++;
        }
        if (b[0][y][x] == symbol && b[1][y][x] == symbol && b[2][y][x] == symbol && b[3][y][x] == symbol)
        {
          nrofavailablewinninglines++;
        }
      }
    }
    // Diagonals (2D)
    for (char i = 0; i < 4; i++)
    {
      if (b[i][0][0] == symbol && b[i][1][1] == symbol && b[i][2][2] == symbol && b[i][3][3] == symbol)
      {
        nrofavailablewinninglines++;
      }
      if (b[0][i][0] == symbol && b[1][i][1] == symbol && b[2][i][2] == symbol && b[3][i][3] == symbol)
      {
        nrofavailablewinninglines++;
      }
      if (b[0][0][i] == symbol && b[1][1][i] == symbol && b[2][2][i] == symbol && b[3][3][i] == symbol)
      {
        nrofavailablewinninglines++;
      }
      if (b[i][3][0] == symbol && b[i][2][1] == symbol && b[i][1][2] == symbol && b[i][0][3] == symbol)
      {
        nrofavailablewinninglines++;
      }
      if (b[3][i][0] == symbol && b[2][i][1] == symbol && b[1][i][2] == symbol && b[0][i][3] == symbol)
      {
        nrofavailablewinninglines++;
      }
      if (b[3][0][i] == symbol && b[2][1][i] == symbol && b[1][2][i] == symbol && b[0][3][i] == symbol)
      {
        nrofavailablewinninglines++;
      }
    }

    // Diagonals (3D)
    if (b[0][0][0] == symbol && b[1][1][1] == symbol && b[2][2][2] == symbol && b[3][3][3] == symbol)
    {
      nrofavailablewinninglines++;
    }
    if (b[3][0][0] == symbol && b[2][1][1] == symbol && b[1][2][2] == symbol && b[0][3][3] == symbol)
    {
      nrofavailablewinninglines++;
    }
    if (b[0][3][0] == symbol && b[1][2][1] == symbol && b[2][1][2] == symbol && b[3][0][3] == symbol)
    {
      nrofavailablewinninglines++;
    }
    if (b[0][0][3] == symbol && b[1][1][2] == symbol && b[2][2][1] == symbol && b[3][3][0] == symbol)
    {
      nrofavailablewinninglines++;
    }
    return nrofavailablewinninglines;
  }

  void updateHeuristics(Move move, char symbol)
  {

    // Check areas around move
    int x = move.x;
    int y = move.y;
    int z = move.z;

    char b[4][4][4];
    for (char i = 0; i < 4; i++)
    {
      for (char j = 0; j < 4; j++)
      {
        for (char k = 0; k < 4; k++)
        {
          b[i][j][k] = board[i][j][k] == '*' ? symbol : board[i][j][k];
        }
      }
    }

    //

    // Straights
    // if (x < 3 && b[x + 1][y][z] == symbol)
    // {
    //   if (x < 2 && b[x + 2][y][z] == symbol)
    //   {
    //     groups[2]++;
    //   }
    //   else
    //   {
    //     groups[1]++;
    //   }
    // }
    // if (x > 0 && b[x - 1][y][z] == symbol)
    // {
    //   if (x > 1 && b[x - 2][y][z] == symbol)
    //   {
    //     groups[2]++;
    //   }
    //   else
    //   {
    //     groups[1]++;
    //   }
    // }
    // if (y < 3 && b[x][y + 1][z] == symbol)
    // {
    //   if (y < 2 && b[x][y + 2][z] == symbol)
    //   {
    //     groups[2]++;
    //   }
    //   else
    //   {
    //     groups[1]++;
    //   }
    // }
    // if (y > 0 && b[x][y - 1][z] == symbol)
    // {
    //   if (y > 1 && b[x][y - 2][z] == symbol)
    //   {
    //     groups[2]++;
    //   }
    //   else
    //   {
    //     groups[1]++;
    //   }
    // }
    // if (z < 3 && b[x][y][z + 1] == symbol)
    // {
    //   if (z < 2 && b[x][y][z + 2] == symbol)
    //   {
    //     groups[2]++;
    //   }
    //   else
    //   {
    //     groups[1]++;
    //   }
    // }
    // if (z > 0 && b[x][y][z - 1] == symbol)
    // {
    //   if (z > 1 && b[x][y][z - 2] == symbol)
    //   {
    //     groups[2]++;
    //   }
    //   else
    //   {
    //     groups[1]++;
    //   }
    // }

    // // 2D Diagonals

    // // Check if 2D diagnoals are applicable
    // if (x == y || x == z || y == z || x + y == 3 || x + z == 3 || y + z == 3)
    // {
    //   if (x < 3 && y < 3 && b[x + 1][y + 1][z] == symbol)
    //   {
    //     if (x < 2 && y < 2 && b[x + 2][y + 2][z] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (x > 0 && y > 0 && b[x - 1][y - 1][z] == symbol)
    //   {
    //     if (x > 1 && y > 1 && b[x - 2][y - 2][z] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z < 3 && y < 3 && b[x][y + 1][z + 1] == symbol)
    //   {
    //     if (z < 2 && y < 2 && b[x][y + 2][z + 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z > 0 && y > 0 && b[x][y - 1][z - 1] == symbol)
    //   {
    //     if (z > 1 && y > 1 && b[x][y - 2][z - 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z < 3 && x < 3 && b[x + 1][y][z + 1] == symbol)
    //   {
    //     if (z < 2 && x < 2 && b[x + 2][y][z + 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z > 0 && x > 0 && b[x - 1][y][z - 1] == symbol)
    //   {
    //     if (z > 1 && x > 1 && b[x - 2][y][z - 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (x < 3 && y < 3 && b[x - 1][y + 1][z] == symbol)
    //   {
    //     if (x < 2 && y < 2 && b[x - 2][y + 2][z] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (x > 0 && y > 0 && b[x + 1][y - 1][z] == symbol)
    //   {
    //     if (x > 1 && y > 1 && b[x + 2][y - 2][z] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z < 3 && y < 3 && b[x][y - 1][z + 1] == symbol)
    //   {
    //     if (z < 2 && y < 2 && b[x][y - 2][z + 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z > 0 && y > 0 && b[x][y + 1][z - 1] == symbol)
    //   {
    //     if (z > 1 && y > 1 && b[x][y + 2][z - 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z < 3 && x < 3 && b[x - 1][y][z + 1] == symbol)
    //   {
    //     if (z < 2 && x < 2 && b[x - 2][y][z + 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }

    //   if (z > 0 && x > 0 && b[x + 1][y][z - 1] == symbol)
    //   {
    //     if (z > 1 && x > 1 && b[x + 2][y][z - 2] == symbol)
    //     {
    //       groups[2]++;
    //     }
    //     else
    //     {
    //       groups[1]++;
    //     }
    //   }
    // }

    // // 3D Diagonals
    // // if ((x == y && x == z) || () )

    // if (symbol == 'X') {
    //   X_group_count[0] += groups[0];
    //   X_group_count[1] += groups[1];
    //   X_group_count[2] += groups[2];
    // } else {
    //   O_group_count[0] += groups[0];
    //   O_group_count[1] += groups[1];
    //   O_group_count[2] += groups[2];
    // }
  }

  void move(Move move, char symbol)
  {

    // Check if legal
    if (!this->isMoveLegal(move) || this->state != ACTIVE)
    {
      return;
    }

    // Do move
    this->board[move.x][move.y][move.z] = symbol;

    char b[4][4][4];
    for (char i = 0; i < 4; i++)
    {
      for (char j = 0; j < 4; j++)
      {
        for (char k = 0; k < 4; k++)
        {
          b[i][j][k] = board[i][j][k] == '*' ? symbol : board[i][j][k];
        }
      }
    }

    char x = move.x;
    char y = move.y;
    char z = move.z;

    // Check for win
    // Straights
    if (b[x][y][0] == symbol && b[x][y][1] == symbol && b[x][y][2] == symbol && b[x][y][3] == symbol)
    {
      this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
      return;
    }
    if (b[x][0][z] == symbol && b[x][1][z] == symbol && b[x][2][z] == symbol && b[x][3][z] == symbol)
    {
      this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
      return;
    }
    if (b[0][y][z] == symbol && b[1][y][z] == symbol && b[2][y][z] == symbol && b[3][y][z] == symbol)
    {
      this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
      return;
    }

    // Diagonals (2D)
    for (char i = 0; i < 4; i++)
    {
      if (b[i][0][0] == symbol && b[i][1][1] == symbol && b[i][2][2] == symbol && b[i][3][3] == symbol)
      {
        this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
        return;
      }
      if (b[0][i][0] == symbol && b[1][i][1] == symbol && b[2][i][2] == symbol && b[3][i][3] == symbol)
      {
        this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
        return;
      }
      if (b[0][0][i] == symbol && b[1][1][i] == symbol && b[2][2][i] == symbol && b[3][3][i] == symbol)
      {
        this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
        return;
      }
      if (b[i][3][0] == symbol && b[i][2][1] == symbol && b[i][1][2] == symbol && b[i][0][3] == symbol)
      {
        this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
        return;
      }
      if (b[3][i][0] == symbol && b[2][i][1] == symbol && b[1][i][2] == symbol && b[0][i][3] == symbol)
      {
        this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
        return;
      }
      if (b[3][0][i] == symbol && b[2][1][i] == symbol && b[1][2][i] == symbol && b[0][3][i] == symbol)
      {
        this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
        return;
      }
    }

    // Diagonals (3D)
    if (b[0][0][0] == symbol && b[1][1][1] == symbol && b[2][2][2] == symbol && b[3][3][3] == symbol)
    {
      this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
      return;
    }
    if (b[3][0][0] == symbol && b[2][1][1] == symbol && b[1][2][2] == symbol && b[0][3][3] == symbol)
    {
      this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
      return;
    }
    if (b[0][3][0] == symbol && b[1][2][1] == symbol && b[2][1][2] == symbol && b[3][0][3] == symbol)
    {
      this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
      return;
    }
    if (b[0][0][3] == symbol && b[1][1][2] == symbol && b[2][2][1] == symbol && b[3][3][0] == symbol)
    {
      this->state = symbol == 'X' ? CROSS_WIN : NOUGHT_WIN;
      return;
    }

    if (this->getLegalMovesCount() == 0)
    {
      this->state = DRAW;
      return;
    }
  }
};