# ========================================================================================================================
# PERFORMANCE COMPARISON TABLE
# ========================================================================================================================
# Grid Size  Radius Iterations CPU Time (s) GPU Time (s) WSE3 Time (s) GPU→CPU Speedup WSE3→GPU Speedup
#     1e+04     0.0      1e+06          N/A          N/A    2.0909e-02             N/A              N/A
#     1e+04     1.0      1e+06   2.2112e+00   9.7309e+00    1.4273e-01            0.23            68.18
#     1e+04     2.0      1e+06   3.8160e+00   9.7270e+00    3.0818e-01            0.39            31.56
#     1e+04     3.0      1e+06   5.5279e+00   9.7356e+00    4.7818e-01            0.57            20.36
#     1e+04     4.0      1e+06   6.5409e+00   9.7659e+00    7.3455e-01            0.67            13.30
#     1e+04     5.0      1e+06   8.4157e+00   9.7529e+00    1.2627e+00            0.86             7.72
#     1e+04     6.0      1e+06   9.9961e+00   9.7708e+00    1.7082e+00            1.02             5.72
#     1e+05     0.0      1e+05          N/A          N/A    2.0909e-03             N/A              N/A
#     1e+05     1.0      1e+05   2.2146e+00   1.0429e+00    1.4273e-02            2.12            73.07
#     1e+05     2.0      1e+05   4.0623e+00   1.0466e+00    3.0818e-02            3.88            33.96
#     1e+05     3.0      1e+05   5.3653e+00   1.0331e+00    4.7818e-02            5.19            21.60
#     1e+05     4.0      1e+05   6.5379e+00   1.0302e+00    7.3455e-02            6.35            14.03
#     1e+05     5.0      1e+05   8.4115e+00   1.0409e+00    1.2627e-01            8.08             8.24
#     1e+05     6.0      1e+05   1.0037e+01   1.0582e+00    1.7082e-01            9.49             6.19
#     9e+05     0.0      1e+04          N/A          N/A    2.3333e-04             N/A              N/A
#     1e+06     1.0      1e+04   1.6103e+00   1.4870e-01    1.4727e-03           10.83           100.97
#     1e+06     2.0      1e+04   2.8188e+00   1.5260e-01    3.0818e-03           18.47            49.52
#     1e+06     3.0      1e+04   4.4377e+00   1.5820e-01    4.7818e-03           28.05            33.08
#     1e+06     4.0      1e+04   6.0163e+00   1.5840e-01    7.3455e-03           37.98            21.56
#     1e+06     5.0      1e+04   7.9296e+00   1.6690e-01    1.2627e-02           47.51            13.22
#     1e+06     6.0      1e+04   1.0013e+01   1.7340e-01    1.7082e-02           57.74            10.15
#     1e+07     1.0      1e+03   2.6174e+00   7.6100e-02    2.2091e-04           34.39           344.49
#     1e+07     2.0      1e+03   4.1815e+00   7.9100e-02    6.7909e-04           52.86           116.48
#     1e+07     3.0      1e+03   5.5225e+00   8.3300e-02    1.0618e-03           66.30            78.45
#     1e+07     4.0      1e+03   6.3532e+00   8.3900e-02    1.6800e-03           75.72            49.94
#     1e+07     5.0      1e+03   8.3064e+00   9.5500e-02    2.3955e-03           86.98            39.87
#     1e+07     6.0      1e+03   1.0094e+01   1.0000e-01    3.3200e-03          100.94            30.12
#     1e+08     1.0      1e+02   3.6835e+00   1.8000e-01    6.1455e-05           20.46          2928.99
#     1e+08     2.0      1e+02   4.5234e+00   1.8960e-01    1.5436e-04           23.86          1228.27
#     1e+08     3.0      1e+02   5.8971e+00   1.3360e-01    2.4573e-04           44.14           543.69
#     1e+08     4.0      1e+02   6.6253e+00   1.8740e-01    2.9236e-04           35.35           640.98
#     1e+08     5.0      1e+02   7.5088e+00   1.8670e-01    3.8691e-04           40.22           482.54
#     1e+08     6.0      1e+02   8.6515e+00   1.4810e-01    4.3018e-04           58.42           344.27
#     1e+09     1.0      1e+01   2.9368e+00   7.3800e-01    4.8173e-05            3.98         15319.87
#     1e+09     2.0      1e+01   4.1719e+00   7.3980e-01    1.5178e-04            5.64          4874.10
#     1e+09     3.0      1e+01   5.3896e+00   7.4180e-01    1.6663e-04            7.27          4451.85
#     1e+09     4.0      1e+01   6.6300e+00   7.4740e-01    2.4775e-04            8.87          3016.70
#     1e+09     5.0      1e+01   7.5125e+00   7.5800e-01    3.0635e-04            9.91          2474.26
#     1e+09     6.0      1e+01   8.8995e+00   7.6000e-01    3.8884e-04           11.71          1954.55

# ========================================================================================================================

