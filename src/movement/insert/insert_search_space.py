from opt_flow.movement import SearchSpace
from movement.insert.insert_args import InsertArgs
from structure.individual import Individual
from structure.node import Node


class InsertSearchSpace(SearchSpace):

    def __iter__(self):
        individual: Individual = self.individual
        rng = self.rng
        instance = individual.instance
        
        # Get unassigned nodes (nodes not in any route)
        unassigned_nodes = self._get_unassigned_nodes(individual)
        
        if not unassigned_nodes:
            return  # No unassigned nodes to insert
        
        # Shuffle unassigned nodes for random exploration
        rng.shuffle(unassigned_nodes)
        
        # Get all routes
        routes = individual.routes
        nb_routes = len(routes)
        
        # Shuffle route indices for exploration diversity
        route_indices = list(range(nb_routes))
        rng.shuffle(route_indices)
        
        # For each unassigned node
        for node in unassigned_nodes:
            node_demand = node.demand
            
            # For each possible target route
            for route_idx in route_indices:
                route = routes[route_idx]
                route_capacity = route.used_capacity
                
                # Check capacity feasibility
                if route_capacity + node_demand > instance.capacity:
                    continue
                
                # Generate all possible insertion positions
                # Positions range from 1 to len(nodes) (after depot up to after last node)
                nodes = route.node_list
                n_nodes = len(nodes)
                
                # Valid insertion positions: 1 through n_nodes (inclusive)
                # position 1 = after depot, position n_nodes = after last node
                insertion_positions = list(range(1, n_nodes + 1))
                rng.shuffle(insertion_positions)
                
                for insert_pos in insertion_positions:
                    yield InsertArgs(
                        route_index=route_idx,
                        insert_index=insert_pos,  # Position where node will be inserted
                        node=node,
                        delta=None  # Will be calculated in simulate()
                    )
    
    def _get_unassigned_nodes(self, individual: Individual) -> list[Node]:
        """
        Get all nodes that are not currently assigned to any route.
        """
        # Get all nodes from the instance
        all_nodes = individual.instance.nodes
        
        # Get nodes already in routes
        assigned_nodes = set()
        for route in individual.routes:
            # Skip depot (usually node 0) as it's in every route
            for node in route.node_list[1:]:  # Start from index 1 to skip depot
                assigned_nodes.add(node.index)
        
        # Find unassigned nodes (excluding depot if it's node 0)
        unassigned = []
        for node in all_nodes:
            # Typically depot is index 0, but we should check instance.depot_index
            if node.index != individual.instance.depot_index and node.index not in assigned_nodes:
                unassigned.append(node)
        
        return unassigned