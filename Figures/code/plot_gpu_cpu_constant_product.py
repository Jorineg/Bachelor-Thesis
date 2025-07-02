import matplotlib.pyplot as plt
import numpy as np
import io
import pandas as pd
from matplotlib.lines import Line2D

# Data from the user - updated with new experimental results
data = """
Width,Height,Radius,Iterations (N),CPU Time (s),GPU Time (s)
100,100,1,1000000,2.2112,9.7309
100,100,2,1000000,3.8160,9.7270
100,100,3,1000000,5.5279,9.7356
100,100,4,1000000,6.5409,9.7659
100,100,5,1000000,8.4157,9.7529
100,100,6,1000000,9.9961,9.7708
100,1000,1,100000,2.2146,1.0429
100,1000,2,100000,4.0623,1.0466
100,1000,3,100000,5.3653,1.0331
100,1000,4,100000,6.5379,1.0302
100,1000,5,100000,8.4115,1.0409
100,1000,6,100000,10.0371,1.0582
1000,1000,1,10000,1.6103,0.1487
1000,1000,2,10000,2.8188,0.1526
1000,1000,3,10000,4.4377,0.1582
1000,1000,4,10000,6.0163,0.1584
1000,1000,5,10000,7.9296,0.1669
1000,1000,6,10000,10.0127,0.1734
1000,10000,1,1000,2.6174,0.0761
1000,10000,2,1000,4.1815,0.0791
1000,10000,3,1000,5.5225,0.0833
1000,10000,4,1000,6.3532,0.0839
1000,10000,5,1000,8.3064,0.0955
1000,10000,6,1000,10.0940,0.1000
10000,10000,1,100,3.6835,0.1800
10000,10000,2,100,4.5234,0.1896
10000,10000,3,100,5.8971,0.1336
10000,10000,4,100,6.6253,0.1874
10000,10000,5,100,7.5088,0.1867
10000,10000,6,100,8.6515,0.1481
100000,10000,1,10,2.9368,0.7380
100000,10000,2,10,4.1719,0.7398
100000,10000,3,10,5.3896,0.7418
100000,10000,4,10,6.6300,0.7474
100000,10000,5,10,7.5125,0.7580
100000,10000,6,10,8.8995,0.7600
"""

# ------------------------------------------------------------------
# Parse CPU / GPU data (using pandas)
# ------------------------------------------------------------------

df_cpu_gpu = pd.read_csv(io.StringIO(data))
df_cpu_gpu['Grid Size'] = df_cpu_gpu['Width'] * df_cpu_gpu['Height']

# Compute throughput (iterations per second)
df_cpu_gpu['CPU Iter/s'] = df_cpu_gpu['Iterations (N)'] / df_cpu_gpu['CPU Time (s)']
df_cpu_gpu['GPU Iter/s'] = df_cpu_gpu['Iterations (N)'] / df_cpu_gpu['GPU Time (s)']
# Also add time in ms for plotting
df_cpu_gpu['CPU Time (ms)'] = df_cpu_gpu['CPU Time (s)'] * 1000
df_cpu_gpu['GPU Time (ms)'] = df_cpu_gpu['GPU Time (s)'] * 1000

# ---------------------------------
# Cerebras WSE3 data (cycles/iteration)
# ---------------------------------

# List of WSE3 measurements (cycles / iteration)
# Cycles have been obtained on a smaller simulated fabric but scale
# perfectly to larger grids.  We therefore associate each measurement
# with a *logical* grid-size (10^9 … 10^5) and compute the time that
# would be required for the constant-work baseline of 1×10^{10} stencil
# updates.

TOTAL_WORK = 10 ** 10
CLOCK_HZ = 1.1e9  # 1.1 GHz
MAX_ON_CHIP_GRID = 762 * 1176  # 896 112

USE_IPS = False

# Helper to convert cycles → seconds for given grid size
def cycles_to_time(cycles_per_iter: int, grid_size: float) -> float:
    iterations = TOTAL_WORK / grid_size
    return cycles_per_iter * iterations / CLOCK_HZ

# Cycles data organised by (grid_size, radius):
wse3_cycles = {
    1e9:  {1: 5299, 2: 16696, 3: 18329, 4: 27253, 5: 33699, 6: 42772},
    1e8:  {1: 676,  2: 1698,  3: 2703,  4: 3216,  5: 4256,  6: 4732},
    1e7:  {1: 243,  2: 747,  3: 1168,  4: 1848,  5: 2635,  6: 3652},
    1e6:  {1: 162,  2: 339,  3: 526,  4: 808,  5: 1389, 6: 1879},
    MAX_ON_CHIP_GRID:  {0: 23}, # r=1 overridden below
    1e5:  {1: 157,  2: 339,  3: 526,  4: 808,  5: 1389, 6: 1879},  # r=1 overridden below
    1e4:  {1: 157,  2: 339,  3: 526,  4: 808,  5: 1389, 6: 1879},  # r=1 overridden below
}

