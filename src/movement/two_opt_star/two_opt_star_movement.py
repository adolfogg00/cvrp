from typing import List
from opt_flow.movement import Movement
from structure.individual import Individual
from structure.route import Route
from structure.node import Node
from movement.two_opt_star.two_opt_star_args import TwoOptStarArgs

class TwoOptStarMovement(Movement):

    def execute(self, args: TwoOptStarArgs):
        individual: Individual = self.individual
        route_i: Route = individual.routes[args.route_i]
        route_j: Route = individual.routes[args.route_j]

        node_list_i = route_i.node_list
        node_list_j = route_j.node_list

        i = args.i
        j = args.j
        delta = args.delta

        if delta is None:
            delta = self._calculate_delta(
                node_list_i,
                node_list_j,
                i,
                j,
                individual.instance.dist_matrix
            )

        individual.total_distance += delta

        # Split routes
        tail_i = node_list_i[i + 1 :]
        tail_j = node_list_j[j + 1 :]

        # Exchange tails
        node_list_i[i + 1 :] = tail_j
        node_list_j[j + 1 :] = tail_i
        
        demand_i = sum(node.demand for node in tail_j)
        demand_j = sum(node.demand for node in tail_i)
        route_i.used_capacity += demand_i - demand_j
        route_j.used_capacity += demand_j - demand_i

    def simulate(self, args: TwoOptStarArgs) -> int:
        individual: Individual = self.individual
        route_i = individual.routes[args.route_i]
        route_j = individual.routes[args.route_j]

        delta = self._calculate_delta(
            route_i.node_list,
            route_j.node_list,
            args.i,
            args.j,
            individual.instance.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(
        self,
        node_list_i: List[Node],
        node_list_j: List[Node],
        i: int,
        j: int,
        dist_matrix
    ) -> int:
        """
        Compute delta for 2-opt* between two different routes.
        """

        # Nodes at cut points
        a = node_list_i[i]
        b = node_list_i[i + 1] if i + 1 < len(node_list_i) else None

        c = node_list_j[j]
        d = node_list_j[j + 1] if j + 1 < len(node_list_j) else None

        delta = 0

        # Remove old edges
        if b:
            delta -= dist_matrix[a.index][b.index]
        if d:
            delta -= dist_matrix[c.index][d.index]

        # Add new edges
        if d:
            delta += dist_matrix[a.index][d.index]
        if b:
            delta += dist_matrix[c.index][b.index]

        return delta
