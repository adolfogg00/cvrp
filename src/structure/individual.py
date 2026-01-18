from opt_flow.structure import BaseIndividual
from structure.instance import Instance
from opt_flow.structure import ScalarObjective, MultiObjective
from structure.route import Route
from typing import List
class Individual(BaseIndividual):
    
    __slots__ = ("instance",)
    def __init__(self, instance: Instance):
        self.instance = instance
        self.routes: List[Route] = []
        self.total_distance = 0.0
        self.total_assigned_nodes = 0
        
    def add_route(self, route: Route):
        self.routes.append(route)
    
    def add_empty_route(self):
        depot = self.instance.depot
        self.routes.append(Route(depot))
        
    def clear_empty_routes(self):
        self.routes = [route for route in self.routes if not route.is_empty()]
        

    def copy(self) -> "Individual":
        new_individual = Individual(self.instance)
        new_individual.routes = [route.copy() for route in self.routes] 
        new_individual.total_distance = self.total_distance
        new_individual.total_assigned_nodes = self.total_assigned_nodes
        return new_individual
    
    def overwrite_with(self, other: "Individual") -> None:
        self.routes = other.routes
        self.total_distance = other.total_distance
        self.total_assigned_nodes = other.total_assigned_nodes
        
    def __eq__(self, other: "Individual") -> bool:
        if other is None:
            return False
        return self.routes == other.routes
    
    def get_objective(self):
        return MultiObjective([
            ScalarObjective("distance", self.total_distance),
            ScalarObjective("assigned_nodes", self.total_assigned_nodes)
        ])