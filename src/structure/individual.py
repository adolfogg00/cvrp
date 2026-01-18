from opt_flow.structure import BaseIndividual
from structure.instance import Instance
from structure.route import Route
from typing import List
class Individual(BaseIndividual):
    
    __slots__ = ("instance",)
    def __init__(self, instance: Instance):
        self.instance = instance
        self.routes: List[Route] = []
        self.total_distance = 0.0
        
    def add_route(self, route: Route):
        self.routes.append(route)
    
    def add_empty_route(self):
        depot = self.instance.depot
        self.routes.append(Route(depot))
        
    def clear_empty_routes(self):
        self.routes = [route for route in self.routes if not route.is_empty()]
        
