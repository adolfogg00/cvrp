from pathlib import Path
import folium
from folium import plugins
from typing import List, Optional
from structure.individual import Individual


class MapVisualizer:
    """
    Creates interactive HTML maps of CVRP solutions using folium.
    """
    
    def __init__(self, output_base_path: Path | str | None = None):
        """
        Parameters
        ----------
        output_base_path : Path | str | None
            Path to the base output directory for maps.
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
    
    def create_map(self, individual: Individual, instance_name: str,
                   algorithm_name: str = "unknown_algorithm",
                   center_on_depot: bool = True) -> Path:
        """
        Create an interactive HTML map of the solution.
        
        Parameters
        ----------
        individual : Individual
            The solution to visualize
        instance_name : str
            Name of the instance
        algorithm_name : str
            Name of the algorithm used
        center_on_depot : bool
            Whether to center the map on the depot
            
        Returns
        -------
        Path
            Path to the created HTML file
        """
        # Create instance-specific output directory
        instance_output_dir = self.output_base_path / instance_name
        instance_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{instance_name}_{algorithm_name}_{timestamp}.html"
        file_path = instance_output_dir / filename
        
        # Determine map center
        depot = individual.instance.depot
        if center_on_depot:
            center = [depot.y, depot.x]  # folium uses [lat, lon] = [y, x]
        else:
            # Calculate centroid of all nodes
            all_nodes = individual.instance.nodes
            avg_x = sum(node.x for node in all_nodes) / len(all_nodes)
            avg_y = sum(node.y for node in all_nodes) / len(all_nodes)
            center = [avg_y, avg_x]
        
        # Create map
        m = folium.Map(
            location=center,
            zoom_start=13,
            tiles='CartoDB positron',  # Clean, light tiles
            control_scale=True
        )
        
        # Add fullscreen button
        plugins.Fullscreen().add_to(m)
        
        # Create color map for routes
        num_routes = len(individual.routes)
        colors = self._generate_colors(num_routes)
        
        # Add routes to map
        for idx, route in enumerate(individual.routes):
            route_color = colors[idx]
            
            # Get coordinates for this route (including return to depot)
            coordinates = []
            for node in route.node_list:
                coordinates.append([node.y, node.x])  # [lat, lon]
            
            # Add route line
            folium.PolyLine(
                locations=coordinates,
                color=route_color,
                weight=3,
                opacity=0.8,
                popup=f"Route {idx + 1}<br>"
                      f"Customers: {len(route.node_list) - 1}<br>"
                      f"Capacity used: {route.used_capacity}/{individual.instance.capacity}",
                tooltip=f"Route {idx + 1}"
            ).add_to(m)
            
            # Add nodes for this route
            for node_idx, node in enumerate(route.node_list):
                is_depot = (node.index == depot.index)
                
                # Determine node color and size
                if is_depot:
                    node_color = 'black'
                    node_size = 10
                    node_icon = 'star'
                else:
                    node_color = route_color
                    node_size = 8
                    node_icon = 'circle'
                
                # Create popup content
                popup_content = f"""
                <b>{'Depot' if is_depot else f'Customer {node.index}'}</b><br>
                ID: {node.index}<br>
                Demand: {node.demand}<br>
                Position: ({node.x}, {node.y})<br>
                Route: {idx + 1}<br>
                Position in route: {node_idx}
                """
                
                # Add marker
                folium.Marker(
                    location=[node.y, node.x],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=f"{'Depot' if is_depot else f'Customer {node.index}'}",
                    icon=folium.Icon(
                        color=node_color,
                        icon=node_icon,
                        prefix='fa' if is_depot else None,
                        icon_color='white' if is_depot else 'black'
                    ),
                    radius=node_size
                ).add_to(m)
        
        # Add legend
        self._add_legend(m, colors, num_routes, individual.total_distance)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save map
        m.save(str(file_path))
        print(f"Map saved to: {file_path}")
        
        return file_path
    
    def create_comparison_map(self, individuals: List[Individual],
                              instance_name: str,
                              algorithm_names: List[str],
                              titles: Optional[List[str]] = None) -> Path:
        """
        Create a comparison map with multiple solutions side by side.
        
        Parameters
        ----------
        individuals : List[Individual]
            List of solutions to compare
        instance_name : str
            Name of the instance
        algorithm_names : List[str]
            Names of the algorithms used
        titles : List[str], optional
            Custom titles for each map
            
        Returns
        -------
        Path
            Path to the created HTML file
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{instance_name}_comparison_{timestamp}.html"
        file_path = self.output_base_path / instance_name / filename
        
        # Calculate bounds for all solutions
        all_nodes = []
        for ind in individuals:
            all_nodes.extend(ind.instance.nodes)
        
        min_x = min(node.x for node in all_nodes)
        max_x = max(node.x for node in all_nodes)
        min_y = min(node.y for node in all_nodes)
        max_y = max(node.y for node in all_nodes)
        
        # Create map with bounds
        center_y = (min_y + max_y) / 2
        center_x = (min_x + max_x) / 2
        
        m = folium.Map(
            location=[center_y, center_x],
            zoom_start=12,
            tiles='CartoDB positron'
        )
        
        # Fit bounds to cover all nodes
        m.fit_bounds([[min_y, min_x], [max_y, max_x]])
        
        # Create feature groups for each solution
        for idx, (individual, algo_name) in enumerate(zip(individuals, algorithm_names)):
            fg = folium.FeatureGroup(
                name=f"{algo_name} (Cost: {individual.total_distance})",
                show=(idx == 0)  # Show first solution by default
            )
            
            # Add routes for this solution
            colors = self._generate_colors(len(individual.routes))
            
            for route_idx, route in enumerate(individual.routes):
                route_color = colors[route_idx]
                
                # Get coordinates
                coordinates = [[node.y, node.x] for node in route.node_list]
                
                folium.PolyLine(
                    locations=coordinates,
                    color=route_color,
                    weight=2,
                    opacity=0.7,
                    popup=f"{algo_name} - Route {route_idx + 1}"
                ).add_to(fg)
            
            fg.add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Add title
        title_html = f"""
        <h3 align="center" style="font-size:16px">
            {instance_name} - Solution Comparison
        </h3>
        """
        m.get_root().html.add_child(folium.Element(title_html))
        
        m.save(str(file_path))
        print(f"Comparison map saved to: {file_path}")
        return file_path
    
    def _generate_colors(self, num_colors: int) -> List[str]:
        """Generate distinct colors for routes."""
        # Use colorbrewer qualitative palette
        color_sets = [
            ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
             '#ffff33', '#a65628', '#f781bf', '#999999'],
            ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
             '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6'],
            ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3',
             '#fdb462', '#b3de69', '#fccde5', '#d9d9d9']
        ]
        
        colors = []
        for i in range(num_colors):
            colors.append(color_sets[i % len(color_sets)][i // len(color_sets) % 9])
        
        return colors
    
    def _add_legend(self, m: folium.Map, colors: List[str],
                    num_routes: int, total_distance: int):
        """Add a legend to the map."""
        from branca.element import Template, MacroElement
        
        # Create legend HTML
        legend_html = f"""
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 250px; 
                    border:2px solid grey; z-index:9999; 
                    font-size:14px; background-color:white;
                    padding: 10px; border-radius: 5px;">
            <h4 style="margin-top:0; margin-bottom:10px;">
                Solution Overview
            </h4>
            <p><b>Total Distance:</b> {total_distance}</p>
            <p><b>Number of Routes:</b> {num_routes}</p>
            <hr style="margin: 10px 0;">
            <p><b>Route Colors:</b></p>
        """
        
        # Add color boxes for each route
        for i, color in enumerate(colors[:min(10, num_routes)]):
            legend_html += f"""
            <div style="margin: 2px 0;">
                <span style="display:inline-block; 
                             width:15px; height:15px; 
                             background-color:{color};
                             margin-right:5px; border:1px solid #666;">
                </span>
                Route {i + 1}
            </div>
            """
        
        if num_routes > 10:
            legend_html += f"<p>... and {num_routes - 10} more routes</p>"
        
        legend_html += """
            <hr style="margin: 10px 0;">
            <p style="font-size:12px; color:#666;">
                • Black star: Depot<br>
                • Colored circles: Customers<br>
                • Click markers for details<br>
                • Toggle layers in top-right
            </p>
        </div>
        """
        
        # Add legend to map
        m.get_root().html.add_child(folium.Element(legend_html))