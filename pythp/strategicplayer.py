from random import randint
import board
import numpy as np
import json


class StrategicPlayer:

    # Cross starts
    def __init__(self, game: board.Board, symbol=board.CROSS) -> None:
        self.board = game
        self.symbol = symbol

    def to_int(self, i, j, k):
        return i * 16 + j * 4 + k

    def int_to_move(self, move_id):
        i = move_id // 16
        j = (move_id - i * 16) // 4
        k = (move_id - i * 16 - j * 4)

        return i,j,k

    def move(self):

        if self.board.state != board.ACTIVE:
            return

        counts, lines = self.board.count_winning_lines(self.symbol)
        counts2, lines2 = self.board.count_winning_lines(
            board.Board.other_side(self.symbol))

        # for p in range(3, -1, -1):
        p = 3
        # If 3 in a row, do it
        if counts[p] > 0:
            for move in lines[p][0]:
                i, j, k = move
                if self.board.is_move_legal(i, j, k):
                    self.board.move(i, j, k, self.symbol)
                    return


        # If opponent 3 in a row, block it
        if counts2[p] > 0:
            for move in lines2[p][0]:
                i, j, k = move
                if self.board.is_move_legal(i, j, k):
                    self.board.move(i, j, k, self.symbol)
                    return

        # 
        count = {}
        transitions = {}
        blocks = {}
        for nr_taken in range(4):
            for line in lines[nr_taken]:
                for move in line:
                    i, j, k = move
                    # print(i,j,k)
                    if self.board.is_move_legal(i, j, k):
                        id = self.to_int(i, j, k)
                        if id not in count.keys():
                            count[id] = 0
                            blocks[id] = [0, 0, 0, 0]
                            transitions[id] = [0,0,0,0]
                        count[id] += 1
                        transitions[id][nr_taken] += 1
        count2 = {}
        transitions2 = {}
        blocks = {}
        for nr_taken in range(4):
            for line in lines2[nr_taken]:
                for move in line:
                    i, j, k = move
                    # print(i,j,k)
                    if self.board.is_move_legal(i, j, k):
                        id = self.to_int(i, j, k)
                        if id not in count2.keys():
                            count2[id] = 0
                            blocks[id] = [0, 0, 0, 0]
                            transitions2[id] = [0,0,0,0]
                        count2[id] += 1
                        transitions2[id][nr_taken] += 1

        # Check for two 2 --> 3 (guaranteed wins)
        for key, val in transitions.items():
            if val[2] > 1:
                i,j,k = self.int_to_move(key)
                self.board.move(i,j,k,self.symbol)
                
                if self.symbol == board.CROSS:
                    print("YES")
                else:
                    print("fine i guess")
                return

        # Detect enemy traps
        # Take move with most own transitions
        traps = []
        for key, val in transitions2.items():
            if val[2] > 1:
                traps.append(key)
        
        ## Take move which causes most transisttions and blocks
        if len(traps) > 0:
            max_score = 0
            max_trap = traps[0]
            for trap in traps:
                # score = sum(transitions2[trap])
                score = 0
                if trap in transitions.keys():
                    score += sum(transitions[trap])
                
                if score > max_score:
                    max_score = score
                    max_trap = trap

            if max_score > 0:
                i,j,k = self.int_to_move(max_trap)
                self.board.move(i,j,k,self.symbol)
                # if self.symbol == board.CROSS:
                #     print("NO")
                return

        # for key, val in transitions2.items():
        #     if val[1] > 1:
        #         i,j,k = self.int_to_move(key)
        #         self.board.move(i,j,k,self.symbol)
        #         if self.symbol == board.CROSS:
        #             print("NO 2")
        #         return
        # # Check for two 1 --> 2
        # for key, val in transitions.items():
        #     if val[1] > 1:
        #         i,j,k = self.int_to_move(key)
        #         self.board.move(i,j,k,self.symbol)
        #         if self.symbol == board.CROSS:
        #             print("2 YES")
        #         else:
        #             print("2 fine i guess")
        #         return
        # for key, val in transitions2.items():
        #     if val[1] > 1:
        #         i,j,k = self.int_to_move(key)
        #         self.board.move(i,j,k,self.symbol)
        #         if self.symbol == board.CROSS:
        #             print("2 NO")
        #         return

        # Backup
        if self.symbol == board.CROSS:
            print("backup")
        
        max_val = 0
        max_key = 0
        for key, val in transitions.items():
            
            # neg_score = 0
            # if key in transitions2.keys():
            #     neg_score += sum(transitions2[key][1:]) * 0.5
            
            score = val[1] #+ neg_score

            if score > max_val:
                max_val = score
                max_key = key
    
        max_val = 0
        max_key = 0
        for key, val in transitions2.items():
            
            # neg_score = 0
            # if key in transitions2.keys():
            #     neg_score += sum(transitions2[key][1:]) * 0.5
            
            score = val[1] * 1 #+ neg_score

            if score > max_val:
                max_val = score
                max_key = key

        # print('tsy')
        i,j,k = self.int_to_move(max_key)
        self.board.move(i,j,k,self.symbol)

        if max_val == 0:
            legal_moves = self.board.get_legal_moves()
            N = len(legal_moves[0])

            if N == 0:
                return

            move = randint(0, N-1)

            self.board.move(legal_moves[0][move], legal_moves[1]
                            [move], legal_moves[2][move], self.symbol)

        return

        # # Check if we have a a trap (that is, two two in a rows that have a common empty space)
        # count = {}
        # transitions = {}
        # blocks = {}
        # for nr_taken in range(4):
        #     for line in lines[nr_taken]:
        #         for move in line:
        #             i, j, k = move
        #             # print(i,j,k)
        #             if self.board.is_move_legal(i, j, k):
        #                 id = self.to_int(i, j, k)
        #                 if id not in count.keys():
        #                     count[id] = 0
        #                     blocks[id] = [0, 0, 0, 0]
        #                     transitions[id] = [0,0,0,0]
        #                 count[id] += 1
        #                 transitions[id][nr_taken] += 1

        # ## We have a trap if there is a move in which transitions[move][2] is greater than 1
        # for key, val in transitions.items():
        #     if val[2] > 1:
        #         i,j,k = self.int_to_move(key)
        #         self.board.move(i,j,k,self.symbol)
        #         if self.symbol == board.CROSS:
        #             print("YES")
        #         return

        ## We also have a trap if a specific space causes a 1 --> 2 and 2 --> 3 transition, basically forcing 

        # Check if we have a a trap (that is, two two in a rows that have a common empty space)
        count2 = {}
        transitions2 = {}
        blocks = {}
        for nr_taken in range(4):
            for line in lines2[nr_taken]:
                for move in line:
                    i, j, k = move
                    # print(i,j,k)
                    if self.board.is_move_legal(i, j, k):
                        id = self.to_int(i, j, k)
                        if id not in count2.keys():
                            count2[id] = 0
                            blocks[id] = [0, 0, 0, 0]
                            transitions2[id] = [0,0,0,0]
                        count2[id] += 1
                        transitions2[id][nr_taken] += 1

        ## We have a trap if there is a move in which transitions[move][2] is greater than 1
        for key, val in transitions2.items():
            if val[2] > 1:
                i,j,k = self.int_to_move(key)
                self.board.move(i,j,k,self.symbol)
                if self.symbol == board.CROSS:
                    print("NO")
                return

        # Choose the move that blocks the most single moves
        # if self.symbol == board.CROSS:
        max_val = 0
        max_key = 0
        for key, val in transitions.items():
            if val[2] > max_val:
                max_val = val[2]
                max_key = key
    

        # print('tsy')
        i,j,k = self.int_to_move(max_key)
        self.board.move(i,j,k,self.symbol)
        return

        # Guaranteed draw, choose random move
        # legal_moves = self.board.get_legal_moves()
        # N = len(legal_moves[0])

        # if N == 0:
        #     return

        # move = randint(0, N-1)

        # self.board.move(legal_moves[0][move], legal_moves[1]
        #                 [move], legal_moves[2][move], self.symbol)
        # # print(self.board, self.board.state)
        # return
        # print(counts, counts, self.board)

       
                        
                        # # Check if it blocks the opponent
                        # # isBlock = False
                        # # blockSize = 0
                        # for p in range(4):
                        #     for opline in lines2[p]:
                        #         for opmove in opline:
                        #             # print(opmove)
                        #             if opmove[0] == i and opmove[1] == j and opmove[2] == k:
                        #                 #isBlock = True
                        #                 #blockSize = p
                        #                 # print("tesy")
                        #                 blocks[id][p] += 1
                        #     #     if isBlock:
                        #     #         break
                        #     # if isBlock:
                        #     #     break

                        # # if isBlock:
                        # #     blocks[blockSize] += 1

        # Calculate scores
        # scores = []
        
        # # if self.symbol == board.CROSS:
        # #     print(transitions.keys())
        # #     print(blocks)
        # #     print(counts)

        # for key, val in transitions.items():
        #     otherval = blocks[key]
        #     score = val[0] * 0.01 + val[1] * 1 + val[2] * 3 - otherval[0] * 0.01 - otherval[1] * 0.1 - otherval[2] * 3

        #     scores.append(score)  

        # move_id = list(transitions.keys())[scores.index(max(scores))]
        # i = move_id // 16
        # j = (move_id - i * 16) // 4
        # k = (move_id - i * 16 - j * 4)

        # self.board.move(i, j, k, self.symbol)

        # # Calculate scores
        # # Take 

        # # Take move with higest 2 --> 3 conversions
        # max_tran = 0
        # move_index = 0
        # for i, tran in enumerate(transitions.values()):
        #     if tran[2] > max_tran:
        #         max_tran = tran[2]
        #         move_index = i

        # # Take i as a move  
        # move_id = list(transitions.keys())[move_index]
        # i = move_id // 16
        # j = (move_id - i * 16) // 4
        # k = (move_id - i * 16 - j * 4)

        # if self.symbol == board.CROSS:
        #     print(max_tran)

        # self.board.move(i,j,k, self.symbol)

        # count2 = {}
        # transitions2 = {}

        # for nr_taken in range(4):
        #     for line in lines2[nr_taken]:

        #         for move in line:
        #             i, j, k = move
        #             if self.board.is_move_legal(i, j, k):

        #                 id = self.to_int(i, j, k)

        #                 if id not in count.keys():
        #                     continue

        #                 if id not in count2.keys():
        #                     count2[id] = 0
        #                     transitions2[id] = [0,0,0,0]

        #                 count2[id] += 1
        #                 transitions2[id][nr_taken] += 1

        # Make scores
        # scores = []
        # for i, trans in i, transitions.values():
        #     score = trans[0] * 1 + trans[1] * 2 + trans[2] * 3 + trans[3] * 4

        #     if t

        #     scores.append(score)

        # # Do

        # # Choose move with highest score
        # # print(transitions.keys())
        # move_id = list(transitions.keys())[scores.index(max(scores))]
        # i = move_id // 16
        # j = (move_id - i * 16) // 4
        # k = (move_id - i * 16 - j * 4)

        # # if self.symbol == board.CROSS:
        #     # print(move_id, i,j,k)

        # self.board.move(i,j,k, self.symbol)

        # # print(json.dumps(count, indent=4))
        # # print(json.dumps(transitions, indent=4))

        # # Now check for forced win sequences (if first player, so 'X')
        # # Forced win sequences are

        # Legal moves
        legal_moves = self.board.get_legal_moves()
        N = len(legal_moves[0])

        if N == 0:
            return

        move = randint(0, N-1)

        self.board.move(legal_moves[0][move], legal_moves[1]
                        [move], legal_moves[2][move], self.symbol)
