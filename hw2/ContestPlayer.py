from OrderedAlphaBetaPlayer import OrderedAlphaBetaPlayer
from Heuristics import *

class ContestPlayer(OrderedAlphaBetaPlayer):
    def __init__(self):
        super().__init__()
        self.heuristic = offensive_To_Defensive_H