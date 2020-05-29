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
        self.player_turn = player_turn
        self.direction_to_state = prev_direction

    def switch_turns(self):
        return 2 if self.player_turn == 1 else 1
    def turn(self):
        return self.player_turn
    def directionToState(self):
        return self.direction_to_state
    def successors(self) -> list:
        def locationIsLegal(location):
            if 0 <= location[0] < len(self.board) \
            and 0 <= location[1] < len(self.board[0]) and \
            self.board[location[0]][location[1]] == 0:
                return True
            return False
        succesors = []
        curr_player_loc = self.self_loc if self.turn() == 1 else self.rival_loc
        for direction in directions:
            next_location = tup_add(curr_player_loc, direction)
            if locationIsLegal(next_location):
                i_curr, j_curr = tup_split(curr_player_loc)
                i_next, j_next = tup_split(next_location)
                next_board = self.board
                next_board[i_curr][j_curr] = -1
                next_board[i_next][j_next] = 1 if self.turn()==1 else 2
                # defining players locations
                if self.turn()==1:
                    next_self_loc, next_rival_loc = next_location, self.rival_loc
                else:
                    next_self_loc, next_rival_loc = self.self_loc, next_location
                succesors.append(GameState(next_board, next_self_loc, next_rival_loc, self.switch_turns(), direction))
        return succesors

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
