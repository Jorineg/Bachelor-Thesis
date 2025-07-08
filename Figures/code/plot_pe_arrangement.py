import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from colors import light_blue, light_green

# Grid and tile parameters
grid_width = 25
grid_height = 16
tile_width = 5
tile_height = 4
stencil_width = 19
stencil_height = 12
radius = 2

# Calculate number of tiles
tiles_x = grid_width // tile_width  # 5
tiles_y = grid_height // tile_height  # 4

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Create the grid visualization
grid = np.zeros((grid_height, grid_width))

# Define regions based on stencil grid size and radius
# For a 19x12 stencil with radius 2 in a 25x16 grid:
# - Left padding: 3 columns (0-2)
# - Right padding: 3 columns (22-24)
# - Top padding: 2 rows (0-1)
# - Bottom padding: 2 rows (14-15)
# - Static region: 2 rows/columns inward from actual stencil boundary

# White region (zero padding)
grid[:, 0:3] = 0  # Left padding
grid[:, 22:25] = 0  # Right padding
grid[0:2, :] = 0  # Top padding
grid[14:16, :] = 0  # Bottom padding

# Light green region (static grid region)
grid[2:4, 3:22] = 1  # Top static
grid[12:14, 3:22] = 1  # Bottom static
grid[4:12, 3:5] = 1  # Left static
grid[4:12, 20:22] = 1  # Right static

# Light blue region (dynamic grid region)
grid[4:12, 5:20] = 2  # Inner region

# Color mapping
colors = ['white', light_blue, light_green]
color_map = plt.matplotlib.colors.ListedColormap(colors)

# Display the grid
im = ax.imshow(grid, cmap=color_map, aspect='equal', origin='upper')

# Add grid lines for individual cells
for i in range(grid_height + 1):
    ax.axhline(y=i-0.5, color='black', linewidth=0.1)
for j in range(grid_width + 1):
    ax.axvline(x=j-0.5, color='black', linewidth=0.1)

# Add thicker lines for tile boundaries
for i in range(0, grid_height + 1, tile_height):
    ax.axhline(y=i-0.5, color='black', linewidth=2)
for j in range(0, grid_width + 1, tile_width):
    ax.axvline(x=j-0.5, color='black', linewidth=2)

# Add text labels for tiles
for tile_y in range(tiles_y):
    for tile_x in range(tiles_x):
        # Calculate tile center
        center_x = tile_x * tile_width + tile_width / 2 - 0.5
        center_y = tile_y * tile_height + tile_height / 2 - 0.5
        
        # Determine if this is a border tile
        # Check if any cell in this tile is white (padding) or light green (static)
        tile_start_x = tile_x * tile_width
        tile_end_x = (tile_x + 1) * tile_width
        tile_start_y = tile_y * tile_height
        tile_end_y = (tile_y + 1) * tile_height
        
        tile_region = grid[tile_start_y:tile_end_y, tile_start_x:tile_end_x]
        
        # If tile contains any non-dynamic (non-blue) cells, it's a border tile
        if np.any(tile_region != 2):
            label = "Border PE"
        else:
            label = "Inner PE"

        # no label for top right tile
        if tile_x == tiles_x - 1 and tile_y == 0:
            continue
        
        ax.text(center_x, center_y, label, ha='center', va='center', 
                fontsize=14, fontweight='bold', color='black')

# Create legend
legend_elements = [
    patches.Patch(facecolor='white', label='Zero padding', edgecolor='black', linewidth=0.5),
    patches.Patch(facecolor=light_green, label='Static grid region'),
    patches.Patch(facecolor=light_blue, label='Dynamic grid region')
]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))

# Set title
ax.set_title(f'PE Arrangement for {stencil_width}×{stencil_height} Stencil Grid with tile size {tile_width}×{tile_height} and radius {radius}', 
             fontsize=14, fontweight='bold')

# Remove axis
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')

# Tight layout
fig.tight_layout()

# Save the plot
plt.savefig('pe_arrangement.png', dpi=300, bbox_inches='tight')
print("Plot saved to pe_arrangement.png") 