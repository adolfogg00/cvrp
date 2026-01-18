from dataclasses import dataclass

@dataclass
class TwoOptArgs:
    route_index : int
    i : int
    j : int
    delta: int | None = None