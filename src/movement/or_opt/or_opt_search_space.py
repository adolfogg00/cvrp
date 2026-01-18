from opt_flow.movement import SearchSpace
from movement.or_opt.or_opt_args import OrOptArgs
from structure.individual import Individual


class OrOptSearchSpace(SearchSpace):

    def __iter__(self):
        individual: Individual = self.individual
        routes = individual.routes
        rng = self.rng

        nb_routes = len(routes)
        shuffled_route_indices = list(range(nb_routes))
        rng.shuffle(shuffled_route_indices)

        for route_index in shuffled_route_indices:
            route = routes[route_index]
            node_list = route.node_list
            n = len(node_list)

            segment_lengths = list(range(1, n - 1))
            rng.shuffle(segment_lengths)

            for k in segment_lengths:
                if n <= k + 1:
                    continue

                start_positions = list(range(1, n - k))
                rng.shuffle(start_positions)

                for start in start_positions:
                    end = start + k - 1

                    insert_positions = list(range(1, n))
                    rng.shuffle(insert_positions)

                    for insert_index in insert_positions:
                        # Cannot insert inside the removed segment
                        if insert_index >= start and insert_index <= end + 1:
                            continue

                        args = OrOptArgs(
                            route_index=route_index,
                            start=start,
                            end=end,
                            insert_index=insert_index,
                            delta=None
                        )
                        yield args
