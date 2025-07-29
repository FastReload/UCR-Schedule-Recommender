import json

def combine_json_files():
    # Define file paths
    file_paths = [
        '/Users/aryan/Desktop/Agents/2025_course_data/202510_course_data.json',
        '/Users/aryan/Desktop/Agents/2025_course_data/202520_course_data.json',
        '/Users/aryan/Desktop/Agents/2025_course_data/202530_course_data.json',
        '/Users/aryan/Desktop/Agents/2025_course_data/202540_course_data.json'
    ]
    
    # Initialize empty list to store all data
    combined_data = []
    
    # Read and combine data from each file
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_data.extend(data)
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
    
    # Write combined data to a new file
    output_path = '/Users/aryan/Desktop/Agents/2025_course_data/combined_course_data.json'
    try:
        with open(output_path, 'w') as outfile:
            json.dump(combined_data, outfile, indent=4)
        print(f"Successfully combined data and saved to {output_path}")
    except Exception as e:
        print(f"Error writing combined file: {str(e)}")

if __name__ == "__main__":
    combine_json_files()