import json
import re
from typing import Dict, List, Set

def load_jsonl_file(filename: str) -> List[Dict]:
    """Load courses from JSONL file"""
    courses = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        course = json.loads(line)
                        courses.append(course)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line: {e}")
                        continue
    except FileNotFoundError:
        print(f"File {filename} not found")
        return []
    
    return courses

def extract_course_code(course_requirement: str) -> Set[str]:
    """Extract course codes from requirement strings like 'CS 010A', 'MATH 009A', etc."""
    codes = set()
    
    # Pattern to match subject codes and numbers
    # Handles cases like: CS 010A, MATH 009A, PHYS 040A, EE 020B, etc.
    pattern = r'\b([A-Z]{2,4})\s*(\d{3}[A-Z]?)\b'
    matches = re.findall(pattern, course_requirement)
    
    for subject, number in matches:
        codes.add(f"{subject}{number}")
    
    return codes

def define_requirements() -> Dict[str, List[str]]:
    """Define all course requirements from the images"""
    
    # Lower-division requirements
    lower_div_requirements = [
        "ENGR 001",  # Professional Development and Mentoring
        "CS 010A",   # Intro to Computer Science for Sci, Math, and Engr I
        "CS 010B",   # Intro to Computer Science for Sci, Math, and Engr II
        "CS 010C",   # Introduction to Data Structures and Algorithms
        "CS 061",    # Machine Organization and Assembly Language Programming
        "CS 011",    # Introduction to Discrete Structures
        "MATH 011",  # Introduction to Discrete Structures (alternative)
        "MATH 009A", # Intro to College Math for the Sciences or First Year Calculus
        "MATH 009B", # First Year Calculus
        "MATH 009C", # First Year Calculus
        "MATH 010A", # Calculus of Several Variables
        "MATH 031",  # Applied Linear Algebra
        "EE 020B",   # Applied Linear Algebra (alternative)
        "PHYS 040A", # General Physics
        "PHYS 040B", # General Physics
        "PHYS 040C", # General Physics
        "EE 020B",   # Course Outside Computer Science Field
        "ME 010",    # Course Outside Computer Science Field (alternative)
        "EE 030A",   # Engineering Circuit Analysis with Lab
        "030LA"      # Engineering Circuit Analysis Lab (alternative)
    ]
    
    # Upper-division requirements
    upper_div_requirements = [
        "ENGR 101",  # Professional Development and Mentoring
        "CS 100",    # Software Construction
        "CS 111",    # Discrete Structures
        "CS 141",    # Intermediate Data Structures and Algorithms
        "CS 150",    # The Theory of Automata and Formal Languages
        "CS 152",    # Compiler Design
        "CS 153",    # Design of Operating Systems
        "CS 161",    # Design and Architecture of Computer Systems
        "CS 179E",   # Project in Computer Science
        "CS 120A",   # Logic Design
        "EE 120A",   # Logic Design (alternative)
        "ENGR 180W", # Technical Communications
        "STAT 155",  # Probability and Statistics for Science and Engineering
    ]
    
    # Technical electives (partial list from image)
    technical_electives = [
        "CS 105", "CS 120B", "CS 122A", "CS 122B", "CS 130",
        "CS 131", "CS 135", "CS 142", "CS 143", "CS 145", "CS 147",
        "CS 160", "CS 162", "CS 164", "CS 165", "CS 166", "CS 167",
        "CS 168", "CS 169", "CS 170", "CS 171", "CS 172", "CS 173",
        "CS 175", "CS 177", "CS 179E", "CS 180", "CS 181", "CS 182",
        "CS 183", "CS 193", "EE 120B", "MATH 120", "MATH 126",
        "MATH 135A", "MATH 135B", "PHIL 124"
    ]
    
    return {
        'lower_division': lower_div_requirements,
        'upper_division': upper_div_requirements,
        'technical_electives': technical_electives
    }

