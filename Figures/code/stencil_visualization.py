import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from colors import green, blue, light_blue, light_green

# Create figure with specified size
fig, ax = plt.subplots(figsize=(10, 6))

# Grid dimensions
grid_width = 8
grid_height = 6

# Create the grid
for i in range(grid_height):
    for j in range(grid_width):
        # Create white square with grey border
        rect = patches.Rectangle((j, grid_height - i - 1), 1, 1, 
                               linewidth=1, edgecolor='grey', facecolor='white')
        ax.add_patch(rect)

# Star-shaped stencil pattern (1-indexed, center at (4,4))
# Convert to 0-indexed coordinates: center at (3,3) in 0-indexed system
center_row = 2  # 4-1 (converting from 1-indexed to 0-indexed)
center_col = 3  # 4-1

# Center cell (green)
center_rect = patches.Rectangle((center_col, grid_height - center_row - 1), 1, 1,
                               linewidth=1, edgecolor='grey', facecolor=light_green)
ax.add_patch(center_rect)

# Adjacent cells in cardinal directions (blue) - radius 2
# Vertical direction (up and down from center)
for offset in [-2, -1, 1, 2]:
    if 0 <= center_row + offset < grid_height:
        rect = patches.Rectangle((center_col, grid_height - (center_row + offset) - 1), 1, 1,
                               linewidth=1, edgecolor='grey', facecolor=light_blue)
        ax.add_patch(rect)

# Horizontal direction (left and right from center)
for offset in [-2, -1, 1, 2]:
    if 0 <= center_col + offset < grid_width:
        rect = patches.Rectangle((center_col + offset, grid_height - center_row - 1), 1, 1,
                               linewidth=1, edgecolor='grey', facecolor=light_blue)
        ax.add_patch(rect)

# Add continuation dots to the right
for i in range(3):
    ax.text(grid_width + 0.2 + i * 0.3, grid_height - 0.5, '•', 
            fontsize=20, ha='center', va='center', color='black')

# Add continuation dots to the bottom
for i in range(3):
    ax.text(0.5, -0.2 - i * 0.3, '•', 
            fontsize=20, ha='center', va='center', color='black')

# Set axis properties with reduced horizontal margins
ax.set_xlim(-0.3, grid_width + 0.3)
ax.set_ylim(-0.3, grid_height + 0.5)
ax.set_aspect('equal')

# Make axes invisible
ax.axis('off')

# Add title
fig.suptitle('2D Star-shaped Stencil Pattern (Radius 2)', fontsize=14)

# Save or display the plot
plt.tight_layout()
# plt.show()
plt.savefig('stencil_visualization.png', bbox_inches='tight')
