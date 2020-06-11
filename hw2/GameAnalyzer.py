import math
from Board import Board
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def tup_add(t1, t2):
    return (t1[0]+t2[0],t1[1]+t2[1])


def tup_split(tup):
    return tup[0], tup[1]


class State:
    def __init__(self,  board : Board, player_loc:tuple,
                 rival_loc:tuple, player_turn:int,
                 num_captured_slots,num_free_slots,prev_direction= None):
        self.board:Board = board
        self.self_loc:tuple = player_loc
        self.rival_loc:tuple = rival_loc
        self.player_turn:int = player_turn
        self.direction_to_state:tuple = prev_direction
        # for heuristics
        self.num_captured_slots = num_captured_slots
        self.num_free_slots_init = num_free_slots

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
        in_board_next_locations = [loc for loc in all_next_locations if 0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        all_next_locations = [tup_add(self.rival_loc, direction) for direction in directions]
        in_board_next_locations = [loc for loc in all_next_locations if
                                   0 <= loc[0] < len(self.board) and 0 <= loc[1] < len(self.board[1])]
        possible_rival_next_locations = [loc for loc in in_board_next_locations if self.board[loc] == 0]
        if (len(possible_next_locations) == 0 and len(possible_rival_next_locations) == 0) or \
                (len(possible_next_locations) == 0 and self.player_turn == 1) or \
                (len(possible_rival_next_locations) == 0 and self.player_turn == 2) :
            return True
        return False
