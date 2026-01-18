from opt_flow.movement import Movement
from structure.individual import Individual
from structure.route import Route
from structure.node import Node
from typing import List
from movement.merge_routes.merge_routes_args import MergeRoutesArgs

class MergeRoutesMovement(Movement):

    def execute(self, args: MergeRoutesArgs):
        individual: Individual = self.individual

        route_i: Route = individual.routes[args.route_i]
        route_j: Route = individual.routes[args.route_j]

        nodes_i = route_i.node_list
        nodes_j = route_j.node_list

        delta = args.delta
        if delta is None:
            delta = self._calculate_delta(
                nodes_i, nodes_j, individual.instance.dist_matrix
            )

        individual.total_distance += delta

        # Merge: skip depot of route_j
        nodes_i.extend(nodes_j[1:])
        route_i.used_capacity += route_j.used_capacity
        route_j.used_capacity = 0
        route_j.node_list = [nodes_j[0]]  
        
    def simulate(self, args: MergeRoutesArgs) -> int:
        individual: Individual = self.individual
        route_i = individual.routes[args.route_i]
        route_j = individual.routes[args.route_j]

        delta = self._calculate_delta(
            route_i.node_list,
            route_j.node_list,
            individual.instance.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(
        self,
        nodes_i: List[Node],
        nodes_j: List[Node],
        dist_matrix
    ) -> int:
        """
        Distance change when merging route_j into route_i.
        """

        # Last node of route_i
        last_i = nodes_i[-1]

        # First customer of route_j (after depot)
        first_j = nodes_j[1]

        delta = 0

        # Remove return-to-depot edges
        delta -= dist_matrix[last_i.index][nodes_i[0].index]
        delta -= dist_matrix[nodes_j[0].index][first_j.index]

        # Add connecting edge
        delta += dist_matrix[last_i.index][first_j.index]

        return delta
