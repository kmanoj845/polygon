import json
import re
import pandas as pd

# Load data from JSON file
with open('cosmos.json', 'r') as file:  # Change 'data.json' to your actual filename
    data = json.load(file)

# Debugging: Print the loaded data to check its structure
# print("Loaded data:", json.dumps(data, indent=4))  # Pretty print the loaded data

document_name = data['document'] 

# Initialize the final output structure
output = {
    "Students": [],
    "School": None,
    "Address": None,
    "Page Number": None
}

# Extract general information
for item in data['labels']:
    # print(f"Processing item: {item}")
    if item['label'] == 'SCHOOL':
        # print('school')
        output["School"] = ' '.join([v['text'] for v in item['value']])
    elif item['label'] == 'ADDRESS':
        output["Address"] = ' '.join([v['text'] for v in item['value']])
    elif item['label'] == 'PAGE NUMBER':
        output["Page Number"] = item['value'][0]['text']


# Extract student details
students = {}
patternsc1 = r'Details/\d+/LANGUAGE SC1\b(?! MKS)' # to distinguish between Details/1/LANGUAGE SC1 and Details/1/LANGUAGE SC1 MKS
patternsc2 = r'Details/\d+/LANGUAGE SC2\b(?! MKS)' # to distinguish between Details/1/LANGUAGE SC2 and Details/1/LANGUAGE SC2 MKS

for item in data['labels']:
    parts = item['label'].split('/')
    if len(parts) < 2:
        continue

    student_index = parts[1]

    # Initialize the student data structure if not already done
    if student_index not in students:
        students[student_index] = {
            "Roll No": None,
            "Name": None,
            "Math Marks": None,
            "Science Marks": None,
            "Social Studies Marks": None,
            "Language SC1": None,
            "Language SC1 Marks": None,
            "Language SC2": None,
            "Language SC2 Marks": None,
            "Grand Total": None,
            "Grade": None,
            "Work Subject": None,
            "Experience Grade": None,
            "Result": None
        }

    # Fill in the student data based on the label
    if 'ROLL NO' in item['label']:
        students[student_index]["Roll No"] = item['value'][0]['text']
    elif 'NAME OF CANDIDATE' in item['label']:
        students[student_index]["Name"] = ' '.join([v['text'] for v in item['value']])
    elif 'MTH MKS' in item['label']:
        students[student_index]["Math Marks"] = item['value'][0]['text']
    elif 'SCI MKS' in item['label']:
        students[student_index]["Science Marks"] = item['value'][0]['text']
    elif 'SOC MKS' in item['label']:
        students[student_index]["Social Studies Marks"] = item['value'][0]['text']
    elif re.search(patternsc1, item['label']): # matches Details/i/LANGUAGE SC1
        students[student_index]["Language SC1"] = item['value'][0]['text']
    elif 'LANGUAGE SC1 MKS' in item['label']:
        students[student_index]["Language SC1 Marks"] = item['value'][0]['text']
    elif re.search(patternsc2, item['label']): # matches Details/i/LANGUAGE SC2
        students[student_index]["Language SC2"] = item['value'][0]['text']
    elif 'LANGUAGE SC2 MKS' in item['label']:
        students[student_index]["Language SC2 Marks"] = item['value'][0]['text']
    elif 'GR. TOTAL' in item['label']:
        students[student_index]["Grand Total"] = item['value'][0]['text']
    elif 'HE GR' in item['label']:
        students[student_index]["Grade"] = item['value'][0]['text']
    elif 'WK SUB' in item['label']:
        students[student_index]["Work Subject"] = item['value'][0]['text']
    elif 'EXP GR' in item['label']:
        students[student_index]["Experience Grade"] = item['value'][0]['text']
    elif 'RESULT' in item['label']:
        students[student_index]["Result"] = item['value'][0]['text']

# Add students to the output structure
output["Students"] = list(students.values())

df = pd.DataFrame(output["Students"])
df['School Name'] = output["School"]
df['School Address'] = output["Address"]
# Display the DataFrame
print(df)

# # Convert the output to JSON
# json_output = json.dumps(output, indent=4)

# # Save the output to a JSON file
# with open('output.json', 'w') as output_file:  # Save to 'output.json'
#     output_file.write(json_output)

# # Optionally print the output
# print("Final Output:", json_output)
