import re

def count_non_empty_values(list_of_lists):
    count = 0
    for sublist in list_of_lists:
        for item in sublist:
            # Adjust this condition based on what you consider "empty"
            if item:  # This will be True for non-empty strings, non-empty lists, non-zero numbers, etc.
                count += 1
    return count

def cumulative_length(list_of_lists):
    total_length = 0
    for sublist in list_of_lists:
        total_length += len(sublist)
    return total_length

def get_top_left_y(polygon):
    return polygon[0]['y']

def sort_by_top_left_x(row):
    return sorted(row, key=lambda item: item['polygon'][0]['x'])

def align_rows_by_top_left_y(data):
    aligned_rows = []
    for row in data:
        if not row:  # Skip empty rows
            aligned_rows.append(row)
            continue
        
        # Find the top y-coordinates of the first element
        first_top_left_y = row[0]['polygon'][0]['y']
        first_top_right_y = row[0]['polygon'][1]['y']

        # Align all elements in the row to this y-coordinate
        aligned_row = []
        for word in row:
            word['polygon'][0]['y'] = first_top_left_y
            word['polygon'][1]['y'] = first_top_right_y
            aligned_row.append(word)
        
        aligned_rows.append(aligned_row)
    
    return aligned_rows

def get_rows(sorted_data, Y_THRESHOLD):
    # Adjust Y_THRESHOLD based on how close together top left 'y' coordinates are
    rows = []
    current_row = []
    for word in sorted_data:
        top_left_y = get_top_left_y(word['polygon'])
        if current_row and abs(top_left_y - get_top_left_y(current_row[0]['polygon'])) > Y_THRESHOLD:
            # If the y coordinate difference is greater than the threshold, finalize the current row
            rows.append(current_row)
            current_row = []
        
        current_row.append(word)
    # Add the last row if it exists
    if current_row:
        rows.append(current_row)
    return rows

def find_closest(numbers, target):
  """Finds the closest number to a target value in a list.

  Args:
    numbers: A list of numbers.
    target: The target value to find the closest number to.

  Returns:
    The closest number to the target value.
  """

  if not numbers:
    return None

  closest_num = numbers[0]
  closest_diff = abs(closest_num - target)

  for num in numbers[1:]:
    diff = abs(num - target)
    if diff < closest_diff:
      closest_num = num
      closest_diff = diff

  return closest_num


def extract_exam_name(data):
    grade_12th = ['higher', 'senior']
    for row in data:
        row_content = [word['content'].strip() for word in row]
        joined_content = " ".join(row_content)
        # print(joined_content)
        contains_term = any(term in joined_content.lower() for term in grade_12th)
        if contains_term:
            return '12th grade'
        else: 
            return '10th grade'


def get_school_centre_code_name(data, school_pattern):
    school_centre_list = []
    if school_pattern == '':
        school_centre_info = {'row_idx': -1,'school_name': 'not found', 'centre_name': 'not found'}
        school_centre_list.append(school_centre_info)
        school_centre_list.append({'no_of_rows': len(data)})
        return school_centre_list
    
    school_pattern = school_pattern.strip("'\"")
    # print(school_pattern)
    for row_idx, row in enumerate(data):
        row_content = [word['content'].strip() for word in row]
        joined_content = " ".join(row_content)
  
        # Extract school and optional center info using regex
        match = re.search(school_pattern, joined_content)

        if match:
            # print(match)
            # print(match.lastindex)
            if match.lastindex == None:
                school_info = match.group().strip()
                school_centre_info = {'row_idx': row_idx,'school_name': school_info, 'centre_name': 'not found'}
                school_centre_list.append(school_centre_info)
            else:
                school_info = match.group(1).strip()
                centre_info = match.group(2).strip() if match.group(2) else 'Not found'
                school_centre_info = {'row_idx': row_idx,'school_name': school_info, 'centre_name': centre_info}
                school_centre_list.append(school_centre_info)
    
    if school_centre_list == []:
        school_centre_info = {'row_idx': -1,'school_name': 'not found', 'centre_name': 'not found'}
        school_centre_list.append(school_centre_info)
    school_centre_list.append({'no_of_rows': len(data)})
    return school_centre_list


def filter_rows(student_rows, filtering_words):
    # Check if any header row is still present and filter these rows
    filtered_rows = [row for row in student_rows if not any(word['content'].lower() in filtering_words for word in row)]
    # print(filtered_rows)
    return filtered_rows


def collect_student_rows_for_no_school_name(data, pattern):
    # Initialize a flag to start collecting after the first match
    collecting = False
    student_rows = []
    for row in data:
        # Check which first row has the pattern
        if (
            any(re.match(pattern, item['content']) for item in row)
            and not collecting
            and len(row) > 1
        ):
            collecting = True  # Start collecting
        # If we are collecting, append the sublist to the result
        if collecting:
            student_rows.append(row)
    return student_rows


