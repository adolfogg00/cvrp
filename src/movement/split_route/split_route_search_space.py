from opt_flow.movement import SearchSpace
from movement.split_route.split_route_args import SplitRouteArgs
from structure.individual import Individual


class SplitRouteSearchSpace(SearchSpace):

    def __iter__(self):
        individual: Individual = self.individual
        routes = individual.routes
        rng = self.rng
        instance = individual.instance
        capacity = instance.capacity

        nb_routes = len(routes)
        route_indices = list(range(nb_routes))
        rng.shuffle(route_indices)

        for route_idx in route_indices:
            route = routes[route_idx]
            nodes = route.node_list
            n_nodes = len(nodes)
            
            # Need at least 3 nodes (depot + 2 customers) to split meaningfully
            # Split can happen after any customer except the last one
            # Valid split positions: after index 1 (first customer) up to n_nodes-2
            if n_nodes < 3:
                continue
            

            # Generate all possible split positions
            # split_index is the index of the first node that goes to the new route
            # Valid split positions: from 2 to n_nodes-1
            # (cannot split before index 2 because we need at least 1 customer in each route)
            possible_splits = list(range(2, n_nodes))
            rng.shuffle(possible_splits)
            
            for split_idx in possible_splits:
                # Check capacity feasibility for both resulting routes
                # Original route nodes: nodes[0:split_idx]
                # New route nodes: nodes[split_idx:]
                
                # Original route capacity after split
                original_nodes = nodes[:split_idx]
                original_capacity = sum(node.demand for node in original_nodes)
                
                # New route capacity
                new_nodes = nodes[split_idx:]
                new_capacity = sum(node.demand for node in new_nodes)
                
                # Both resulting routes must respect capacity constraints
                if original_capacity > capacity or new_capacity > capacity:
                    continue
                
                # Additionally, we might want to ensure we don't create trivial routes
                # with just the depot (though this shouldn't happen with our split_idx range)
                if len(original_nodes) <= 1 or len(new_nodes) <= 1:
                    continue
                
                # Yield the split move
                yield SplitRouteArgs(
                    route_index=route_idx,
                    split_index=split_idx,
                    delta=None  # Will be calculated in simulate()
                )