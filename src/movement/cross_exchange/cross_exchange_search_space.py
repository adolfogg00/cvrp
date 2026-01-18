from opt_flow.movement import SearchSpace
from movement.cross_exchange.cross_exchange_args import CrossExchangeArgs
from structure.individual import Individual


class CrossExchangeSearchSpace(SearchSpace):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Maximum segment length to exchange (k)
        self.k = kwargs.get('k', 3)  # Default to exchanging segments of up to 3 nodes

    def __iter__(self):
        individual: Individual = self.individual
        routes = individual.routes
        rng = self.rng
        instance = individual.instance
        capacity = instance.capacity
        k = self.k

        nb_routes = len(routes)
        
        # Shuffle route indices for exploration diversity
        route_indices = list(range(nb_routes))
        rng.shuffle(route_indices)
        
        # Consider all pairs of different routes
        for idx in range(nb_routes):
            route_i_idx = route_indices[idx]
            route_i = routes[route_i_idx]
            nodes_i = route_i.node_list
            cap_i = route_i.used_capacity
            n_i = len(nodes_i)
            
            # Route needs at least 1 customer to exchange a segment
            if n_i <= 2:  # depot + at most 1 customer
                continue
            
            for jdx in range(idx + 1, nb_routes):
                route_j_idx = route_indices[jdx]
                route_j = routes[route_j_idx]
                nodes_j = route_j.node_list
                cap_j = route_j.used_capacity
                n_j = len(nodes_j)
                
                # Route needs at least 1 customer to exchange a segment
                if n_j <= 2:  # depot + at most 1 customer
                    continue
                
                # Generate all possible segments in route_i (excluding depot)
                # i_start is the first customer index in the segment (≥1)
                # i_end is the last customer index in the segment
                i_segments = []
                for i_start in range(1, n_i):  # Start from first customer
                    for length in range(1, min(k + 1, n_i - i_start + 1)):
                        i_end = i_start + length - 1
                        i_segments.append((i_start, i_end))
                
                rng.shuffle(i_segments)
                
                for i_start, i_end in i_segments:
                    # Calculate segment properties for route_i
                    seg_i = nodes_i[i_start:i_end + 1]
                    seg_i_demand = sum(node.demand for node in seg_i)
                    
                    # Generate all possible segments in route_j (excluding depot)
                    j_segments = []
                    for j_start in range(1, n_j):  # Start from first customer
                        for length in range(1, min(k + 1, n_j - j_start + 1)):
                            j_end = j_start + length - 1
                            j_segments.append((j_start, j_end))
                    
                    rng.shuffle(j_segments)
                    
                    for j_start, j_end in j_segments:
                        # Calculate segment properties for route_j
                        seg_j = nodes_j[j_start:j_end + 1]
                        seg_j_demand = sum(node.demand for node in seg_j)
                        
                        # Check capacity feasibility after exchange
                        # route_i gets seg_j instead of seg_i
                        new_cap_i = cap_i - seg_i_demand + seg_j_demand
                        # route_j gets seg_i instead of seg_j
                        new_cap_j = cap_j - seg_j_demand + seg_i_demand
                        
                        if new_cap_i > capacity or new_cap_j > capacity:
                            continue
                        
                        # Check that segments are not empty
                        if not seg_i or not seg_j:
                            continue
                        
                        # Yield the cross exchange move
                        yield CrossExchangeArgs(
                            route_i=route_i_idx,
                            route_j=route_j_idx,
                            i_start=i_start,
                            i_end=i_end,
                            j_start=j_start,
                            j_end=j_end,
                            delta=None  # Will be calculated in simulate()
                        )