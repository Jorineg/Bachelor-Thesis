# Algorithm comparison plot saved as 'algo_comparison.png'

# Algorithm Comparison Results:
# ======================================================================
# WSE Type   Algorithm            Grid Size       Throughput (Gcells/s)
# ----------------------------------------------------------------------
# WSE2       Tiled (r1-optimized) 745,500         4989.6
# WSE2       Single-cell          745,500         39604.7

# WSE3       Tiled (r1-optimized) 896,112         5026.3
# WSE3       Single-cell          896,112         34091.2

import matplotlib.pyplot as plt
import numpy as np
from colors import light_blue, blue, light_green, green, light_red, red

# WSE Hardware specifications
WSE2_CLOCK_RATE = 850e6  # Hz
WSE3_CLOCK_RATE = 875e6  # Hz
WSE2_DIMENSIONS = (750, 994)  # width x height
WSE3_DIMENSIONS = (762, 1176)  # width x height

# Algorithm performance data (cycles per iteration) - only radius 1
algorithm_data = {
    'WSE2': {
        'Non-tiled (r=1)': 16,
        'Tiled (r=1)': 127,
    },
    'WSE3': {
        'Non-tiled (r=1)': 23,
        'Tiled (r=1)': 156,
    }
}

def calculate_throughput(cycles_per_iter, clock_rate, grid_size):
    """Calculate throughput in Gcells/s"""
    iterations_per_second = clock_rate / cycles_per_iter
    cells_per_second = grid_size * iterations_per_second
    return cells_per_second / 1e9  # Convert to Gcells/s

def get_max_grid_size(wse_type, algorithm_type):
    """Get maximum grid size for different algorithms"""
    if wse_type == 'WSE2':
        width, height = WSE2_DIMENSIONS
        total_pes = width * height  # 745,500 PEs
    else:
        width, height = WSE3_DIMENSIONS
        total_pes = width * height  # 896,112 PEs
    
    if 'Non-tiled' in algorithm_type:
        # Non-tiled uses one cell per PE
        return total_pes
    else:
        # Tiled implementation with 1x1 tiles - also one cell per PE
        return total_pes * 1 * 1

# Calculate throughput for each algorithm
labels = ['WSE2', 'WSE3']
nontiled_throughputs = []
tiled_throughputs = []

for wse_type in ['WSE2', 'WSE3']:
    clock_rate = WSE2_CLOCK_RATE if wse_type == 'WSE2' else WSE3_CLOCK_RATE
    
    # Non-tiled throughput
    nontiled_cycles = algorithm_data[wse_type]['Non-tiled (r=1)']
    nontiled_grid_size = get_max_grid_size(wse_type, 'Non-tiled (r=1)')
    nontiled_throughput = calculate_throughput(nontiled_cycles, clock_rate, nontiled_grid_size)
    nontiled_throughputs.append(nontiled_throughput)
    
    # Tiled throughput
    tiled_cycles = algorithm_data[wse_type]['Tiled (r=1)']
    tiled_grid_size = get_max_grid_size(wse_type, 'Tiled (r=1)')
    tiled_throughput = calculate_throughput(tiled_cycles, clock_rate, tiled_grid_size)
    tiled_throughputs.append(tiled_throughput)

# Create bar plot
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, tiled_throughputs, width, label='Tiled (r1-optimized)', color=light_blue)
rects2 = ax.bar(x + width/2, nontiled_throughputs, width, label='Single-cell', color=blue)

# Add some text for labels, title and axes ticks
ax.set_ylabel('Throughput (Gcells/s)')
ax.set_title('Algorithm Comparison: Throughput at Maximum Grid Size')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Add value labels on bars
ax.bar_label(rects1, padding=3, fmt='%.1f')  # tiled bars
ax.bar_label(rects2, padding=3, fmt='%.1f')  # non-tiled bars

fig.tight_layout()
plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# Save the plot
plt.savefig('algo_comparison.png', dpi=300, bbox_inches='tight')
print("Algorithm comparison plot saved as 'algo_comparison.png'")

# Print detailed results
print("\nAlgorithm Comparison Results:")
print("=" * 70)
print(f"{'WSE Type':<10} {'Algorithm':<20} {'Grid Size':<15} {'Throughput (Gcells/s)':<20}")
print("-" * 70)

for i, wse_type in enumerate(['WSE2', 'WSE3']):
    # Tiled results
    tiled_grid = get_max_grid_size(wse_type, 'Tiled (r=1)')
    print(f"{wse_type:<10} {'Tiled (r1-optimized)':<20} {tiled_grid:<15,} {tiled_throughputs[i]:<20.1f}")
    
    # Non-tiled results
    nontiled_grid = get_max_grid_size(wse_type, 'Non-tiled (r=1)')
    print(f"{wse_type:<10} {'Single-cell':<20} {nontiled_grid:<15,} {nontiled_throughputs[i]:<20.1f}")
    print()

print("=" * 70)
print("Notes:")
print("- Single-cell: 1 cell per PE (limited by WSE physical dimensions)")
print("- Tiled (r1-optimized): 1×1 tiles (1 cell per PE, same grid size but with tiled algorithm overhead)")
print(f"- WSE-2 dimensions: {WSE2_DIMENSIONS[0]}×{WSE2_DIMENSIONS[1]} = {WSE2_DIMENSIONS[0]*WSE2_DIMENSIONS[1]:,} PEs")
print(f"- WSE-3 dimensions: {WSE3_DIMENSIONS[0]}×{WSE3_DIMENSIONS[1]} = {WSE3_DIMENSIONS[0]*WSE3_DIMENSIONS[1]:,} PEs")

plt.show() 