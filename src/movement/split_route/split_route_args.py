from dataclasses import dataclass

@dataclass
class SplitRouteArgs:
    route_index: int   # route to split
    split_index: int   # index of first node in new route
    delta: int | None = None