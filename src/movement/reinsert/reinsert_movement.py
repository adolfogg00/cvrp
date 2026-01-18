from typing import List
from opt_flow.movement import Movement
from structure.individual import Individual
from structure.route import Route
from structure.node import Node
from movement.reinsert.reinsert_args import ReinsertArgs

class ReinsertMovement(Movement):

    def execute(self, args: ReinsertArgs):
        individual: Individual = self.individual
        from_route: Route = individual.routes[args.from_route]
        to_route: Route = individual.routes[args.to_route]

        node_list_from = from_route.node_list
        node_list_to = to_route.node_list

        i = args.node_index
        j = args.insert_after
        delta = args.delta

        if delta is None:
            delta = self._calculate_delta(node_list_from, node_list_to, i, j, individual.instance.dist_matrix)

        # Update total distance
        individual.total_distance += delta

        # Remove node
        node = node_list_from.pop(i)
        
        demand = node.demand
        from_route.used_capacity -= demand
        to_route.used_capacity += demand

        # Adjust insertion index if moving within the same route and before insertion
        if from_route == to_route and j >= i:
            j -= 1

        # Insert node
        node_list_to.insert(j + 1, node)

    def simulate(self, args: ReinsertArgs) -> int:
        individual: Individual = self.individual
        from_route: Route = individual.routes[args.from_route]
        to_route: Route = individual.routes[args.to_route]

        delta = self._calculate_delta(
            from_route.node_list,
            to_route.node_list,
            args.node_index,
            args.insert_after,
            individual.instance.dist_matrix
        )
        args.delta = delta
        return delta

    def _calculate_delta(
        self,
        node_list_from: List[Node],
        node_list_to: List[Node],
        i: int,
        j: int,
        dist_matrix
    ) -> int:
        """
        Compute change in distance when removing node i from node_list_from and inserting
        it after node j in node_list_to.
        """

        node = node_list_from[i]

        # Neighbors in from_route
        before = node_list_from[i - 1]
        after = node_list_from[i + 1] if (i + 1) < len(node_list_from) else None

        delta = 0

        # Remove edges in from_route
        delta -= dist_matrix[before.index][node.index]
        if after:
            delta -= dist_matrix[node.index][after.index]
            delta += dist_matrix[before.index][after.index]
        # else: node was last, only remove edge before

        # Add edges in to_route
        insert_after_node = node_list_to[j]
        insert_after_next = node_list_to[j + 1] if (j + 1) < len(node_list_to) else None

        delta += dist_matrix[insert_after_node.index][node.index]
        if insert_after_next:
            delta += dist_matrix[node.index][insert_after_next.index]
            delta -= dist_matrix[insert_after_node.index][insert_after_next.index]

        return delta
