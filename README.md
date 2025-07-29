# UCR Schedule Recommender — Data Preprocessing Utilities

This directory contains preprocessing scripts used to prepare, filter, and transform course schedule data into structured JSONL format for the UCR Schedule Recommender system.

## Please run in the same order mentioned here so that the files are consistent.

## Contents

### combine.py
- Merges multiple files into a single unified dataset.
- Ensures deduplication and consistent formatting across merged entries.

### convert.py
- Converts json files into JSONL format compatible with downstream RAG agents and semantic search.
- Supports flexible schema handling.

### course_filter.py
- Filters the course data based on specific criteria such as department, course type, or division.
- Useful for creating targeted subsets of the dataset (e.g., Computer Science electives only).
- Also adds what type of course it is at the end (eg: requirement_category: "core")

### split.py
- Splits a large combined course JSONL into smaller files categorized by department or level.
- Ideal for modularizing data ingestion for RAG Agent (less than 2 mb per file).

## Expected Input Format

The data used by these scripts must follow the JSON structure below. It is JSON here so thats its easy to verify the columns, please keep the files in JSONL format. Each entry should contain the following fields:

```json
{
  "id": 929083,
  "term": "202540",
  "termDesc": "Fall 2025",
  "courseReferenceNumber": "26117",
  "partOfTerm": "1",
  "courseNumber": "002B",
  "courseDisplay": "002B",
  "subject": "PHYS",
  "sequenceNumber": "024",
  "campusDescription": "Riverside",
  "scheduleTypeDescription": "Discussion",
  "courseTitle": "GENERAL PHYSICS",
  "creditHours": 0,
  "maximumEnrollment": 32,
  "enrollment": 31,
  "seatsAvailable": 1,
  "waitCapacity": 0,
  "waitCount": 0,
  "waitAvailable": 0,
  "creditHour": 4,
  "openSection": true,
  "isSectionLinked": true,
  "subjectCourse": "PHYS002B",
  "displayName": "Anderson, Michael",
  "emailAddress": "michaelg.anderson@ucr.edu",
  "meetingTime": {
    "beginTime": "1700",
    "building": "INTN",
    "buildingDescription": "CHASS Interdisciplinary-North",
    "campus": "C",
    "campusDescription": "Riverside",
    "creditHourSession": 0.0,
    "endDate": "12/05/2025",
    "endTime": "1750",
    "friday": false,
    "hoursWeek": 0.83,
    "monday": false,
    "room": "1006",
    "saturday": false,
    "startDate": "09/25/2025",
    "sunday": false,
    "term": "202540",
    "thursday": false,
    "tuesday": false,
    "wednesday": true
  },
  "instructionalMethod": "I",
  "instructionalMethodDescription": "In-Person",
  "prerequisites": "Prerequisites: PHYS002B and Mathematics 009B (or equivalents)",
  "courseCode": "PHYS002B",
  "requirement_category": "other_courses"
}
```


## Requirements

- Python 3.11+
- No external libraries required (uses built-in Python modules like `json`, `argparse`, and `os`)

## License

MIT License © 2025 FastReload
