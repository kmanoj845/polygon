import matplotlib.pyplot as plt
import matplotlib.patches as patches
import rotate_polygon as cp
import importlib
importlib.reload(cp)

def get_xy(polygon):
    return [(point['x'], point['y']) for point in polygon]

# Define polygons
polygon1 = [{'x': 744.0, 'y': 23.0}, {'x': 762.0, 'y': 23.0}, {'x': 762.0, 'y': 39.0}, {'x': 744.0, 'y': 39.0}]
polygon2 = [{'x': 181.0, 'y': 204.0}, {'x': 235.0, 'y': 201.0}, {'x': 235.0, 'y': 218.0}, {'x': 182.0, 'y': 219.0}]
# Define the parameters
center = (0, 0)  # define based on the need
angle = 0.84  # Angle in degrees

rotated_polygon1 = cp.rotate_polygon(polygon1, angle, center)
rotated_polygon2 = cp.rotate_polygon(polygon2, angle, center)

# Create a figure and axis
fig, ax = plt.subplots()

# Create patches for the original and rotated polygons
original_patch1 = patches.Polygon(get_xy(polygon1), closed=True, edgecolor='b', facecolor='none', linestyle='--', label='Polygon 1')
original_patch2 = patches.Polygon(get_xy(polygon2), closed=True, edgecolor='r', facecolor='none', linestyle='--', label='Polygon 2')

rotated_patch1 = patches.Polygon(get_xy(rotated_polygon1), closed=True, edgecolor='b', facecolor='none', linestyle='-', label='Rotated Polygon 1')
rotated_patch2 = patches.Polygon(get_xy(rotated_polygon2), closed=True, edgecolor='r', facecolor='none', linestyle='-', label='Rotated Polygon 2')

# Add patches to the plot
ax.add_patch(original_patch1)
ax.add_patch(original_patch2)

ax.add_patch(rotated_patch1)
ax.add_patch(rotated_patch2)


# Set plot limits
all_points = (
    get_xy(polygon1)
    + get_xy(polygon2)
    + get_xy(rotated_polygon1)
    + get_xy(rotated_polygon2)
)


x_vals, y_vals = zip(*all_points)
print(x_vals, y_vals)
ax.set_xlim(min(x_vals) - 10, max(x_vals) + 10)
ax.set_ylim(min(y_vals) - 10, max(y_vals) + 10)

# Add labels, legend, and title
ax.set_xlabel('X-axis (rightward)')
ax.set_ylabel('Y-axis (downward)')
ax.set_title('Polygons and Their Rotated Versions')
ax.legend()

# Show grid
ax.grid(True)

# Display the plot
plt.gca().invert_yaxis()  # Invert y-axis to match image coordinate system
plt.show()
