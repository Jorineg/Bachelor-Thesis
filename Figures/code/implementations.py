import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. Setup the plot
# Create a figure (the window) and axes (the canvas)
# We make it larger to have more space to work with
fig, ax = plt.subplots(figsize=(10, 8))

# Define some styles for consistency
BOX_STYLE = dict(boxstyle='round,pad=0.5', facecolor='#ddd', edgecolor='black')
ARROW_STYLE = dict(arrowstyle='->', connectionstyle='arc3', edgecolor='black')

# 2. Define coordinates and draw the boxes
# You manually define the (x, y) center for each box
coords = {
    'A': (0.5, 0.9),
    'A1': (0.25, 0.7),
    'A2': (0.75, 0.7),
    'A21': (0.6, 0.5),
    'A22': (0.9, 0.5)
}

# Add boxes and their text
ax.text(coords['A'][0], coords['A'][1], 'Implementations', ha='center', va='center', bbox=BOX_STYLE)
ax.text(coords['A1'][0], coords['A1'][1], 'Single Cell\nRadius=1', ha='center', va='center', bbox=BOX_STYLE)
ax.text(coords['A2'][0], coords['A2'][1], 'Tiled', ha='center', va='center', bbox=BOX_STYLE)
ax.text(coords['A21'][0], coords['A21'][1], 'r1-Optimized', ha='center', va='center', bbox=BOX_STYLE)
# Add A22 yourself as practice!


# 3. Draw the arrows between boxes
# Use annotate to draw an arrow from point A to point A1
ax.annotate('', xy=coords['A1'], xytext=coords['A'], arrowprops=ARROW_STYLE)
ax.annotate('', xy=coords['A2'], xytext=coords['A'], arrowprops=ARROW_STYLE)
ax.annotate('', xy=coords['A21'], xytext=coords['A2'], arrowprops=ARROW_STYLE)
# Add the arrow for A22 yourself!


# 4. Create the legend with absolute positioning
# Place the legend text at a specific corner of the figure
# The coordinates (0.95, 0.95) are in "figure fraction" units (top right)
legend_text = "✓= Supported\n(✓)= Supported with minimal changes\n✗= Not supported"
fig.text(0.95, 0.95, legend_text, ha='right', va='top', fontsize=9, color='#333',
         bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))


# 5. Clean up the plot
# Set the visible area of the canvas
ax.set(xlim=(0, 1.2), ylim=(0.4, 1.0))
# Hide the axis lines and ticks
ax.axis('off')

# Display the plot
plt.savefig('implementations.png', dpi=300, bbox_inches='tight')