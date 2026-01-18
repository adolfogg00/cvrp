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
        
    def copy(self) -> "Route":
        new_route = Route(self.node_list[0])
        new_route.node_list = self.node_list.copy()
        new_route.used_capacity = self.used_capacity
        return new_route
    
    def __eq__(self, other: "Route") -> bool:
        if other is None:
            return False
        return self.node_list == other.node_list