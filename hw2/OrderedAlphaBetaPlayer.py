from AlphaBetaPlayer import AlphaBetaPlayer
from Heuristics import *

class OrderedAlphaBetaPlayer(AlphaBetaPlayer):
    def __init__(self):
        super().__init__()
        self.heuristic = attack_defencive_H
        self.sorted_succesors:list = []



    def choose_move(self,state:State,depth:int) ->tuple:
        def sorted_list():
            sorted(self.sorted_succesors, key=lambda value: value[1], reverse=True)

            return [value[0] for  value in self.sorted_succesors]
        curMax = -math.inf
        alpha = -math.inf
        beta = math.inf
        best_move = None
        if depth==1:
           self.sorted_succesors=[]
           for successor in self.successors(state):
               best_move = successor.directionToState()
               self.sorted_succesors.append([successor,0])
        new_sorted_list=[]
        for successor in sorted_list(): #self.succesors

            score = self.AB_RB_MiniMax(successor,depth-1,alpha,beta)
            # best_move = successor.directionToState()
            new_sorted_list.append([successor,score])
            if score >= curMax:
                curMax = score
                best_move = successor.directionToState()
            alpha = max(curMax, alpha)
        self.sorted_succesors=new_sorted_list
        return best_move


   # def successors(self,state:State):
   #     list_of_successors=super().successors(state)
   #     list_of_successors.sort(key=lambda state:self.AB_RB_MiniMax(state, depth - 1, alpha, beta))
   #    ord