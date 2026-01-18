


class Node:
    
    __slots__ = ("id", "index", "x", "y", "demand")
    def __init__(self, id_: int, x: int, y: int, demand: int):
        self.x = x
        self.y = y
        self.demand = demand
        self.id = id_
        self.index = id_ - 1