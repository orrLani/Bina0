from .graph_problem_interface import *
from .astar import AStar
from typing import Optional, Callable
import numpy as np
import math


class AStarEpsilon(AStar):
    """
    This class implements the (weighted) A*Epsilon search algorithm.
    A*Epsilon algorithm basically works like the A* algorithm, but with
    another way to choose the next node to expand from the open queue.
    """

    solver_name = 'A*eps'

    def __init__(self,
                 heuristic_function_type: HeuristicFunctionType,
                 within_focal_priority_function: Callable[[SearchNode, GraphProblem, 'AStarEpsilon'], float],
                 heuristic_weight: float = 0.5,
                 max_nr_states_to_expand: Optional[int] = None,
                 focal_epsilon: float = 0.1,
                 max_focal_size: Optional[int] = None):
        # A* is a graph search algorithm. Hence, we use close set.
        super(AStarEpsilon, self).__init__(heuristic_function_type, heuristic_weight,
                                           max_nr_states_to_expand=max_nr_states_to_expand)
        self.focal_epsilon = focal_epsilon
        if focal_epsilon < 0:
            raise ValueError(f'The argument `focal_epsilon` for A*eps should be >= 0; '
                             f'given focal_epsilon={focal_epsilon}.')
        self.within_focal_priority_function = within_focal_priority_function
        self.max_focal_size = max_focal_size

    def _init_solver(self, problem):
        super(AStarEpsilon, self)._init_solver(problem)

    def _extract_next_search_node_to_expand(self, problem: GraphProblem) -> Optional[SearchNode]:
        """
        Extracts the next node to expand from the open queue,
         by focusing on the current FOCAL and choosing the node
         with the best within_focal_priority from it.
        TODO [Ex.38]: Implement this method!
        Find the minimum expanding-priority value in the `open` queue.
        Calculate the maximum expanding-priority of the FOCAL, which is
         the min expanding-priority in open multiplied by (1 + eps) where
         eps is stored under `self.focal_epsilon`.
        Create the FOCAL by popping items from the `open` queue and inserting
         them into a focal list. Don't forget to satisfy the constraint of
         `self.max_focal_size` if it is set (not None).
        Notice: You might want to pop items from the `open` priority queue,
         and then choose an item out of these popped items. Don't forget:
         the other items have to be pushed back into open.
        Inspect the base class `BestFirstSearch` to retrieve the type of
         the field `open`. Then find the definition of this type and find
         the right methods to use (you might want to peek the head node, to
         pop/push nodes and to query whether the queue is empty).
        For each node (candidate) in the created focal, calculate its priority
         by callingthe function `self.within_focal_priority_function` on it.
         This function expects to get 3 values: the node, the problem and the
         solver (self). You can create an array of these priority value. Then,
         use `np.argmin()` to find the index of the item (within this array)
         with the minimal value. After having this index you could pop this
         item from the focal (at this index). This is the node that have to
         be eventually returned.
        Don't forget to handle correctly corner-case like when the open queue
         is empty. In this case a value of `None` has to be returned.
        Note: All the nodes that were in the open queue at the beginning of this
         method should be kept in the open queue at the end of this method, except
         for the extracted (and returned) node.
        """

        # # while  list_to_back:
        # #     self.open.push_node(list_to_back.pop())
        # #
        # # while  list_to_back:
        # #     self.open.push_node(list_to_back.pop())
        # # while()

        list_nodes=[]


        if self.open.is_empty():
            return None

        min_node=self.open.peek_next_node()
        f=min_node.expanding_priority
        while not self.open.is_empty():
            list_nodes.append(self.open.pop_next_node())

     #   for item in list_nodes:
      #      self.open.push_node(item)



        list_to_back=[]
        index=0
        list_to_focal=[]
        for node in list_nodes:
            if len(list_to_focal)<self.max_focal_size:
                if(node.expanding_priority<=f*(1+self.focal_epsilon)):
                    list_to_focal.append(node)
                else:
                    list_to_back.append(node)

            else:
                break

        focal_array =[self.within_focal_priority_function(node,problem,self) for node in list_to_focal]
        index=np.argmin(focal_array)

        elemnt =list_to_focal[index]
        del list_to_focal[index]


        for item in list_to_back:
            self.open.push_node(item)

        for item in  list_to_focal:
            self.open.push_node(item)

        self.close.add_node(elemnt)
        return elemnt