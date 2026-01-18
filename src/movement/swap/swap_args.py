from dataclasses import dataclass

@dataclass
class SwapArgs:
    route_i: int        # index of first route
    route_j: int        # index of second route
    index_i: int        # node index in route_i
    index_j: int        # node index in route_j
    delta: int | None = None