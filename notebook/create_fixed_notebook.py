import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, '1 . EDA STUDENT PERFORMANCE .ipynb')
output_path = os.path.join(base_dir, '1_EDA_STUDENT_PERFORMANCE_FIXED.ipynb')

replacements = {
    "'parental level of education'": "'parental_level_of_education'",
    '"parental level of education"': '"parental_level_of_education"',
    "'race/ethnicity'": "'race_ethnicity'",
    '"race/ethnicity"': '"race_ethnicity"',
    "'test preparation course'": "'test_preparation_course'",
    '"test preparation course"': '"test_preparation_course"',
    "'math score'": "'math_score'",
    '"math score"': '"math_score"',
    "'reading score'": "'reading_score'",
    '"reading score"': '"reading_score"',
    "'writing score'": "'writing_score'",
    '"writing score"': '"writing_score"'
}

if not os.path.exists(input_path):
    print(f"File not found: {input_path}")
    exit(1)

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Double check and force replacements
count = 0
for cell in data['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            original_line = line
            for old, new in replacements.items():
                if old in line:
                    line = line.replace(old, new)
                    count += 1
            new_source.append(line)
        cell['source'] = new_source

print(f"Made {count} replacements.")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=1)

print(f"Saved fixed notebook to {output_path}")