import matplotlib.pyplot as plt
import numpy as np
import io
import pandas as pd
from matplotlib.lines import Line2D
from colors import blue_to_green_4, light_blue, blue, light_green, green, light_red, red

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
WSE3_NON_TILED_CYCLES_PER_ITERATION = 23

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
    MAX_ON_CHIP_GRID:  {0: WSE3_NON_TILED_CYCLES_PER_ITERATION}, # r=1 overridden below
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
                time_s = cycles_to_time(WSE3_NON_TILED_CYCLES_PER_ITERATION, grid_size)
                time_ms = time_s * 1000
                iter_per_sec = 1.0 / (WSE3_NON_TILED_CYCLES_PER_ITERATION / CLOCK_HZ)
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
# Print consolidated performance table
# ------------------------------------------------------------------

print("=" * 120)
print("PERFORMANCE COMPARISON TABLE")
print("=" * 120)

# Create a consolidated table with all data
consolidated_data = []

# Get all unique combinations of grid size and radius from both datasets
all_combinations = set()
for _, row in df_cpu_gpu.iterrows():
    all_combinations.add((row['Grid Size'], row['Radius']))
for _, row in df_wse3.iterrows():
    all_combinations.add((row['Grid Size'], row['Radius']))

# Sort combinations by grid size, then radius
all_combinations = sorted(list(all_combinations))

for grid_size, radius in all_combinations:
    # Get CPU/GPU data
    cpu_gpu_row = df_cpu_gpu[(df_cpu_gpu['Grid Size'] == grid_size) & (df_cpu_gpu['Radius'] == radius)]
    # Get WSE3 data
    wse3_row = df_wse3[(df_wse3['Grid Size'] == grid_size) & (df_wse3['Radius'] == radius)]
    
    row_data = {
        'Grid Size': f'{grid_size:.0e}',
        'Radius': radius,
        'Iterations': 'N/A',
        'CPU Time (s)': 'N/A',
        'GPU Time (s)': 'N/A',
        'WSE3 Time (s)': 'N/A',
        'GPU→CPU Speedup': 'N/A',
        'WSE3→GPU Speedup': 'N/A'
    }
    
    if not cpu_gpu_row.empty:
        iterations = cpu_gpu_row['Iterations (N)'].iloc[0]
        cpu_time = cpu_gpu_row['CPU Time (s)'].iloc[0]
        gpu_time = cpu_gpu_row['GPU Time (s)'].iloc[0]
        
        row_data['Iterations'] = f'{iterations:.0e}'
        row_data['CPU Time (s)'] = f'{cpu_time:.4e}'
        row_data['GPU Time (s)'] = f'{gpu_time:.4e}'
        row_data['GPU→CPU Speedup'] = f'{cpu_time / gpu_time:.2f}'
        
        if not wse3_row.empty:
            wse3_time = wse3_row['WSE3 Time (s)'].iloc[0]
            row_data['WSE3 Time (s)'] = f'{wse3_time:.4e}'
            row_data['WSE3→GPU Speedup'] = f'{gpu_time / wse3_time:.2f}'
    
    elif not wse3_row.empty:
        # WSE3 only data (no corresponding CPU/GPU data)
        wse3_time = wse3_row['WSE3 Time (s)'].iloc[0]
        row_data['WSE3 Time (s)'] = f'{wse3_time:.4e}'
        # Calculate iterations based on constant work assumption
        iterations = TOTAL_WORK / grid_size
        row_data['Iterations'] = f'{iterations:.0e}'
    
    consolidated_data.append(row_data)

# Create DataFrame and print
df_consolidated = pd.DataFrame(consolidated_data)
print(df_consolidated.to_string(index=False))

print("\n" + "=" * 120)

# ------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Get all unique radii from both CPU/GPU and WSE3 data
use_radii = [0, 1, 2, 4, 6]

cpu_gpu_radii = sorted(set(df_cpu_gpu['Radius'].unique()) & set(use_radii))
wse3_radii = sorted(set(df_wse3['Radius'].unique()) & set(use_radii))
all_radii = sorted(set(cpu_gpu_radii + wse3_radii))

# Create color mapping
# colors = plt.cm.nipy_spectral(np.linspace(0.5, 0.1, len(all_radii)))
colors = [light_blue] + blue_to_green_4
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
        ax.plot(df_wse3_rad['Grid Size'], df_wse3_rad['WSE3 ' + metric], linestyle=':', color=color_map[radius], marker='o')

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
    Line2D([0], [0], color='black', lw=2, linestyle='-', label='CPU'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', label='GPU'),
    Line2D([0], [0], color='black', lw=2, linestyle=':', label='WSE-3')
]
plt.legend(handles=legend_elements_device, loc='lower center', title='Device')

ax.grid(True, which="both", ls="--")

# Save the plot
filename = 'gpu_cpu_wse3_constant_product_ips.png' if USE_IPS else 'gpu_cpu_wse3_constant_product.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Plot saved to {filename}")
