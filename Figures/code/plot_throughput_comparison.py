import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from colors import light_blue, blue, light_green, green, light_red, red, blue_to_green_4

# Constants for WSE-3
CLOCK_FREQ = 1.1e9  # 1.1 GHz
PHYSICAL_WIDTH = 762  # P_w
PHYSICAL_HEIGHT = 1176  # P_h
USE_RADII = [1, 2, 6]

# Experimental data
experimental_data = [
    {"Grid Size": "5x5", "Tile Size": "1x1", "Radius": 1, "WSE3 Cycles/Iter": 157},
    {"Grid Size": "8x8", "Tile Size": "2x2", "Radius": 1, "WSE3 Cycles/Iter": 177},
    {"Grid Size": "10x10", "Tile Size": "2x2", "Radius": 2, "WSE3 Cycles/Iter": 339},
    {"Grid Size": "11x11", "Tile Size": "3x3", "Radius": 1, "WSE3 Cycles/Iter": 197},
    {"Grid Size": "13x13", "Tile Size": "3x3", "Radius": 2, "WSE3 Cycles/Iter": 419},
    {"Grid Size": "14x14", "Tile Size": "4x4", "Radius": 1, "WSE3 Cycles/Iter": 131},
    {"Grid Size": "16x16", "Tile Size": "4x4", "Radius": 2, "WSE3 Cycles/Iter": 478},
    {"Grid Size": "20x20", "Tile Size": "4x4", "Radius": 4, "WSE3 Cycles/Iter": 808},
    {"Grid Size": "17x17", "Tile Size": "5x5", "Radius": 1, "WSE3 Cycles/Iter": 191},
    {"Grid Size": "19x19", "Tile Size": "5x5", "Radius": 2, "WSE3 Cycles/Iter": 635},
    {"Grid Size": "23x23", "Tile Size": "5x5", "Radius": 4, "WSE3 Cycles/Iter": 1036},
    {"Grid Size": "23x23", "Tile Size": "7x7", "Radius": 1, "WSE3 Cycles/Iter": 297},
    {"Grid Size": "25x25", "Tile Size": "7x7", "Radius": 2, "WSE3 Cycles/Iter": 1003},
    {"Grid Size": "29x29", "Tile Size": "7x7", "Radius": 4, "WSE3 Cycles/Iter": 1875},
    {"Grid Size": "33x33", "Tile Size": "7x7", "Radius": 6, "WSE3 Cycles/Iter": 2645},
    {"Grid Size": "32x32", "Tile Size": "10x10", "Radius": 1, "WSE3 Cycles/Iter": 558},
    {"Grid Size": "34x34", "Tile Size": "10x10", "Radius": 2, "WSE3 Cycles/Iter": 1712},
    {"Grid Size": "38x38", "Tile Size": "10x10", "Radius": 4, "WSE3 Cycles/Iter": 2747},
    {"Grid Size": "42x42", "Tile Size": "10x10", "Radius": 6, "WSE3 Cycles/Iter": 4179},
    {"Grid Size": "47x47", "Tile Size": "15x15", "Radius": 1, "WSE3 Cycles/Iter": 1078},
    {"Grid Size": "49x49", "Tile Size": "15x15", "Radius": 2, "WSE3 Cycles/Iter": 3418},
    {"Grid Size": "53x53", "Tile Size": "15x15", "Radius": 4, "WSE3 Cycles/Iter": 6879},
    {"Grid Size": "57x57", "Tile Size": "15x15", "Radius": 6, "WSE3 Cycles/Iter": 9890},
    {"Grid Size": "62x62", "Tile Size": "20x20", "Radius": 1, "WSE3 Cycles/Iter": 1788},
    {"Grid Size": "64x64", "Tile Size": "20x20", "Radius": 2, "WSE3 Cycles/Iter": 4572},
    {"Grid Size": "68x68", "Tile Size": "20x20", "Radius": 4, "WSE3 Cycles/Iter": 9754},
    {"Grid Size": "72x72", "Tile Size": "20x20", "Radius": 6, "WSE3 Cycles/Iter": 13355},
    {"Grid Size": "77x77", "Tile Size": "25x25", "Radius": 1, "WSE3 Cycles/Iter": 2852},
    {"Grid Size": "79x79", "Tile Size": "25x25", "Radius": 2, "WSE3 Cycles/Iter": 8149},
    {"Grid Size": "83x83", "Tile Size": "25x25", "Radius": 4, "WSE3 Cycles/Iter": 14870},
    {"Grid Size": "87x87", "Tile Size": "25x25", "Radius": 6, "WSE3 Cycles/Iter": 22865},
    {"Grid Size": "92x92", "Tile Size": "30x30", "Radius": 1, "WSE3 Cycles/Iter": 3988},
    {"Grid Size": "94x94", "Tile Size": "30x30", "Radius": 2, "WSE3 Cycles/Iter": 12431},
    {"Grid Size": "98x98", "Tile Size": "30x30", "Radius": 4, "WSE3 Cycles/Iter": 20182},
    {"Grid Size": "102x102", "Tile Size": "30x30", "Radius": 6, "WSE3 Cycles/Iter": 31526},
    {"Grid Size": "122x122", "Tile Size": "40x40", "Radius": 1, "WSE3 Cycles/Iter": 6748},
    {"Grid Size": "124x124", "Tile Size": "40x40", "Radius": 2, "WSE3 Cycles/Iter": 16880},
    {"Grid Size": "128x128", "Tile Size": "40x40", "Radius": 4, "WSE3 Cycles/Iter": 36805},
    {"Grid Size": "132x132", "Tile Size": "40x40", "Radius": 6, "WSE3 Cycles/Iter": 50378},
    {"Grid Size": "152x152", "Tile Size": "50x50", "Radius": 1, "WSE3 Cycles/Iter": 10627},
    {"Grid Size": "154x154", "Tile Size": "50x50", "Radius": 2, "WSE3 Cycles/Iter": 33546},
    {"Grid Size": "158x158", "Tile Size": "50x50", "Radius": 4, "WSE3 Cycles/Iter": 54425},
    {"Grid Size": "162x162", "Tile Size": "50x50", "Radius": 6, "WSE3 Cycles/Iter": 85330},
    {"Grid Size": "182x182", "Tile Size": "60x60", "Radius": 1, "WSE3 Cycles/Iter": 14907},
    {"Grid Size": "184x184", "Tile Size": "60x60", "Radius": 2, "WSE3 Cycles/Iter": 37207},
    {"Grid Size": "188x188", "Tile Size": "60x60", "Radius": 4, "WSE3 Cycles/Iter": 81445},
    {"Grid Size": "192x192", "Tile Size": "60x60", "Radius": 6, "WSE3 Cycles/Iter": 111297},
    {"Grid Size": "192x192", "Tile Size": "64x64", "Radius": 1, "WSE3 Cycles/Iter": 16924},
    {"Grid Size": "194x194", "Tile Size": "64x64", "Radius": 2, "WSE3 Cycles/Iter": 42228},
    {"Grid Size": "198x198", "Tile Size": "64x64", "Radius": 4, "WSE3 Cycles/Iter": 92532},
]

