import matplotlib.pyplot as plt
import numpy as np
from colors import light_blue, blue, light_green, green, light_red, red

# Data
labels = ['WSE2', 'WSE3']
nontiled_values = [16, 23]
tiled_values = [127, 156]


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, nontiled_values, width, label='Non-tiled', color=light_blue)
rects2 = ax.bar(x + width/2, tiled_values, width, label='Tiled (r=1)', color=blue)

# Add some text for labels, title and axes ticks
ax.set_ylabel('Cycles per Iteration')
ax.set_title('Performance Comparison: Non-tiled vs. Tiled (r=1)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# Save the plot
plt.savefig('algo_comparison.png', dpi=300)

plt.show() 