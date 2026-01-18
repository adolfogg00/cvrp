from dataclasses import dataclass
from structure.node import Node

@dataclass
class InsertArgs:
    route_index: int     # target route
    insert_index: int    # position where node is inserted
    node: Node           # node to insert
    delta: int | None = None