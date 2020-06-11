from AlphaBetaPlayer import AlphaBetaPlayer
from Heuristics import *

class LiteAlphaBetaPlayer(AlphaBetaPlayer):
    def __init__(self):
        super().__init__()
        self.heuristic = defencive_H