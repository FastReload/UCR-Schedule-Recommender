#create subagent folders using a list of names
import os

def create_folders(folder_names):
    """
    Create folders in the subagent directory based on the provided list of folder names.
    
    Args:
        folder_names (list): A list of folder names to create.
    """
    path = "main_agent/sub_agents/"
    
    for folder_name in folder_names:
        folder_path = os.path.join(path, folder_name)
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder_name}' created successfully.")
        except Exception as e:
            print(f"Error creating folder '{folder_name}': {e}") 


def doop_files(majors):
    # Extract just the major codes for folder creation
    major_codes = [code for code, _ in majors]

    create_folders(major_codes)  # Assumes this function takes a list of strings

    for major_code, major_desc in majors:
        # Paths
        base_path = 'main_agent/sub_agents/DS'
        target_path = os.path.join('main_agent/sub_agents', major_code)

        # Ensure the target directory exists
        os.makedirs(target_path, exist_ok=True)

        # Filenames to process
        filenames = ['__init__.py', 'agent.py', 'prompt.py']

        # Replacement rules
        upper_replace = ('DS', f'{major_code.upper()}')
        lower_replace = ('ds', f'{major_code.lower()}')
        desc_replace = ('Data Science', major_desc)

        for filename in filenames:
            source_file = os.path.join(base_path, filename)
            target_file = os.path.join(target_path, filename)

            with open(source_file, 'r') as f:
                content = f.read()

            # Apply replacements
            content = content.replace(*desc_replace)
            content = content.replace(*upper_replace)
            content = content.replace(*lower_replace)

            with open(target_file, 'w') as f:
                f.write(content)

            print(f'Created: {target_file}')


majors = [
    ("BEBM", "Bioengineering BS + MS"),
    ("BIEN", "Bioengineering"),
    ("CEN", "Computer Engineering"),
    ("CHBM", "Chemical Engineering BS + MS"),
    ("CHEN", "Chemical Engineering"),
    ("CNBM", "Computer Engineering BS + MS"),
    ("CSBA", "Computer Sci/Bus Applications"),
    ("CSBM", "Computer Science BS + MS"),
    ("EEBM", "Electrical Engineering BS + MS"),
    ("ELEN", "Electrical Engineering"),
    ("ENBM", "Environmental Engr BS + MS"),
    ("ENEN", "Environmental Engineering"),
    ("ENRB", "Robotics"),
    ("ENUN", "Engineering (Undeclared)"),
    ("MCBM", "Mechanical Engineering BS + MS"),
    ("MSE", "Materials Science and Engineer"),
    ("ENGR", "Engineering (Prep)")
]


doop_files(majors)