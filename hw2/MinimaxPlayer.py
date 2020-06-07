from Board import Board
import time as t
from Heuristics import *
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def tup_add(t1, t2):
    return (t1[0]+t2[0],t1[1]+t2[1])

def calculate_blocked_time(time:t)->t:
    return 4*time

def tup_split(tup):
    return tup[0],tup[1]



class MinimaxPlayer:
    def __init__(self):
        self.board:Board=None
        self.loc:tuple =None
        self.rival_loc:tuple = None
        self.leaves=0
       # self.heuristic=defencive_H
        self.heuristic= attack_defencive_H
        # for heuristics

        self.num_free_slots_init = 0
        self.num_captured_slots = 0


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
                succesors.append(State(next_board, next_self_loc,next_rival_loc,3-state.player_turn
                                       ,num_captured_slots= self.num_captured_slots+1,
                                       num_free_slots=state.num_free_slots_init,prev_direction=direction))
        return succesors


    def set_game_params(self,board):
        self.board=board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                if val == 2:
                    self.rival_loc = (i, j)
                # for calculate heuristics
                if val == 0:
                    self.num_free_slots_init += 1

    def RB_MiniMax(self,state: State, depth: int):
        if state.is_final_state():
            score = final_H(state)
            return score
        if depth == 0:
            self.leaves += 1
            return self.heuristic(state)
        agent_to_move = state.turn()
        if agent_to_move == 1:
            # my turn
            curMax = -math.inf
            for successor in self.successors(state):
                score = self.RB_MiniMax(successor, depth - 1)
                curMax = max(score, curMax)
            return curMax
        else:
            curMin = math.inf
            # deciding_agent=state.switch_turns()
            for successor in self.successors(state):
                score = self.RB_MiniMax(successor, depth - 1)
                curMin = min(score, curMin)
            return curMin

    def choose_move(self,state:State,depth:int)->tuple:

        curMax = -math.inf
        best_move = None
        for successor in self.successors(state):
            score = self.RB_MiniMax(successor,depth)
            if score >= curMax:
                curMax = score
                best_move = successor.directionToState()
        return best_move


    def make_move(self,time):
        id_time_start = t.time()
        depth=1
        self.num_captured_slots += 1
        initial_state = State(self.board.copy(), self.loc, self.rival_loc, 1,num_captured_slots=1,
                              num_free_slots=self.num_free_slots_init)
        best_move=self.choose_move(initial_state,depth)
        last_iteration_time = t.time() - id_time_start
        #next_iteration_time_max = last_iteration_time*4
        next_iteration_time_max =calculate_blocked_time(last_iteration_time)
        time_until_now=t.time()-id_time_start
        #DEBUG = self.loc==(0,3)
        #DEBUG= self.loc==(1,7)
        DEBUG= False
        while time_until_now+next_iteration_time_max<time or (DEBUG and depth<50):
            depth+=1
            iteartion_start_time =t.time()
            best_move=self.choose_move(initial_state,depth)
            last_iteration_time=t.time()-iteartion_start_time
            next_iteration_time_max =calculate_blocked_time(last_iteration_time)
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
        return best_move #for wet
       # return depth # for print grath to dry

    def set_rival_move(self,loc):
        #old rival location
        self.num_captured_slots += 1
        self.board[self.rival_loc] = -1
        self.rival_loc = loc
        #new rival location
        self.board[self.rival_loc] = 2
