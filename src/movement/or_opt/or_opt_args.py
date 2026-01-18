from dataclasses import dataclass

@dataclass
class OROptArgs:
    route_index: int    # route where the segment is moved
    i: int              # start index of the segment to move
    length: int         # length of the segment
    j: int              # insertion index (after this node)
    delta: int | None = None  # optional precomputed delta