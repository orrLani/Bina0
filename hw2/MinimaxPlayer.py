import math
from GameAnalyzer import GameState

def MiniMax(state : GameState, deciding_agent):
    score = state.evaluateIfFinal()
    if score is not None:
        return score
    agent_to_move = state.turn()
    if agent_to_move == deciding_agent:
        curMax = -math.inf
        for successor in state.successors():
            score = MiniMax(successor, deciding_agent)
            curMax = max(score,curMax)
        return curMax
    else:
        curMin = math.inf
        for successor in state.successors():
            score = MiniMax(successor, deciding_agent)
            curMin = min(score,curMin)
        return curMin

class MinimaxPlayer:
    def __init__(self):
        self.board = None
        self.loc = None
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
        initial_state = GameState(self.board, self.loc, self.rival_loc, 1)
        curMax = -math.inf
        best_move=None
        for successor in initial_state.successors():
            score = MiniMax(successor, 1)
            newMax = max(score,curMax)
            if newMax >= curMax:
                newMax=curMax
                best_move = successor.directionToState()
        return best_move


    def set_rival_move(self,loc):
        #old rival location
        self.board[self.rival_loc] = -1
        #new rival location
        self.board[loc]=2
        self.rival_loc=loc
        # TODO: implement more options?