from opt_flow.movement import SearchSpace
from movement.two_opt_star.two_opt_star_args import TwoOptStarArgs
from structure.individual import Individual


class TwoOptStarSearchSpace(SearchSpace):

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
            n_i = len(nodes_i)

            if n_i <= 1:
                continue

            for idx_j in range(idx_i + 1, nb_routes):
                route_j = routes[idx_j]
                nodes_j = route_j.node_list
                cap_j = route_j.used_capacity
                n_j = len(nodes_j)

                if n_j <= 1:
                    continue

                # possible cut positions (exclude depot)
                cut_i_positions = list(range(0, n_i - 1))
                cut_j_positions = list(range(0, n_j - 1))
                rng.shuffle(cut_i_positions)
                rng.shuffle(cut_j_positions)

                for i in cut_i_positions:
                    tail_i = nodes_i[i + 1 :]
                    if not tail_i:
                        continue

                    demand_tail_i = sum(node.demand for node in tail_i)

                    for j in cut_j_positions:
                        tail_j = nodes_j[j + 1 :]
                        if not tail_j:
                            continue

                        demand_tail_j = sum(node.demand for node in tail_j)

                        # Capacity feasibility check (matches movement)
                        new_cap_i = cap_i - demand_tail_i + demand_tail_j
                        new_cap_j = cap_j - demand_tail_j + demand_tail_i

                        if new_cap_i > capacity or new_cap_j > capacity:
                            continue

                        yield TwoOptStarArgs(
                            route_i=idx_i,
                            route_j=idx_j,
                            i=i,
                            j=j,
                            delta=None
                        )
