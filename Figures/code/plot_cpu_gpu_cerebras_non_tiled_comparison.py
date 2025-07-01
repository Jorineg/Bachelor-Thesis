# ===========================================================================

# WSE-2 Grid (750 x 994):
#   CPU: 8,080 IPS
#   GPU: 74,644 IPS
#   Cerebras Non-Tiled: 68,750,000 IPS

# WSE-3 Grid (762 x 1176):
#   CPU: 6,716 IPS
#   GPU: 70,398 IPS
#   Cerebras Non-Tiled: 47,826,087 IPS
# ===========================================================================

# Speedups:
# WSE-2: GPU vs CPU: 9×, Cerebras vs GPU: 921×, Cerebras vs CPU: 8508×
# WSE-3: GPU vs CPU: 10×, Cerebras vs GPU: 679×, Cerebras vs CPU: 7121×
# ===========================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

# Constants
CEREBRAS_CLOCK_RATE = 1.1e9  # 1.1 GHz

# WSE-2 data (750 x 994 grid)
wse2_cpu_time = 1.2376  # seconds for 10,000 iterations
wse2_cpu_iterations = 10000
wse2_cpu_ips = wse2_cpu_iterations / wse2_cpu_time

wse2_gpu_time = 1.3397  # seconds for 100,000 iterations
wse2_gpu_iterations = 100000
wse2_gpu_ips = wse2_gpu_iterations / wse2_gpu_time

wse2_cerebras_cycles_per_iter = 16
wse2_cerebras_ips = CEREBRAS_CLOCK_RATE / wse2_cerebras_cycles_per_iter

# WSE-3 data (762 x 1176 grid - corrected size)
wse3_cpu_time = 1.4889  # seconds for 10,000 iterations
wse3_cpu_iterations = 10000
wse3_cpu_ips = wse3_cpu_iterations / wse3_cpu_time

wse3_gpu_time = 1.4205  # seconds for 100,000 iterations
wse3_gpu_iterations = 100000
wse3_gpu_ips = wse3_gpu_iterations / wse3_gpu_time

wse3_cerebras_cycles_per_iter = 23
wse3_cerebras_ips = CEREBRAS_CLOCK_RATE / wse3_cerebras_cycles_per_iter

# Print all iterations per second values
print("Performance Comparison: CPU, GPU, and Cerebras Non-Tiled Implementation")
print("=" * 75)

print("\nWSE-2 Grid (750 x 994):")
print(f"  CPU: {wse2_cpu_ips:,.0f} IPS")
print(f"  GPU: {wse2_gpu_ips:,.0f} IPS")
print(f"  Cerebras Non-Tiled: {wse2_cerebras_ips:,.0f} IPS")

print("\nWSE-3 Grid (762 x 1176):")
print(f"  CPU: {wse3_cpu_ips:,.0f} IPS")
print(f"  GPU: {wse3_gpu_ips:,.0f} IPS")
print(f"  Cerebras Non-Tiled: {wse3_cerebras_ips:,.0f} IPS")

print("=" * 75)

# Print speedup information
print("\nSpeedups:")
for i, label in enumerate(['WSE-2', 'WSE-3']):
    cpu = [wse2_cpu_ips, wse3_cpu_ips][i]
    gpu = [wse2_gpu_ips, wse3_gpu_ips][i]
    cerebras = [wse2_cerebras_ips, wse3_cerebras_ips][i]
    
    speedup_gpu_vs_cpu = gpu / cpu
    speedup_cerebras_vs_gpu = cerebras / gpu
    speedup_cerebras_vs_cpu = cerebras / cpu
    
    print(f"{label}: GPU vs CPU: {speedup_gpu_vs_cpu:.0f}×, Cerebras vs GPU: {speedup_cerebras_vs_gpu:.0f}×, Cerebras vs CPU: {speedup_cerebras_vs_cpu:.0f}×")

print("=" * 75)
print()

# Prepare data for plotting
labels = ['WSE-2 Grid\n(750×994)', 'WSE-3 Grid\n(762×1176)']
cpu_data = [wse2_cpu_ips, wse3_cpu_ips]
gpu_data = [wse2_gpu_ips, wse3_gpu_ips]
cerebras_data = [wse2_cerebras_ips, wse3_cerebras_ips]

# Create grouped bar plot
x = np.arange(len(labels))
width = 0.25  # Width of individual bars
spacing = 0.8  # Total width of each group

fig, ax = plt.subplots(figsize=(12, 10))

# Create grouped bars
bars1 = ax.bar(x - width, cpu_data, width, label='CPU (AMD EPYC 9554)', color='#2E86AB', alpha=0.8)
bars2 = ax.bar(x, gpu_data, width, label='GPU (NVIDIA H100)', color='#A23B72', alpha=0.8)
bars3 = ax.bar(x + width, cerebras_data, width, label='Cerebras WSE (Non-Tiled)', color='#F18F01', alpha=0.8)

# Custom formatting function for scientific notation (same as other plot)
def custom_format(y):
    s = f'{y:.1e}'
    parts = s.split('e')
    return f"{parts[0]}e{int(parts[1])}"

# Add value labels above bars (same style as other plot)
ax.bar_label(bars1, padding=3, fmt=custom_format, fontsize=12)
ax.bar_label(bars2, padding=3, fmt=custom_format, fontsize=12)
ax.bar_label(bars3, padding=3, fmt=custom_format, fontsize=12)

# Customize plot
ax.set_ylabel('Iterations per Second (log scale)', fontsize=12, fontweight='bold')
ax.set_title('Performance Comparison: CPU, GPU, and Cerebras Non-Tiled Implementation\nfor Radius-1 Stencil', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

# Set log scale
ax.set_yscale('log')
ax.grid(axis='y', linestyle='--', alpha=0.3)

# Set y-axis limits to better show the differences
ax.set_ylim(1e3, 2e8)



plt.tight_layout()
plt.savefig('cpu_gpu_cerebras_non_tiled_comparison.png', dpi=300, bbox_inches='tight')
print("Plot saved to cpu_gpu_cerebras_non_tiled_comparison.png") 