from opt_flow.movement import Movement
from structure.individual import Individual
from structure.route import Route
from structure.node import Node
from typing import List
from movement.insert.insert_args import InsertArgs

class InsertMovement(Movement):

    def execute(self, args: InsertArgs):
        individual: Individual = self.individual
        route: Route = individual.routes[args.route_index]
        nodes = route.node_list

        delta = args.delta
        if delta is None:
            delta = self._calculate_delta(
                nodes,
                args.insert_index,
                args.node,
                individual.instance.dist_matrix
            )

        individual.total_distance += delta

        nodes.insert(args.insert_index, args.node)
        route.used_capacity += args.node.demand

    def simulate(self, args: InsertArgs) -> int:
        individual: Individual = self.individual
        route = individual.routes[args.route_index]

        delta = self._calculate_delta(
            route.node_list,
            args.insert_index,
            args.node,
            individual.instance.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(
        self,
        nodes: List[Node],
        insert_index: int,
        node: Node,
        dist_matrix
    ) -> int:
        """
        Distance change when inserting a node into a route.
        """

        prev_node = nodes[insert_index - 1]

        # If inserting at the end, next node is depot
        if insert_index < len(nodes):
            next_node = nodes[insert_index]
        else:
            next_node = nodes[0]  # depot

        delta = (
            - dist_matrix[prev_node.index][next_node.index]
            + dist_matrix[prev_node.index][node.index]
            + dist_matrix[node.index][next_node.index]
        )

        return delta
