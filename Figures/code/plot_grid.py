import matplotlib.pyplot as plt
import matplotlib.patches as patches
from colors import light_blue, blue, light_green, green, light_red, red

# Create figure and axis with larger width to accommodate two grids
fig, ax = plt.subplots(figsize=(10, 6))

# Grid dimensions (swapped from original)
width, height = 7, 8
spacing = 1  # One square spacing between grids

def create_grid(offset_x=0):
    """Create a grid with specified x offset"""
    # Create grid with individual squares
    for i in range(width):
        for j in range(height):
            # Determine color based on position
            if (2 <= i <= 4) and (2 <= j <= 5):
                # Middle 3x4 area (light green)
                color = light_green
            elif ((0 <= i <= 1) or (5 <= i <= 6)) and ((0 <= j <= 1) or (6 <= j <= 7)):
                # Corner 2x2 areas (white)
                color = 'white'
            else:
                # Side areas (light blue - halo regions)
                color = light_blue
                
            # Add square with grey edge
            square = patches.Rectangle((i + offset_x, j), 1, 1, linewidth=.5, edgecolor='grey', facecolor=color)
            ax.add_patch(square)

# Create left grid (first PE)
create_grid(offset_x=0)

# Create right grid (second PE) with spacing
create_grid(offset_x=width + spacing)

# Right grid rectangles (current grid)
# Blue rectangle for leftmost inner region (data to be sent west)
right_blue_rect = patches.Rectangle((2 + width + spacing, 2), 2, 4, linewidth=5, edgecolor=blue, facecolor='none')
ax.add_patch(right_blue_rect)

# Green rectangle for left halo region (receives data from west)
right_green_rect = patches.Rectangle((0 + width + spacing, 2), 2, 4, linewidth=5, edgecolor=green, facecolor='none')
ax.add_patch(right_green_rect)

# Left grid rectangles (neighboring PE)
# Green rectangle for rightmost inner region (data to be sent east)
left_green_rect = patches.Rectangle((3, 2), 2, 4, linewidth=5, edgecolor=green, facecolor='none')
ax.add_patch(left_green_rect)

# Blue rectangle for right halo region (receives data from east)
left_blue_rect = patches.Rectangle((5, 2), 2, 4, linewidth=5, edgecolor=blue, facecolor='none')
ax.add_patch(left_blue_rect)

# Add arrows to show data exchange at different y levels
# Upper arrow (green) from left grid's rightmost inner region to right grid's left halo region
arrow1 = patches.FancyArrowPatch((4, 5), (width + spacing + 1, 5),
                                connectionstyle="arc3,rad=0", 
                                arrowstyle='->', 
                                mutation_scale=20, 
                                color=green,
                                linewidth=5)
ax.add_patch(arrow1)

# Lower arrow (blue) from right grid's leftmost inner region to left grid's right halo region
arrow2 = patches.FancyArrowPatch((3 + width + spacing, 3), (6, 3),
                                connectionstyle="arc3,rad=0", 
                                arrowstyle='->', 
                                mutation_scale=20, 
                                color=blue,
                                linewidth=5)
ax.add_patch(arrow2)

# Create legend elements
legend_elements = [
    patches.Patch(color=light_green, label='Grid tile represented by one PE'),
    patches.Patch(color=light_blue, label='Halo region used to store received data'),
    patches.Patch(color=green, label='Data send from left PE to right PE'),
    patches.Patch(color=blue, label='Data send from right PE to left PE'),
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

plt.title('Data Exchange Between Neighboring Processing Elements')
plt.tight_layout()
plt.savefig('grid_visualization.png', dpi=300, bbox_inches='tight')
# plt.show() 