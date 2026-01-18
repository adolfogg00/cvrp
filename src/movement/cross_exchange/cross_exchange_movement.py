from opt_flow.movement import Movement
from structure.individual import Individual
from structure.node import Node
from typing import List
from movement.cross_exchange.cross_exchange_args import CrossExchangeArgs

class CrossExchangeMovement(Movement):

    def execute(self, args: CrossExchangeArgs):
        individual: Individual = self.individual

        route_i = individual.routes[args.route_i]
        route_j = individual.routes[args.route_j]

        nodes_i = route_i.node_list
        nodes_j = route_j.node_list

        delta = args.delta
        if delta is None:
            delta = self._calculate_delta(
                nodes_i, nodes_j,
                args.i_start, args.i_end,
                args.j_start, args.j_end,
                individual.instance.dist_matrix
            )

        individual.total_distance += delta

        # Extract segments
        seg_i = nodes_i[args.i_start : args.i_end + 1]
        seg_j = nodes_j[args.j_start : args.j_end + 1]

        # Replace segments
        nodes_i[args.i_start : args.i_end + 1] = seg_j
        nodes_j[args.j_start : args.j_end + 1] = seg_i
        
        route_i.used_capacity += sum(node.demand for node in seg_j) - sum(node.demand for node in seg_i)
        route_j.used_capacity += sum(node.demand for node in seg_i) - sum(node.demand for node in seg_j)

    def simulate(self, args: CrossExchangeArgs) -> int:
        individual: Individual = self.individual

        delta = self._calculate_delta(
            individual.routes[args.route_i].node_list,
            individual.routes[args.route_j].node_list,
            args.i_start, args.i_end,
            args.j_start, args.j_end,
            individual.instance.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(
        self,
        nodes_i: List[Node],
        nodes_j: List[Node],
        i_start: int,
        i_end: int,
        j_start: int,
        j_end: int,
        dist_matrix
    ) -> int:
        """
        O(1) delta computation for cross exchange.
        """

        # Route i boundary nodes
        a = nodes_i[i_start - 1]
        b = nodes_i[i_start]
        c = nodes_i[i_end]
        d = nodes_i[i_end + 1] if i_end + 1 < len(nodes_i) else nodes_i[0]

        # Route j boundary nodes
        e = nodes_j[j_start - 1]
        f = nodes_j[j_start]
        g = nodes_j[j_end]
        h = nodes_j[j_end + 1] if j_end + 1 < len(nodes_j) else nodes_j[0]

        delta = 0

        # Remove old edges
        delta -= dist_matrix[a.index][b.index]
        delta -= dist_matrix[c.index][d.index]
        delta -= dist_matrix[e.index][f.index]
        delta -= dist_matrix[g.index][h.index]

        # Add new edges
        delta += dist_matrix[a.index][f.index]
        delta += dist_matrix[g.index][d.index]
        delta += dist_matrix[e.index][b.index]
        delta += dist_matrix[c.index][h.index]

        return delta
