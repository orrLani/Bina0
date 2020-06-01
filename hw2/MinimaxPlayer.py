


import math
import numpy as np
from Board import Board
import time as t
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DECININGAGENT=1

def tup_add(t1, t2):
    #this function get two tuples (a_1,a_2),(b_1,b_2) and return new tuple (a_1+a_2,b1+b_2)
    return (t1[0]+t2[0],t1[1]+t2[1])



def calculate_max_time(lefts:int,time:t):
    return 3*time

def tup_split(tup):
    """
    this function get tubple and split (a,b) to a,b
    :param tup:
    :return: tup[0],tup[1]
    """
    return tup[0],tup[1]



class State:
    def __init__(self,  board : Board, player_loc:tuple,
                 rival_loc:tuple, player_turn:int,
                 prev_direction= None):
        self.board:Board = board
        self.self_loc:tuple = player_loc
        self.rival_loc:tuple = rival_loc
        self.player_turn:int = player_turn
        self.direction_to_state:tuple = prev_direction

    def turn(self):
        return self.player_turn

    def directionToState(self):
        return self.direction_to_state



    def is_final_state(self) ->bool:
        """
        check if is a final state
        :return:
        """
        all_next_locations = [tup_add(self.self_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if
                                   0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        all_next_locations = [tup_add(self.rival_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if
                                   0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_rival_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        if len(possible_next_locations) == 0 or len(possible_rival_next_locations) == 0:
            return True
        return False
    def print_board_to_terminal(self, board):
        board_to_print = np.flipud(board.copy())
        # print(board_to_print)
        print('_' * len(board_to_print[0]) * 4)
        for row in board_to_print:
            row = [str(int(x)) if x != -1 else 'X' for x in row]
            print(' | '.join(row))
            print('_' * len(row) * 4)

    def final_state_heuristic(self)->float:
        """
        return the heuristic of the final state
        """
        all_next_locations = [tup_add(self.self_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if
                                   0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        all_next_locations = [tup_add(self.rival_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if
                                   0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_rival_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        if len(possible_next_locations) == 0 and len(possible_rival_next_locations) == 0:
            return 0
        if len(possible_next_locations) == 0:
            return -math.inf
        else:
            return math.inf
        """
        if (self.player_turn==DECININGAGENT and  len(possible_rival_next_locations) == 0)\
               or (self.player_turn!=DECININGAGENT and  len(possible_next_locations) == 0):
            return math.inf
        else:
            return -math.inf
"""


        # if len(possible_rival_next_locations) == 0:
        #     #    print("good finel board is")
        #     #    self.print_board_to_terminal(board=self.board)
        #         return math.inf
        # if len(possible_next_locations) == 0:
        # #    print("bas finel board is")
        # #    self.print_board_to_terminal(board=self.board)
        #
        #     return -math.inf
    def count_moves(self,loc):
        num_steps_available = 0
        for d in directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:  # then move is legal
                num_steps_available += 1
        return num_steps_available

    def extension_state_heuristic(self):
        if self.player_turn==DECININGAGENT:
            return self.count_moves(self.self_loc)-(self.count_moves(self.rival_loc)*2)
        return self.count_moves(self.rival_loc)-(self.count_moves(self.self_loc)*2)





    def extension_state_heuristic_1(self):
        num_steps_available = 0
        for d in directions:
            if self.player_turn==1:
                i = self.self_loc[0] + d[0]
                j = self.self_loc[1] + d[1]
            else:
                i = self.rival_loc[0] + d[0]
                j = self.rival_loc[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:  # then move is legal
                num_steps_available += 1


        if num_steps_available == 0:
            return -1
        else:
            return 4 - num_steps_available




class MinimaxPlayer:
    def __init__(self):
        self.board:Board=None
        self.loc:tuple =None
        self.rival_loc:tuple = None
        self.leaves=0

    def successors(self,state: State) -> list:
        """
        this function get a state and return all list of all the succ
        :param state:
        :return:
        """

        def locationIsLegal(location):
            if 0 <= location[0] < len(state.board) and 0 <= location[1] < len(state.board[0]) and \
                    state.board[location[0]][location[1]] == 0:
                return True
            return False

        succesors = []
        curr_player_loc = state.self_loc if state.turn() == 1 else state.rival_loc
        for direction in directions:
            next_location = tup_add(curr_player_loc, direction)
            if locationIsLegal(next_location):
                i_curr, j_curr = tup_split(curr_player_loc)
                i_next, j_next = tup_split(next_location)
                next_board = state.board.copy()
                next_board[i_curr][j_curr] = -1
                next_board[i_next][j_next] = 1 if state.turn() == 1 else 2
                # defining players locations
                if state.turn() == 1:
                    next_self_loc, next_rival_loc = next_location, state.rival_loc
                else:
                    next_self_loc, next_rival_loc = state.self_loc, next_location
                succesors.append(State(next_board, next_self_loc,next_rival_loc,3-state.player_turn, direction))
        return succesors




    def RB_MiniMax(self,state : State,depth:int):
        if state.is_final_state():
            score=state.final_state_heuristic()
            return score
        if depth==0:
            self.leaves+=1
            return state.extension_state_heuristic()
        agent_to_move = state.turn()
        if agent_to_move ==1:
        # my turn
            curMax = -math.inf
            for successor in self.successors(state):

                score = self.RB_MiniMax(successor,depth-1)
                curMax = max(score,curMax)
            return curMax
        else:
            curMin = math.inf
        # deciding_agent=state.switch_turns()
            for successor in self.successors(state):
                score = self.RB_MiniMax(successor,depth-1)
                curMin = min(score,curMin)
            return curMin





    def MiniMax(self,state : State):
        if state.is_final_state():
            score=state.final_state_heuristic()
            state.print_board_to_terminal(state.board)
            print(score)
            return score
        agent_to_move = state.turn()
        if agent_to_move ==1:
        # my turn
            curMax = -math.inf
            for successor in self.successors(state):
                score = self.MiniMax(successor)
                curMax = max(score,curMax)
            return curMax
        else:
            curMin = math.inf
        # deciding_agent=state.switch_turns()
            for successor in self.successors(state):
                score = self.MiniMax(successor)
                curMin = min(score,curMin)
            return curMin


    def set_game_params(self,board):
        self.board=board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                if val == 2:
                    self.rival_loc = (i, j)

    def choose_move(self,state:State,depth:int)->tuple:
        curMax = -math.inf
        best_move = None
        for successor in self.successors(state):
            #if self.loc[0] == 0 and self.loc[1] == 5:
             #   print("yess")
            score = self.RB_MiniMax(successor,depth)
            if score >= curMax:
                curMax = score
                best_move = successor.directionToState()

        return best_move


    def make_move(self,time):
        id_time_start = t.time()
        depth=1
        initial_state = State(self.board.copy(), self.loc, self.rival_loc, 1)
        best_move=self.choose_move(initial_state,depth)
        last_iteration_time = t.time() - id_time_start
        next_iteration_time_max = last_iteration_time*3
        time_until_now=t.time()-id_time_start
        while time_until_now+next_iteration_time_max<time:
            depth+=1
            iteartion_start_time =t.time()
            best_move=self.choose_move(initial_state,depth)
            last_iteration_time=t.time()-iteartion_start_time
            next_iteration_time_max = last_iteration_time * 3
            time_until_now=t.time()-id_time_start
        if best_move is None:
            #print("My Board is NOTGOOD")
            #print(self.board)

            exit()

        self.board[self.loc] = -1
        #print("the best move is" + str(best_move))
        self.loc = tup_add(best_move,self.loc)
        self.board[self.loc] = 1

      #  print("Our board after")
      #  print(self.board)

        return best_move


    def make_move_2(self,time):
        time_start = t.time()
        print("our player in loc" + str(self.loc))
        initial_state = State(self.board.copy(), self.loc, self.rival_loc, 1)
        curMax = -math.inf
        best_move = None
        for successor in self.successors(initial_state):
            score = self.MiniMax(successor)
            newMax = max(score, curMax)
            if newMax >= curMax:
                newMax = curMax
                best_move = successor.directionToState()
                # need to update the board
        print(newMax)
        if best_move is None:
            #print("My Board is NOTGOOD")
            #print(self.board)

            exit()

        self.board[self.loc] = -1
        print("the best move is" + str(best_move))
        self.loc = (best_move[0] + self.loc[0], best_move[1] + self.loc[1])

        self.board[self.loc] = 1

      #  print("Our board after")
      #  print(self.board)

        return best_move


    def set_rival_move(self,loc):
        #old rival location
        self.board[self.rival_loc] = -1
        self.rival_loc = loc
        #new rival location
        self.board[self.rival_loc] = 2
