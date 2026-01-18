from pathlib import Path
from typing import Dict
from readers.matrix_reader import MatrixReader
from structure.node import Node
from structure.instance import Instance


from pathlib import Path


class InstanceReader:

    def __init__(self, instances_path: Path | str | None = None):
        """
        Parameters
        ----------
        instances_path : Path | str | None
            Path to the 'instances' directory.
            Can be absolute or relative.
            If None, defaults to '<project_root>/instances'.
        """

        if instances_path is None:
            # Default: project_root / instances
            self.instances_path = (
                Path(__file__).resolve().parents[2] / "instances"
            )
        else:
            instances_path = Path(instances_path)

            # If relative, interpret it from the CURRENT WORKING DIRECTORY
            if not instances_path.is_absolute():
                instances_path = Path.cwd() / instances_path

            self.instances_path = instances_path.resolve()

        if not self.instances_path.exists():
            raise FileNotFoundError(
                f"Instances directory not found: {self.instances_path}"
            )

    def read(self, family: str, instance_name: str) -> Instance:
        file_path = (
            self.instances_path
            / family
            / family
            / f"{instance_name}.vrp"
        )

        if not file_path.exists():
            raise FileNotFoundError(f"Instance file not found: {file_path}")

        capacity = None
        coords: Dict[int, tuple[int, int]] = {}
        demands: Dict[int, int] = {}
        depot_id = None
        section = None
        with file_path.open("r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("CAPACITY"):
                    capacity = int(line.split(":")[1])

                elif line == "NODE_COORD_SECTION":
                    section = "coords"

                elif line == "DEMAND_SECTION":
                    section = "demands"

                elif line == "DEPOT_SECTION":
                    section = "depot"

                elif line == "EOF":
                    break

                elif section == "coords":
                    i, x, y = map(int, line.split())
                    coords[i] = (x, y)

                elif section == "demands":
                    i, d = map(int, line.split())
                    demands[i] = d

                elif section == "depot":
                    value = int(line)
                    if value == -1:
                        break
                    depot_id = value

        if capacity is None or depot_id is None:
            raise ValueError("Invalid CVRP instance format")
        depot = Node(depot_id, *coords[depot_id], demands[depot_id])

        nodes = [
            Node(i, coords[i][0], coords[i][1], demands[i])
            for i in sorted(coords)
            if i != depot_id
        ]

        dist_matrix = MatrixReader.read(depot=depot, nodes=nodes)
        return Instance(depot=depot, nodes=nodes, capacity=capacity, dist_matrix=dist_matrix)
