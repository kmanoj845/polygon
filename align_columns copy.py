import math

def is_lower_polygon_to_the_right_of_midpoint(upper_xs, lower_xs):
    """
    input: 
    upper_xs= (1, 6)
    lower_xs= (3, 9)
    """
    # Unpack x coordinates
    x1, x2 = upper_xs  # Upper xs
    x3, x4 = lower_xs   # Lower xs
    
    # Calculate the midpoint of the upper line
    midpoint_x = math.ceil((x1 + x2) / 2)

    # Check if the lower line starts to the right of the midpoint
    return x3 > midpoint_x


def group_columns(x_bounds, PROXIMITY):
    columns = []
    current_column = []
    for current_x_left, current_x_right in x_bounds:
        if not current_column:
            # Start a new column
            current_column.append((current_x_left, current_x_right))
        else:
            # Check if the new x-coordinates are within the proximity range of the current column
            # last_x_left, last_x_right = current_column[-1]    # Was creating issue when a lower row was cutting across 
                                                                # multiple columns
            first_x_left, first_x_right = current_column[0] # First element of column is considered for alignment
            if (
                (abs(current_x_left - first_x_left) <= PROXIMITY)   #Left alignment
                or
                # (   # Current left x between top ploygon xs
                #     (current_x_left > first_x_left) 
                #     and
                #     (current_x_left < first_x_right) 
                # )
                (   # Current polygon starts before the midpoint of first polygon
                    not is_lower_polygon_to_the_right_of_midpoint(
                        (first_x_left, first_x_right), 
                        (current_x_left, current_x_right)
                        )
                )
                or
                (abs(current_x_right - first_x_right) <= PROXIMITY) # Right alignment
                
            ):
                current_column.append((current_x_left, current_x_right))
            else:
                # Finalize the current column and start a new one
                columns.append(current_column)
                # pprint(current_column, '\n')
                current_column = [(current_x_left, current_x_right)]
    
    # Append the last column if not empty
    if current_column:
        columns.append(current_column)
    return columns


def arrange_data(data, PROXIMITY):
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
    columns = group_columns(x_bounds, PROXIMITY) # proximity in pixels
    # pprint(columns)
    # Map x-coordinate to column index
    x_to_col = {}
    for col_idx, col_xs in enumerate(columns):
        for x_left, x_right in col_xs:
            x_to_col[(x_left, x_right)] = col_idx

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

