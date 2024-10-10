def are_polygons_close(polygon1, polygon2, threshold):
    """
    Determine if two polygons are close enough to merge based on their x-coordinates.
    """
    # Get the top right x-coordinate of the first polygon
    top_right_x = polygon1[1]['x']
    # Get the top left x-coordinate of the second polygon
    top_left_x = polygon2[0]['x']
    
    return top_left_x - top_right_x <= threshold

def merge_polygon_coordinates(polygon1, polygon2):
    """
    Merge two polygons into one by updating the coordinates to cover the full area.
    """
    # Extend the coordinates to cover both polygons
    all_x = [p['x'] for p in polygon1 + polygon2]
    all_y = [p['y'] for p in polygon1 + polygon2]
    
    merged_polygon = [
        {'x': min(all_x), 'y': min(all_y)},
        {'x': max(all_x), 'y': min(all_y)},
        {'x': max(all_x), 'y': max(all_y)},
        {'x': min(all_x), 'y': max(all_y)}
    ]
    
    return merged_polygon

def merge_close_polygons(data, MERGING_THRESHOLD):
    merged_data = []
    i = 0
    while i < len(data):
        current_item = data[i]
        if i + 1 < len(data):
            next_item = data[i + 1]
            
            if are_polygons_close(current_item['polygon'], next_item['polygon'], MERGING_THRESHOLD):
                # Merge the two items
                merged_polygon = merge_polygon_coordinates(current_item['polygon'], next_item['polygon'])
                merged_content = current_item['content'] + '' + next_item['content']
                
                merged_item = {
                    'content': merged_content,
                    'polygon': merged_polygon,
                    'span': current_item['span'],  # Assuming span is from the first item
                    'confidence': (current_item['confidence'] + next_item['confidence']) / 2
                }
                
                # Add the merged item to the list
                merged_data.append(merged_item)
                
                # Skip the next item since it's merged
                i += 2
            else:
                # No merge, add the current item
                merged_data.append(current_item)
                i += 1
        else:
            # Last item with no pair to merge with
            merged_data.append(current_item)
            i += 1
    
    return merged_data