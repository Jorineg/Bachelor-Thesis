import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from colors import light_blue, blue, light_green, green, light_red, red

# Define the data
data = [
    {"Grid Size": "260x44", "Tile Size": "86x14", "Radius": 1, "WSE2 Cycles/Iter": 7741, "WSE3 Cycles/Iter": 5299},
    {"Grid Size": "262x46", "Tile Size": "86x14", "Radius": 2, "WSE2 Cycles/Iter": 16678, "WSE3 Cycles/Iter": 16696},
    {"Grid Size": "264x48", "Tile Size": "86x14", "Radius": 3, "WSE2 Cycles/Iter": 18305, "WSE3 Cycles/Iter": 18329},
    {"Grid Size": "266x50", "Tile Size": "86x14", "Radius": 4, "WSE2 Cycles/Iter": 27168, "WSE3 Cycles/Iter": 27253},
    {"Grid Size": "268x52", "Tile Size": "86x14", "Radius": 5, "WSE2 Cycles/Iter": 33304, "WSE3 Cycles/Iter": 33699},
    {"Grid Size": "270x54", "Tile Size": "86x14", "Radius": 6, "WSE2 Cycles/Iter": 42663, "WSE3 Cycles/Iter": 42772},
    {"Grid Size": "44x29", "Tile Size": "14x9", "Radius": 1, "WSE2 Cycles/Iter": 841, "WSE3 Cycles/Iter": 676},
    {"Grid Size": "46x31", "Tile Size": "14x9", "Radius": 2, "WSE2 Cycles/Iter": 1656, "WSE3 Cycles/Iter": 1698},
    {"Grid Size": "48x33", "Tile Size": "14x9", "Radius": 3, "WSE2 Cycles/Iter": 2672, "WSE3 Cycles/Iter": 2703},
    {"Grid Size": "50x35", "Tile Size": "14x9", "Radius": 4, "WSE2 Cycles/Iter": 3190, "WSE3 Cycles/Iter": 3216},
    {"Grid Size": "52x37", "Tile Size": "14x9", "Radius": 5, "WSE2 Cycles/Iter": 4194, "WSE3 Cycles/Iter": 4256},
    {"Grid Size": "54x39", "Tile Size": "14x9", "Radius": 6, "WSE2 Cycles/Iter": 4753, "WSE3 Cycles/Iter": 4732},
    {"Grid Size": "44x5", "Tile Size": "14x1", "Radius": 1, "WSE2 Cycles/Iter": 232, "WSE3 Cycles/Iter": 243},
    {"Grid Size": "46x7", "Tile Size": "14x2", "Radius": 2, "WSE2 Cycles/Iter": 705, "WSE3 Cycles/Iter": 747},
    {"Grid Size": "48x9", "Tile Size": "14x3", "Radius": 3, "WSE2 Cycles/Iter": 1118, "WSE3 Cycles/Iter": 1168},
    {"Grid Size": "50x11", "Tile Size": "14x4", "Radius": 4, "WSE2 Cycles/Iter": 1809, "WSE3 Cycles/Iter": 1848},
    {"Grid Size": "52x13", "Tile Size": "14x5", "Radius": 5, "WSE2 Cycles/Iter": 2612, "WSE3 Cycles/Iter": 2635},
    {"Grid Size": "54x15", "Tile Size": "14x6", "Radius": 6, "WSE2 Cycles/Iter": 3643, "WSE3 Cycles/Iter": 3652},
    {"Grid Size": "8x5", "Tile Size": "2x1", "Radius": 1, "WSE2 Cycles/Iter": 131, "WSE3 Cycles/Iter": 162},
    {"Grid Size": "10x10", "Tile Size": "2x2", "Radius": 2, "WSE2 Cycles/Iter": 271, "WSE3 Cycles/Iter": 339},
    {"Grid Size": "15x15", "Tile Size": "3x3", "Radius": 3, "WSE2 Cycles/Iter": 450, "WSE3 Cycles/Iter": 526},
    {"Grid Size": "20x20", "Tile Size": "4x4", "Radius": 4, "WSE2 Cycles/Iter": 775, "WSE3 Cycles/Iter": 808},
    {"Grid Size": "25x25", "Tile Size": "5x5", "Radius": 5, "WSE2 Cycles/Iter": 1364, "WSE3 Cycles/Iter": 1389},
    {"Grid Size": "30x30", "Tile Size": "6x6", "Radius": 6, "WSE2 Cycles/Iter": 1859, "WSE3 Cycles/Iter": 1879},
    {"Grid Size": "5x5", "Tile Size": "1x1", "Radius": 1, "WSE2 Cycles/Iter": 127, "WSE3 Cycles/Iter": 157},
    {"Grid Size": "64x64", "Tile Size": "64x64", "Radius": 1, "WSE2 Cycles/Iter": 25270, "WSE3 Cycles/Iter": 16924},
    {"Grid Size": "64x64", "Tile Size": "64x64", "Radius": 2, "WSE2 Cycles/Iter": 42358, "WSE3 Cycles/Iter": 42238},
    {"Grid Size": "64x64", "Tile Size": "64x64", "Radius": 3, "WSE2 Cycles/Iter": 71647, "WSE3 Cycles/Iter": 71460},
]

