import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib
from colors import light_blue, light_green, light_red

# Use matplotlib's built-in math renderer (no global LaTeX)
matplotlib.rcParams['text.usetex'] = False

# Parameters
tile_width = 7
tile_height = 5
compute_width = 5
compute_height = 3
radius = 1
meta_grid_size = 9
gap_size = 1

# Create figure
fig, ax = plt.subplots(figsize=(14, 10))

def draw_tile(ax, start_x, start_y, fill_center=True, center_color=light_green, 
              highlight_region=None, show_grid=True, show_halo=True):
    """Draw a single 7x5 tile with proper coloring"""
    
    # Define regions within the tile
    center_start_x = 1  # Center region starts at column 1
    center_start_y = 1  # Center region starts at row 1
    
    for i in range(tile_width):
        for j in range(tile_height):
            x = start_x + i
            y = start_y + j
            
            # Determine color based on position within tile
            if (center_start_x <= i < center_start_x + compute_width and 
                center_start_y <= j < center_start_y + compute_height):
                # Center 5x3 region
                if fill_center:
                    color = center_color
                else:
                    color = 'white'
            elif ((i == 0 or i == tile_width-1) and 
                  (j == 0 or j == tile_height-1)):
                # Corner cells (white)
                color = 'white'
            else:
                # Halo regions (light blue or white if show_halo is False)
                color = light_blue if show_halo else 'white'
            
            # Draw cell
            square = patches.Rectangle((x, y), 1, 1, linewidth=0.5, 
                                     edgecolor='grey', facecolor=color)
            ax.add_patch(square)
    
    # Add highlight region if specified
    if highlight_region is not None:
        dx, dy = highlight_region
        highlight_x = start_x + center_start_x + dx
        highlight_y = start_y + center_start_y + dy
        
        # Draw red rectangle around the highlighted region
        red_rect = patches.Rectangle(
            (highlight_x, highlight_y), compute_width, compute_height,
            linewidth=3, edgecolor='red', facecolor='none'
        )
        ax.add_patch(red_rect)
    
    # Add tile border if grid should be shown
    if show_grid:
        tile_border = patches.Rectangle((start_x, start_y), tile_width, tile_height, 
                                      linewidth=0.5, edgecolor='grey', facecolor='none')
        ax.add_patch(tile_border)

def draw_arrow(ax, start_x, start_y, end_x, end_y, color='black', reverse=False):
    """Draw an arrow from start to end position"""
    if reverse:
        start_x, end_x = end_x, start_x
        start_y, end_y = end_y, start_y
    ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(color=color, headwidth=20, headlength=20, width=2))

# Calculate positions for the 5 buffer tiles
# 3 bottom tiles and 2 right tiles
buffer_positions = [
    # Bottom row (3 tiles)
    (0, 0),  # Bottom left
    (1, 0),  # Bottom center  
    (2, 0),  # Bottom right
    # Right column (2 tiles)
    (2, 1),  # Right middle
    (2, 2),  # Right top
]

# Shifts for radius 1: up, right, down, left, center
shifts = [
    (0, 1, "acc = 0 + w_1 \\cdot buf_{north}"),      # up 1
    (1, 0, "acc = acc + w_1 \\cdot buf_{east}"),   # right 1  
    (0, -1, "acc = acc + w_1 \\cdot buf_{south}"),   # down 1
    (-1, 0, "acc = acc + w_1 \\cdot buf_{west}"),   # left 1
    (0, 0, "buf_{center} = acc + w_0 \\cdot buf_{center}")   # center
]

# Draw the 5 buffer tiles
tile_centers = []
for i, (grid_x, grid_y) in enumerate(buffer_positions):
    # Calculate actual position with gaps
    actual_x = grid_x * (tile_width + gap_size)
    actual_y = grid_y * (tile_height + gap_size)
    
    # Get the corresponding shift for this tile
    dx, dy, direction = shifts[i]
    
    # Draw the tile with highlight
    draw_tile(ax, actual_x, actual_y, fill_center=True, center_color=light_green, 
              highlight_region=(dx, dy), show_grid=True)
    
    # Store center position for arrows
    center_x = actual_x + tile_width/2
    center_y = actual_y + tile_height/2
    tile_centers.append((center_x, center_y))
    
    # Add labels
    label_x = actual_x + tile_width/2
    label_y = actual_y - 0.3
    ax.text(label_x, label_y, f'${direction}$', ha='center', va='top', 
            fontsize=15, fontweight='bold')

# Draw accumulator tile in upper left area
# Position it at the same y level as the buffer center tile
acc_x = 0
acc_y = 2 * (tile_height + gap_size)

draw_tile(ax, acc_x, acc_y, fill_center=True, center_color=light_red, 
          highlight_region=None, show_grid=True, show_halo=False)

# Add accumulator label
acc_label_x = acc_x + 1.5    # move to the left to avoid overlap with arrow
acc_label_y = acc_y - 0.3
ax.text(acc_label_x, acc_label_y, 'Accumulator', ha='center', va='top', 
        fontsize=15, fontweight='bold')

# Draw arrows from buffer tiles to accumulator
acc_center_x = acc_x + tile_width/2
acc_center_y = acc_y + tile_height/2

# Define slight offsets for arrow endpoints to avoid all arrows converging to same point
arrow_offsets = [
    (-1, -1),  
    (0, -1),
    (1, -1),   
    (1, 0),  
    (1, 1)    
]

for i, (center_x, center_y) in enumerate(tile_centers):
    offset_x, offset_y = arrow_offsets[i]
    end_x = acc_center_x + offset_x + 1
    end_y = acc_center_y + offset_y
    draw_arrow(ax, center_x, center_y, end_x, end_y, color='red', reverse=i==4)



# Create legend
legend_elements = [
    patches.Patch(facecolor=light_green, label='Grid tile (own data)'),
    patches.Patch(facecolor=light_blue, label='Halo region (neighbor data)'),
    patches.Patch(facecolor=light_red, label='Accumulator (intermediate results)')
]

ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.0), fontsize=15)

# Set title
ax.set_title(f'Stencil Computation Pattern (Radius {radius}, Tile Size {compute_width}×{compute_height})', 
             fontsize=16, fontweight='bold', pad=20)

# Set axis properties
max_x = max(acc_x + tile_width, 3 * (tile_width + gap_size))
max_y = max(acc_y + tile_height, 2 * (tile_height + gap_size))
ax.set_xlim(0, max_x -1)
ax.set_ylim(-0.3, max_y)
ax.set_aspect('equal')
ax.axis('off')

# Tight layout
fig.tight_layout()

# Save the plot
plt.savefig('stencil_static.png', dpi=300, bbox_inches='tight')
print("Plot saved to stencil_static.png") 