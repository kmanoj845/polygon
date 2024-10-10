import re
from pprint import pprint
import os
import ocr
import image_correction
import helper as hp
import merge_polygons
import importlib
importlib.reload(merge_polygons)
importlib.reload(hp)
importlib.reload(ocr)

image_name = 'Page25.png'
year = 'cert'
image_path = os.path.join(os.getcwd(), 'data', year, image_name)

if all(w == 0 for w in (0, 0, 0)):
    print('--- Calling OCR with original image ---')
    ocr_data = ocr.get_ocr_data(image_path) # Call OCR API using original image
    image_angle = round(ocr_data.to_dict()['pages'][0]['angle'], 2)
else:
    # Get image correction
    print('--- Calling OCR with corrected image ---')
    corrected_image = image_correction.do_image_correction(image_path, 0, 0, 0)
    # ocr_data = ocr.get_ocr_data(corrected_image)  # Call OCR API using corrected image
    corrected_image.show() # Uncomment this line to see corrected image

ocr_words = ocr_data.to_dict()['pages'][0]['words']  # 'AnalyzeResult' object is not subscriptable, hence to_dict()

pattern = r'^[A-Za-z0-9]+$'
matched_dicts = [entry for entry in ocr_words if re.match(pattern, entry['content'])]
# Output the collected dictionaries
# pprint(matched_dicts)

# Sort the data first by y coordinate and then by x coordinate
sorted_data = sorted(matched_dicts, key=lambda word: (word['polygon'][0]['y'], word['polygon'][0]['x']))

# Get rows based on how far Y values are
rows = hp.get_rows(sorted_data, Y_THRESHOLD=10)  # Threshold in pixels

# Sort each row by the top-left x-coordinate
sorted_rows = [hp.sort_by_top_left_x(row) for row in rows]

# Align the rows
aligned_rows = hp.align_rows_by_top_left_y(sorted_rows) # Make top y coordinates same 

# Merge close polygons (first end and next start x coordinate within merging_threshold pixels) 
merged_rows = [merge_polygons.merge_close_polygons(row, MERGING_THRESHOLD=5) for row in aligned_rows]
# data_points = hp.cumulative_length(merged_rows)
