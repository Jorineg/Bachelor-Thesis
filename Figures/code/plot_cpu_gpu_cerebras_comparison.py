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
