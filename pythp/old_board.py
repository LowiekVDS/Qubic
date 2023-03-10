import numpy as np
from random import randint
from enum import Enum
import gym
from gym import spaces

EMPTY = 0
CROSS = 1
NOUGHT = 2
WILDCARD = 3



BOARD_SIZE = 4 * 4 * 4

ACTIVE = 0
WIN_CROSS = CROSS
WIN_NOUGHT = NOUGHT
DRAW = 3

class GameResult(Enum):
    """
    Enum to encode different states of the game. A game can be in progress (NOT_FINISHED), lost, won, or draw
    """
    NOT_FINISHED = ACTIVE
    NAUGHT_WIN = WIN_NOUGHT
    CROSS_WIN = WIN_CROSS
    DRAW = DRAW

WINNING_LINES = [
    [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3]],
    [[0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 1, 3]],
    [[0, 2, 0], [0, 2, 1], [0, 2, 2], [0, 2, 3]],
    [[0, 3, 0], [0, 3, 1], [0, 3, 2], [0, 3, 3]],
    [[1, 0, 0], [1, 0, 1], [1, 0, 2], [1, 0, 3]],
    [[1, 1, 0], [1, 1, 1], [1, 1, 2], [1, 1, 3]],
    [[1, 2, 0], [1, 2, 1], [1, 2, 2], [1, 2, 3]],
    [[1, 3, 0], [1, 3, 1], [1, 3, 2], [1, 3, 3]],
    [[2, 0, 0], [2, 0, 1], [2, 0, 2], [2, 0, 3]],
    [[2, 1, 0], [2, 1, 1], [2, 1, 2], [2, 1, 3]],
    [[2, 2, 0], [2, 2, 1], [2, 2, 2], [2, 2, 3]],
    [[2, 3, 0], [2, 3, 1], [2, 3, 2], [2, 3, 3]],
    [[3, 0, 0], [3, 0, 1], [3, 0, 2], [3, 0, 3]],
    [[3, 1, 0], [3, 1, 1], [3, 1, 2], [3, 1, 3]],
    [[3, 2, 0], [3, 2, 1], [3, 2, 2], [3, 2, 3]],
    [[3, 3, 0], [3, 3, 1], [3, 3, 2], [3, 3, 3]],

    [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0]],
    [[0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1]],
    [[0, 0, 2], [0, 1, 2], [0, 2, 2], [0, 3, 2]],
    [[0, 0, 3], [0, 1, 3], [0, 2, 3], [0, 3, 3]],
    [[1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 3, 0]],
    [[1, 0, 1], [1, 1, 1], [1, 2, 1], [1, 3, 1]],
    [[1, 0, 2], [1, 1, 2], [1, 2, 2], [1, 3, 2]],
    [[1, 0, 3], [1, 1, 3], [1, 2, 3], [1, 3, 3]],
    [[2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 3, 0]],
    [[2, 0, 1], [2, 1, 1], [2, 2, 1], [2, 3, 1]],
    [[2, 0, 2], [2, 1, 2], [2, 2, 2], [2, 3, 2]],
    [[2, 0, 3], [2, 1, 3], [2, 2, 3], [2, 3, 3]],
    [[3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0]],
    [[3, 0, 1], [3, 1, 1], [3, 2, 1], [3, 3, 1]],
    [[3, 0, 2], [3, 1, 2], [3, 2, 2], [3, 3, 2]],
    [[3, 0, 3], [3, 1, 3], [3, 2, 3], [3, 3, 3]],

    [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]],
    [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1]],
    [[0, 0, 2], [1, 0, 2], [2, 0, 2], [3, 0, 2]],
    [[0, 0, 3], [1, 0, 3], [2, 0, 3], [3, 0, 3]],
    [[0, 1, 0], [1, 1, 0], [2, 1, 0], [3, 1, 0]],
    [[0, 1, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1]],
    [[0, 1, 2], [1, 1, 2], [2, 1, 2], [3, 1, 2]],
    [[0, 1, 3], [1, 1, 3], [2, 1, 3], [3, 1, 3]],
    [[0, 2, 0], [1, 2, 0], [2, 2, 0], [3, 2, 0]],
    [[0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1]],
    [[0, 2, 2], [1, 2, 2], [2, 2, 2], [3, 2, 2]],
    [[0, 2, 3], [1, 2, 3], [2, 2, 3], [3, 2, 3]],
    [[0, 3, 0], [1, 3, 0], [2, 3, 0], [3, 3, 0]],
    [[0, 3, 1], [1, 3, 1], [2, 3, 1], [3, 3, 1]],
    [[0, 3, 2], [1, 3, 2], [2, 3, 2], [3, 3, 2]],
    [[0, 3, 3], [1, 3, 3], [2, 3, 3], [3, 3, 3]],

    [[0, 0, 0], [0, 1, 1], [0, 2, 2], [0, 3, 3]],
    [[0, 3, 0], [0, 2, 1], [0, 1, 2], [0, 0, 3]],
    [[1, 0, 0], [1, 1, 1], [1, 2, 2], [1, 3, 3]],
    [[1, 3, 0], [1, 2, 1], [1, 1, 2], [1, 0, 3]],
    [[2, 0, 0], [2, 1, 1], [2, 2, 2], [2, 3, 3]],
    [[2, 3, 0], [2, 2, 1], [2, 1, 2], [2, 0, 3]],
    [[3, 0, 0], [3, 1, 1], [3, 2, 2], [3, 3, 3]],
    [[3, 3, 0], [3, 2, 1], [3, 1, 2], [3, 0, 3]],

    [[0, 0, 0], [1, 0, 1], [2, 0, 2], [3, 0, 3]],
    [[3, 0, 0], [2, 0, 1], [1, 0, 2], [0, 0, 3]],
    [[0, 1, 0], [1, 1, 1], [2, 1, 2], [3, 1, 3]],
    [[3, 1, 0], [2, 1, 1], [1, 1, 2], [0, 1, 3]],
    [[0, 2, 0], [1, 2, 1], [2, 2, 2], [3, 2, 3]],
    [[3, 2, 0], [2, 2, 1], [1, 2, 2], [0, 2, 3]],
    [[0, 3, 0], [1, 3, 1], [2, 3, 2], [3, 3, 3]],
    [[3, 3, 0], [2, 3, 1], [1, 3, 2], [0, 3, 3]],


    [[0, 0, 0], [1, 1, 0], [2, 2, 0], [3, 3, 0]],
    [[3, 0, 0], [2, 1, 0], [1, 2, 0], [0, 3, 0]],
    [[0, 0, 1], [1, 1, 1], [2, 2, 1], [3, 3, 1]],
    [[3, 0, 1], [2, 1, 1], [1, 2, 1], [0, 3, 1]],
    [[0, 0, 2], [1, 1, 2], [2, 2, 2], [3, 3, 2]],
    [[3, 0, 2], [2, 1, 2], [1, 2, 2], [0, 3, 2]],
    [[0, 0, 3], [1, 1, 3], [2, 2, 3], [3, 3, 3]],
    [[3, 0, 3], [2, 1, 3], [1, 2, 3], [0, 3, 3]],

    [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]],
    [[0, 0, 3], [1, 1, 2], [2, 2, 1], [3, 3, 0]],

    [[0, 3, 3], [1, 2, 2], [2, 1, 1], [3, 0, 0]],
    [[0, 3, 0], [1, 2, 1], [2, 1, 2], [3, 0, 3]]

]