# Constants
WSE2_PEAK_PERFORMANCE_PER_PE = 2  # flops/cycle
WSE3_PEAK_PERFORMANCE_PER_PE = 4  # flops/cycle
USE_RADII = [1, 2, 4, 6]  # Only plot these radii

def parse_tile_size(tile_size_str):
    """Parse tile size string like '86x14' and return width, height, and product"""
    width, height = map(int, tile_size_str.split('x'))
    return width, height, width * height

def calculate_percent_pflops(tile_width, tile_height, radius, cycles_per_iter, peak_performance):
    """Calculate percentage of peak FLOPS"""
    # Determine algorithm and flops per cell per iteration
    if radius == 1:
        flops_per_cell_per_iter = 6  # r1 optimized version
    else:
        flops_per_cell_per_iter = 9  # normal version
    
    # Calculate total flops for 1 PE
    total_flops_per_iter = tile_height * tile_width * flops_per_cell_per_iter
    
    # Calculate flops per cycle
    flops_per_cycle = total_flops_per_iter / cycles_per_iter
    
    # Calculate percentage of peak performance
    percent_pflops = (flops_per_cycle / peak_performance) * 100
    
    return percent_pflops

# Process data for both WSE2 and WSE3
wse2_tile_products = []
wse2_percent_pflops_list = []
wse2_radii = []

wse3_tile_products = []
wse3_percent_pflops_list = []
wse3_radii = []

for entry in data:
    radius = entry["Radius"]
    # Filter for only the desired radii
    if radius not in USE_RADII:
        continue
        
    tile_width, tile_height, tile_product = parse_tile_size(entry["Tile Size"])
    
    # WSE2 data
    wse2_cycles_per_iter = entry["WSE2 Cycles/Iter"]
    wse2_percent_pflops = calculate_percent_pflops(tile_width, tile_height, radius, wse2_cycles_per_iter, WSE2_PEAK_PERFORMANCE_PER_PE)
    
    wse2_tile_products.append(tile_product)
    wse2_percent_pflops_list.append(wse2_percent_pflops)
    wse2_radii.append(radius)
    
    # WSE3 data
    wse3_cycles_per_iter = entry["WSE3 Cycles/Iter"]
    wse3_percent_pflops = calculate_percent_pflops(tile_width, tile_height, radius, wse3_cycles_per_iter, WSE3_PEAK_PERFORMANCE_PER_PE)
    
    wse3_tile_products.append(tile_product)
    wse3_percent_pflops_list.append(wse3_percent_pflops)
    wse3_radii.append(radius)

# Create DataFrames for easier plotting
df_wse2 = pd.DataFrame({
    'Tile Product': wse2_tile_products,
    'Percent PFLOPS': wse2_percent_pflops_list,
    'Radius': wse2_radii
})

df_wse3 = pd.DataFrame({
    'Tile Product': wse3_tile_products,
    'Percent PFLOPS': wse3_percent_pflops_list,
    'Radius': wse3_radii
})

# Create the plot
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate non-tiled performance for both WSE2 and WSE3
non_tiled_tile_product = 1  # 1x1 tile
non_tiled_wse2_cycles = 16
non_tiled_wse3_cycles = 23
non_tiled_wse2_percent_pflops = calculate_percent_pflops(1, 1, 1, non_tiled_wse2_cycles, WSE2_PEAK_PERFORMANCE_PER_PE)
non_tiled_wse3_percent_pflops = calculate_percent_pflops(1, 1, 1, non_tiled_wse3_cycles, WSE3_PEAK_PERFORMANCE_PER_PE)

# Get unique radii and assign colors from the consistent color scheme
unique_radii = sorted(df_wse3['Radius'].unique())
color_map = {1: light_blue, 2: blue, 4: light_green, 6: green}

# Plot non-tiled version first
ax.plot(non_tiled_tile_product, non_tiled_wse2_percent_pflops, 
        'o', color=light_red, markersize=8, alpha=0.8)
ax.plot(non_tiled_tile_product, non_tiled_wse3_percent_pflops, 
        '^', color=light_red, markersize=8, alpha=0.8)

