from structure.node import Node


class Route:
    
    def __init__(self, depot: Node):
        self.node_list = [depot]
        self.used_capacity = 0
        
    def is_empty(self) -> bool:
        return len(self.node_list) == 1
    
    def add_node(self, node: Node):
        self.node_list.append(node)
        self.used_capacity += node.demand