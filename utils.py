import numpy as np
import folium
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate Euclidean distance between two geographical points.
    
    Args:
    - lat1, lon1: Latitude and Longitude of the first point.
    - lat2, lon2: Latitude and Longitude of the second point.
    
    Returns:
    - distance: Euclidean distance between the two points.
    """
    return np.linalg.norm([lat2 - lat1, lon2 - lon1])

def create_distance_matrix(locations):
    """
    Create a distance matrix from a list of locations.
    
    Args:
    - locations: List of (latitude, longitude) tuples for each city and depot.
    
    Returns:
    - distance_matrix: A square matrix with distances between all locations.
    """
    n = len(locations)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = calculate_distance(locations[i][0], locations[i][1], locations[j][0], locations[j][1])
    return distance_matrix

def validate_config(config):
    """
    Validate the configuration dictionary.
    
    Args:
    - config: The configuration dictionary with depot, cities, and vehicles information.
    
    Returns:
    - is_valid: Boolean value indicating if the configuration is valid.
    """
    if not config:
        return False
    
    # Ensure the config has all necessary keys
    required_keys = ["Depot", "Cities", "Vehicles"]
    for key in required_keys:
        if key not in config:
            return False

    # Ensure all cities have latitude, longitude, and demand
    for city in config["Cities"]:
        if not all(k in city for k in ["City", "Latitude", "Longitude", "Demand"]):
            return False

    # Check vehicle capacity and number of vehicles
    if "Capacity" not in config["Vehicles"] or "Number" not in config["Vehicles"]:
        return False
    if config["Vehicles"]["Capacity"] <= 0 or config["Vehicles"]["Number"] <= 0:
        return False

    return True

def visualize_route_on_map(map, route, locations, color="blue"):
    """
    Visualize a single vehicle route on the map.
    
    Args:
    - map: The Folium map object.
    - route: A list of city indices representing the route.
    - locations: List of (latitude, longitude) tuples for each city and depot.
    - color: Color for the route (default is blue).
    """
    for i in range(len(route) - 1):
        start_location = locations[route[i]]
        end_location = locations[route[i + 1]]
        folium.PolyLine(
            locations=[start_location, end_location],
            color=color,
            weight=4
        ).add_to(map)