def collect_student_rows(data, school_centre_list, filtering_words=None):
    pattern = re.compile(r'^\d{5,7}') # assuming roll numbers will be 5 to 7 digit long

    # Extract unique row_idx values and determine the ranges
    row_indices = sorted(item['row_idx'] for item in school_centre_list[:-1]) #leave no_of_rows out
    # If school name is not mentioned in the sheet
    if row_indices[0] == -1:
        student_rows = collect_student_rows_for_no_school_name(data, pattern)
        
    else:
        # Create a list to hold the selected rows
        student_rows = []
        collecting = False
        # Iterate over the data and start collecting rows after first school name
        for i, row in enumerate(data):
            if (
                any(re.match(pattern, item['content']) for item in row) 
                and 
                not collecting
                and 
                (i not in row_indices)
                ):
                collecting = True
            
            # Skip the row with second school name also
            if collecting and (i not in row_indices):
                student_rows.append(row)

    if filtering_words != None:
        # print(filtering_words)
        student_rows = filter_rows(student_rows, filtering_words)
    return student_rows


def collect_rows(data, school_centre_list, filtering_words=None):
    pattern = re.compile(r'^\d{5,7}') # assuming roll numbers will be 5 to 7 digit long
    # Extract unique row_idx values and determine the ranges
    row_indices = sorted(item['row_idx'] for item in school_centre_list[:-1]) #leave no_of_rows entry out
    
    if filtering_words != None:
        # print(filtering_words)
        filtered_rows = filter_rows(data, filtering_words)
    
    student_rows = []
    for row in filtered_rows:
        # discard any serial number from image
        if len(row) < 2:
            # print(row)
            continue
        elif any(re.match(pattern, item['content']) for item in row) and (len(row) < 2):
            # print(row)
            continue
        else:
            student_rows.append(row)

    return student_rows


def insert_school_centre(data, school_centre_list):
    
    return




# # Sample data based on your description
# data = [
#     {'row_idx': 1, 'school_name': 'SCHOOL -1015 GOVT GS SSS NO-1 SECT IV OR.AMBEDKAR NGR N D'},
#     {'row_idx': 23, 'school_name': 'SCHOOL -1017 GOVT GIRLS SSS NO2 SECT IV DR.AMBEDKAR NGR ND'},
#     {'no_of_rows': 62}
# ]

# # Create a sample DataFrame (replace this with your actual DataFrame)
# df = pd.DataFrame({
#     'row_idx': range(1, 63),  # Assume we have rows from 1 to 62
#     'school_name': [''] * 62
# })

# # Extract school names and row indices from the list
# school_info = [(entry['row_idx'], entry['school_name']) for entry in data if 'row_idx' in entry]

# # Sort school_info by row_idx in ascending order
# school_info.sort(key=lambda x: x[0])

# # Fill school names into the DataFrame from the bottom
# for i in range(len(school_info) - 1, -1, -1):
#     current_row_idx = school_info[i][0]
#     current_school_name = school_info[i][1]

#     # Determine the next row_idx or the end of the DataFrame
#     next_row_idx = school_info[i + 1][0] if i + 1 < len(school_info) else df['row_idx'].max() + 1

#     # Fill the school name for all rows from current_row_idx to next_row_idx - 1
#     df.loc[(df['row_idx'] >= current_row_idx) & (df['row_idx'] < next_row_idx), 'school_name'] = current_school_name

# # Display the updated DataFrame
# print(df[20:25])



# column_names = [f'Column_{i}' for i in range(n)]

# # Extract school names and row indices from the list
# school_info = [(entry['row_idx'], entry['school_name']) for entry in school_centre_list if 'row_idx' in entry]

# # Sort school_info by row_idx in ascending order
# school_info.sort(key=lambda x: x[0])

# # Fill school names into the DataFrame from the bottom
# for i in range(len(school_info) - 1, -1, -1):
#     current_row_idx = school_info[i][0]
#     current_school_name = school_info[i][1]

#     # Determine the next row_idx or the end of the DataFrame
#     next_row_idx = school_info[i + 1][0] if i + 1 < len(school_info) else df['row_idx'].max() + 1

#     # Fill the school name for all rows from current_row_idx to next_row_idx - 1
#     df.loc[(df['row_idx'] >= current_row_idx) & (df['row_idx'] < next_row_idx), 'school_name'] = current_school_name

# # Display the updated DataFrame
# print(df[20:25])

def function_a():
    return "Function A called"

def function_b():
    return "Function B called"

def function_c():
    return "Function C called"

# Mapping function names to functions
function_map = {
    'a': function_a
}

def call_function(func_name):
    func = function_map.get(func_name)
    if func:
        return func()
    else:
        return "Function not found"

# Example usage
result = call_function('b')
print(result)  # Output: Function B called

