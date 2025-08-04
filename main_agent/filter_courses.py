import json
import re

input_file = "2025_combined_undergraduate_courses.jsonl"
output_file = "CHEM_courses_filtered.jsonl" #change for every course type

allowed_meeting_fields = {
    "beginTime", "building", "buildingDescription", "campus", "campusDescription", "category",
    "endDate", "endTime", "friday", "hoursWeek", "meetingScheduleType", "meetingType",
    "meetingTypeDescription", "monday", "room", "saturday", "startDate", "sunday",
    "term", "thursday", "tuesday", "wednesday"
}

#to map prerequsites to shorter names
subject_map = { 
    "Mathematics": "MATH",
    "Computer Science": "CS",
    "Chemical Engineering": "CHE",
    "Materials Sci and Engineering": "MSE",
    "Mechanical Engineering": "ME",
    "Environmental Engineering": "ENVE",
    "Electrical Engineering": "EE",
    "Computer Engineering": "CEN",
    "Bioengineering": "BIEN",
    "English": "ENGL",
    "Statistics": "STAT",
    "Engineering": "ENGR",
    "Physics": "PHYS",
    "Chemistry": "CHEM",
    "Chemical and Environmental Eng": "CEE",
    "Biology" : "BIOL",
    "Business" : "BUS",
    "Economics" : "ECON",
    "Sociology" : "SOC", #Requirement in csba (attempted to add non bcoe required courses like SOC, CHEM, etc.)
    "Biochemistry" : "BCH"
}


#Regular formatting of prerequisites : ((xyz)) and ((abc)) or ((fgh))

# def simplify_prerequisites(text, course_code=None):
#     if not text:
#         return ""

#     # remove prereq labels using regex
#     text = re.sub(r'^Prerequisites:\s*', '', text, flags=re.IGNORECASE)

#     # remove course code
#     if course_code:
#         text = re.sub(rf"^{re.escape(course_code)}(?=\s*\()", "", text)

#     #replace subject name with code
#     for full, short in subject_map.items():
#         text = re.sub(rf"Course or Test:\s*{re.escape(full)}\s+(\d+[A-Z]?)", rf"{short}\1", text)

#     # remove other info like grades
#     text = re.sub(r"Minimum Grade of [A-Z\-]+\s*", "", text)
#     text = re.sub(r"May (not )?be taken concurrently\.?", "", text)

#     #format
#     text = text.replace("\n", " ")
#     text = re.sub(r"\(\s*", "(", text)
#     text = re.sub(r"\s*\)", ")", text)
#     text = re.sub(r"\s+", " ", text).strip()

#     return text


#FOR PLACEMENT example MATH needing a placement score, another example is CHEM

