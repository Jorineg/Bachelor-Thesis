#               WSE2_min  WSE2_max  WSE3_min  WSE3_max  WSE2_fluctuation  \
#  Radius Tile                                                             
#  2      5x5        585       599       635       635          2.393162   
#  1      1x1        125       127       155       157          1.600000   
#  7      7x7       2769      2804      2783      2793          1.263994   
#  1      5x5        283       286       191       191          1.060071   
#  3      5x5        838       846       886       886          0.954654   
 
#               WSE3_fluctuation  
#  Radius Tile                    
#  2      5x5           0.000000  
#  1      1x1           1.290323  
#  7      7x7           0.359324  
#  1      5x5           0.000000  
#  3      5x5           0.000000  )

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as mticker
from colors import light_blue, blue, light_green, green, light_red, red

# Data from the benchmark results for tiled PE stability

# Tile 1x1, Radius 1
grid_sizes_1x1_r1 = [3, 5, 7, 10, 15, 20, 25]
grid_sizes_str_1x1_r1 = [f'{x}x{x}' for x in grid_sizes_1x1_r1]
num_elements_1x1_r1 = [x*x for x in grid_sizes_1x1_r1]
wse2_1x1_r1 = [125, 127, 127, 127, 127, 127, 127]
wse3_1x1_r1 = [155, 157, 156, 156, 156, 156, 156]

# Tile 5x5, Radius 1
grid_sizes_5x5_r1 = [7, 17, 27, 37, 47, 57]
grid_sizes_str_5x5_r1 = [f'{x}x{x}' for x in grid_sizes_5x5_r1]
num_elements_5x5_r1 = [x*x for x in grid_sizes_5x5_r1]
wse2_5x5_r1 = [283, 286, 285, 285, 285, 285]
wse3_5x5_r1 = [191, 191, 191, 191, 191, 191]

# Tile 5x5, Radius 3
grid_sizes_5x5_r3 = [11, 21, 31, 41, 51, 61]
grid_sizes_str_5x5_r3 = [f'{x}x{x}' for x in grid_sizes_5x5_r3]
num_elements_5x5_r3 = [x*x for x in grid_sizes_5x5_r3]
wse2_5x5_r3 = [838, 843, 846, 842, 844, 838]
wse3_5x5_r3 = [886, 886, 886, 886, 886, 886]

# Tile 7x7, Radius 7
grid_sizes_7x7_r7 = [21, 35, 49, 63, 77, 91, 105]
grid_sizes_str_7x7_r7 = [f'{x}x{x}' for x in grid_sizes_7x7_r7]
num_elements_7x7_r7 = [x*x for x in grid_sizes_7x7_r7]
wse2_7x7_r7 = [2804, 2781, 2779, 2771, 2769, 2774, 2771]
wse3_7x7_r7 = [2792, 2783, 2791, 2786, 2786, 2791, 2793]

def get_size(size, radius, tile_size):
    inner_size = size - 2 * radius
    remainder_size = inner_size % tile_size
    if remainder_size != 0:
        pad_size = tile_size - remainder_size
        size += pad_size
    return size

# Compute number of active PEs for each grid size
active_pes_1x1_r1 = [((get_size(w, 1, 1) - 2 * 1) // 1 + 2) ** 2 for w in grid_sizes_1x1_r1]
active_pes_5x5_r1 = [((get_size(w, 1, 5) - 2 * 1) // 5 + 2) ** 2 for w in grid_sizes_5x5_r1]
active_pes_5x5_r3 = [((get_size(w, 3, 5) - 2 * 3) // 5 + 2) ** 2 for w in grid_sizes_5x5_r3]
active_pes_7x7_r7 = [((get_size(w, 7, 7) - 2 * 7) // 7 + 2) ** 2 for w in grid_sizes_7x7_r7]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data for Tile 1x1, Radius 1
ax.plot(active_pes_1x1_r1, wse2_1x1_r1, 'o-', color=blue)
ax.plot(active_pes_1x1_r1, wse3_1x1_r1, 'o--', color=blue)

# Plot data for Tile 5x5, Radius 1
ax.plot(active_pes_5x5_r1, wse2_5x5_r1, 'o-', color=light_green)
ax.plot(active_pes_5x5_r1, wse3_5x5_r1, 'o--', color=light_green)

# Plot data for Tile 5x5, Radius 3
ax.plot(active_pes_5x5_r3, wse2_5x5_r3, 'o-', color=green)
ax.plot(active_pes_5x5_r3, wse3_5x5_r3, 'o--', color=green)

# Plot data for Tile 7x7, Radius 7
ax.plot(active_pes_7x7_r7, wse2_7x7_r7, 'o-', color=red)
ax.plot(active_pes_7x7_r7, wse3_7x7_r7, 'o--', color=red)

# Add titles and labels
ax.set_title('Stencil PE Stability Benchmark Results (Tiled)')
ax.set_xlabel('Number of Active PEs')
ax.set_ylabel('Cycles per Iteration')
ax.set_yscale('log')

# Create custom legends
legend_elements_params = [
    Line2D([0], [0], color=blue, markersize=10, label='Tile 1x1, Radius 1'),
    Line2D([0], [0], color=light_green, markersize=10, label='Tile 5x5, Radius 1'),
    Line2D([0], [0], color=green, markersize=10, label='Tile 5x5, Radius 3'),
    Line2D([0], [0], color=red, markersize=10, label='Tile 7x7, Radius 7')
]

legend_elements_wse = [
    Line2D([0], [0], color='black', lw=2, linestyle='-', label='WSE2'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', label='WSE3')
]

# Create first legend for the parameter sets
first_legend = ax.legend(handles=legend_elements_params, loc='upper right', title='Experiments', bbox_to_anchor=(1, 1))
ax.add_artist(first_legend)

# Create second legend for the WSE versions
ax.legend(handles=legend_elements_wse, loc='upper right', title='WSE Version', bbox_to_anchor=(1, 0.75))

# Customize grid
ax.grid(True, which="major", linestyle='--', alpha=0.7)
ax.grid(True, which="minor", linestyle=':', alpha=0.5)

# Update xticks computation to use active PEs
all_active_pes = sorted(set(active_pes_1x1_r1 + active_pes_5x5_r1 + active_pes_5x5_r3 + active_pes_7x7_r7))
all_grid_sizes_str = [f'{int(np.sqrt(p))}x{int(np.sqrt(p))}' for p in all_active_pes]  # quick mapping

ax.set_xticks(all_active_pes)
ax.set_xticklabels([])

for p, s in zip(all_active_pes, all_grid_sizes_str):
    ax.text(p, -0.1, str(p), ha='center', va='top', transform=ax.get_xaxis_transform(), fontsize=9)
    ax.text(p, -0.125, f'({s})', ha='right', va='top', rotation=45, transform=ax.get_xaxis_transform(), fontsize=9)

# Ensure log scale on x-axis
ax.set_xscale('log')

# Save the plot to a file
plt.savefig('tiled_pe_stability.png', dpi=300, bbox_inches='tight')

print("Plot saved as tiled_pe_stability.png") 