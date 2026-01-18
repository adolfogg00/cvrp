from opt_flow.structure import Data
from structure.node import Node
from typing import List
import numpy as np

class Instance(Data):
    
    __slots__ = ("depot", "nodes", "capacity")
    def __init__(self, depot: Node, nodes: List[Node], capacity: int, dist_matrix: np.ndarray):
        self.depot = depot
        self.nodes = nodes
        self.capacity = capacity
        self.dist_matrix = dist_matrix