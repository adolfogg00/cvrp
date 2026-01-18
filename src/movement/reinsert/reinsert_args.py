from dataclasses import dataclass

@dataclass
class ReinsertArgs:
    from_route: int    # index of the route to remove the node from
    to_route: int      # index of the route to insert into
    node_index: int    # index of the node in from_route.node_list
    insert_after: int  # index in to_route.node_list after which to insert
    delta: int | None = None