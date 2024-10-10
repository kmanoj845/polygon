import numpy as np

def rotate_polygon(polygon, angle_degrees, center=(0, 0)):
    """
    input: polygon = [{'x': 7.0, 'y': 2.0}, {'x': 36.0, 'y': 2.0}, {'x': 36.0, 'y': 34.0}, {'x': 7.0, 'y': 34.0}]
    """
    angle_radians = np.radians(angle_degrees)
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)
    cx, cy = center
    rotated_polygon = []
    for point in polygon:
        # print(point)
        # Translate point to origin
        x_trans = point['x'] - cx
        y_trans = point['y'] - cy
        
        # Apply rotation matrix
        x_rot = x_trans * cos_theta - y_trans * sin_theta
        y_rot = x_trans * sin_theta + y_trans * cos_theta
        
        # Translate point back
        x_new = x_rot + cx
        y_new = y_rot + cy

        rotated_polygon.append({'x': float(np.round(x_new, 2)), 'y': float(np.round(y_new, 2))})
    
    return rotated_polygon
