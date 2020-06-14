import math
from GameAnalyzer import State
from Board import Board
directions = [(1,0),(-1,0),(0,1),(0,-1)]
import Board

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





def improved_H(state: State):
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

    return improved_H(state) + dist(state.self_loc, state.rival_loc)




def offensive_To_Defensive_H(state:State):
    distance = dist(state.self_loc,state.rival_loc)
    ratio_available_steps = (state.num_free_slots_init-state.num_captured_slots)/state.num_free_slots_init
    def vacancies_slots(loc, board:Board, search_space):
        """
        this function get a board and search_space and return the num of free slots on the search space
        like bfs until  until deepness of depth
        :param loc:
        :param board:
        :param agent:
        :return:
        """
        if search_space==0:
            search_space=1
        index = 0
        d=0
        list = []
        list.append(loc)
        while index < len(list) and d<search_space:
            head_loc = list[index] # get the first organ
            index += 1
            for direction in directions:
                i, j = head_loc[0] + direction[0], head_loc[1] + direction[1]
                if (i,j) not in list and 0 <= i < len(board) and \
                        0 <= j < len(board[0]) and state.board[i][j] == 0:
                    list.append((i, j))
                d+=1
        return index

    def count_moves(loc):
        num_steps_available = 0
        for d in directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(state.board) and 0 <= j < len(state.board[0]) and state.board[i][j] == 0:  # then move is legal
                num_steps_available += 1
        return num_steps_available
    ratio_available_steps = (state.num_free_slots_init-state.num_captured_slots)/state.num_free_slots_init
    size = state.board.size
    search_space= (size)*ratio_available_steps
    agent = vacancies_slots(state.self_loc, state.board, search_space)
    opponent = vacancies_slots(state.rival_loc, state.board, search_space)

    if ratio_available_steps>0.5:
        return agent-((1+ratio_available_steps)*opponent)
    else:
        return ((2-ratio_available_steps)*agent) -opponent




def most_longest_path_H_heavy(state:State):
    def getAllNextLocs(board: Board, loc):
        """
        returns a list of all possible next locations on board given a location
        """
        next_locs = []
        for d in directions:
            possible_loc = tup_add(loc,d)
            if 0 <= possible_loc[0] < len(board) and 0 <= possible_loc[1] < len(board[0]) and \
                    board[possible_loc] == 0:
                next_locs.append(possible_loc)
        return next_locs
    def getAllNextLocsPlusBoards(board: Board, loc):
        """
        returns a list of all possible next locations on board given a location
        """
        next_locs = []
        for d in directions:
            possible_loc = tup_add(loc,d)
            if 0 <= possible_loc[0] < len(board) and 0 <= possible_loc[1] < len(board[0]) and \
                    board[possible_loc] == 0:
                        if (d == (1,0)):
                            next_locs.append( ((0,possible_loc[1]) , board[possible_loc[0]:]) )
                        if (d == (-1,0)):
                            next_locs.append( (possible_loc, board[:possible_loc[0]+1]) )
                        if (d == (0,-1)):
                            next_locs.append((possible_loc,  board[0:,0:possible_loc[1]+1]))
                        if (d == (0,1)):
                            next_locs.append( ( (possible_loc[0],0), board[0:,possible_loc[1]:]))



        return next_locs

    # def simulateMove(board, loc, next_loc):
    #     """
    #     simulate movement of player in location =loc to next location
    #     """
    #     board[next_loc]=board[loc]
    #     board[loc]=-5
    #     pass
    #
    #
    #
    # def restoreMove(board, loc , from_loc):
    #     """
    #     restores board from moving to location = from_loc
    #     """
    #     board[loc]=board[from_loc]
    #     board[from_loc]=0
    #     pass
    flag =1

    def count_longest_path(board: Board, loc):
        """
        returns longest path available for a player in location = loc
        """
        next_locs = getAllNextLocs(board,loc)
        if not next_locs:
            return 0
        longest_path_size=0
        for next_loc in next_locs:
            #saved = board[next_loc]
            board[next_loc[0]][next_loc[1]] = 1
            curr_path_size = count_longest_path(board,next_loc)
            board[next_loc[0]][next_loc[1]] = 0
            if curr_path_size>=longest_path_size:
                longest_path_size=curr_path_size
        return 1+longest_path_size
        # for tup in next_locs:
        #     next_loc, next_board = tup_split(tup)
        #     #saved = board[next_loc]
        #     next_board[next_loc[0]][next_loc[1]] = 1
        #     curr_path_size = count_longest_path(next_board,next_loc)
        #     next_board[next_loc[0]][next_loc[1]] = 0
        #     if curr_path_size>=longest_path_size:
        #         longest_path_size=curr_path_size
        # return 1+longest_path_size

    temp_board = state.board.copy()
    my_longest = count_longest_path(temp_board, state.self_loc)
    his_longest = count_longest_path(temp_board,state.rival_loc)
    result = my_longest-his_longest
    return result

