import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from colors import blue, green

# Data from the benchmark results

# Experiment: Grid 3x3, Radius 1
iterations_3x3 = np.arange(1, 11)
wse2_3x3 = np.array([8, 15, 12, 12, 12, 12, 12, 14, 12, 12])
wse3_3x3 = np.array([10, 24, 17, 17, 17, 17, 17, 17, 17, 17])

# Experiment: Grid 10x10, Radius 1
iterations_10x10 = np.arange(1, 9)
wse2_10x10 = np.array([8, 14, 16, 16, 17, 16, 17, 15])
wse3_10x10 = np.array([1, 23, 24, 23, 23, 23, 23, 23])

# Create the plot
plt.figure(figsize=(10, 6))

# Plot data for Grid 3x3, Radius 1
plt.plot(iterations_3x3, wse2_3x3, 'o-', color=blue, linestyle='-')
plt.plot(iterations_3x3, wse3_3x3, 'o-', color=blue, linestyle='--')

# Plot data for Grid 10x10, Radius 1
plt.plot(iterations_10x10, wse2_10x10, 'o-', color=green, linestyle='-')
plt.plot(iterations_10x10, wse3_10x10, 'o-', color=green, linestyle='--')

# Add titles and labels
plt.title('Stencil Iteration Benchmark Results (Single-cell)')
plt.xlabel('Iteration')
plt.ylabel('Cycles for Iteration')

# Create custom legends
legend_elements_params = [
    Line2D([0], [0], color=blue, markersize=10, label='Grid 3x3, Radius 1'),
    Line2D([0], [0], color=green, markersize=10, label='Grid 10x10, Radius 1')
]

legend_elements_wse = [
    Line2D([0], [0], color='black', lw=2, linestyle='-', label='WSE2'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', label='WSE3')
]

# Create first legend for the parameter sets
first_legend = plt.legend(handles=legend_elements_params, loc='lower right', title='Experiments', bbox_to_anchor=(1, 0))
plt.gca().add_artist(first_legend)

# Create second legend for the WSE versions
plt.legend(handles=legend_elements_wse, loc='lower right', title='WSE Version', bbox_to_anchor=(1, 0.15))

plt.grid(True)
plt.xticks(np.arange(1, 11, 1))

# Save the plot to a file
plt.savefig('non_tiled_iteration_stability.png', bbox_inches='tight', dpi=300)

print("Plot saved as non_tiled_iteration_stability.png")