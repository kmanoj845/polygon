import math
from pprint import pprint

def is_left_aligned(x_coords_first, x_coords_current, PROXIMITY):
    """
    input: 
    x_coords_first = (1, 6)
    x_coords_current = (3, 9) 
    """
    first_x_left, first_x_right = x_coords_first
    current_x_left, current_x_right = x_coords_current
    
    return abs(current_x_left - first_x_left) <= PROXIMITY


def is_right_aligned(x_coords_first, x_coords_current, PROXIMITY):
    """
    input: 
    x_coords_first = (1, 6)
    x_coords_current = (3, 9) 
    """
    first_x_left, first_x_right = x_coords_first
    current_x_left, current_x_right = x_coords_current
    
    return abs(current_x_right - first_x_right) <= PROXIMITY


def is_lower_polygon_starts_to_the_right_of_midpoint(x_coords_first, x_coords_current):
    """
    input: 
    x_coords_first = (1, 6)
    x_coords_current = (3, 9)
    """
    # Unpack x coordinates
    first_x_left, first_x_right = x_coords_first
    current_x_left, current_x_right = x_coords_current
    
    # Calculate the midpoint of the upper line
    midpoint_x = math.ceil((first_x_left + first_x_right) / 2)

    # Check if the lower line starts to the right of the midpoint
    return current_x_left > midpoint_x


def is_lower_polygon_starts_below(x_coords_first, x_coords_current):
    """
    input: 
    x_coords_first = (1, 6)
    x_coords_current = (3, 9)
    """
    # Unpack x coordinates
    first_x_left, first_x_right = x_coords_first
    current_x_left, current_x_right = x_coords_current

    return (
        (current_x_left > first_x_left)
        and
        (current_x_left < first_x_right)
        )


def is_lower_polygon_starts_to_the_right_of_midpoint(x_coords_first, x_coords_current):
    """
    input: 
    x_coords_first = (1, 6)
    x_coords_current = (3, 9)
    """
    # Unpack x coordinates
    first_x_left, first_x_right = x_coords_first
    current_x_left, current_x_right = x_coords_current
    
    # Calculate the midpoint of the upper line
    midpoint_x = math.ceil((first_x_left + first_x_right) / 2)

    # Check if the lower line starts to the right of the midpoint
    return current_x_left > midpoint_x


def left_or_right_or_below(x_coords_first, x_coords_current, PROXIMITY):
    """
    input: 
    x_coords_first = (1, 6)
    x_coords_current = (3, 9)
    """
    
    return (
        is_left_aligned(x_coords_first, x_coords_current, PROXIMITY)
        or
        is_right_aligned(x_coords_first, x_coords_current, PROXIMITY)
        or
        is_lower_polygon_starts_below(x_coords_first, x_coords_current)
    )


def left_or_before_midpoint(x_coords_first, x_coords_current, PROXIMITY):
    return (
        is_left_aligned(x_coords_first, x_coords_current, PROXIMITY)
        or
        not is_lower_polygon_starts_to_the_right_of_midpoint(x_coords_first, x_coords_current)
    )


def left_or_right_or_before_midpoint(x_coords_first, x_coords_current, PROXIMITY):
    return (
        is_left_aligned(x_coords_first, x_coords_current, PROXIMITY)
        or
        is_left_aligned(x_coords_first, x_coords_current, PROXIMITY)
        or
        not is_lower_polygon_starts_to_the_right_of_midpoint(x_coords_first, x_coords_current)
    )


def left_or_below(x_coords_first, x_coords_current, PROXIMITY):
    return (
        is_left_aligned(x_coords_first, x_coords_current, PROXIMITY)
        or
        is_lower_polygon_starts_below(x_coords_first, x_coords_current)
    )


function_map = {
    'left_or_right_or_below': left_or_right_or_below,
    'left_or_below': left_or_below,
    'left_or_before_midpoint': left_or_before_midpoint,
    'left_or_right_or_before_midpoint': left_or_right_or_before_midpoint,
    'left_alignment': is_left_aligned,
    'right_alignment': is_right_aligned
}


def group_columns(x_bounds, PROXIMITY, align_function_name):
    columns = []
    current_column = []
    # pprint(x_bounds)
    for x_coords_current in x_bounds:
        if not current_column:
            # Start a new column
            current_column.append(x_coords_current)
        else: # current_column[0] for first element, current_column[-1] for previous element
            if function_map[align_function_name](current_column[-1], x_coords_current, PROXIMITY):   #dynamically get
                current_column.append(x_coords_current)                                             #align function from function_map
            else:
                # Finalize the current column and start a new one
                columns.append(current_column)
                # pprint(current_column, '\n')
                current_column = [x_coords_current]
    
    # Append the last column if not empty
    if current_column:
        columns.append(current_column)
    return columns


def arrange_data(data, PROXIMITY, align_function_name):
    # Step 1: Collect all entries with their coordinates and row index
    entries = []
    for row_idx, row in enumerate(data):
        for entry in row:
            content = entry['content']
            x = entry['polygon'][0]['x']    # Left x
            y = entry['polygon'][0]['y']    # Left y
            right_x = entry['polygon'][1]['x']
            entries.append((content, x, y, right_x, row_idx))
    
    # Step 2: Sort entries by y-coordinate (top to bottom), then by x-coordinate (left to right)
    entries.sort(key=lambda e: (e[2], e[1]))
    x_bounds = sorted(set((x, right_x) for _, x, _, right_x, _ in entries))

    # Step 3: Determine columns based on proximity of left and right x-coordinates
    columns = group_columns(x_bounds, PROXIMITY, align_function_name) # proximity in pixels
    # pprint(columns)
    # Map x-coordinate to column index
    x_to_col = {}
    for col_idx, col_xs in enumerate(columns):
        for x_left, x_right in col_xs:
            x_to_col[(x_left, x_right)] = col_idx
    # pprint(x_to_col)
    # Step 4: Prepare the grid with the right dimensions
    max_row_idx = max(row_idx for _, _, _, _, row_idx in entries)
    max_columns = len(columns)
    grid = [['' for _ in range(max_columns)] for _ in range(max_row_idx + 1)]

    # Step 5: Populate the grid
    for content, x, y, right_x, row_idx in entries:
        # Find the closest column for the x-coordinate
        closest_col_idx = min(x_to_col.keys(), key=lambda bounds: abs(bounds[0] - x) + abs(bounds[1] - right_x))
        col_idx = x_to_col[closest_col_idx]
        if grid[row_idx][col_idx]:
            grid[row_idx][col_idx] = grid[row_idx][col_idx] + ' ' + content
        else:
            grid[row_idx][col_idx] = content
    
    return grid

