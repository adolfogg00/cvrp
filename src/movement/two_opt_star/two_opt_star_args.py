from dataclasses import dataclass

@dataclass
class TwoOptStarArgs:
    route_i: int
    route_j: int
    i: int           # cut index in route_i
    j: int           # cut index in route_j
    delta: int | None = None
