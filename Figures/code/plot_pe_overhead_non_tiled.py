import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as mticker
from colors import blue

# Data from the user
grid_sizes = ['3x3', '4x4', '5x5', '6x6', '7x7', '8x8', '9x9', '10x10', '15x15', '20x20', '30x30', '50x50']
num_elements = [int(s.split('x')[0]) * int(s.split('x')[1]) for s in grid_sizes]
wse2_cycles = [12, 15, 16, 16, 16, 16, 16, 16, 16, 15, 15, 15]
wse3_cycles = [17, 21, 23, 23, 22, 24, 23, 23, 23, 23, 23, 23]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data
ax.plot(num_elements, wse2_cycles, 'o-', color=blue, label='WSE2')
ax.plot(num_elements, wse3_cycles, 'o--', color=blue, label='WSE3')

# Add titles and labels
ax.set_title('Cycle Count vs. Grid Size for Single-cell Stencil')
ax.set_xlabel('Number of active PEs')
ax.set_ylabel('Cycles per Iteration')
ax.set_xscale('log')

# Set custom ticks and labels
ax.set_xticks(num_elements)
ax.set_xticklabels([])  # We will draw custom labels

# Manually create labels to rotate only the second line
for p, s in zip(num_elements, grid_sizes):
    # The number, un-rotated
    ax.text(p, -0.06, str(p), ha='center', va='top', transform=ax.get_xaxis_transform(), fontsize=9)
    # The (size), rotated
    ax.text(p, -0.085, f'({s})', ha='right', va='top', rotation=45, transform=ax.get_xaxis_transform(), fontsize=9)

# Customize grid
ax.grid(True, which="major", linestyle='--', alpha=0.7)
ax.grid(True, which="minor", linestyle=':', alpha=0.5)

# remove markers from legend
legend = ax.legend()
for line in legend.get_lines():
    line.set_marker('')

    
# Save the plot to a file
plt.savefig('pe_overhead_non_tiled.png', dpi=300, bbox_inches='tight')

print("Plot saved as pe_overhead_non_tiled.png") 