# Plot WSE2 data (dotted lines with round markers)
for radius in unique_radii:
    data_subset = df_wse2[df_wse2['Radius'] == radius].sort_values('Tile Product')
    ax.plot(data_subset['Tile Product'], data_subset['Percent PFLOPS'], 
            'o:', color=color_map[radius], 
            markersize=6, linewidth=2, alpha=0.8)

# Plot WSE3 data (solid lines with triangle markers)
for radius in unique_radii:
    data_subset = df_wse3[df_wse3['Radius'] == radius].sort_values('Tile Product')
    ax.plot(data_subset['Tile Product'], data_subset['Percent PFLOPS'], 
            '^-', color=color_map[radius], 
            markersize=6, linewidth=2, alpha=0.8)

ax.set_xscale('log')
ax.set_xlabel('Tile Size (Product)', fontsize=12)
ax.set_ylabel('Percent of Peak FLOPS (%)', fontsize=12)
ax.set_title('WSE2 vs WSE3 Performance: Percentage of Peak FLOPS vs Tile Size', fontsize=14)

# Create custom legends
legend_elements_params = [
    Line2D([0], [0], color=light_red, lw=2, 
           label='Radius 1 (non-tiled)')
]
legend_elements_params.extend([
    Line2D([0], [0], color=color_map[radius], lw=2, 
           label=f'Radius {radius}') 
    for radius in unique_radii
])

legend_elements_wse = [
    Line2D([0], [0], color='black', lw=2, linestyle=':', marker='o', 
           markersize=6, label='WSE2'),
    Line2D([0], [0], color='black', lw=2, linestyle='-', marker='^', 
           markersize=6, label='WSE3')
]

# Create first legend for the parameter sets
first_legend = ax.legend(handles=legend_elements_params, loc='upper left', title='Radius', bbox_to_anchor=(0, 1))
ax.add_artist(first_legend)

# Create second legend for the WSE versions
ax.legend(handles=legend_elements_wse, loc='upper left', title='WSE Version', bbox_to_anchor=(0, 0.7))

# Customize grid
ax.grid(True, which="major", linestyle='--', alpha=0.7)
ax.grid(True, which="minor", linestyle=':', alpha=0.5)

# Show the plot
# plt.show()
plt.savefig('percent_pflops.png', dpi=300, bbox_inches='tight')

# Print some summary statistics
print("Summary Statistics:")
print(f"WSE2 Peak Performance per PE: {WSE2_PEAK_PERFORMANCE_PER_PE} flops/cycle")
print(f"WSE3 Peak Performance per PE: {WSE3_PEAK_PERFORMANCE_PER_PE} flops/cycle")
print(f"Number of experiments (filtered): {len(wse3_tile_products)}")
print(f"Radii plotted: {USE_RADII}")
print(f"Tile product range: {min(wse3_tile_products)} to {max(wse3_tile_products)}")
print(f"WSE2 Percent PFLOPS range: {min(wse2_percent_pflops_list):.2f}% to {max(wse2_percent_pflops_list):.2f}%")
print(f"WSE3 Percent PFLOPS range: {min(wse3_percent_pflops_list):.2f}% to {max(wse3_percent_pflops_list):.2f}%")
print(f"Algorithm selection: Radius 1 → r1 optimized (6 flops/cell), Others → normal (9 flops/cell)")
print(f"Non-tiled version: Tile 1x1 → WSE2: {non_tiled_wse2_cycles} cycles/iter ({non_tiled_wse2_percent_pflops:.2f}%), WSE3: {non_tiled_wse3_cycles} cycles/iter ({non_tiled_wse3_percent_pflops:.2f}%)")
print(f"Plot saved as 'percent_pflops.png'")

# Show constant product analysis
print("\nConstant Product Analysis:")
print("Tile Product | Radius |    WSE2 %    |    WSE3 %")
print("-" * 50)
print(f"          1 | 1 (NT) | {non_tiled_wse2_percent_pflops:12.2f} | {non_tiled_wse3_percent_pflops:12.2f}")  # Non-tiled entry
for product in sorted(df_wse3['Tile Product'].unique()):
    wse2_subset = df_wse2[df_wse2['Tile Product'] == product].sort_values('Radius')
    wse3_subset = df_wse3[df_wse3['Tile Product'] == product].sort_values('Radius')
    
    for (_, wse2_row), (_, wse3_row) in zip(wse2_subset.iterrows(), wse3_subset.iterrows()):
        print(f"{product:11} | {wse2_row['Radius']:6} | {wse2_row['Percent PFLOPS']:12.2f} | {wse3_row['Percent PFLOPS']:12.2f}")
