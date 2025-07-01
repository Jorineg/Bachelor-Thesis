# Iterations per Second (IPS) by Hardware and Radius:
# =======================================================
# CPU:
#   r=1: 312.891 IPS
#   r=2: 189.491 IPS
#   r=3: 136.717 IPS
#   r=4: 115.075 IPS

# GPU:
#   r=1: 12642.225 IPS
#   r=2: 12165.450 IPS
#   r=3: 11210.762 IPS
#   r=4: 11185.682 IPS

# WSE2:
#   r=1: 3942652.330 IPS
#   r=2: 1812191.104 IPS
#   r=3: 1098901.099 IPS
#   r=4: 642148.278 IPS

# WSE3:
#   r=1: 4526748.971 IPS
#   r=2: 1472556.894 IPS
#   r=3: 941780.822 IPS
#   r=4: 595238.095 IPS
# =======================================================


import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

# Constants
CEREBRAS_CLOCK_RATE = 1.1e9
N_ITERATIONS = 1000

# Data for CPU
cpu_times = {
    1: 3.1960,
    2: 5.2773,
    3: 7.3144,
    4: 8.6900,
}
cpu_ips = {r: N_ITERATIONS / t for r, t in cpu_times.items()}

# Data for GPU
gpu_times = {
    1: 0.0791,
    2: 0.0822,
    3: 0.0892,
    4: 0.0894,
}
gpu_ips = {r: N_ITERATIONS / t for r, t in gpu_times.items()}

# Data for WSE2 (using 11xX tile sizes)
wse2_cycles_per_iter = {
    1: 279,
    2: 607,
    3: 1001,
    4: 1713,
}
wse2_ips = {r: CEREBRAS_CLOCK_RATE / c for r, c in wse2_cycles_per_iter.items()}

# Data for WSE3 (using 14xX tile sizes)
wse3_cycles_per_iter = {
    1: 243,
    2: 747,
    3: 1168,
    4: 1848,
}
wse3_ips = {r: CEREBRAS_CLOCK_RATE / c for r, c in wse3_cycles_per_iter.items()}

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
print()

# Prepare data for plotting
# To disable a hardware platform, simply comment it out in the list below
labels = [
    # 'WSE2',
    'WSE3',
    'GPU',
    'CPU',
]
radii = [1, 2, 3, 4]
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

fig, ax = plt.subplots(figsize=(12, 8))

def custom_format(y):
    s = f'{y:.1e}'
    parts = s.split('e')
    return f"{parts[0]}e{int(parts[1])}"

for i, r in enumerate(radii):
    offset = (i - n / 2 + 0.5) * width
    values = [data[label][i] for label in labels]
    rects = ax.bar(x + offset, values, width, label=f'r={r}')
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
