from AlphaBetaPlayer import AlphaBetaPlayer
from Heuristics import *

class HeavyAlphaBetaPlayer(AlphaBetaPlayer):
    def __init__(self):
        super().__init__()
        self.heuristic = most_longest_path_H_heavy