def simplify_prerequisites(text, course_code=None):
    if not text:
        return ""

    #remove prereq label
    text = re.sub(r'^Prerequisites:\s*', '', text, flags=re.IGNORECASE)

    #Remove the course code even if jammed against following words
    if course_code:
        text = re.sub(rf"^{re.escape(course_code)}", "", text)

    #catch and convert score only prerequisites
    score_match = re.search(r'Score for Prereq (\d+)\s+to\s+(\d+)', text)
    if score_match:
        low, high = score_match.groups()
        return f"Placement score of {low}-{high}"

    #replace subject names with codes
    for full, short in subject_map.items():
        text = re.sub(rf"Course or Test:\s*{re.escape(full)}\s+(\d+[A-Z]*)", rf"{short}\1", text)
    
    text = text.replace('\u2013', '-').replace('–', '-')

    #remove grade and concurrency statements
    text = re.sub(r"Minimum Grade of [A-Z\-]+\s*", "", text)
    text = re.sub(r"May (not )?be taken concurrently\.?", "", text)

    #clean up parentheses and spacing
    text = text.replace("\n", " ")
    text = re.sub(r"\(\s*", "(", text)
    text = re.sub(r"\s*\)", ")", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text if text else None

#FOR PICKING 2 out of 5 courses as prerequisites like electrical engineering

# def simplify_prerequisites(text, course_code=None):
#     if not text:
#         return ""

#     # Remove prerequisite label
#     text = re.sub(r'^Prerequisites:\s*', '', text, flags=re.IGNORECASE)

#     # Remove the course's own code if it appears
#     if course_code:
#         text = re.sub(rf"^{re.escape(course_code)}(?=\s*\()", "", text)

#     # Handle "PICK2" rule block and replace with clean format
#     def handle_pick2_block(match):
#         block = match.group(0)
#         courses = re.findall(r'([A-Za-z\s&]+?)\s+(\d+[A-Z]*)', block)
#         formatted = []
#         for subject, number in courses:
#             subject = subject.strip()
#             short = subject_map.get(subject)
#             if short:
#                 formatted.append(f"({short}{number})")
#         return f"(Pick 2 of: {' or '.join(formatted)})"

#     text = re.sub(r'\(Rule: PICK2:.*?End of Rule PICK2\)', handle_pick2_block, text)
#     text = re.sub(r'\(Rule: PICK2: Pick 2 of 5 courses for a total of 2 conditions\)', 'Pick 2:', text)


#     # Replace remaining course listings with short codes
#     for full, short in subject_map.items():
#         text = re.sub(rf"Course or Test:\s*{re.escape(full)}\s+(\d+[A-Z]*)", rf"({short}\1)", text)
#         text = re.sub(rf"\b{re.escape(full)}\s+(\d+[A-Z]*)", rf"({short}\1)", text)

#     # Remove grades and concurrency
#     text = re.sub(r"Minimum Grade of [A-Z\-]+\s*", "", text)
#     text = re.sub(r"May (not )?be taken concurrently\.?", "", text)

#     # Final clean-up formatting
#     text = text.replace("\n", " ")
#     text = re.sub(r"\(\s*", "(", text)
#     text = re.sub(r"\s*\)", ")", text)
#     text = re.sub(r"\(\((.*?)\)\)", r"(\1)", text)  # remove ((...))
#     text = re.sub(r"\s+", " ", text).strip()

#     return text



def extract_fields(course):
    meeting = course.get("meetingsFaculty", [])
    meeting_time_raw = meeting[0]["meetingTime"] if meeting and "meetingTime" in meeting[0] else {}
    meeting_time = {k: v for k, v in meeting_time_raw.items() if k in allowed_meeting_fields}

    faculty = course.get("faculty", [])
    primary_faculty = next((f for f in faculty if f.get("primaryIndicator")), faculty[0] if faculty else {})

    return {
        "id": course.get("id"),
        "term": course.get("term"),
        "termDesc": course.get("termDesc"),
        "courseReferenceNumber": course.get("courseReferenceNumber"),
        "partOfTerm": course.get("partOfTerm"),
        "courseNumber": course.get("courseNumber"),
        "courseDisplay": course.get("courseDisplay"),
        "subject": course.get("subject"),
        "sequenceNumber": course.get("sequenceNumber"),
        "campusDescription": course.get("campusDescription"),
        "scheduleTypeDescription": course.get("scheduleTypeDescription"),
        "courseTitle": course.get("courseTitle"),
        "creditHours": course.get("creditHours"),
        "maximumEnrollment": course.get("maximumEnrollment"),
        "enrollment": course.get("enrollment"),
        "seatsAvailable": course.get("seatsAvailable"),
        "waitCapacity": course.get("waitCapacity"),
        "waitCount": course.get("waitCount"),
        "waitAvailable": course.get("waitAvailable"),
        "creditHour": course.get("creditHourHigh", course.get("creditHours")),
        "openSection": course.get("openSection"),
        "isSectionLinked": course.get("isSectionLinked"),
        "subjectCourse": course.get("subjectCourse"),
        "displayName": primary_faculty.get("displayName"),
        "emailAddress": primary_faculty.get("emailAddress"),
        "meetingTime": meeting_time,
        "instructionalMethod": course.get("instructionalMethod"),
        "instructionalMethodDescription": course.get("instructionalMethodDescription"),
        "prerequisites": simplify_prerequisites(course.get("prerequisites"), course.get("subjectCourse")),
        "courseCode": course.get("subjectCourse")
    }

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        course = json.loads(line)
        #change for every course type
        if course.get("subject") == "CHEM":
            filtered = extract_fields(course)
            json.dump(filtered, outfile)
            outfile.write("\n")

print(f"Filtered CHEM courses written to {output_file}")


