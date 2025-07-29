import json
jsonl_output_path = '/Users/aryan/Desktop/Agents/2025_course_data/combined_course_data.jsonl'
try:
        with open("/Users/aryan/Desktop/Agents/2025_course_data/combined_course_data.json", 'r') as json_file:
            data = json.load(json_file)
            with open(jsonl_output_path, 'w') as jsonl_file:
                for item in data:
                    jsonl_file.write(json.dumps(item) + '\n')
        print(f"Successfully converted to JSONL and saved to {jsonl_output_path}")
except Exception as e:
        print(f"Error converting to JSONL: {str(e)}")