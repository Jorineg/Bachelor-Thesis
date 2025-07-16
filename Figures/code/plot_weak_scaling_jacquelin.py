import matplotlib.pyplot as plt
import numpy as np
from colors import blue

# Data from the table
data = {
    'nx': [200, 400, 600, 755, 755, 755, 755, 755],
    'ny': [200, 400, 600, 500, 600, 900, 990, 994],
    'nz': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    'Throughput': [533.64, 2097.60, 4731.53, 4956.17, 5945.40, 8922.08, 9782.14, 9862.78],
}

# Calculate the number of grid points
grid_points = [nx * ny for nx, ny in zip(data['nx'], data['ny'])]

# Calculate the ideal throughput based on the first data point
ideal_throughput_scaling = [(gp / grid_points[0]) * data['Throughput'][0] for gp in grid_points]

# Calculate weak scaling efficiency in %
weak_scaling = [(data['Throughput'][i] / ideal_throughput_scaling[i]) * 100 for i in range(len(data['Throughput']))]

# Create x-tick labels
x_labels = [f"{nx}x{ny}" for nx, ny in zip(data['nx'], data['ny'])]

# Remove the second-to-last label (755x990) for better spacing
x_labels_filtered = x_labels.copy()
x_labels_filtered[-2] = ""  # Remove second-to-last label

# Create plot
plt.figure(figsize=(10, 6))

plt.plot(grid_points, weak_scaling, marker='o', linestyle='-', color=blue, label='WSE2 scaling')

# Set plot labels and title
plt.xlabel("X*Y size [grid points]")
plt.ylabel("Weak scaling, fixed Z dimension, [% ideal scaling]")
plt.title("Weak scaling experiments by Jacquelin et al.")
plt.ylim(95, 102)
plt.xticks(grid_points, x_labels_filtered, rotation=45)

# Add grid
plt.grid(True, which='both', linestyle=':', linewidth=0.5)
plt.legend()

# Save the figure
plt.savefig('weak_scaling_jacquelin.png', bbox_inches='tight', dpi=300)

# plt.show()
