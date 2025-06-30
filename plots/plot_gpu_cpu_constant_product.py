import matplotlib.pyplot as plt
import pandas as pd
import io
import numpy as np
from matplotlib.lines import Line2D

# Data from the user
data = """
Width,Height,Radius,Iterations (N),CPU Time (s),GPU Time (s)
100,1000,1,100000,3.0084,1.1863
100,1000,2,100000,6.6235,1.1865
100,1000,3,100000,8.7346,1.0426
100,1000,4,100000,9.2117,1.0335
1000,1000,1,10000,2.3059,0.1662
1000,1000,2,10000,3.9838,0.1545
1000,1000,3,10000,6.1400,0.1584
1000,1000,4,10000,8.8315,0.1606
1000,10000,1,1000,3.1960,0.0791
1000,10000,2,1000,5.2773,0.0822
1000,10000,3,1000,7.3144,0.0892
1000,10000,4,1000,8.6900,0.0894
10000,10000,1,100,4.5866,0.1581
10000,10000,2,100,5.7850,0.1607
10000,10000,3,100,7.0106,0.1631
10000,10000,4,100,8.6211,0.1629
100000,10000,1,10,3.7215,1.0044
100000,10000,2,10,5.3538,1.0080
100000,10000,3,10,7.1955,1.0105
100000,10000,4,10,8.6839,1.0116
100,100,1,1000000,3.0581,11.3245
100,100,2,1000000,6.6062,11.3364
"""

df = pd.read_csv(io.StringIO(data))

# Plotting
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

radii = df['Radius'].unique()
colors = plt.cm.viridis(np.linspace(0, 1, len(radii)))

for i, radius in enumerate(radii):
    radius_data = df[df['Radius'] == radius]
    # The data needs to be sorted by Iterations for a correct line plot
    radius_data = radius_data.sort_values(by='Iterations (N)')
    
    ax.plot(radius_data['Iterations (N)'], radius_data['CPU Time (s)'], linestyle='-', color=colors[i])
    ax.plot(radius_data['Iterations (N)'], radius_data['GPU Time (s)'], linestyle='--', color=colors[i])

# Set log scale for x and y-axis for better visualization
ax.set_xscale('log')
ax.set_yscale('log')

# Adding titles and labels
ax.set_title('CPU vs GPU Performance for Stencil Operations')
ax.set_xlabel('Number of Iterations (N)')
ax.set_ylabel('Time (s)')

# Create custom legends
legend_elements_radius = [Line2D([0], [0], color=colors[i], lw=2, label=f'Radius {r}') for i, r in enumerate(radii)]
first_legend = plt.legend(handles=legend_elements_radius, loc='upper left', title='Radius')
ax.add_artist(first_legend)

legend_elements_device = [
    Line2D([0], [0], color='black', lw=2, linestyle='-', label='CPU'),
    Line2D([0], [0], color='black', lw=2, linestyle='--', label='GPU')
]
plt.legend(handles=legend_elements_device, loc='lower right', title='Device')

ax.grid(True, which="both", ls="--")

# Save the plot
plt.savefig('gpu_cpu_constant_product.png', dpi=300, bbox_inches='tight')

print("Plot saved to gpu_cpu_constant_product.png")
