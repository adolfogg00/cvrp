from opt_flow.movement import SearchSpace
from movement.reinsert.reinsert_args import ReinsertArgs
from structure.individual import Individual


class ReinsertSearchSpace(SearchSpace):

    def __iter__(self):
        individual: Individual = self.individual
        routes = individual.routes
        rng = self.rng
        instance = individual.instance
        capacity = instance.capacity

        nb_routes = len(routes)
        
        # Create shuffled indices for both from_route and to_route
        route_indices = list(range(nb_routes))
        rng.shuffle(route_indices)
        
        for from_idx in route_indices:
            from_route = routes[from_idx]
            from_nodes = from_route.node_list
            from_capacity = from_route.used_capacity
            
            # Skip routes with only depot (no customers to move)
            # Need at least 1 customer to move (depot + at least 1 customer)
            if len(from_nodes) <= 2:  # depot + at most 1 customer
                continue
            
            # Generate all movable nodes (customers only, not depot)
            # Depot is at index 0, so customers start at index 1
            movable_nodes = list(range(1, len(from_nodes)))
            rng.shuffle(movable_nodes)
            
            for node_idx in movable_nodes:
                node = from_nodes[node_idx]
                node_demand = node.demand
                
                # After removing the node, check if from_route would still be valid
                # It should still have at least depot + 1 customer
                if len(from_nodes) - 1 <= 1:  # Would leave only depot or depot + 0 customers?
                    # Actually, this shouldn't happen since we check len(from_nodes) > 2 above
                    # and we're moving only one node
                    continue
                
                # Now consider all possible destination routes
                for to_idx in route_indices:
                    to_route = routes[to_idx]
                    to_nodes = to_route.node_list
                    to_capacity = to_route.used_capacity
                    
                    # Check capacity feasibility
                    if to_capacity + node_demand > capacity:
                        continue
                    
                    # Skip if moving within same route to the same position
                    if from_idx == to_idx:
                        # Generate all possible insertion positions in the same route
                        # After removal, the node will be at position node_idx
                        # Valid insertion positions: 0 to len(to_nodes)-1 (after depot up to after last node)
                        # But we need to handle the index adjustment when moving within same route
                        possible_insertions = list(range(len(to_nodes)))
                        rng.shuffle(possible_insertions)
                        
                        for insert_pos in possible_insertions:
                            # Skip if inserting after itself (before removal)
                            if insert_pos == node_idx or insert_pos == node_idx - 1:
                                continue
                            
                            yield ReinsertArgs(
                                from_route=from_idx,
                                to_route=to_idx,
                                node_index=node_idx,
                                insert_after=insert_pos,
                                delta=None
                            )
                    else:
                        # Moving to different route
                        # Valid insertion positions: 0 to len(to_nodes)-1 (after depot up to after last node)
                        possible_insertions = list(range(len(to_nodes)))
                        rng.shuffle(possible_insertions)
                        
                        for insert_pos in possible_insertions:
                            yield ReinsertArgs(
                                from_route=from_idx,
                                to_route=to_idx,
                                node_index=node_idx,
                                insert_after=insert_pos,
                                delta=None
                            )