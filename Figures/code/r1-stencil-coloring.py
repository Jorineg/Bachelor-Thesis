import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Grid dimensions (show a reasonable section to demonstrate the pattern)
width, height = 8, 5

# Define colors for each value (0-5)
colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c']

# Coloring function: f(x,y) = (x + 2y) mod 6
def coloring_function(x, y):
    return (x + 2*y) % 6

# Create grid with individual squares
for i in range(width):
    for j in range(height):
        # Calculate color index using the coloring function
        color_index = coloring_function(i, j)
        color = colors[color_index]
        
        # Add square with black edge
        square = patches.Rectangle((i, j), 1, 1, linewidth=0.5, edgecolor='black', facecolor=color)
        ax.add_patch(square)
        
        # Add text showing the color index
        ax.text(i + 0.5, j + 0.5, str(color_index), ha='center', va='center', 
                fontsize=18, fontweight='bold', color='black')

# Set axis limits and aspect
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')

# remove axis
ax.axis('off')

# Add grid lines for clarity
ax.set_xticks(range(width + 1))
ax.set_yticks(range(height + 1))
ax.grid(True, color='black', linewidth=0.5)

# Remove axis labels and tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Add title with the function
plt.title('Coloring Pattern for Radius-1 Non-Tiled Stencil\nf(x,y) = (x + 2y) mod 6', fontsize=14, fontweight='bold')

# Create legend with numbers
legend_elements = [patches.Patch(facecolor=colors[i], edgecolor='black', label=str(i)) 
                  for i in range(6)]
# ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1))

plt.tight_layout()
plt.savefig('r1-stencil-coloring.png', dpi=300, bbox_inches='tight')
# plt.show()
