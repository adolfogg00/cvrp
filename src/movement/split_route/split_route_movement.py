from opt_flow.movement import Movement
from structure.individual import Individual
from structure.route import Route
from structure.node import Node
from typing import List
from movement.split_route.split_route_args import SplitRouteArgs

class SplitRouteMovement(Movement):

    def execute(self, args: SplitRouteArgs):
        individual: Individual = self.individual
        route: Route = individual.routes[args.route_index]
        nodes = route.node_list

        delta = args.delta
        if delta is None:
            delta = self._calculate_delta(
                nodes, args.split_index, individual.instance.dist_matrix
            )

        individual.total_distance += delta

        # Create new route with same depot
        depot = nodes[0]
        new_route = Route(depot)

        # Move nodes from split_index onward
        new_route.node_list.extend(nodes[args.split_index:])

        # Shrink original route
        del nodes[args.split_index:]

        # Append new route
        individual.routes.append(new_route)
        route.used_capacity = sum(node.demand for node in route.node_list)
        new_route.used_capacity = sum(node.demand for node in new_route.node_list)

    def simulate(self, args: SplitRouteArgs) -> int:
        individual: Individual = self.individual
        route = individual.routes[args.route_index]

        delta = self._calculate_delta(
            route.node_list,
            args.split_index,
            individual.instance.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(
        self,
        nodes: List[Node],
        split_index: int,
        dist_matrix
    ) -> int:
        """
        Distance change caused by splitting a route.
        """

        depot = nodes[0]
        prev_node = nodes[split_index - 1]
        first_new = nodes[split_index]

        delta = 0

        # Remove edge prev → first_new
        delta -= dist_matrix[prev_node.index][first_new.index]

        # Add returns to depot
        delta += dist_matrix[prev_node.index][depot.index]
        delta += dist_matrix[depot.index][first_new.index]

        return delta
