from opt_flow.movement import Movement
from movement.two_opt.two_opt_args import TwoOptArgs
from structure.individual import Individual
from structure.route import Route
from typing import List
from structure.node import Node

class TwoOptMovement(Movement):

    def execute(self, args: TwoOptArgs):
        individual: Individual = self.individual
        route: Route = individual.routes[args.route_index]
        i = args.i
        j = args.j
        node_list = route.node_list
        delta = args.delta
        if delta is None:
            delta = self._calculate_delta(
                node_list, i, j, individual.instance.dist_matrix
            )
        individual.total_distance += delta
        node_list[i : j + 1] = reversed(
            node_list[i : j + 1]
        )
        

    def simulate(self, args: TwoOptArgs) -> float:
        individual: Individual = self.individual
        data = individual.instance
        route: Route = individual.routes[args.route_index]
        node_list = route.node_list
        i = args.i
        j = args.j
        delta = self._calculate_delta(
            node_list, i, j, data.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(self, node_list: List[Node], i: int, j: int, dist_matrix) -> int:
        n = len(node_list)
        a_index = node_list[i - 1].index
        b_index = node_list[i].index
        c_index = node_list[j].index
        d_index = node_list[(j + 1) % n].index
        delta = (
            - dist_matrix[a_index][b_index]
            - dist_matrix[c_index][d_index]
            + dist_matrix[a_index][c_index]
            + dist_matrix[b_index][d_index]
        )
        return delta