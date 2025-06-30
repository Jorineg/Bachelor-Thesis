import matplotlib.pyplot as plt
import numpy as np

# Data from the benchmark results

# Experiment: Grid 10x10, Tile 1x1, Radius 1
iterations_10x10_r1 = np.arange(1, 11)
wse2_10x10_r1 = np.array([127, 127, 127, 127, 127, 127, 127, 127, 127, 127])
wse3_10x10_r1 = np.array([156, 156, 156, 157, 157, 157, 157, 157, 157, 157])

# Experiment: Grid 10x10, Tile 3x3, Radius 2
iterations_10x10_r2 = np.arange(1, 11)
wse2_10x10_r2 = np.array([371, 371, 371, 371, 370, 370, 370, 370, 371, 370])
wse3_10x10_r2 = np.array([408, 419, 419, 419, 419, 419, 419, 419, 419, 419])

# Experiment: Grid 100x100, Tile 10x10, Radius 1
iterations_100x100_r1 = np.arange(1, 9)
wse2_100x100_r1 = np.array([780, 801, 782, 781, 782, 784, 791, 791])
wse3_100x100_r1 = np.array([558, 558, 558, 558, 558, 558, 558, 558])

# Experiment: Grid 100x100, Tile 10x10, Radius 2
iterations_100x100_r2 = np.arange(1, 9)
wse2_100x100_r2 = np.array([1660, 1679, 1673, 1689, 1667, 1672, 1681, 1676])
wse3_100x100_r2 = np.array([1700, 1709, 1716, 1712, 1711, 1709, 1712, 1712])

# Experiment: Grid 100x100, Tile 10x10, Radius 5
iterations_100x100_r5 = np.arange(1, 9)
wse2_100x100_r5 = np.array([3332, 3340, 3333, 3345, 3355, 3341, 3373, 3369])
wse3_100x100_r5 = np.array([3369, 3379, 3372, 3378, 3381, 3380, 3380, 3378])

# Create the plot
plt.figure(figsize=(12, 8))

# Plot data for Grid 10x10, R1
plt.plot(iterations_10x10_r1, wse2_10x10_r1, 'o-', color='blue', linestyle='-')
plt.plot(iterations_10x10_r1, wse3_10x10_r1, 'o-', color='blue', linestyle='--')

# Plot data for Grid 10x10, R2
plt.plot(iterations_10x10_r2, wse2_10x10_r2, 's-', color='red', linestyle='-')
plt.plot(iterations_10x10_r2, wse3_10x10_r2, 's-', color='red', linestyle='--')

# Plot data for Grid 100x100, R1
plt.plot(iterations_100x100_r1, wse2_100x100_r1, '^-', color='green', linestyle='-')
plt.plot(iterations_100x100_r1, wse3_100x100_r1, '^-', color='green', linestyle='--')

# Plot data for Grid 100x100, R2
plt.plot(iterations_100x100_r2, wse2_100x100_r2, 'P-', color='purple', linestyle='-')
plt.plot(iterations_100x100_r2, wse3_100x100_r2, 'P-', color='purple', linestyle='--')

# Plot data for Grid 100x100, R5
plt.plot(iterations_100x100_r5, wse2_100x100_r5, 'D-', color='orange', linestyle='-')
plt.plot(iterations_100x100_r5, wse3_100x100_r5, 'D-', color='orange', linestyle='--')


# Add titles and labels
plt.title('Stencil Iteration Benchmark Results (Tiled)')
plt.xlabel('Iteration')
plt.ylabel('Cycles for Iteration')

# Create custom legends
from matplotlib.lines import Line2D

legend_elements_params = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Grid: 10x10, Tile: 1x1, R=1'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10, label='Grid: 10x10, Tile: 3x3, R=2'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='green', markersize=10, label='Grid: 100x100, Tile: 10x10, R=1'),
    Line2D([0], [0], marker='P', color='w', markerfacecolor='purple', markersize=10, label='Grid: 100x100, Tile: 10x10, R=2'),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='orange', markersize=10, label='Grid: 100x100, Tile: 10x10, R=5')
]

legend_elements_wse = [
    Line2D([0], [0], color='black', lw=2, linestyle='-', label='WSE2'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', label='WSE3')
]

# Create first legend for the parameter sets
first_legend = plt.legend(handles=legend_elements_params, loc='upper right', title='Experiments', bbox_to_anchor=(1, 0.93))
plt.gca().add_artist(first_legend)

# Create second legend for the WSE versions
plt.legend(handles=legend_elements_wse, loc='upper right', title='WSE Version', bbox_to_anchor=(1, 0.7))

plt.grid(True)
plt.xticks(np.arange(1, 11, 1))

# Save the plot to a file
plt.savefig('tiled_iteration_stability.png')

print("Plot saved as tiled_iteration_stability.png") 