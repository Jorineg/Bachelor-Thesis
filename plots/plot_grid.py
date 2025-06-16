import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Grid dimensions
width, height = 9, 7

# Create grid with individual squares
for i in range(width):
    for j in range(height):
        # Determine color based on position
        if (2 <= i <= 6) and (2 <= j <= 4):
            # Middle 5x3 area (green)
            color = 'lightgreen'
        elif ((0 <= i <= 1) or (7 <= i <= 8)) and ((0 <= j <= 1) or (5 <= j <= 6)):
            # Corner 2x2 areas (white)
            color = 'white'
        else:
            # Side areas (yellow)
            color = 'yellow'
            
        # Add square with black edge
        square = patches.Rectangle((i, j), 1, 1, linewidth=.5, edgecolor='grey', facecolor=color)
        ax.add_patch(square)

# Add orange rectangle surrounding the 2 upper rows of the middle area
orange_rect = patches.Rectangle((2, 3), 5, 2, linewidth=5, edgecolor='orange', facecolor='none')
ax.add_patch(orange_rect)

# Add purple rectangle surrounding the 2 leftmost columns of the middle part
purple_rect = patches.Rectangle((2, 2), 2, 3, linewidth=5, edgecolor='purple', facecolor='none')
ax.add_patch(purple_rect)

# Create legend elements
legend_elements = [
    patches.Patch(color='lightgreen', label='Grid tile represented by one PE'),
    patches.Patch(color='orange', label='Data sent to the north'),
    patches.Patch(color='purple', label='Data sent to the west'),
    patches.Patch(color='yellow', label='Halo region used to store received data from the neighbours')
]

# Add legend
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))

# Set axis limits and aspect
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')

# remove axis
ax.axis('off')

# Remove axis ticks
ax.set_xticks([])
ax.set_yticks([])

plt.title('Grid Visualization')
plt.tight_layout()
plt.savefig('grid_visualization.png', dpi=300)
plt.show() 