class Board(gym.Env):

    def __init__(self) -> None:
        super(Board, self,).__init__()
        self.board = np.zeros((4, 4, 4), dtype=int)
        self.state = ACTIVE
        self.winning_move = ''

        self.line = -1

    @staticmethod
    def other_side(side: int) -> int:
        """
        Utility method to return the value of the other player than the one passed as input
        :param side: The side we want to know the opposite of
        :return: The opposite side to the one passed as input
        """
        if side == EMPTY:
            raise ValueError("EMPTY has no 'other side'")

        if side == CROSS:
            return NOUGHT

        if side == NOUGHT:
            return CROSS

        raise ValueError("{} is not a valid side".format(side))

    def __str__(self):

        # res = ''
        # res += '=========\n'
        # for i in range(4):
        #     if i > 0:
        #         res += '---------\n'
        #     for j in range(4):
        #         res += '|'
        #         for k in range(4):

        #             if self.board[i, j, k] == CROSS:
        #                 res += 'X'
        #             elif self.board[i, j, k] == NOUGHT:
        #                 res += 'O'
        #             elif self.board[i, j, k] == WILDCARD:
        #                 res += '*'
        #             else:
        #                 res += ' '

        #             res += '|'
        #         res += '\n'
        # res += '========='

        res = ''
        res += "==========={}  {}=====\n".format(self.state, self.line)
        for i in range(4):
            for j in range(4):
                res += '|'
                for k in range(4):
                    
                    pos = self.board[i, j, k]

                    if pos == CROSS:
                        res += 'X'
                    elif pos == NOUGHT:
                        res += 'O'
                    elif pos == WILDCARD:
                        res += '*'
                    else:
                        res += ' '
                    
                    # res += ' '
            res += '|\n'
        res += "=====================\n"
        return res

    def to_tensor(self):
        tensor = np.zeros((4, 4, 4, 4), dtype=bool)

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    tensor[i, j, k, self.board[i, j, k]] = True

        return tensor.flatten()

    def add_wildcards(self, nr):
        for n in range(nr):
            i = randint(0, 3)
            j = randint(0, 3)
            k = randint(0, 3)

            while self.board[i, j, k] == WILDCARD:
                i = randint(0, 3)
                j = randint(0, 3)
                k = randint(0, 3)

            self.board[i, j, k] = WILDCARD

    def is_move_legal(self, i, j, k):
        return self.board[i, j, k] == EMPTY

    def clear(self):
        self.state = ACTIVE
        self.board = np.zeros((4, 4, 4), dtype=int)
        self.winning_move = ''

    def count_winning_lines(self, symbol):
        """
        Counts how many winning lines {symbol} has still available and also sorts them according to size
          0: no space taken
          1: 1 space taken (or wildcard)
          2: 2 spaces taken (or wildcards)
          3: 3 spaces taken (or wildcards)
        """

        # Check for end states
        board = np.copy(self.board)
        board[np.where(board == WILDCARD)] = symbol
        # board[np.where(board == EMPTY)] = symbol

        counts = [0, 0, 0, 0]

        other_symbol = CROSS if symbol == NOUGHT else NOUGHT

        for line in WINNING_LINES:
            numSym = 0
            numOther = 0
            for coords in line:
                if board[coords[0], coords[1], coords[2]] == symbol:
                    numSym += 1
                elif board[coords[0], coords[1], coords[2]] == other_symbol:
                    numOther += 1

            if numOther == 0:
                counts[numSym] += 1

        return counts
        
    def move(self, x, y, z, symbol):

        if self.is_move_legal(x, y, z) and self.state == ACTIVE:
            self.board[x, y, z] = symbol

            # Check for end states
            board = np.copy(self.board)
            board[np.where(board == WILDCARD)] = symbol

            for i,line in enumerate(WINNING_LINES):
                numSym = 0
                numOther = 0
                for coords in line:
                    if board[coords[0], coords[1], coords[2]] == symbol:
                        numSym += 1

                if numSym == 4:
                    self.line = i
                    self.state = symbol
                    return self.state
            
            if len(self.get_legal_moves()[0]) == 0:
                self.state = DRAW

        return self.state
        #     # Straights (three to check)
        #     for i in range(4):
        #         for j in range(4):
        #             if np.all(board[:, i, j] == symbol) or np.all(board[i, :, j] == symbol) or np.all(board[i, j, :] == symbol):
        #                 self.state = symbol
        #                 self.winning_move = 'straight'
        #                 return self.state

        #     # Diagonals in 2D planes
        #     for i in range(4):

        #         if board[i, 0, 0] == board[i, 1, 1] == board[i, 2, 2] == board[i, 3, 3] == symbol or board[i, 3, 0] == board[i, 2, 1] == board[i, 1, 2] == board[i, 0, 3] == symbol:
        #             self.state = symbol
        #             self.winning_move = '2ddiag'
        #             return self.state
        #         elif board[0, i, 0] == board[1, i, 1] == board[2, i, 2] == board[3, i, 3] == symbol or board[3, i, 0] == board[2, i, 1] == board[1, i, 2] == board[0, i, 3] == symbol:
        #             self.state = symbol
        #             self.winning_move = '2ddiag'
        #             return self.state
        #         elif board[0, 0, i] == board[1, 1, i] == board[2, 2, i] == board[3, 3, i] == symbol or board[0, 3, i] == board[1, 2, i] == board[2, 1, i] == board[3, 0, i] == symbol:
        #             self.state = symbol
        #             self.winning_move = '2ddiag'
        #             return self.state

        #     # 3D diagonals (4 in total)
        #     if board[0, 0, 0] == board[1, 1, 1] == board[2, 2, 2] == board[3, 3, 3] == symbol or board[3, 0, 0] == board[2, 1, 1] == board[1, 2, 2] == board[0, 3, 3] == symbol or board[0, 0, 3] == board[1, 1, 2] == board[2, 2, 1] == board[3, 3, 0] == symbol or board[0, 3, 0] == board[1, 2, 1] == board[2, 1, 2] == board[3, 0, 3] == symbol:
        #         self.state = symbol
        #         self.winning_move = '3ddiag'
        #         return self.state

        # if len(self.get_legal_moves()[0]) == 0:
        #     self.state = DRAW
        #     self.winning_move = 'draw'

        # return self.state

    def get_legal_moves(self):
        return np.where(self.board == EMPTY)

    def get_nr_of_legal_moves(self):
        return len(self.get_legal_moves()[0])

    # def __str__(self) -> str:
    #   return str(self.board) + '\n' + self.winning_move
