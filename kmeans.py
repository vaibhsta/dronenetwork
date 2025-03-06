import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from scipy.interpolate import griddata


size = 50  
x, y = np.meshgrid(np.linspace(0, size, size), np.linspace(0, size, size))

release_points = [(25, 25), (10, 40)]  

wind_x, wind_y = 0.5, -0.2 
wind_influence = np.sqrt(wind_x**2 + wind_y**2)

pheromone_name = "Ferrugineol"
decay_factor = 0.05 

def pheromone_dispersion(t):
    """Simulate pheromone dispersion at time step t."""
    concentration = np.zeros_like(x)
    
    for (x0, y0) in release_points:
        # Dynamic spread with wind influence
        spread_x = 5 + 0.2 * t  # Increasing spread over time
        spread_y = 5 + 0.2 * t
        mean = [x0 + wind_x * t, y0 + wind_y * t]  # Shift due to wind
        cov = [[spread_x**2, 0], [0, spread_y**2]]  # Covariance matrix (spread)
        rv = multivariate_normal(mean, cov)
        concentration += rv.pdf(np.dstack((x, y))) * np.exp(-decay_factor * t)  # Decay over time
    
    return concentration, spread_x

# Set initial time step
initial_time = 30  # Adjusted so it's visible
concentration, dispersion_radius = pheromone_dispersion(initial_time)

# Identify low-pheromone concentration areas for additional dispensing
num_samples = 500
latitudes = np.random.uniform(10, 20, num_samples)
longitudes = np.random.uniform(30, 40, num_samples)
wind_speed = np.random.uniform(0, 10, num_samples)
humidity = np.random.uniform(20, 100, num_samples)
pheromone_concentration = (100 * np.exp(-0.1 * wind_speed) * (humidity / 100))

X = np.column_stack((latitudes, longitudes, pheromone_concentration))
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Create a grid for heatmap overlay
grid_lat = np.linspace(latitudes.min(), latitudes.max(), 100)
grid_lon = np.linspace(longitudes.min(), longitudes.max(), 100)
grid_lat, grid_lon = np.meshgrid(grid_lat, grid_lon)
grid_concentration = griddata((latitudes, longitudes), pheromone_concentration, (grid_lat, grid_lon), method='cubic')

# 3D Visualisation setup
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Latitude")
ax.set_ylabel("Longitude")
ax.set_zlabel("Pheromone Concentration")
ax.set_title(f"3D Dispersion of {pheromone_name} with Low-Concentration Overlay")

# Heatmap overlay (surface plot)
ax.plot_surface(grid_lat, grid_lon, grid_concentration, cmap='hot', alpha=0.4)

# Scatter plot with cluster labels
ax.scatter(latitudes, longitudes, pheromone_concentration, c=clusters, cmap='viridis', s=50, alpha=0.6)
ax.scatter(*zip(*release_points), 0, color='red', marker='o', s=100, label="Pheromone Release Points")

# Add a low concentration point (example: where pheromone is dispersed but decayed)
low_concentration_point = (18, 35)  # Example location of low concentration
low_concentration_value = np.min(grid_concentration)  # Take minimum concentration value as an example

# Mark the low-concentration point
ax.scatter(low_concentration_point[0], low_concentration_point[1], low_concentration_value, 
           color='blue', marker='x', s=150, label="Low Concentration Point")

# Annotations
ax.text(5, 5, np.max(concentration), f"Decay Factor: {decay_factor}", color='white')
ax.text(10, 5, np.max(concentration) * 0.8, f"Wind Influence: {wind_influence}", color='white')
ax.text(15, 5, np.max(concentration) * 0.6, f"Dispersion Radius: {dispersion_radius:.2f}", color='white')
ax.legend()

plt.show()
