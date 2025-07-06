import numpy as np
import matplotlib.pyplot as plt
import math
from colors import light_blue, blue, light_green, green, light_red, red

# Parameters
r = 1  # radius
tile_sizes = range(1, 21)  # tile sizes from 1 to 20

# Calculate cycle counts
non_tiled_cycles = [7] * len(tile_sizes)  # constant 7 cycles

# For each tile size (where tile_width = tile_height)
wse2_pessimistic = []  # WSE-2 with s=4, pessimistic estimate
wse3_optimistic = []   # WSE-3 with s=8, optimistic estimate

for t in tile_sizes:
    t_w = t
    t_h = t
    
    # WSE-2 pessimistic: ⌈(t_w * t_h * (4r + 1)) / s⌉ + 2r * (t_w + t_h)
    computation_wse2 = math.ceil((t_w * t_h * (4*r + 1)) / 4)
    communication = 2 * r * (t_w + t_h)
    wse2_pessimistic.append(computation_wse2 + communication)
    
    # WSE-3 optimistic: ⌈(t_w * t_h * (4r + 1)) / s⌉
    computation_wse3 = math.ceil((t_w * t_h * (4*r + 1)) / 8)
    wse3_optimistic.append(computation_wse3)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(tile_sizes, non_tiled_cycles, 'b-', label='Rank 1 non-tiled (constant 7 cycles)', color=blue)
plt.plot(tile_sizes, wse2_pessimistic, 'r-', label='Rank 1 WSE-2 pessimistic (s=4)', color=green)
plt.plot(tile_sizes, wse3_optimistic, 'g-', label='Rank 1 WSE-3 optimistic (s=8)', color=red)

plt.xlabel('Tile Size (tile width = tile height)')
plt.ylabel('Cycles per Iteration')
plt.title('Stencil Performance Comparison')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Set y-axis to log scale
plt.yscale('log')

# Set x-axis ticks to integers only
plt.xticks(range(1, 21))

# Add points for specific tile sizes
# for i in [1, 5, 10, 15, 20]:
#     if i in tile_sizes:
#         idx = i - 1  # Convert to 0-based index
#         plt.plot(i, non_tiled_cycles[idx], 'bo')
#         plt.plot(i, wse2_pessimistic[idx], 'ro')
#         plt.plot(i, wse3_optimistic[idx], 'go')
        
#         # Add value annotations for selected points
#         if i in [1, 10, 20]:
#             plt.annotate(f"{non_tiled_cycles[idx]}", (i, non_tiled_cycles[idx]), 
#                         textcoords="offset points", xytext=(0,10), ha='center')
#             plt.annotate(f"{wse2_pessimistic[idx]}", (i, wse2_pessimistic[idx]), 
#                         textcoords="offset points", xytext=(0,10), ha='center')
#             plt.annotate(f"{wse3_optimistic[idx]}", (i, wse3_optimistic[idx]), 
#                         textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.savefig('stencil_performance_comparison.png', dpi=300)
plt.show() 