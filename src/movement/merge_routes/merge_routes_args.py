from dataclasses import dataclass

@dataclass
class MergeRoutesArgs:
    route_i: int      # index of the route that will remain
    route_j: int      # index of the route that will be merged and removed
    delta: int | None = None