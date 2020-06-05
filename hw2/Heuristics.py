import math
from GameAnalyzer import State
directions = [(1,0),(-1,0),(0,1),(0,-1)]

def tup_add(t1, t2):
    return (t1[0]+t2[0],t1[1]+t2[1])


def tup_split(tup):
    return tup[0], tup[1]

def final_H(state: State):
    """
            return the heuristic of the final state
            """
    all_next_locations = [tup_add(state.self_loc, direction) for direction in directions]
    in_board_next_locations = [loc for loc in all_next_locations if
                               0 <= loc[0] < len(state.board) and 0 <= loc[1] < len(state.board[1])]
    possible_next_locations = [loc for loc in in_board_next_locations if state.board[loc] == 0]
    all_next_locations = [tup_add(state.rival_loc, direction) for direction in directions]
    in_board_next_locations = [loc for loc in all_next_locations if
                               0 <= loc[0] < len(state.board) and 0 <= loc[1] < len(state.board[1])]
    possible_rival_next_locations = [loc for loc in in_board_next_locations if state.board[loc] == 0]
    if len(possible_next_locations) == 0 and len(possible_rival_next_locations) == 0:
        return 0
    if len(possible_next_locations) == 0:
        return -math.inf
    if len(possible_rival_next_locations) == 0:
        return math.inf
    return 0





def defencive_H(state: State):
    def count_moves(loc):
        num_steps_available = 0
        for d in directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(state.board) and 0 <= j < len(state.board[0]) and state.board[i][j] == 0:  # then move is legal
                num_steps_available += 1
        return num_steps_available
    return count_moves(state.self_loc) - (count_moves(state.rival_loc))


def dist(loc1,loc2):
    x1,y1=tup_split(loc1)
    x2,y2=tup_split(loc2)
    return math.hypot(x1-x2, y1-y2)

def goToEnemy_H(state: State):

    return defencive_H(state)+dist(state.self_loc,state.rival_loc)


def attack_defencive_H(state:State):
    distance = dist(state.self_loc,state.rival_loc)
    ratio_available_steps = state.num_captured_slots/state.num_free_slots_init
    def count_moves(loc):
        num_steps_available = 0
        for d in directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(state.board) and 0 <= j < len(state.board[0]) and state.board[i][j] == 0:  # then move is legal
                num_steps_available += 1
        return num_steps_available

    distance =dist(state.rival_loc,state.self_loc)
    return (ratio_available_steps*(count_moves(state.self_loc) + (0*distance))-
            ((1-ratio_available_steps)*(count_moves(state.rival_loc)+(0*distance))))











