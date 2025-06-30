import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as mticker

# Data from the user
grid_sizes = ['3x3', '6x6', '10x10', '20x20', '50x50']
num_elements = [int(s.split('x')[0]) * int(s.split('x')[1]) for s in grid_sizes]
wse2_cycles = [12, 16, 16, 16, 16]
wse3_cycles = [17, 20, 23, 23, 23]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data
ax.plot(num_elements, wse2_cycles, 'o-', color='blue', label='WSE2')
ax.plot(num_elements, wse3_cycles, 'o--', color='blue', label='WSE3')

# Add titles and labels
ax.set_title('Cycle Count vs. Grid Size for Non-Tiled Stencil')
ax.set_xlabel('Number of Elements in Grid (Grid Size)')
ax.set_ylabel('Cycles per Iteration')
ax.set_xscale('log')

# Set custom ticks and labels
labels = [f"{p}\n({s})" for s, p in zip(grid_sizes, num_elements)]
ax.set_xticks(num_elements)
ax.set_xticklabels(labels)

# Customize grid
ax.grid(True, which="major", linestyle='--', alpha=0.7)
ax.grid(True, which="minor", linestyle=':', alpha=0.5)

ax.legend()

# Save the plot to a file
plt.savefig('pe_overhead_non_tiled.png', dpi=300, bbox_inches='tight')

print("Plot saved as pe_overhead_non_tiled.png") 