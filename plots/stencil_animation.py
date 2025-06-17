import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

def create_stencil_animation():
    # Create figure with subplots using gridspec for better control over spacing
    fig, (ax_grid, ax_text) = plt.subplots(1, 2, figsize=(16, 8), 
                                           gridspec_kw={'width_ratios': [2.5, 1]})
    
    # Grid dimensions
    width, height = 9, 7
    
    # Green region boundaries
    green_left, green_right = 2, 6
    green_bottom, green_top = 2, 4
    green_width = green_right - green_left + 1  # 5
    green_height = green_top - green_bottom + 1  # 3
    
    def setup_grid():
        ax_grid.clear()
        
        # Create grid with individual squares
        for i in range(width):
            for j in range(height):
                # Determine color based on position
                if (green_left <= i <= green_right) and (green_bottom <= j <= green_top):
                    # Middle 5x3 area (green)
                    color = 'lightgreen'
                elif ((0 <= i <= 1) or (7 <= i <= 8)) and ((0 <= j <= 1) or (5 <= j <= 6)):
                    # Corner 2x2 areas (white)
                    color = 'white'
                else:
                    # Side areas (yellow)
                    color = 'yellow'
                    
                # Add square with black edge
                square = patches.Rectangle((i, j), 1, 1, linewidth=.5, edgecolor='grey', facecolor=color)
                ax_grid.add_patch(square)
        
        # Add a single robust outer border
        outer_border = patches.Rectangle((0, 0), width, height, linewidth=1, edgecolor='grey', facecolor='none', clip_on=False)
        ax_grid.add_patch(outer_border)
        
        # Set axis limits and aspect
        ax_grid.set_xlim(0, width)
        ax_grid.set_ylim(0, height)
        ax_grid.set_aspect('equal')
        ax_grid.axis('off')
        ax_grid.set_title('Stencil Algorithm Visualization')
    
    def setup_text_area():
        ax_text.clear()
        ax_text.set_xlim(0, 1)
        ax_text.set_ylim(0, 1)
        ax_text.axis('off')
        ax_text.set_title('Algorithm Steps')
    
    # Animation sequence:
    # Shifts: [up1, right1, down1, left1, up2, right2, down2, left2, center]
    # Note: matplotlib coordinates have y=0 at bottom, so up is positive dy, down is negative dy
    shifts = [
        (1, 0, 1, "up"),     # 1 up (positive dy)
        (0, 1, 1, "right"),  # 1 right  
        (-1, 0, 1, "down"),  # 1 down (negative dy)
        (0, -1, 1, "left"),  # 1 left
        (2, 0, 2, "up"),     # 2 up (positive dy)
        (0, 2, 2, "right"),  # 2 right
        (-2, 0, 2, "down"),  # 2 down (negative dy)
        (0, -2, 2, "left"),  # 2 left
        (0, 0, 0, "center")  # center (final step)
    ]
    
    # Pre-generate all text lines with LaTeX-style math formatting
    text_lines = [
        r"$acc = w_1 \cdot \mathrm{shift}(\mathrm{buf_c}, 1, \mathrm{UP})$",
        r"$acc = acc + w_1 \cdot \mathrm{shift}(\mathrm{buf_c}, 1, \mathrm{RIGHT})$",
        r"$acc = acc + w_1 \cdot \mathrm{shift}(\mathrm{buf_c}, 1, \mathrm{DOWN})$",
        r"$acc = acc + w_1 \cdot \mathrm{shift}(\mathrm{buf_c}, 1, \mathrm{LEFT})$",
        r"$acc = acc + w_2 \cdot \mathrm{shift}(\mathrm{buf_c}, 2, \mathrm{UP})$",
        r"$acc = acc + w_2 \cdot \mathrm{shift}(\mathrm{buf_c}, 2, \mathrm{RIGHT})$",
        r"$acc = acc + w_2 \cdot \mathrm{shift}(\mathrm{buf_c}, 2, \mathrm{DOWN})$",
        r"$acc = acc + w_2 \cdot \mathrm{shift}(\mathrm{buf_c}, 2, \mathrm{LEFT})$",
        r"$\mathrm{buf_c} = w_0 \cdot \mathrm{buf_c} + acc$"
    ]
    
    def animate(frame):
        setup_grid()
        setup_text_area()
        
        if frame < len(shifts):
            dy, dx, offset, direction = shifts[frame]
            
            # Calculate black rectangle position
            rect_x = green_left + dx
            rect_y = green_bottom + dy
            
            # Add black rectangle
            black_rect = patches.Rectangle(
                (rect_x, rect_y), green_width, green_height, 
                linewidth=4, edgecolor='black', facecolor='none'
            )
            ax_grid.add_patch(black_rect)
        
        # Display all text lines permanently with active indicator
        y_pos = 0.9
        for i in range(len(text_lines)):
            # Add black dot for active line
            if i == frame:
                ax_text.text(0, y_pos, '●', fontsize=17.5, 
                           transform=ax_text.transAxes, color='black')
            
            # Display text line (always show all lines)
            ax_text.text(0.08, y_pos, text_lines[i], fontsize=17.5, 
                       transform=ax_text.transAxes, color='black')
            y_pos -= 0.08
        
        # Add legend (always visible)
        legend_elements = [
            patches.Patch(color='lightgreen', label='Grid tile (computation area)'),
            patches.Patch(color='yellow', label='Halo region (neighbor data)'),
            patches.Patch(color='black', label='Current stencil access pattern')
        ]
        ax_grid.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))
    
    # Create animation
    ani = animation.FuncAnimation(
        fig, animate, frames=len(shifts), interval=2500, repeat=True
    )
    
    # Adjust layout manually for a smaller gap and proper padding
    fig.subplots_adjust(left=0, right=0.97, top=0.93, bottom=0.03, wspace=0.0)
    
    # Save as GIF
    print("Creating GIF animation... This might take a moment.")
    ani.save('stencil_algorithm_animation.gif', writer='pillow', fps=0.8, dpi=150)
    print("Animation saved as 'stencil_algorithm_animation.gif'")
    
    plt.show()
    return ani

if __name__ == "__main__":
    ani = create_stencil_animation() 