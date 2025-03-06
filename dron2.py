import pydeck as pdk
import numpy as np
import pandas as pd
import random
import datetime

FARM_CENTER = (5.984978, 80.392144)  

num_points = 3
random_latitudes = [FARM_CENTER[0] + random.uniform(-0.005, 0.005) for _ in range(num_points)]
random_longitudes = [FARM_CENTER[1] + random.uniform(-0.005, 0.005) for _ in range(num_points)]

drone_data = pd.DataFrame({
    "lat": random_latitudes,
    "lon": random_longitudes,
    "charge_level": [f"{random.randint(50, 100)}%" for _ in range(num_points)],
    "flight_time": [f"{random.randint(10, 30)} min" for _ in range(num_points)],
    "time_to_return": [f"{random.randint(5, 15)} min" for _ in range(num_points)],
    "pheromone_status": [random.choice(["Low", "Medium", "High"]) for _ in range(num_points)]
})

drone_data["tooltip"] = drone_data.apply(
    lambda row: f"""
    <div style='font-size: 16px; padding: 10px; line-height: 1.8;'>
        <b>Location:</b> {row['lat']:.5f}, {row['lon']:.5f}<br>
        <b>Charge Level:</b> {row['charge_level']}<br>
        <b>Flight Time:</b> {row['flight_time']}<br>
        <b>Time to Return:</b> {row['time_to_return']}<br>
        <b>Pheromone Status:</b> {row['pheromone_status']}
    </div>
    """,
    axis=1
)

hub_data = pd.DataFrame({
    "lat": [FARM_CENTER[0]],
    "lon": [FARM_CENTER[1]],
    "tooltip": ["Hub - Central Point"]
})

# Create DataFrame for bold lines from each point to the hub
lines_data = []
for lat, lon in zip(random_latitudes, random_longitudes):
    lines_data.append({"lat1": lat, "lon1": lon, "lat2": FARM_CENTER[0], "lon2": FARM_CENTER[1]})

lines_df = pd.DataFrame(lines_data)

# Create DataFrame for thin lines connecting scatter points
thin_lines_data = []
for i in range(num_points):
    for j in range(i + 1, num_points):
        thin_lines_data.append({
            "lat1": random_latitudes[i], "lon1": random_longitudes[i],
            "lat2": random_latitudes[j], "lon2": random_longitudes[j]
        })

thin_lines_df = pd.DataFrame(thin_lines_data)

# Scatterplot Layer for drone points (red) with tooltips
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=drone_data,
    get_position="[lon, lat]",
    get_color="[255, 0, 0, 200]",
    get_radius=30,
    pickable=True,
    tooltip=True,
    get_tooltip="tooltip"
)

# Scatterplot Layer for the hub (darker green)
hub_layer = pdk.Layer(
    "ScatterplotLayer",
    data=hub_data,
    get_position="[lon, lat]",
    get_color="[0, 150, 0, 255]",  # Darker green for the hub
    get_radius=50,
    pickable=True,
    tooltip=True,
    get_tooltip="tooltip"
)

# Line Layer for bold connections to the hub (black)
line_layer = pdk.Layer(
    "LineLayer",
    data=lines_df,
    get_source_position=["lon1", "lat1"],
    get_target_position=["lon2", "lat2"],
    get_color=[255, 255, 255, 255],  # Black color
    get_width=5
)

# Line Layer for thin connections between red points (gray)
thin_line_layer = pdk.Layer(
    "LineLayer",
    data=thin_lines_df,
    get_source_position=["lon1", "lat1"],
    get_target_position=["lon2", "lat2"],
    get_color=[100, 100, 100, 180],  # Gray color
    get_width=2
)

# Define the map's initial view state
view_state = pdk.ViewState(
    latitude=FARM_CENTER[0], longitude=FARM_CENTER[1], zoom=16, pitch=50
)

# Sidebar information
current_time = datetime.datetime.now().strftime("%I:%M %p")  # Current local time
weather_conditions = {
    "Wind Speed": "15 km/h",
    "Time of Day": current_time,
    "Season": "Maha (Major Harvest Season)",
    "Farm Area": "3.8 hectares",
    "Humidity": "80%"
}

# Generate improved sidebar HTML with increased width
sidebar_html = f"""
<div style="position: absolute; top: 10px; left: 10px; width: 280px; background: white; 
            padding: 15px; border-radius: 8px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2); 
            font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5;">
    <h3 style="margin: 0 0 10px; text-align: center;">Farm Data</h3>
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td><b>Wind Speed</b></td><td align="right">{weather_conditions["Wind Speed"]}</td></tr>
        <tr><td><b>Time of Day</b></td><td align="right">{weather_conditions["Time of Day"]}</td></tr>
        <tr><td><b>Season</b></td><td align="right">{weather_conditions["Season"]}</td></tr>
        <tr><td><b>Farm Area</b></td><td align="right">{weather_conditions["Farm Area"]}</td></tr>
        <tr><td><b>Humidity</b></td><td align="right">{weather_conditions["Humidity"]}</td></tr>
    </table>
</div>
"""

# Create the Deck object with dark mode map
deck = pdk.Deck(
    layers=[scatter_layer, hub_layer, line_layer, thin_line_layer],
    initial_view_state=view_state,
    map_style="dark",
    tooltip={"html": "{tooltip}"},
)

# Save the map to an HTML file with the sidebar
with open("farm_map_with_sidebar.html", "w") as f:
    f.write(deck.to_html(as_string=True) + sidebar_html)

print("Map has been saved as farm_map_with_sidebar.html")
