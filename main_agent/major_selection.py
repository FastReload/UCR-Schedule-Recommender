import json
import os

data_dir = "/Users/ritidesai/Desktop/cleaned_courses"

#categorized courses by requirement type in major_requirements folder
lower_div = {
    "CHEM001A", "CHEM01LA", "CHEM001B", "CHEM01LB", "CHEM001C", "CHEM01LC",
    "CS009A", "CS010A",
    "EE005",
    "MATH009A", "MATH009B", "MATH009C", "MATH010A", "MATH010B", "MATH046",
    "ME009", "ME010",
    "MSE001", "MSE002L", "MSE003L", "MSE004L",
    "PHYS040A", "PHYS040B", "PHYS040C",
    "CHEM008A", "CHEM08LA",
    "STAT010"
}

upper_div = {
    "CHE100",
    "EE138",
    "ENGR180W",
    "ME110", "ME114", "ME156",
    "MSE134", "MSE135", "MSE160", "MSE161", "MSE175A", "MSE175B"
}

technical_electives = {
    "MSE143",
    "BIEN136", "MSE136",
    "BIEN140A", "CEE140A",
    "BIEN140B", "CEE140B",
    "CHE105", "CHE161",
    "EE133", "EE136", "EE137", "EE139", "EE162",
    "ME153",
    "MSE142", "MSE148", "MSE155", "MSE156", "MSE197"
}

# combine depending on categories (can add more: a breadth requirements column)
all_required = lower_div | upper_div | technical_electives

output_path = "MSE_major_courses.jsonl"

with open(output_path, "w") as outfile:
    for filename in os.listdir(data_dir):
        if filename.endswith("_courses.jsonl"):
            with open(os.path.join(data_dir, filename), "r") as infile:
                for line in infile:
                    course = json.loads(line)
                    code = course.get("subjectCourse")
                    if code in all_required:
                        # Add requirement type depending on all_requirement variable
                        if code in lower_div:
                            course["requirementType"] = "Lower-division"
                        elif code in upper_div:
                            course["requirementType"] = "Upper-division"
                        elif code in technical_electives:
                            course["requirementType"] = "Technical elective"
                        else:
                            course["requirementType"] = "Uncategorized"

                        json.dump(course, outfile)
                        outfile.write("\n")

print(f"Labeled MSE major courses written to {output_path}")
