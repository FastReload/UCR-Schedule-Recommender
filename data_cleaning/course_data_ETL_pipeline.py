# Major Data ETL Pipeline

# libraries
import json
import pandas as pd

# Utility to convert military time (e.g. 1300 → 13:00)
def add_colon(time_str):
    if pd.isna(time_str) or len(str(time_str)) != 4:
        return time_str
    return f"{time_str[:2]}:{time_str[2:]}"

# Utility to flatten then re-nest dot-separated keys
def row_to_nested_json(row):
    nested = {}
    for col, val in row.items():
        keys = col.split('.')
        d = nested
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = val
    return nested

# Main ETL function
def process_jsonl_file(input_path, output_path):
    with open(input_path, 'r') as f:
        data = [json.loads(line) for line in f]

    df = pd.json_normalize(data)

    drop_cols = [
        'term', 'partOfTerm', 'courseNumber', 'courseDisplay', 'courseCode', 'subject',
        'waitCapacity', 'waitCount', 'waitAvailable', 'creditHour', 'maximumEnrollment',
        'enrollment', 'seatsAvailable', 'openSection', 'instructionalMethod',
        'meetingTime.campus', 'meetingTime.category', 'meetingTime.meetingScheduleType',
        'meetingTime.meetingTypeDescription', 'meetingTime.term'
    ]
    df.drop(columns=drop_cols, inplace=True, errors='ignore')

    df.rename(columns={
        'termDesc': 'term',
        'displayName': 'instructor',
        'instructionalMethodDescription': 'instructionalMethod'
    }, inplace=True)

    df['meetingTime.beginTime'] = df['meetingTime.beginTime'].apply(add_colon)
    df['meetingTime.endTime'] = df['meetingTime.endTime'].apply(add_colon)

    column_order = [
        'subjectCourse', 'courseTitle', 'term', 'courseReferenceNumber',
        'prerequisites', 'sequenceNumber', 'scheduleTypeDescription', 'isSectionLinked',
        'creditHours', 'instructionalMethod', 'instructor', 'emailAddress',
        'campusDescription', 'meetingTime.campusDescription',
        'meetingTime.building', 'meetingTime.buildingDescription', 'meetingTime.room',
        'meetingTime.startDate', 'meetingTime.endDate', 'meetingTime.beginTime',
        'meetingTime.endTime', 'meetingTime.hoursWeek', 'meetingTime.meetingType',
        'meetingTime.monday', 'meetingTime.tuesday', 'meetingTime.wednesday',
        'meetingTime.thursday', 'meetingTime.friday', 'meetingTime.saturday',
        'meetingTime.sunday', 'id'
    ]
    df = df[[col for col in column_order if col in df.columns]]

    df['prerequisites'] = df['prerequisites'].replace('', 'no prerequisites')

    mask = (
        (df['instructionalMethod'].str.lower() == 'online') &
        (df['meetingTime.beginTime'].isna()) &
        (df['meetingTime.endTime'].isna())
    )
    df.loc[mask, ['meetingTime.beginTime', 'meetingTime.endTime']] = 'asynchronous'

    for col in df.columns:
        df[col] = df[col].fillna('unknown')

    reconstructed_data = [row_to_nested_json(row) for _, row in df.iterrows()]

    with open(output_path, 'w') as f:
        for item in reconstructed_data:
            f.write(json.dumps(item) + '\n')

    print(f"Processed {input_path} → {output_path}")

# --- Hardcoded list of input/output file paths ---

input_files = [
    "ENGR_courses_filtered.jsonl",
    "CEE_courses_filtered.jsonl",
    "STAT_courses_filtered.jsonl",
    "CS_courses_filtered.jsonl",
    "MSE_courses_filtered.jsonl",
    "ENVE_courses_filtered.jsonl",
    "BIEN_courses_filtered.jsonl",
    "ME_courses_filtered.jsonl",
    "MATH_courses_filtered.jsonl",
    "EE_courses_filtered.jsonl"
]

output_files = [
    "cleaned/ENGR_courses.jsonl",
    "cleaned/CEE_courses.jsonl",
    "cleaned/STAT_courses.jsonl",
    "cleaned/CS_courses.jsonl",
    "cleaned/MSE_courses.jsonl",
    "cleaned/ENVE_courses.jsonl",
    "cleaned/BIEN_courses.jsonl",
    "cleaned/ME_courses.jsonl",
    "cleaned/MATH_courses.jsonl",
    "cleaned/EE_courses.jsonl"
]

# --- Run the ETL for each pair ---
if __name__ == "__main__":
    for input_path, output_path in zip(input_files, output_files):
        process_jsonl_file(input_path, output_path)
