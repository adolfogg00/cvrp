from opt_flow.movement import SearchSpace
from movement.remove.remove_args import RemoveArgs
from structure.individual import Individual


class RemoveSearchSpace(SearchSpace):

    def __iter__(self):
        individual: Individual = self.individual
        routes = individual.routes
        rng = self.rng
        
        nb_routes = len(routes)
        
        # Shuffle route indices for exploration diversity
        route_indices = list(range(nb_routes))
        rng.shuffle(route_indices)
        
        # Consider each route
        for route_idx in route_indices:
            route = routes[route_idx]
            nodes = route.node_list
            
            # A route must have at least 1 customer to remove
            # (depot + at least 1 customer = minimum 2 nodes)
            if len(nodes) <= 2:  # Only depot or depot + 1 customer
                continue
            
            # Generate all removable nodes (customer nodes only, not depot)
            # Depot is at index 0, so customers start at index 1
            removable_indices = list(range(1, len(nodes)))
            rng.shuffle(removable_indices)
            
            for remove_idx in removable_indices:
                # Create the remove move
                yield RemoveArgs(
                    route_index=route_idx,
                    remove_index=remove_idx,
                    delta=None  # Will be calculated in simulate()
                )