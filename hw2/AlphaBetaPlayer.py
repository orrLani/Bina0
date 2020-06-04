from MinimaxPlayer import MinimaxPlayer
from Heuristics import *
class AlphaBetaPlayer(MinimaxPlayer):
    def __init__(self):
        super().__init__()
        self.heuristic = goToEnemy_H
    def choose_move(self,state:State,depth:int) ->tuple:
        def AB_RB_MiniMax(state: State, depth: int, alpha: int, beta: int):
            if state.is_final_state():
                return final_H(state)
            if depth == 0:
                self.leaves += 1
                return self.heuristic(state)
            agent_to_move = state.turn()
            if agent_to_move == 1:
                # my turn
                curMax = -math.inf
                for successor in self.successors(state):
                    score = AB_RB_MiniMax(successor, depth - 1, alpha, beta)
                    curMax = max(score, curMax)
                    alpha = max(curMax,alpha)
                    if curMax >= beta:
                        return math.inf
                return curMax
            else:
                curMin = math.inf
                # deciding_agent=state.switch_turns()
                for successor in self.successors(state):
                    score = AB_RB_MiniMax(successor, depth - 1, alpha, beta)
                    curMin = min(score, curMin)
                    beta=min(curMin,beta)
                    if curMin <= alpha:
                        return -math.inf
                return curMin

        curMax = -math.inf
        alpha = math.inf
        beta = -math.inf
        best_move = None
        for successor in self.successors(state):
            score = AB_RB_MiniMax(successor,depth,alpha,beta)
            if score >= curMax:
                curMax = score
                best_move = successor.directionToState()
            alpha = max(curMax, alpha)
        return best_move