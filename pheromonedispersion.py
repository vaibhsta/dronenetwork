import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D

# Define grid size
size = 50  # Grid size (50x50 area)
x, y = np.meshgrid(np.linspace(0, size, size), np.linspace(0, size, size))

# Define pheromone release points
release_points = [(25, 25), (10, 40)]  # (x, y) coordinates

# Define wind influence (directional bias)
wind_x, wind_y = 0.5, -0.2  # Wind influence factors
wind_influence = np.sqrt(wind_x**2 + wind_y**2)

# Pheromone properties
pheromone_name = "Ferrugineol"
decay_factor = 0.05  # Rate of pheromone decay

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

# 3D Visualization setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Latitudunal Coordinate (in cm)")
ax.set_ylabel("Longitudinal Coordinate (in cm)")
ax.set_zlabel("Pheromone Concentration")
ax.set_title(f"3D Dispersion of {pheromone_name}")

# Set initial time step
initial_time = 30  # Adjusted so it's visible
concentration, dispersion_radius = pheromone_dispersion(initial_time)
ax.plot_surface(x, y, concentration, cmap='plasma', edgecolor='none', alpha=0.6)  # Adjusted transparency
ax.contourf(x, y, concentration, zdir='z', offset=0, cmap='plasma', alpha=0.5)  # 2D projection for a gas-like effect
ax.scatter(*zip(*release_points), 0, color='red', marker='o', s=50, label="Release Points")

# Annotations
ax.text(5, 5, np.max(concentration), f"Decay Factor: {decay_factor}", color='black')
ax.text(10, 5, np.max(concentration) * 0.8, f"Wind Influence: {wind_influence}", color='black')
ax.text(15, 5, np.max(concentration) * 0.6, f"Dispersion Radius: {dispersion_radius:.2f}", color='black')
ax.legend()

plt.show()
