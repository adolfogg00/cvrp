from opt_flow.movement import Movement
from typing import List
from structure.route import Route
from structure.node import Node
from structure.individual import Individual
from movement.or_opt.or_opt_args import OROptArgs

class OROptMovement(Movement):

    def execute(self, args: OROptArgs):
        individual: Individual = self.individual
        route: Route = individual.routes[args.route_index]

        node_list = route.node_list
        i = args.i
        j = args.j
        length = args.length
        delta = args.delta

        if delta is None:
            delta = self._calculate_delta(node_list, i, length, j, individual.instance.dist_matrix)

        # Update total distance
        individual.total_distance += delta

        # Extract the segment
        segment = node_list[i:i+length]

        # Remove the segment
        del node_list[i:i+length]

        # Adjust insertion index if segment was removed before insertion point
        if j >= i:
            j -= length

        # Insert segment after node j
        node_list[j+1:j+1] = segment

    def simulate(self, args: OROptArgs) -> int:
        individual: Individual = self.individual
        route: Route = individual.routes[args.route_index]
        delta = self._calculate_delta(route.node_list, args.i, args.length, args.j, individual.instance.dist_matrix)
        args.delta = delta
        return delta

    def _calculate_delta(self, node_list: List[Node], i: int, length: int, j: int, dist_matrix) -> int:
        """
        Compute the change in total distance for moving a segment [i:i+length] 
        to after position j in the same route.
        """

        n = len(node_list)
        segment_start = node_list[i]
        segment_end = node_list[i + length - 1]

        # Nodes immediately before and after the segment
        before_seg = node_list[i - 1]
        after_seg = node_list[i + length] if (i + length) < n else None

        # Node after insertion point
        after_insert = node_list[j + 1] if (j + 1) < n else None
        insert_node = node_list[j]

        delta = 0

        # Remove old edges
        delta -= dist_matrix[before_seg.index][segment_start.index]
        if after_seg:
            delta -= dist_matrix[segment_end.index][after_seg.index]

        # Add new edges
        delta += dist_matrix[before_seg.index][after_seg.index] if after_seg else 0
        delta += dist_matrix[insert_node.index][segment_start.index]
        if after_insert:
            delta += dist_matrix[segment_end.index][after_insert.index]

        return delta
