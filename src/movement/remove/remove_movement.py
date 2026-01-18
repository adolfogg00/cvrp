from opt_flow.movement import Movement
from structure.individual import Individual
from structure.route import Route
from structure.node import Node
from typing import List
from movement.remove.remove_args import RemoveArgs

class RemoveMovement(Movement):

    def execute(self, args: RemoveArgs):
        individual: Individual = self.individual
        route: Route = individual.routes[args.route_index]
        nodes = route.node_list

        delta = args.delta
        if delta is None:
            delta = self._calculate_delta(
                nodes,
                args.remove_index,
                individual.instance.dist_matrix
            )

        individual.total_distance += delta
        individual.total_assigned_nodes -= 1

        # Remove node
        route.used_capacity -= nodes[args.remove_index].demand
        nodes.pop(args.remove_index)

    def simulate(self, args: RemoveArgs) -> int:
        individual: Individual = self.individual
        route = individual.routes[args.route_index]

        delta = self._calculate_delta(
            route.node_list,
            args.remove_index,
            individual.instance.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(
        self,
        nodes: List[Node],
        remove_index: int,
        dist_matrix
    ) -> int:
        """
        Distance change when removing a node from a route.
        """

        prev_node = nodes[remove_index - 1]
        removed_node = nodes[remove_index]

        # If removing last node, next is depot
        if remove_index + 1 < len(nodes):
            next_node = nodes[remove_index + 1]
        else:
            next_node = nodes[0]  # depot

        delta = (
            - dist_matrix[prev_node.index][removed_node.index]
            - dist_matrix[removed_node.index][next_node.index]
            + dist_matrix[prev_node.index][next_node.index]
        )

        return delta
