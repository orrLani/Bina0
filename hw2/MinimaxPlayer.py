import math
# from GameAnalyzer import GameState
import math
from Board import Board
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def tup_add(t1, t2):
    return (t1[0]+t2[0],t1[1]+t2[1])


def tup_split(tup):
    return tup[0], tup[1]


class GameState:
    def __init__(self,  board : Board, player_loc, rival_loc, player_turn, prev_direction= None):
        self.board = board
        self.self_loc = player_loc
        self.rival_loc = rival_loc
        self.player_turn:int = player_turn
        self.direction_to_state = prev_direction

    def switch_turns(self):
        # TODO FOR WHAT THIS FUNCTION IF I CANT CHNGE SELF.PLAYERR_TURN
         return 2 if self.player_turn == 1 else 1
        # CHNGE TOO
        # self.player_turn = 2 if self.player_turn==1 else self.player_turn=1
        # 1 is for my turn2 , 2 is for oppsti turn

    def orr_switch_turns(self):
        if self.player_turn==1:
            self.player_turn=2
        else:
            self.player_turn=1
    def turn(self):
        return self.player_turn
    def directionToState(self):
        return self.direction_to_state

    def is_final_state(self) ->bool:
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

    def heuristic(self) ->float:
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
        if len(possible_rival_next_locations) == 0:
            return math.inf
        if len(possible_next_locations) == 0:
            return -math.inf



    def evaluateIfFinal(self) -> int:
        all_next_locations = [tup_add(self.self_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if 0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        all_next_locations = [tup_add(self.rival_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if 0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_rival_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        if len(possible_next_locations) == 0 and len(possible_next_locations) == 0:
            return 0
        if len(possible_rival_next_locations) == 0:
            return math.inf
        if len(possible_next_locations) == 0:
            return -math.inf
        return None

    def evaluate(self,heuristic):
        #TODO
        pass



def successors(state:GameState) -> list:
    """
    this function get a state and return all list of all the succ
    :param state:
    :return:
    """
    def locationIsLegal(location):
        if 0 <= location[0] < len(state.board) and 0 <= location[1] < len(state.board[0]) and state.board[location[0]][location[1]] == 0:
            return True
        return False


    succesors = []
    curr_player_loc = state.self_loc if state.turn() == 1 else state.rival_loc
    for direction in directions:
        next_location = tup_add(curr_player_loc, direction)
        if locationIsLegal(next_location):
            i_curr, j_curr = tup_split(curr_player_loc)
            i_next, j_next = tup_split(next_location)
            next_board = state.board
            next_board[i_curr][j_curr] = -1
            next_board[i_next][j_next] = 1 if state.turn()==1 else 2
            # defining players locations
            if state.turn()==1:
                next_self_loc, next_rival_loc = next_location, state.rival_loc
            else:
                next_self_loc, next_rival_loc = state.self_loc, next_location
            succesors.append(GameState(next_board, next_self_loc, next_rival_loc,state.switch_turns(), direction))
    return succesors





def MiniMax(state : GameState):
    if state.is_final_state():
        score=state.heuristic()
        return score
    agent_to_move = state.turn()
    if agent_to_move ==1:
        # opsit turn
        curMax = -math.inf
        # deciding_agent=state.switch_turns()
        for successor in successors(state):
            score = MiniMax(successor)
            curMax = max(score,curMax)
        return curMax
    else:
        curMin = math.inf
       # deciding_agent=state.switch_turns()
        for successor in successors(state):
            score = MiniMax(successor)
            curMin = min(score,curMin)
        return curMin

class MinimaxPlayer:
    def __init__(self):
        self.board = None
        self.loc:tuple = None
        self.rival_loc = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                if val == 2:
                    self.rival_loc = (i, j)

        # TODO: implement more options?


    def make_move(self,time):
        print("our player in loc"+str(self.loc))
        initial_state = GameState(self.board, self.loc, self.rival_loc, 1)
        curMax = -math.inf
        best_move = None
        for successor in successors(initial_state):
            score = MiniMax(successor)
            newMax = max(score, curMax)
            if newMax >= curMax:
                newMax = curMax
                best_move = successor.directionToState()

                #need to update the board

        # print("My Board is")
        # print(self.board)
        if best_move is None:

            exit()

        self.board[self.loc]=-1
        print("the best move is"+ str(best_move))
        self.loc=(best_move[0]+self.loc[0],best_move[1]+self.loc[1])

        self.board[self.loc]=1

        return best_move


    def set_rival_move(self,loc):
        #old rival location
        self.board[self.rival_loc] = -1
        #new rival location
        self.board[loc]=2
        self.rival_loc=loc
        # TODO: implement more options?