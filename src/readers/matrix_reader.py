import math
from typing import List

import numpy as np

from structure.node import Node


class MatrixReader:
    """
    Builds an EUC_2D distance matrix from a depot and a list of nodes.
    Index 0 is the depot, indices 1..n are customers.
    """

    @staticmethod
    def read(depot: Node, nodes: List[Node]) -> np.ndarray:
        """
        Parameters
        ----------
        depot : Node
        nodes : List[Node]

        Returns
        -------
        np.ndarray
            (n+1) x (n+1) integer distance matrix
        """

        all_nodes = [depot] + nodes
        n = len(all_nodes)

        matrix = np.zeros((n, n), dtype=int)

        for i in range(n):
            xi, yi = all_nodes[i].x, all_nodes[i].y
            for j in range(n):
                xj, yj = all_nodes[j].x, all_nodes[j].y
                dx = xi - xj
                dy = yi - yj
                dist = math.sqrt(dx * dx + dy * dy)
                matrix[i, j] = int(dist + 0.5)

        return matrix

