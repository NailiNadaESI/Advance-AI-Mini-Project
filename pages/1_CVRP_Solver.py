import streamlit as st
from aco_solver import ACO, Graph
from utils import visualize_route_on_map
import numpy as np
import folium
from streamlit_folium import st_folium

# Check if configuration exists in session state
if "config" not in st.session_state or st.session_state["config"] is None:
    st.error("No problem configuration found. Please configure the problem in the Home page first.")
else:
    config = st.session_state["config"]

    # Get cities and depot data from the configuration
    cities = config["Cities"]
    depot = config["Depot"]
    demands = [0] + [city["Demand"] for city in cities]  # Demand for depot is 0
    locations = [(depot["Latitude"], depot["Longitude"])] + [(city["Latitude"], city["Longitude"]) for city in cities]
    
    # Create a distance matrix for the cities and depot
    distance_matrix = np.zeros((len(locations), len(locations)))
    for i in range(len(locations)):
        for j in range(len(locations)):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(np.array(locations[i]) - np.array(locations[j]))

    # Create the graph
    graph = Graph(distance_matrix, demands, config["Vehicles"]["Capacity"])

    # Sidebar ACO Parameters
    st.sidebar.header("ACO Parameters")
    num_ants = st.sidebar.slider("Number of Ants", 10, 100, 50)
    num_iterations = st.sidebar.slider("Number of Iterations", 10, 500, 100)
    alpha = st.sidebar.slider("Alpha (Pheromone Weight)", 0.1, 5.0, 1.0)
    beta = st.sidebar.slider("Beta (Distance Weight)", 0.1, 5.0, 2.0)
    evaporation_rate = st.sidebar.slider("Evaporation Rate", 0.01, 1.0, 0.1)

    aco = ACO(num_ants, num_iterations, alpha, beta, evaporation_rate)

    if st.button("Solve CVRP"):
        # Run ACO algorithm to solve the problem
        best_solution, best_cost = aco.solve(graph)

        # Store solution and cost in session state to persist across interactions
        st.session_state.best_solution = best_solution
        st.session_state.best_cost = best_cost

        # Display the solution's cost and details
        st.subheader("Best Solution")
        st.write(f"Best Cost: {best_cost}")
        for vehicle_idx, route in enumerate(best_solution):
            st.write(f"Vehicle {vehicle_idx + 1}: {route}")

    # If the best solution exists, visualize it on the map
    if "best_solution" in st.session_state:
        st.subheader("Visualize Routes on the Map")
        best_solution = st.session_state.best_solution
        best_cost = st.session_state.best_cost

        # Define a list of distinct colors for each vehicle
        color_palette = ["blue", "green", "red", "purple", "orange", "darkblue", "pink", "brown", "gray", "lightblue"]

        # Create the map, centered on the depot
        map_center = [depot["Latitude"], depot["Longitude"]]  # Center map on depot
        map = folium.Map(location=map_center, zoom_start=13)

        # Visualize depot
        folium.Marker(location=map_center, popup="Depot", icon=folium.Icon(color="red")).add_to(map)

        # Visualize cities
        for _, city in enumerate(cities):
            folium.Marker(
                location=[city["Latitude"], city["Longitude"]],
                popup=f"{city['City']} (Demand: {city['Demand']})",
                icon=folium.Icon(color="blue")
            ).add_to(map)

        # Visualize each vehicle's route on the map with a unique color
        for vehicle_idx, route in enumerate(best_solution):
            color = color_palette[vehicle_idx % len(color_palette)]  # Cycle through the color palette
            visualize_route_on_map(map, route, locations, color=color)

        # Display the map with the routes
        st_folium(map, width=700, height=500)
