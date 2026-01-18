from typing import List
from opt_flow.movement import Movement
from structure.individual import Individual
from structure.route import Route
from structure.node import Node
from movement.swap.swap_args import SwapArgs

class SwapMovement(Movement):

    def execute(self, args: SwapArgs):
        individual: Individual = self.individual
        route_i: Route = individual.routes[args.route_i]
        route_j: Route = individual.routes[args.route_j]

        node_list_i = route_i.node_list
        node_list_j = route_j.node_list

        i = args.index_i
        j = args.index_j
        delta = args.delta

        if delta is None:
            delta = self._calculate_delta(
                node_list_i, node_list_j, i, j, individual.instance.dist_matrix
            )

        individual.total_distance += delta

        # Swap nodes
        node_list_i[i], node_list_j[j] = node_list_j[j], node_list_i[i]
        
        demand_i = node_list_j[j].demand
        demand_j = node_list_i[i].demand
        demand_delta = demand_j - demand_i
        route_i.used_capacity += demand_delta
        route_j.used_capacity -= demand_delta

    def simulate(self, args: SwapArgs) -> int:
        individual: Individual = self.individual
        route_i = individual.routes[args.route_i]
        route_j = individual.routes[args.route_j]

        delta = self._calculate_delta(
            route_i.node_list,
            route_j.node_list,
            args.index_i,
            args.index_j,
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
        Compute distance delta for swapping node_list_i[i] with node_list_j[j].
        """

        node_i = node_list_i[i]
        node_j = node_list_j[j]

        # Neighbors of node_i
        prev_i = node_list_i[i - 1]
        next_i = node_list_i[i + 1] if i + 1 < len(node_list_i) else None

        # Neighbors of node_j
        prev_j = node_list_j[j - 1]
        next_j = node_list_j[j + 1] if j + 1 < len(node_list_j) else None

        delta = 0

        # --- Remove old edges (route i) ---
        delta -= dist_matrix[prev_i.index][node_i.index]
        if next_i:
            delta -= dist_matrix[node_i.index][next_i.index]
            delta += dist_matrix[prev_i.index][next_i.index]

        # --- Remove old edges (route j) ---
        delta -= dist_matrix[prev_j.index][node_j.index]
        if next_j:
            delta -= dist_matrix[node_j.index][next_j.index]
            delta += dist_matrix[prev_j.index][next_j.index]

        # --- Add new edges (node_j in route i) ---
        delta += dist_matrix[prev_i.index][node_j.index]
        if next_i:
            delta += dist_matrix[node_j.index][next_i.index]
            delta -= dist_matrix[prev_i.index][next_i.index]

        # --- Add new edges (node_i in route j) ---
        delta += dist_matrix[prev_j.index][node_i.index]
        if next_j:
            delta += dist_matrix[node_i.index][next_j.index]
            delta -= dist_matrix[prev_j.index][next_j.index]

        return delta
