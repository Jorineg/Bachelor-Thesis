import matplotlib.pyplot as plt
import matplotlib.patches as patches
from colors import light_blue, blue, light_green, green, light_red, red

# Create figure and axis with larger width to accommodate two grids
fig, ax = plt.subplots(figsize=(10, 6))

# Grid dimensions (swapped from original)
width, height = 7, 8
spacing = 1  # One square spacing between grids

def create_grid(offset_x=0, is_right_pe=False):
    """Create a grid with specified x offset"""
    # Create grid with individual squares
    for i in range(width):
        for j in range(height):
            # Determine color based on position
            if (2 <= i <= 4) and (2 <= j <= 5):
                # Middle 3x4 area (light green)
                color = light_green
            elif is_right_pe:
                # For right PE: everything else is light blue
                color = light_blue
            else:
                # For left PE: only top and bottom halo regions are light blue
                if (2 <= i <= 4) and ((0 <= j <= 1) or (6 <= j <= 7)):
                    # Top and bottom halo regions
                    color = light_blue
                else:
                    # Everything else is white
                    color = 'white'
                
            # Add square with grey edge
            square = patches.Rectangle((i + offset_x, j), 1, 1, linewidth=.5, edgecolor='grey', facecolor=color)
            ax.add_patch(square)

# Create left grid (first PE)
create_grid(offset_x=0, is_right_pe=False)

# Create right grid (second PE) with spacing
create_grid(offset_x=width + spacing, is_right_pe=True)

# Add blue rectangles
# Left PE: 4th and 5th column (1-indexed) = columns 3 and 4 (0-indexed)
left_blue_rect = patches.Rectangle((3, 0), 2, 8, linewidth=3, edgecolor=blue, facecolor='none')
ax.add_patch(left_blue_rect)

# Right PE: first two columns (0-indexed)
right_blue_rect = patches.Rectangle((0 + width + spacing, 0), 2, 8, linewidth=3, edgecolor=blue, facecolor='none')
ax.add_patch(right_blue_rect)

# Add arrow pointing from left to right
arrow = patches.FancyArrowPatch((4, 4), (width + spacing + 1, 4),
                               connectionstyle="arc3,rad=0", 
                               arrowstyle='->', 
                               mutation_scale=20, 
                               color=blue,
                               linewidth=3)
ax.add_patch(arrow)

# Create legend elements
legend_elements = [
    patches.Patch(color=light_green, label='Grid tile represented by one PE'),
    patches.Patch(color=light_blue, label='Halo region used to store received data'),
    patches.Patch(color=blue, label='Data exchange between PEs'),
]

# Add legend
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))

# Set axis limits and aspect
ax.set_xlim(-0.5, 2 * width + spacing + 0.5)
ax.set_ylim(-0.5, height + 0.5)
ax.set_aspect('equal')

# remove axis
ax.axis('off')

# Remove axis ticks
ax.set_xticks([])
ax.set_yticks([])

plt.title('Data Exchange Between Processing Elements for box-shaped stencils')
plt.tight_layout()
plt.savefig('box_shaped_data_exchange.png', dpi=300, bbox_inches='tight')
# plt.show() 