def most_longest_path_H_heavy2(state:State):
    def getAllNextLocs(board: Board, loc):
        """
        returns a list of all possible next locations on board given a location
        """
        next_locs = []
        for d in directions:
            possible_loc = tup_add(loc,d)
            if 0 <= possible_loc[0] < len(board) and 0 <= possible_loc[1] < len(board[0]) and \
                    board[possible_loc] == 0:
                next_locs.append(possible_loc)
        return next_locs
    def getAllNextLocsPlusBoards(board: Board, loc):
        """
        returns a list of all possible next locations on board given a location
        """
        next_locs = []
        for d in directions:
            possible_loc = tup_add(loc,d)
            if 0 <= possible_loc[0] < len(board) and 0 <= possible_loc[1] < len(board[0]) and \
                    board[possible_loc] == 0:
                        if (d == (1,0)):
                            next_locs.append( ((0,possible_loc[1]) , board[possible_loc[0]:]) )
                        if (d == (-1,0)):
                            next_locs.append( (possible_loc, board[:possible_loc[0]+1]) )
                        if (d == (0,-1)):
                            next_locs.append((possible_loc,  board[0:,0:possible_loc[1]+1]))
                        if (d == (0,1)):
                            next_locs.append( ( (possible_loc[0],0), board[0:,possible_loc[1]:]))



        return next_locs

    # def simulateMove(board, loc, next_loc):
    #     """
    #     simulate movement of player in location =loc to next location
    #     """
    #     board[next_loc]=board[loc]
    #     board[loc]=-5
    #     pass
    #
    #
    #
    # def restoreMove(board, loc , from_loc):
    #     """
    #     restores board from moving to location = from_loc
    #     """
    #     board[loc]=board[from_loc]
    #     board[from_loc]=0
    #     pass
    def count_longest_path(board: Board, loc):
        """
        returns longest path available for a player in location = loc
        """
        next_locs = getAllNextLocsPlusBoards(board,loc)
        if not next_locs :
            return 0

        longest_path_size=0
        # for next_loc in next_locs:
        #     #saved = board[next_loc]
        #     board[next_loc[0]][next_loc[1]] = 1
        #     curr_path_size = count_longest_path(board,next_loc)
        #     board[next_loc[0]][next_loc[1]] = 0
        #     if curr_path_size>=longest_path_size:
        #         longest_path_size=curr_path_size
        # return 1+longest_path_size
        for tup in next_locs:
            next_loc, next_board = tup_split(tup)
            #saved = board[next_loc]
            next_board[next_loc[0]][next_loc[1]] = 1
            curr_path_size = count_longest_path(next_board,next_loc)
            next_board[next_loc[0]][next_loc[1]] = 0
            if curr_path_size>=longest_path_size:
                longest_path_size=curr_path_size
        return 1+longest_path_size

    temp_board = state.board.copy()
    result = count_longest_path(temp_board, state.self_loc) - count_longest_path(temp_board,state.rival_loc)
    return result








