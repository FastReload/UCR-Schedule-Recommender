
# Hybrid RAG Pipeline for Course Recommendations

---

## 0. Why Use Vertex AI Instead of Direct SQL Queries?

- Direct database queries work for simple lookups:
  - e.g. “List all core CS courses in Fall 2025.”
- But fail for:
  - Semantic understanding
  - Synonyms and related terms
  - Reasoning about prerequisites and degree progress
  - Natural language conversations
- **Example:**
  - User: “Any cool AI classes next quarter?”
  - SQL might miss:
    - “Machine Learning Principles”
    - “Neural Networks”
  - Vertex AI vector search finds these by meaning.
- Vertex AI + RAG provides:
  - Semantic search
  - Personalized recommendations
  - Natural language answers
- **Best practice:**
  - Use direct queries for exact lookups.
  - Use Vertex AI for conversational, personalized advising.

---

## 1. User Sends Query → Agent Builder

- Example:
  ```
  "What should I take next quarter?"
  ```

---

## 2. Agent Builder:

- Extracts major, quarter, interests:
  - Example detection:
    - major = “Computer Science”
    - quarter = “Fall”
    - courseType = “Core”
- Asks follow-up questions if missing:
  - Example:
    ```
    Bot: "Can you tell me your major?"
    ```

---

## 3. Build Vector Search Filters

- Filters to narrow the search:
  - major:
    - e.g. major = “Computer Science”
  - term:
    - e.g. quarters_offered = “Fall”
  - courseType:
    - e.g. Core, Elective, Breadth
- This ensures only relevant chunks are retrieved.

---

## 4. Run Vector Search → Retrieve Relevant Chunks

- Retrieves only documents matching filters:
  - Example finds:
    - “CS 010A - Introduction to Computer Science”
    - “MATH 009 - Calculus I”
    - “HIST 010 - World History”
- Each course document includes prerequisites if available:
  - e.g. “CS 141 - Intermediate Data Structures”
    - Prerequisite: CS 010A

---

## 5. Prepare Prompt

- Add strict instructions to prioritize core courses first:
  - Example:
    ```
    "Always recommend core courses first if available.
    If no suitable core courses exist, suggest electives or breadth
    from the list below. Do not invent courses."
    ```

- Separate retrieved data into sections:
  - Core courses
  - Electives
  - Breadth requirements

- **Include prerequisites in the prompt** so the LLM can reason about course eligibility:
  - Store prerequisites directly in your course documents as metadata.
  - When Agent Builder retrieves a course, it automatically includes the prerequisite info as part of the retrieved chunk.
  - The LLM then checks:
    - Which courses the student is eligible for
    - Whether any required prerequisites are missing
  - Example:
    ```
    Student has completed:
      - CS 010A
    LLM sees:
      - CS 141 requires CS 010A
    So it safely recommends CS 141.
    ```

- **Why not code prerequisites directly into Agent Builder?**
  - Because writing complex prerequisite logic (e.g. "requires both CS 010A and MATH 009") is cumbersome in pure logic rules.
  - The LLM is excellent at:
    - Interpreting flexible prerequisite rules
    - Reasoning about completed courses vs. requirements
    - Explaining why certain courses are recommended or skipped

- **Example Prompt Structure:**

    ```
    INSTRUCTIONS:
    You are an academic advisor. Recommend courses only from
    the lists below. Start by recommending core courses. If there
    are no suitable core courses for the student's next term,
    suggest electives or breadth options. Do not invent any
    course names.

    STUDENT CONTEXT:
    - Major: Computer Science
    - Quarter: Fall 2025
    - Completed courses: CS 008
    - Remaining breadth: Humanities

    COURSES AVAILABLE:

    ## Core:
    - CS 010A - Introduction to Computer Science
      Prerequisites: None

    - CS 141 - Intermediate Data Structures
      Prerequisites: CS 010A

    ## Electives:
    - MATH 009 - Calculus I
      Prerequisites: None

    ## Breadth:
    - HIST 010 - World History
      Prerequisites: None
    ```

- If no core courses are retrieved:
  - Add fallback instructions:
    ```
    "No core courses found. Recommend electives or breadth
    from the list below."
    ```

---

## 6. LLM Generates Recommendations

- Analyzes:
  - Student’s progress
  - Completed courses
  - Prerequisites for each course
  - Term availability
- Decides which courses to recommend based on eligibility.
- **Example personalized plan:**
  ```
  "Since you’ve completed CS 010A, you’re eligible for CS 141.
  You might also consider MATH 009 as an elective.
  HIST 010 would fulfill your Humanities breadth requirement."
  ```

---

## 7. Return Response to User

- Sends final recommendations back to the student:
  ```
  "Here’s my suggestion for Fall 2025:
  • Core: CS 141 - Intermediate Data Structures
  • Elective: MATH 009 - Calculus I
  • Breadth: HIST 010 - World History"
  ```

- Display recommendations in a **calendar-like table** for better visualization:

    | Day        | Time         | Course                                |
    |------------|--------------|---------------------------------------|
    | Mon/Wed    | 09:00-10:20  | CS 141 - Intermediate Data Structures |
    | Tues/Thurs | 11:00-12:20  | MATH 009 - Calculus I                  |
    | Friday     | 13:00-15:50  | HIST 010 - World History               |

- Helps the student visualize how courses fit into their weekly schedule.

---

## TL;DR

- Store prerequisites in your data.
- Agent Builder retrieves them as part of the course chunks.
- The LLM reasons about whether the student meets prerequisites.
- Only recommend courses the student is eligible to take.