def parse_tile_size(tile_size_str):
    """Parse tile size string like '4x4' and return width, height, and product"""
    width, height = map(int, tile_size_str.split('x'))
    return width, height, width * height

def calculate_c_comp(t_w, t_h, radius):
    """Calculate C_comp_iter based on equation from the document"""
    if radius == 1:
        # r1-optimized version: 4 @fadds (simd=4) + 2 @fmuls (simd=1)
        # n_fadds = 4, simd_fadds = 4, n_fmuls = 2, simd_fmuls = 1
        cycles = t_w * t_h * (4/4 + 2/1)  # = 3 * t_w * t_h
    else:
        # general implementation: 4r @fmacs (simd=1) + 1 @fmuls (simd=1)
        # n_fmacs = 4*r, simd_fmacs = 1, n_fmuls = 1, simd_fmuls = 1
        cycles = t_w * t_h * ((4*radius)/1 + 1/1)  # = 4*r * t_w * t_h + t_w * t_h
    return cycles

def calculate_c_comm(t_w, t_h, radius):
    """Calculate C_comm_iter based on equation from the document"""
    return 4 * radius * (t_w + t_h)

def calculate_throughput(cycles_per_iter, t_w, t_h):
    """Calculate throughput in Gcells/s based on equation from the document"""
    # T = P_h * P_w * f_clk * t_w * t_h / C_iter
    throughput = (PHYSICAL_HEIGHT * PHYSICAL_WIDTH * CLOCK_FREQ * t_w * t_h) / cycles_per_iter
    return throughput / 1e9  # Convert to Gcells/s

def calculate_theoretical_bounds(t_w, t_h, radius):
    """Calculate both theoretical upper bounds T_max and T_ours"""
    c_comp = calculate_c_comp(t_w, t_h, radius)
    c_comm = calculate_c_comm(t_w, t_h, radius)
    
    # T_max: perfect overlap (max of comp and comm)
    c_max_iter = max(c_comp, c_comm)
    t_max = calculate_throughput(c_max_iter, t_w, t_h)
    
    # T_ours: no overlap (sum of comp and comm)
    c_ours_iter = c_comp + c_comm
    t_ours = calculate_throughput(c_ours_iter, t_w, t_h)
    
    return t_max, t_ours

# Process experimental data
exp_tile_products = []
exp_throughputs = []
exp_radii = []

for entry in experimental_data:
    radius = entry["Radius"]
    if radius not in USE_RADII:
        continue
    
    t_w, t_h, tile_product = parse_tile_size(entry["Tile Size"])
    cycles_per_iter = entry["WSE3 Cycles/Iter"]
    
    throughput = calculate_throughput(cycles_per_iter, t_w, t_h)
    
    exp_tile_products.append(tile_product)
    exp_throughputs.append(throughput)
    exp_radii.append(radius)

