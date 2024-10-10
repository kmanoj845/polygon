import numpy as np

def calculate_proximity(x_bounds):
    """Calculate proximity values between consecutive x-coordinates."""
    proximities = []
    for i in range(1, len(x_bounds)):
        prev_x_right = x_bounds[i - 1][1]
        curr_x_left = x_bounds[i][0]
        proximity = curr_x_left - prev_x_right
        proximities.append(proximity)
    print(proximities)
    return proximities

def find_median_proximity(data):
    """
    It accepts list of lists where each list is:
    [
    {'content': '157245', 
    'polygon': [{'x': 2087.0, 'y': 10.0}, 
    {'x': 2211.0, 'y': 8.0}, 
    {'x': 2212.0, 'y': 41.0}, 
    {'x': 2087.0, 'y': 40.0}], 
    'span': {'offset': 179, 'length': 6}, 'confidence': 0.995}
    ]
    """
    row_proximities = []
    for row in data:
        x_bounds = sorted(set((entry['polygon'][0]['x'], entry['polygon'][1]['x']) for entry in row))
        if len(x_bounds) > 1:
            # print(x_bounds)
            proximities = calculate_proximity(x_bounds)
            row_median_proximity = np.median(proximities) if proximities else 0
            row_proximities.append(row_median_proximity)
        # print(row_proximities)
    overall_median_proximity = np.median(row_proximities) if row_proximities else 0
    return overall_median_proximity


# # Find the median proximity
# median_proximity = find_median_proximity(merged_rows)

# print(f"Overall Median Proximity: {median_proximity}")








# merged_entries = count_non_empty_values(merged_rows)
# grid_size = cumulative_length(grid)

