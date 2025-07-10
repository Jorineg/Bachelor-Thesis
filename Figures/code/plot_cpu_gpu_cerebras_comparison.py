# Iterations per Second (IPS) by Hardware and Radius:
# =======================================================
# CPU:
#   r=1: 382.059 IPS
#   r=2: 239.149 IPS
#   r=3: 181.077 IPS
#   r=4: 157.401 IPS
#   r=5: 120.389 IPS
#   r=6: 99.069 IPS

# GPU:
#   r=1: 13140.604 IPS
#   r=2: 12642.225 IPS
#   r=3: 12004.802 IPS
#   r=4: 11918.951 IPS
#   r=5: 10471.204 IPS
#   r=6: 10000.000 IPS

# WSE2:
#   r=1: 3046594.982 IPS
#   r=2: 1426174.497 IPS
#   r=3: 849150.849 IPS
#   r=4: 495915.986 IPS
#   r=5: 387243.736 IPS
#   r=6: 252225.519 IPS

# WSE3:
#   r=1: 3600823.045 IPS
#   r=2: 1171352.075 IPS
#   r=3: 749143.836 IPS
#   r=4: 473484.848 IPS
#   r=5: 332194.381 IPS
#   r=6: 239529.154 IPS
# =======================================================

# Speedup Calculations:
# =======================================================
# GPU vs CPU Speedup:
#   r=1: 34.4x
#   r=2: 52.9x
#   r=4: 75.7x
#   r=6: 100.9x

# WSE2 vs GPU Speedup:
#   r=1: 231.8x
#   r=2: 112.8x
#   r=4: 41.6x
#   r=6: 25.2x

# WSE3 vs GPU Speedup:
#   r=1: 274.0x
#   r=2: 92.7x
#   r=4: 39.7x
#   r=6: 24.0x
# =======================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from colors import light_blue_to_light_green, light_blue_to_blue_3, light_blue_to_blue_4, blue_to_green_4, blue_to_green_5, light_blue, blue, light_green, green, light_red, red

colors = [light_blue, blue, light_green, green, light_red, red]

matplotlib.use('Agg')

# Constants
CEREBRAS_WSE2_CLOCK_RATE = 850e6
CEREBRAS_WSE3_CLOCK_RATE = 875e6
N_ITERATIONS = 1000

# Data for CPU
cpu_times = {
    1: 2.6174,
    2: 4.1815,
    3: 5.5225,
    4: 6.3532,
    5: 8.3064,
    6: 10.0940,
}
cpu_ips = {r: N_ITERATIONS / t for r, t in cpu_times.items()}

# Data for GPU
gpu_times = {
    1: 0.0761,
    2: 0.0791,
    3: 0.0833,
    4: 0.0839,
    5: 0.0955,
    6: 0.1000,
}
gpu_ips = {r: N_ITERATIONS / t for r, t in gpu_times.items()}

# Data for WSE2 (using 11xX tile sizes)
wse2_cycles_per_iter = {
    1: 279,
    2: 596,
    3: 1001,
    4: 1714,
    5: 2195,
    6: 3370,
}
wse2_ips = {r: CEREBRAS_WSE2_CLOCK_RATE / c for r, c in wse2_cycles_per_iter.items()}

# Data for WSE3 (using 14xX tile sizes)
wse3_cycles_per_iter = {
    1: 243,
    2: 747,
    3: 1168,
    4: 1848,
    5: 2634,
    6: 3653,
}
wse3_ips = {r: CEREBRAS_WSE3_CLOCK_RATE / c for r, c in wse3_cycles_per_iter.items()}

radii = [1, 2, 4, 6]

# Print all iterations per second values with 3 decimal places
print("Iterations per Second (IPS) by Hardware and Radius:")
print("=" * 55)

print("CPU:")
for r in sorted(cpu_ips.keys()):
    print(f"  r={r}: {cpu_ips[r]:.3f} IPS")

print("\nGPU:")
for r in sorted(gpu_ips.keys()):
    print(f"  r={r}: {gpu_ips[r]:.3f} IPS")

print("\nWSE2:")
for r in sorted(wse2_ips.keys()):
    print(f"  r={r}: {wse2_ips[r]:.3f} IPS")

print("\nWSE3:")
for r in sorted(wse3_ips.keys()):
    print(f"  r={r}: {wse3_ips[r]:.3f} IPS")

print("=" * 55)

# Calculate and print speedups
print("\nSpeedup Calculations:")
print("=" * 55)

print("GPU vs CPU Speedup:")
for r in radii:
    if r in cpu_ips and r in gpu_ips:
        speedup = gpu_ips[r] / cpu_ips[r]
        print(f"  r={r}: {speedup:.1f}x")

print("\nWSE2 vs GPU Speedup:")
for r in radii:
    if r in gpu_ips and r in wse2_ips:
        speedup = wse2_ips[r] / gpu_ips[r]
        print(f"  r={r}: {speedup:.1f}x")

print("\nWSE3 vs GPU Speedup:")
for r in radii:
    if r in gpu_ips and r in wse3_ips:
        speedup = wse3_ips[r] / gpu_ips[r]
        print(f"  r={r}: {speedup:.1f}x")

print("=" * 55)
print()

# Prepare data for plotting
# To disable a hardware platform, simply comment it out in the list below
labels = [
    # 'WSE2',
    'WSE3',
    'GPU',
    'CPU',
]

data = {
    'WSE2': [wse2_ips[r] for r in radii],
    'WSE3': [wse3_ips[r] for r in radii],
    'GPU': [gpu_ips[r] for r in radii],
    'CPU': [cpu_ips[r] for r in radii],
}

r_values = list(data.values())[0]

# Plotting
x = np.arange(len(labels))
width = 0.2
n = len(radii)

fig, ax = plt.subplots(figsize=(10, 6))

def custom_format(y):
    s = f'{y:.1e}'
    parts = s.split('e')
    return f"{parts[0]}e{int(parts[1])}"

for i, r in enumerate(radii):
    offset = (i - n / 2 + 0.5) * width
    values = [data[label][i] for label in labels]
    rects = ax.bar(x + offset, values, width, label=f'r={r}', color=light_blue_to_blue_4[i])
    ax.bar_label(rects, padding=3, fmt=custom_format, fontsize=12)

# Add some text for labels, title and axes ticks.
ax.set_ylabel('Iterations per Second (log scale)')
ax.set_title('Performance Comparison by Hardware and Stencil Radius')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='upper right')

ax.set_yscale('log')
ax.grid(axis='y', linestyle='--', alpha=0.7)

fig.tight_layout()
plt.savefig('cpu_gpu_cerebras_comparison.png')
print("Plot saved to cpu_gpu_cerebras_comparison.png")
