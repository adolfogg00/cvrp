from dataclasses import dataclass

@dataclass
class RemoveArgs:
    route_index: int     # route from which node is removed
    remove_index: int    # index of node to remove
    delta: int | None = None