def match_courses(courses: List[Dict], requirements: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
    """Match courses from JSONL file to requirements"""
    
    matched_courses = {
        'lower_division': [],
        'upper_division': [],
        'technical_electives': [],
        'other_courses': []
    }
    
    # Create sets of required course codes for efficient lookup
    lower_codes = set()
    upper_codes = set()
    tech_elective_codes = set()
    
    for req in requirements['lower_division']:
        lower_codes.update(extract_course_code(req))
    
    for req in requirements['upper_division']:
        upper_codes.update(extract_course_code(req))
    
    for req in requirements['technical_electives']:
        tech_elective_codes.update(extract_course_code(req))
    
    # Match each course
    for course in courses:
        subject = course.get('subject', '')
        course_number = course.get('courseNumber', '')
        course_code = f"{subject}{course_number}"
        
        # Create a complete course info dict with all original data
        course_info = course.copy()  # Include all original fields
        course_info['courseCode'] = course_code  # Add the derived course code
        
        # Match to appropriate category
        if course_code in lower_codes:
            matched_courses['lower_division'].append(course_info)
        elif course_code in upper_codes:
            matched_courses['upper_division'].append(course_info)
        elif course_code in tech_elective_codes:
            matched_courses['technical_electives'].append(course_info)
        else:
            # Only include CS, MATH, PHYS, EE, ENGR courses in "other"
            if subject in ['CS', 'MATH', 'PHYS', 'EE', 'ENGR']:
                matched_courses['other_courses'].append(course_info)
    
    return matched_courses

def print_results(matched_courses: Dict[str, List[Dict]]):
    """Print the matched courses in a readable format"""
    
    print("=" * 80)
    print("COMPUTER SCIENCE DEGREE REQUIREMENTS ANALYSIS")
    print("=" * 80)
    
    for category, courses in matched_courses.items():
        if not courses:
            continue
            
        category_name = category.replace('_', ' ').title()
        print(f"\n{category_name} ({len(courses)} courses found):")
        print("-" * 50)
        
        # Sort courses by subject and course number
        sorted_courses = sorted(courses, key=lambda x: (x['subject'], x['courseNumber']))
        
        for course in sorted_courses:
            print(f"  {course['courseCode']}: {course['courseTitle']}")
            print(f"    Credits: {course['creditHours']}, Term: {course['term']}")
            print()

def save_results_to_jsonl(matched_courses: Dict[str, List[Dict]], output_filename: str):
    """Save results to a JSONL file with category information added to each course"""
    with open(output_filename, 'w', encoding='utf-8') as f:
        for category, courses in matched_courses.items():
            for course in courses:
                # Add category information to each course record
                course_with_category = course.copy()
                course_with_category['requirement_category'] = category
                
                # Write each course as a separate JSON line
                f.write(json.dumps(course_with_category, ensure_ascii=False) + '\n')
    
    print(f"Results saved to {output_filename}")

def save_results_to_json(matched_courses: Dict[str, List[Dict]], output_filename: str):
    """Save results to a JSON file (keeping original function for backwards compatibility)"""
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(matched_courses, f, indent=2, ensure_ascii=False)
    print(f"Results also saved to {output_filename}")

def main():
    """Main function to run the course extraction"""
    
    # Load courses from JSONL file
    jsonl_filename = "2025_course_data/combined_course_data.jsonl"  # Change this to your file name
    print(f"Loading courses from {jsonl_filename}...")
    courses = load_jsonl_file(jsonl_filename)
    
    if not courses:
        print("No courses loaded. Please check your file.")
        return
    
    print(f"Loaded {len(courses)} courses")
    
    # Define requirements
    requirements = define_requirements()
    
    # Match courses to requirements
    matched_courses = match_courses(courses, requirements)
    
    # Print results
    print_results(matched_courses)
    
    # Save results to JSONL file (primary output)
    save_results_to_jsonl(matched_courses, "matched_courses.jsonl")
    
    # Save results to JSON file (for reference)
    save_results_to_json(matched_courses, "matched_courses.json")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    total_lower = len(matched_courses['lower_division'])
    total_upper = len(matched_courses['upper_division'])
    total_tech = len(matched_courses['technical_electives'])
    
    print(f"Lower Division Requirements Found: {total_lower}")
    print(f"Upper Division Requirements Found: {total_upper}")
    print(f"Technical Electives Found: {total_tech}")
    print(f"Other Relevant Courses: {len(matched_courses['other_courses'])}")

if __name__ == "__main__":
    main()