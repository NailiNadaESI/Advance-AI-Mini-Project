import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Title
st.title("Capacitated Vehicle Routing Problem (CVRP) - Home")

# Initialize session state
if "cities_df" not in st.session_state:
    st.session_state["cities_df"] = None
if "config" not in st.session_state:
    st.session_state["config"] = None

# Sidebar for configuration
st.sidebar.header("Problem Configuration")

# Depot Input
st.sidebar.subheader("Depot")
depot_lat = st.sidebar.number_input("Depot Latitude", value=37.7749)
depot_lon = st.sidebar.number_input("Depot Longitude", value=-122.4194)

# Cities
num_cities = st.sidebar.slider("Number of Cities", 2, 20, 5)
manual_entry = st.sidebar.checkbox("Manual City Entry")

if st.sidebar.button("Generate Cities"):
    if manual_entry:
        city_data = []
        for i in range(num_cities):
            lat = st.sidebar.number_input(f"City {i+1} Latitude", value=37.77 + i * 0.01)
            lon = st.sidebar.number_input(f"City {i+1} Longitude", value=-122.42 - i * 0.01)
            demand = st.sidebar.number_input(f"City {i+1} Demand", value=2, min_value=1, max_value=10)
            city_data.append({"City": f"City {i+1}", "Latitude": lat, "Longitude": lon, "Demand": demand})
        st.session_state["cities_df"] = pd.DataFrame(city_data)
    else:
        st.session_state["cities_df"] = pd.DataFrame({
            "City": [f"City {i+1}" for i in range(num_cities)],
            "Latitude": np.random.uniform(depot_lat - 0.05, depot_lat + 0.05, num_cities),
            "Longitude": np.random.uniform(depot_lon - 0.05, depot_lon + 0.05, num_cities),
            "Demand": np.random.randint(1, 5, num_cities),
        })

# Vehicles
num_vehicles = st.sidebar.slider("Number of Vehicles", 1, 10, 3)
vehicle_capacity = st.sidebar.number_input("Vehicle Capacity", value=10)

# Display Summary
st.subheader("Problem Configuration")
st.write("### Depot")
st.write(f"Latitude: {depot_lat}, Longitude: {depot_lon}")
st.write("### Cities")
if st.session_state["cities_df"] is not None:
    st.dataframe(st.session_state["cities_df"])
else:
    st.write("No cities generated yet.")
st.write("### Vehicles")
st.write(f"Number of Vehicles: {num_vehicles}, Capacity: {vehicle_capacity}")

# Map Visualization
st.subheader("Map")
if st.session_state["cities_df"] is not None:
    map_center = [depot_lat, depot_lon]
    map = folium.Map(location=map_center, zoom_start=13)
    folium.Marker(location=map_center, popup="Depot", icon=folium.Icon(color="red")).add_to(map)

    for _, city in st.session_state["cities_df"].iterrows():
        folium.Marker(
            location=[city["Latitude"], city["Longitude"]],
            popup=f"{city['City']} (Demand: {city['Demand']})",
            icon=folium.Icon(color="blue"),
        ).add_to(map)

    st_folium(map, width=700, height=500)

# Save Configuration
st.subheader("Export Configuration")
if st.session_state["cities_df"] is not None:
    config = {
        "Depot": {"Latitude": depot_lat, "Longitude": depot_lon},
        "Cities": st.session_state["cities_df"].to_dict(orient="records"),
        "Vehicles": {"Number": num_vehicles, "Capacity": vehicle_capacity},
    }
    st.session_state["config"] = config
    st.download_button("Download Configuration as JSON", pd.io.json.dumps(config), file_name="cvrp_config.json")
