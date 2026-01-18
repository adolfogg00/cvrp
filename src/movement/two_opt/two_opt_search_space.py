from opt_flow.movement import SearchSpace
from movement.two_opt.two_opt_args import TwoOptArgs
from structure.individual import Individual

class TwoOptSearchSpace(SearchSpace):
    
    def __iter__(self):
        individual: Individual = self.individual
        nb_routes = len(individual.routes)
        shuffled_route_indices = list(range(nb_routes))
        rng = self.rng
        routes = individual.routes
        rng.shuffle(shuffled_route_indices)
        for route_index in shuffled_route_indices:
            route = routes[route_index]
            node_list = route.node_list
            n = len(node_list)
            start_positions = list(range(1, n - 1))
            rng.shuffle(start_positions)
            for i in start_positions:
                end_positions = list(range(i + 1, n))
                rng.shuffle(end_positions)
                for j in end_positions:
                    args = TwoOptArgs(
                        route_index=route_index,
                        i=i,
                        j=j,
                        delta=None
                    )
                    yield args