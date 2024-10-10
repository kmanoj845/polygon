import pandas as pd
import time
import yaml
from pprint import pprint
from datetime import datetime
import os
import ocr
import image_correction
import align_columns
import helper as hp
import merge_polygons
import importlib
importlib.reload(merge_polygons)
importlib.reload(align_columns)
importlib.reload(hp)
importlib.reload(image_correction)
importlib.reload(ocr)

# Record the start time
start_time = time.time()

image_name = 'RS001-1977_1.png'
year = '1977'
format = 'form1'
image_path = os.path.join(os.getcwd(), 'data', year, format, image_name)

# read the cofig
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# pprint(config)

y_threshold = config[f'year_{year}'][format]['Y_THRESHOLD']
proximity = config[f'year_{year}'][format]['PROXIMITY']
merging_threshold = config[f'year_{year}'][format]['MERGING_THRESHOLD']
school_pattern = config[f'year_{year}'][format]['SCHOOL_PATTERN']
filtering_words = config[f'year_{year}'][format]['filtering_words']

# BGR weights for image enhancement
blue, green, red = [value for value in config[f'year_{year}'][format]['weights'].values()]

if all(w == 0 for w in (blue, green, red)):
    print('--- Calling OCR with original image ---')
    ocr_data = ocr.get_ocr_data(image_path) # Call OCR API using original image
    image_angle = round(ocr_data.to_dict()['pages'][0]['angle'], 2)
else:
    # Get image correction
    print('--- Calling OCR with corrected image ---')
    corrected_image = image_correction.do_image_correction(image_path, blue, green, red)
    ocr_data = ocr.get_ocr_data(corrected_image)  # Call OCR API using corrected image
    # corrected_image.show() # Uncomment this line to see corrected image

ocr_words = ocr_data.to_dict()['pages'][0]['words']  # 'AnalyzeResult' object is not subscriptable, hence to_dict()

def get_student_data(ocr_words):
    # Sort the data first by y coordinate and then by x coordinate
    sorted_data = sorted(ocr_words, key=lambda word: (word['polygon'][0]['y'], word['polygon'][0]['x']))

    # Get rows based on how far Y values are
    rows = hp.get_rows(sorted_data, Y_THRESHOLD=y_threshold)  # Threshold in pixels

    # Sort each row by the top-left x-coordinate
    sorted_rows = [hp.sort_by_top_left_x(row) for row in rows]

    # Align the rows
    aligned_rows = hp.align_rows_by_top_left_y(sorted_rows) # Make top y coordinates same 

    # Merge close polygons (first end and next start x coordinate within merging_threshold pixels) 
    merged_rows = [merge_polygons.merge_close_polygons(row, MERGING_THRESHOLD=merging_threshold) for row in aligned_rows]
    # data_points = hp.cumulative_length(merged_rows)

    exam_name = hp.extract_exam_name(merged_rows)
    school_centre_list = hp.get_school_centre_code_name(merged_rows, school_pattern)
    # student_data = hp.collect_student_rows(merged_rows, school_centre_list, filtering_words)
    student_data = hp.collect_rows(merged_rows, school_centre_list, filtering_words)
    return student_data

student_data = get_student_data(ocr_words)
all_words = [word for inner_list in student_data for word in inner_list]
student_data = get_student_data(all_words)
align_function_name = config[f'year_{year}'][format]['ALIGN_Fn']
# create grid from student data
grid = align_columns.arrange_data(student_data, proximity, align_function_name)


# Get the current date and time
formatted_time = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
# # print("Formatted date and time:", formatted_time)
save_file_name = image_path.split('.')[0]
save_file_path = os.path.join((os.getcwd()),f'{save_file_name}_{formatted_time}.xlsx') 
df = pd.DataFrame(grid)
df.to_excel(save_file_path, index=False, header=False)
print(f'---saved at {save_file_path}--')
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

