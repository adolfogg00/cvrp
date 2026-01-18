from pathlib import Path
from structure.individual import Individual
from datetime import datetime
import json


class RouteWriter:
    """
    Writes CVRP solutions in CVRPLib format.
    Creates output folder structure: output/<instance_name>/
    """
    
    def __init__(self, output_base_path: Path | str | None = None):
        """
        Parameters
        ----------
        output_base_path : Path | str | None
            Path to the base output directory.
            If None, defaults to '<project_root>/output'.
        """
        if output_base_path is None:
            self.output_base_path = (
                Path(__file__).resolve().parents[2] / "output"
            )
        else:
            output_base_path = Path(output_base_path)
            if not output_base_path.is_absolute():
                output_base_path = Path.cwd() / output_base_path
            self.output_base_path = output_base_path.resolve()
        
        # Create base output directory if it doesn't exist
        self.output_base_path.mkdir(parents=True, exist_ok=True)
    
    def write(self, individual: Individual, instance_name: str, 
              algorithm_name: str = "unknown_algorithm") -> Path:
        """
        Write solution to file in CVRPLib format.
        
        Parameters
        ----------
        individual : Individual
            The solution to write
        instance_name : str
            Name of the instance (e.g., 'A-n32-k5')
        algorithm_name : str
            Name of the algorithm used
            
        Returns
        -------
        Path
            Path to the written solution file
        """
        # Create instance-specific output directory
        instance_output_dir = self.output_base_path / instance_name
        instance_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{instance_name}_{algorithm_name}_{timestamp}.sol"
        file_path = instance_output_dir / filename
        
        # Prepare solution data
        solution_data = []
        route_number = 1
        
        for route in individual.routes:
            # Skip empty routes (only depot)
            if len(route.node_list) <= 1:
                continue
                
            # Get customer node IDs (exclude depot)
            customer_ids = []
            for node in route.node_list[1:]:  # Skip depot
                customer_ids.append(str(node.index))
            
            if customer_ids:  # Only add non-empty routes
                solution_data.append(f"Route #{route_number}: {' '.join(customer_ids)}")
                route_number += 1
        
        # Add summary information
        total_distance = individual.total_distance
        num_routes = route_number - 1
        used_capacity = sum(route.used_capacity for route in individual.routes)
        
        summary = [
            f"Cost {total_distance}",
            f"Routes {num_routes}",
            f"Used capacity {used_capacity}",
            f"Algorithm {algorithm_name}",
            f"Timestamp {timestamp}"
        ]
        
        # Write to file
        with file_path.open('w') as f:
            f.write('\n'.join(solution_data + summary))
        
        print(f"Solution written to: {file_path}")
        return file_path
    
    def write_json(self, individual: Individual, instance_name: str,
                   algorithm_name: str = "unknown_algorithm") -> Path:
        """
        Write solution to JSON file with detailed information.
        
        Returns
        -------
        Path
            Path to the written JSON file
        """
        # Create instance-specific output directory
        instance_output_dir = self.output_base_path / instance_name
        instance_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{instance_name}_{algorithm_name}_{timestamp}.json"
        file_path = instance_output_dir / filename
        
        # Prepare solution data
        routes_data = []
        total_demand = 0
        
        for route_idx, route in enumerate(individual.routes, 1):
            # Get all nodes in route (including depot)
            nodes_data = []
            route_demand = 0
            
            for node in route.node_list:
                node_data = {
                    "id": node.index,
                    "x": node.x,
                    "y": node.y,
                    "demand": node.demand,
                    "is_depot": (node.index == individual.instance.depot.index)
                }
                nodes_data.append(node_data)
                route_demand += node.demand
            
            route_data = {
                "route_id": route_idx,
                "nodes": nodes_data,
                "used_capacity": route.used_capacity,
                "num_customers": len(route.node_list) - 1,  # Exclude depot
                "total_demand": route_demand
            }
            routes_data.append(route_data)
            total_demand += route_demand
        
        # Compile full solution data
        solution_data = {
            "instance": instance_name,
            "algorithm": algorithm_name,
            "timestamp": timestamp,
            "total_distance": individual.total_distance,
            "num_routes": len(individual.routes),
            "total_demand": total_demand,
            "vehicle_capacity": individual.instance.capacity,
            "depot": {
                "id": individual.instance.depot.index,
                "x": individual.instance.depot.x,
                "y": individual.instance.depot.y
            },
            "routes": routes_data,
            "metadata": {
                "execution_time": getattr(individual, 'execution_time', None),
                "iterations": getattr(individual, 'iterations', None),
                "best_iteration": getattr(individual, 'best_iteration', None)
            }
        }
        
        # Write to JSON file
        with file_path.open('w') as f:
            json.dump(solution_data, f, indent=2, default=str)
        
        print(f"JSON solution written to: {file_path}")
        return file_path