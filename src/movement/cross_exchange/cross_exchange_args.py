from dataclasses import dataclass

@dataclass
class CrossExchangeArgs:
    route_i: int
    route_j: int
    i_start: int
    i_end: int
    j_start: int
    j_end: int
    delta: int | None = None
