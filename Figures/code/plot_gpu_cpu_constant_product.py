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
    1e5:  {1: 157,  2: 339,  3: 526,  4: 808,  5: 1389, 6: 1879},  # r=1 overridden below
    1e4:  {1: 157,  2: 339,  3: 526,  4: 808,  5: 1389, 6: 1879},  # r=1 overridden below
}

# Build DataFrame for WSE3
wse3_rows = []
for grid_size, radius_dict in wse3_cycles.items():
    for radius, cycles in radius_dict.items():
        eff_cycles = 23 if (radius == 1 and grid_size <= MAX_ON_CHIP_GRID) else cycles
        time_s = cycles_to_time(eff_cycles, grid_size)
        wse3_rows.append({'Grid Size': grid_size, 'Radius': radius, 'WSE3 Time (s)': time_s})

df_wse3 = pd.DataFrame(wse3_rows)

# ------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

radii_sorted = sorted(df_cpu_gpu['Radius'].unique())
colors = plt.cm.viridis(np.linspace(0, 1, len(radii_sorted)))

for i, radius in enumerate(radii_sorted):
    # CPU / GPU lines
    df_rad = df_cpu_gpu[df_cpu_gpu['Radius'] == radius].sort_values('Grid Size')
    ax.plot(df_rad['Grid Size'], df_rad['CPU Time (s)'], linestyle='-',  color=colors[i])
    ax.plot(df_rad['Grid Size'], df_rad['GPU Time (s)'], linestyle='--', color=colors[i])

    # WSE3 line (may have fewer points)
    df_wse3_rad = df_wse3[df_wse3['Radius'] == radius].sort_values('Grid Size')
    if not df_wse3_rad.empty:
        ax.plot(df_wse3_rad['Grid Size'], df_wse3_rad['WSE3 Time (s)'], linestyle='-.', color=colors[i])

# Set log scale for x and y-axis for better visualization
ax.set_xscale('log')
ax.set_yscale('log')

# Adding titles and labels
ax.set_title('CPU vs GPU Performance for Stencil Operations')
ax.set_xlabel('Grid Size (Width × Height)')
ax.set_ylabel('Time (s)')

# Create custom legends
legend_elements_radius = [Line2D([0], [0], color=colors[i], lw=2, label=f'Radius {r}') for i, r in enumerate(radii_sorted)]

# Draw the radius legend first so it stays when device legend is added later
first_legend = plt.legend(handles=legend_elements_radius, loc='upper left', title='Radius')
ax.add_artist(first_legend)

legend_elements_device = [
    Line2D([0], [0], color='black', lw=2, linestyle='-',  label='CPU'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', label='GPU'),
    Line2D([0], [0], color='black', lw=2, linestyle='-.', label='WSE3')
]
plt.legend(handles=legend_elements_device, loc='lower right', title='Device')

ax.grid(True, which="both", ls="--")

# Save the plot
plt.savefig('gpu_cpu_wse3_constant_product.png', dpi=300, bbox_inches='tight')

print("Plot saved to gpu_cpu_wse3_constant_product.png")