# Build DataFrame for WSE3
wse3_rows = []
for grid_size, radius_dict in wse3_cycles.items():
    for radius, cycles in radius_dict.items():
        if radius <= 1:
            # Add both tiled and non-tiled versions for radius 1
            if grid_size <= MAX_ON_CHIP_GRID:
                # Non-tiled version (23 cycles)
                time_s = cycles_to_time(23, grid_size)
                time_ms = time_s * 1000
                iter_per_sec = 1.0 / (23 / CLOCK_HZ)
                wse3_rows.append({'Grid Size': grid_size, 'Radius': 0, 'WSE3 Iter/s': iter_per_sec, 'WSE3 Time (s)': time_s, 'WSE3 Time (ms)': time_ms})
            
            if radius == 1:
                # Tiled version (original cycles)
                time_s = cycles_to_time(cycles, grid_size)
                time_ms = time_s * 1000
                iter_per_sec = 1.0 / (cycles / CLOCK_HZ)
                wse3_rows.append({'Grid Size': grid_size, 'Radius': radius, 'WSE3 Iter/s': iter_per_sec, 'WSE3 Time (s)': time_s, 'WSE3 Time (ms)': time_ms})
        else:
            # Other radii (unchanged)
            time_s = cycles_to_time(cycles, grid_size)
            time_ms = time_s * 1000
            iter_per_sec = 1.0 / (cycles / CLOCK_HZ)
            wse3_rows.append({'Grid Size': grid_size, 'Radius': radius, 'WSE3 Iter/s': iter_per_sec, 'WSE3 Time (s)': time_s, 'WSE3 Time (ms)': time_ms})

df_wse3 = pd.DataFrame(wse3_rows)

# ------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

# Get all unique radii from both CPU/GPU and WSE3 data
use_radii = [0, 1, 2, 4, 6]

cpu_gpu_radii = sorted(set(df_cpu_gpu['Radius'].unique()) & set(use_radii))
wse3_radii = sorted(set(df_wse3['Radius'].unique()) & set(use_radii))
all_radii = sorted(set(cpu_gpu_radii + wse3_radii))

# Create color mapping
colors = plt.cm.nipy_spectral(np.linspace(0.5, 0.1, len(all_radii)))
color_map = {radius: colors[i] for i, radius in enumerate(all_radii)}

metric = 'Iter/s' if USE_IPS else 'Time (ms)'

# Plot CPU/GPU data
for radius in cpu_gpu_radii:
    df_rad = df_cpu_gpu[df_cpu_gpu['Radius'] == radius].sort_values('Grid Size')
    ax.plot(df_rad['Grid Size'], df_rad['CPU ' + metric], linestyle='-',  color=color_map[radius], marker='o')
    ax.plot(df_rad['Grid Size'], df_rad['GPU ' + metric], linestyle='--', color=color_map[radius], marker='o')

# Plot WSE3 data
for radius in wse3_radii:
    df_wse3_rad = df_wse3[df_wse3['Radius'] == radius].sort_values('Grid Size')
    if not df_wse3_rad.empty:
        ax.plot(df_wse3_rad['Grid Size'], df_wse3_rad['WSE3 ' + metric], linestyle='-.', color=color_map[radius], marker='o')

# Set log scale for x and y-axis for better visualization
ax.set_xscale('log')
ax.set_yscale('log')

# Adding titles and labels
ax.set_title('CPU vs GPU vs WSE-3 Performance for Star-Shaped Stencil')
ax.set_xlabel('Grid Size (Width × Height)')
ylabel = 'Iterations per second' if USE_IPS else 'Time (ms) for constant work (grid size × iterations = 1e10)'
ax.set_ylabel(ylabel)

# Move legends
legend_elements_radius = []
for radius in all_radii:
    legend_elements_radius.append(Line2D([0], [0], color=color_map[radius], lw=2, label=f'Radius {radius if radius != 0 else "1 (non-tiled)"}'))

first_legend = plt.legend(handles=legend_elements_radius, loc='lower left', title='Radius')
ax.add_artist(first_legend)

legend_elements_device = [
    Line2D([0], [0], color='black', lw=2, linestyle='-',  marker='o', label='CPU'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', marker='o', label='GPU'),
    Line2D([0], [0], color='black', lw=2, linestyle='-.', marker='o', label='WSE-3')
]
plt.legend(handles=legend_elements_device, loc='lower center', title='Device')

ax.grid(True, which="both", ls="--")

# Save the plot
filename = 'gpu_cpu_wse3_constant_product_ips.png' if USE_IPS else 'gpu_cpu_wse3_constant_product.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Plot saved to {filename}")
