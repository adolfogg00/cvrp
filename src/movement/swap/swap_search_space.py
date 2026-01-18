from opt_flow.movement import SearchSpace
from movement.swap.swap_args import SwapArgs
from structure.individual import Individual


class SwapSearchSpace(SearchSpace):

    def __iter__(self):
        individual: Individual = self.individual
        routes = individual.routes
        rng = self.rng
        capacity = individual.instance.capacity

        nb_routes = len(routes)
        route_indices = list(range(nb_routes))
        rng.shuffle(route_indices)

        for idx_i in range(nb_routes):
            route_i = routes[idx_i]
            nodes_i = route_i.node_list
            cap_i = route_i.used_capacity

            # skip empty or depot-only routes
            if len(nodes_i) <= 1:
                continue

            for idx_j in range(idx_i + 1, nb_routes):
                route_j = routes[idx_j]
                nodes_j = route_j.node_list
                cap_j = route_j.used_capacity

                if len(nodes_j) <= 1:
                    continue

                # candidate node positions (exclude depot)
                indices_i = list(range(1, len(nodes_i)))
                indices_j = list(range(1, len(nodes_j)))
                rng.shuffle(indices_i)
                rng.shuffle(indices_j)

                for i in indices_i:
                    node_i = nodes_i[i]
                    demand_i = node_i.demand

                    for j in indices_j:
                        node_j = nodes_j[j]
                        demand_j = node_j.demand

                        # Capacity feasibility check
                        new_cap_i = cap_i - demand_i + demand_j
                        new_cap_j = cap_j - demand_j + demand_i

                        if new_cap_i > capacity or new_cap_j > capacity:
                            continue

                        yield SwapArgs(
                            route_i=idx_i,
                            route_j=idx_j,
                            index_i=i,
                            index_j=j,
                            delta=None
                        )