# Calculate theoretical bounds for all square tile sizes 1x1 to 64x64
theoretical_data = []
for i in range(1, 65):  # 1 to 64 inclusive
    t_w = t_h = i
    tile_product = i * i
    
    for radius in USE_RADII:
        t_max, t_ours = calculate_theoretical_bounds(t_w, t_h, radius)
        theoretical_data.append({
            'Tile Product': tile_product,
            'Radius': radius,
            'T_max': t_max,
            'T_ours': t_ours
        })

# Create DataFrames
df_exp = pd.DataFrame({
    'Tile Product': exp_tile_products,
    'Throughput': exp_throughputs,
    'Radius': exp_radii
})

df_theoretical = pd.DataFrame(theoretical_data)

# Create the plot
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Color mapping for radii
color_map = {1: light_blue, 2: blue, 4: light_green, 6: green}

# Plot theoretical upper bounds with markers
for radius in USE_RADII:
    data_subset = df_theoretical[df_theoretical['Radius'] == radius].sort_values('Tile Product')
    
    # T_max (perfect overlap)
    ax.plot(data_subset['Tile Product'], data_subset['T_max'], 
            '-', color=color_map[radius], linewidth=1.5, 
            alpha=0.7)
    
    # T_ours (no overlap)
    ax.plot(data_subset['Tile Product'], data_subset['T_ours'], 
            '--', color=color_map[radius], linewidth=1.5, 
            alpha=0.7)

# Plot experimental data with lines and markers
for radius in USE_RADII:
    data_subset = df_exp[df_exp['Radius'] == radius].sort_values('Tile Product')
    if not data_subset.empty:
        # Plot both line and markers for experimental data
        ax.plot(data_subset['Tile Product'], data_subset['Throughput'], 
                '^:', color=color_map[radius], markersize=8, linewidth=2,
                alpha=1.0)

# Set log scale for both axes
ax.set_xscale('log')
ax.set_yscale('log')

# Set labels and title
ax.set_xlabel('Tile Size (Product)', fontsize=12)
ax.set_ylabel('Throughput (Gcells/s)', fontsize=12)
ax.set_title('WSE-3 Throughput: Experimental vs Theoretical Upper Bounds', fontsize=14)

# Create custom legends
legend_elements_bounds = [
    Line2D([0], [0], color='black', lw=2, linestyle='-', 
           label='T_max (perfect overlap)'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', 
           label='T_ours (no overlap)'),
    Line2D([0], [0], color='black', lw=2, linestyle=':', marker='^', 
           markersize=6, label='Experimental')
]

legend_elements_radii = [
    Line2D([0], [0], color=color_map[radius], lw=2, 
           label=f'Radius {radius}') 
    for radius in USE_RADII
]

# Create first legend for bounds types
first_legend = ax.legend(handles=legend_elements_bounds, loc='lower center', title='Data Type')
ax.add_artist(first_legend)

# Create second legend for radii
ax.legend(handles=legend_elements_radii, loc='lower right', title='Radius')

# Customize grid
ax.grid(True, which="major", linestyle='--', alpha=0.7)
ax.grid(True, which="minor", linestyle=':', alpha=0.5)

# Let matplotlib auto-scale the axes first, then adjust if needed
ax.autoscale()

# Save the plot
plt.tight_layout()
plt.savefig('throughput_comparison_wse3.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'throughput_comparison_wse3.png'")

# Print summary statistics
print("\nSummary Statistics:")
print(f"WSE-3 Constants:")
print(f"  Clock frequency: {CLOCK_FREQ/1e9:.1f} GHz")
print(f"  Physical dimensions: {PHYSICAL_WIDTH}×{PHYSICAL_HEIGHT} PEs")
print(f"  Total PEs: {PHYSICAL_WIDTH * PHYSICAL_HEIGHT:,}")
print(f"\nExperimental data points: {len(df_exp)}")
print(f"Theoretical data points per radius: {len(df_theoretical)//len(USE_RADII)}")
print(f"Radii analyzed: {USE_RADII}")
print(f"Tile product range: {min(df_theoretical['Tile Product'])} to {max(df_theoretical['Tile Product'])}")

# Print comparison table for experimental vs theoretical
print("\nExperimental vs Theoretical Comparison:")
print("Tile Size | Radius | Experimental | T_max | T_ours | Exp/T_max | Exp/T_ours")
print("-" * 80)
for _, exp_row in df_exp.iterrows():
    tile_product = exp_row['Tile Product']
    radius = exp_row['Radius']
    exp_throughput = exp_row['Throughput']
    
    theoretical_row = df_theoretical[
        (df_theoretical['Tile Product'] == tile_product) & 
        (df_theoretical['Radius'] == radius)
    ]
    
    if not theoretical_row.empty:
        t_max = theoretical_row['T_max'].iloc[0]
        t_ours = theoretical_row['T_ours'].iloc[0]
        
        print(f"{tile_product:8} | {radius:6} | {exp_throughput:12.2f} | {t_max:5.2f} | {t_ours:6.2f} | {exp_throughput/t_max:9.3f} | {exp_throughput/t_ours:10.3f}") 