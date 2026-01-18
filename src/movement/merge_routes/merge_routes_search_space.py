from opt_flow.movement import SearchSpace
from movement.merge_routes.merge_routes_args import MergeRoutesArgs
from structure.individual import Individual


class MergeRoutesSearchSpace(SearchSpace):

    def __iter__(self):
        individual: Individual = self.individual
        routes = individual.routes
        rng = self.rng
        instance = individual.instance
        capacity = instance.capacity

        nb_routes = len(routes)
        
        # Need at least 2 routes to merge
        if nb_routes < 2:
            return
        
        # Shuffle route indices for exploration diversity
        route_indices = list(range(nb_routes))
        rng.shuffle(route_indices)
        
        # Consider all pairs of different routes
        for idx in range(nb_routes):
            route_i_idx = route_indices[idx]
            route_i = routes[route_i_idx]
            cap_i = route_i.used_capacity
            
            # Skip routes that are empty (only depot)
            if len(route_i.node_list) <= 1:
                continue
            
            for jdx in range(idx + 1, nb_routes):
                route_j_idx = route_indices[jdx]
                route_j = routes[route_j_idx]
                cap_j = route_j.used_capacity
                
                # Skip routes that are empty (only depot)
                if len(route_j.node_list) <= 1:
                    continue
                
                # Check capacity feasibility after merging
                # route_i gets all customers from route_j
                combined_capacity = cap_i + cap_j
                
                if combined_capacity > capacity:
                    continue
                
                # Yield the merge move (both directions)
                # Merge route_j into route_i
                yield MergeRoutesArgs(
                    route_i=route_i_idx,
                    route_j=route_j_idx,
                    delta=None
                )
                
                # Also consider merging route_i into route_j
                # (Different delta calculation since merging direction matters)
                yield MergeRoutesArgs(
                    route_i=route_j_idx,
                    route_j=route_i_idx,
                    delta=None
                )