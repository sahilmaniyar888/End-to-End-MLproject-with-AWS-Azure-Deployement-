import pandas as pd
import os

try:
    df = pd.read_csv('data/stud.csv')
    print("Columns in dataframe:")
    print(df.columns.tolist())
    
    expected_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course', 'math_score', 'reading_score', 'writing_score']
    
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        print(f"MISSING EXPECTED COLUMNS: {missing}")
    else:
        print("All expected columns are present with underscores.")

except Exception as e:
    print(f"Error reading CSV: {e}")
